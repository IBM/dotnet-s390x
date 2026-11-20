import io
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest


class BootstrapSdkTests(unittest.TestCase):
    """Exercise the build wrapper with tiny SDK archives, without building .NET."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        repo = Path(__file__).resolve().parents[1]
        for name in ("dotnet-build", "dotnet-versions"):
            (self.root / name).write_text((repo / name).read_text())
        self.source = self.root / "dotnet"
        self.source.mkdir()
        self.run_command("git", "init", "-q", str(self.source))
        self.run_command("git", "-C", str(self.source), "-c", "user.name=Test",
                         "-c", "user.email=test@example.invalid", "commit",
                         "--allow-empty", "-qm", "fixture")
        # Exit immediately after observing the selected SDK, before compilation.
        (self.source / "build.sh").write_text(
            '#!/bin/bash\nset -eu\n'
            'while [ "$#" -gt 0 ]; do\n'
            '    if [ "$1" = --with-sdk ]; then\n'
            '        "$2/dotnet" > ../selected-sdk\n'
            '        exit 42\n'
            '    fi\n'
            '    shift\n'
            'done\nexit 43\n'
        )
        (self.source / "build.sh").chmod(0o755)

    def run_command(self, *args):
        return subprocess.run(args, cwd=self.root, text=True,
                              capture_output=True, check=True)

    def archive(self, name, version, executable=True):
        path = self.root / name
        content = f"#!/bin/sh\necho {version}\n".encode()
        with tarfile.open(path, "w:gz") as archive:
            entry = tarfile.TarInfo("dotnet")
            entry.mode = 0o755 if executable else 0o644
            entry.size = len(content)
            archive.addfile(entry, io.BytesIO(content))
        return path

    def invoke(self, archive):
        selected = self.root / "selected-sdk"
        selected.unlink(missing_ok=True)
        result = subprocess.run(
            ["bash", "./dotnet-build", "--with-sdk", str(archive)],
            cwd=self.root, env={**os.environ, "ARCH": "s390x"},
            text=True, capture_output=True,
        )
        # The stub's deliberate exit bypasses the unrelated Git restoration
        # in dotnet-build. Restore fixture metadata before the next invocation.
        backup = self.source / ".git.bak"
        if backup.exists():
            backup.rename(self.source / ".git")
        return result, selected.read_text().strip() if selected.exists() else None

    def assert_selected(self, archive, expected):
        result, selected = self.invoke(archive)
        self.assertEqual(result.returncode, 42, result.stderr)
        self.assertEqual(selected, expected)

    def test_extracts_first_sdk(self):
        self.assert_selected(self.archive("first.tar.gz", "first"), "first")

    def test_switches_sdk_and_removes_old_files(self):
        self.assert_selected(self.archive("first.tar.gz", "first"), "first")
        stale = self.root / ".bootstrap-sdk" / "old-sdk-file"
        stale.touch()
        self.assert_selected(self.archive("second.tar.gz", "second"), "second")
        self.assertFalse(stale.exists())

    def test_refreshes_archive_replaced_at_same_path(self):
        self.assert_selected(self.archive("sdk.tar.gz", "first"), "first")
        self.assert_selected(self.archive("sdk.tar.gz", "second"), "second")

    def test_rejects_invalid_input_without_using_or_losing_cached_sdk(self):
        self.assert_selected(self.archive("first.tar.gz", "first"), "first")
        corrupt = self.root / "corrupt.tar.gz"
        corrupt.write_text("not a tar archive")
        not_executable = self.archive("invalid-sdk.tar.gz", "invalid", executable=False)
        for archive in (self.root / "missing.tar.gz", corrupt, not_executable):
            with self.subTest(archive=archive.name):
                result, selected = self.invoke(archive)
                self.assertNotEqual(result.returncode, 0)
                self.assertIsNone(selected, result.stderr)
                cached = self.run_command(str(self.root / ".bootstrap-sdk" / "dotnet"))
                self.assertEqual(cached.stdout.strip(), "first")
                self.assertEqual(list(self.root.glob(".bootstrap-sdk.*")), [])


if __name__ == "__main__":
    unittest.main()

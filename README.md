# dotnet-s390x

Scripts to cross-build .NET for s390x.

## Basic usage

1. Remove stale files:

```
./dotnet-s390x-cleanup
```

2. Apply patches:

```
./dotnet-s390x-prepare
```

3. Build:

```
./dotnet-s390x-build
```

## Docker

If you don't want to configure your machine for .NET development, prefix all
commands with `docker/run`, e.g.:

```
docker/run ./dotnet-s390x-build
```

## Building the latest version

After cleanup, run:

```
./dotnet-s390x-bump
```

This will check out the latest sources and create a local tag.

## Building a specific version

After cleanup, run:

```
./dotnet-s390x-bump "$installer_version"
```

where `$installer_version` is something like `7.0.100-preview.7.22362.1`.

This  will check out the corresponding sources and create a local tag. 

## Uploading binaries to GitHub

Before first use, run:

```
gh auth login
```

and follow the instructions.

Make sure you used `./dotnet-s390x-bump`, since it creates a tag.

After bulding, run:

```
./dotnet-s390x-release
```

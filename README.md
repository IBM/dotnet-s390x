# dotnet-s390x

Scripts to cross-build .NET for s390x and ppc64le.

## Basic usage

1. Remove stale files:

```
./dotnet-cleanup
```

2. Apply patches:

```
./dotnet-prepare
```

3. Build:

```
./dotnet-build
```

or

```
ARCH=ppc64le ./dotnet-build
```

## Docker

If you don't want to configure your machine for .NET development, prefix all
commands with `docker/run`, e.g.:

```
docker/run ./dotnet-build
```

or

```
ARCH=ppc64le docker/run ./dotnet-build
```

## Building the latest version

After cleanup, run:

```
./dotnet-bump
```

This will check out the latest sources and create a local tag.

## Building a specific version

After cleanup, run:

```
./dotnet-bump "$installer_version"
```

where `$installer_version` is something like `7.0.100-preview.7.22362.1`.

This will check out the corresponding sources and create a local tag. 

## Uploading binaries to GitHub

Before first use, run:

```
gh auth login
```

and follow the instructions.

Make sure you used `./dotnet-bump`, since it creates a tag.

After building, run:

```
./dotnet-release
```

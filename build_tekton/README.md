# Multi-Arch with Tekton and Kaniko

This is a demo for building a multi-architecture image with Tekton and Kaniko.

## Considerations

### One step per build

Kaniko is built to do one thing and do it well - build a container in a container.
It doesn't have the `qemu` or `buildx` magic to emulate different processor architecutres.
We could do this ourselves, but the main goal of for me was to build multi-arch images for a hetergenous cluster.
This means I have nodes with all the architectures I want to target.

The solution? Build the container for each architecture natively on different nodes, then use the manifest tool to combine them all into a multi-arch manifest.

### Multiple workspaces?

I'm using longhorn for volumes, which (as far as I know) doesn't support mounting a single volume to multiple pods on different hosts.
You can use one workspace, but since it can only be attached to one pod at a time, Tekton will run all the build steps in series.
If you give each build step it's own workspace, they can build it parallel.
I could probably do something clever with downloading the source once and copying it to all the workspaces but I haven't got there yet!

### My own Kaniko task

The Kaniko task at `https://raw.githubusercontent.com/tektoncd/catalog/v1beta1/kaniko/kaniko.yaml` uses an old (really old) version of `gcr.io/kaniko-project/executor` that isn't multi-arch. So I updated it to latest - which is multi-arch. I should probably re-pin this because using `latest` makes me nervous.

#!/bin/bash

## SteamCMD assumes it is going to be run from the directory it resides in,
## Further, it overwrites itself after every invocation.
## Thus, I've wrapped it in a pushd / popd to get to the point where we can
## add steamcmd to the path and get the desired behavior

## Assumes that this script is in the steamcmd directory, as we pull the
## location of steam cmd from the directory where this script resides.

STEAMCMDLOC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

pushd $STEAMCMDLOC
./steamcmd.sh $@
popd

#!/bin/bash

## SteamCMD assumes it is going to be run from the directory it resides in,
## Further, it overwrites itself after every invocation.
## Thus, I've wrapped it in a pushd / popd to get to the point where we can
## add steamcmd to the path and get the desired behavior

## Specify the steamcmd directory explicitly.  Previously, we used some bash
## magic to find the location of the script being invoked, but we could get the
## location of the symbolic link to the script instead of the location of the
## script itself.
STEAMCMDLOC=/usr/lib/steamcmd/

leditPath=$(which ledit)

pushd $STEAMCMDLOC
if [ -e $leditPath ] ; then
    ledit ./steamcmd.sh $@
else
    ./steamcmd.sh $@
fi
popd

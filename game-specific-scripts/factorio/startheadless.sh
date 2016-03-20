#!/bin/bash
## Just a wrapper around the command line for starting a factorio instances

NAME=$1
CMD="/home/servers/factorio/bin/x64/factorio --start-server $NAME"

echo "Scren not found, issuing on this shell $CMD"
$CMD


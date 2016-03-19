#!/bin/bash

export LD_PRELOAD='/usr/$LIB/libstdc++.so.6'
NAME="testMultiplayer2.zip"

echo "/home/servers/factorio/bin/x64/factorio --start-server $NAME"
/home/servers/factorio/bin/x64/factorio --start-server $NAME

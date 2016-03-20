#!/bin/bash
## Copies a game from the init directory to save.
## assumes you're the factorio user

factorio="factorio"

if [ $# -ne 1 ] ; then
    echo "initToLive expects one argument, the initial world state zip name (not path, name)"
    echo "usage: ./initToLive.sh AwesomeWorld.zip"
    exit 1
fi

initName=$1

if [ $factorio = $USER ]; then
    if [ ! -e ~/.factorio ]; then
        echo "It appears factorio isn't installed."
        exit 1
    fi
    pushd ~/.factorio
    if [ -e init/$1 ]; then
        if [ -e saves/$1 ]; then
            read -p "Clobbering a save file, is that ok?" -n 1 -r
            echo
            if [[ $REPLY = ^[Yy]$ ]]; then
                cp init/$1 saves/$1
            fi
        else
            cp init/$1 saves/$1
            popd
        fi
    else
        echo "Couldn't find Initial Game State in init/$1"
        popd
        exit 1
    fi
else
    echo "Factorio Commands need to be issued by factorio."
    echo "Use su first."
    exit 1
fi

exit 0

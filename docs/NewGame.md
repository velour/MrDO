How To Support a New Game

What is this?
=============

We want to be able to support the starting and stopping of many games on MrDO.
This document captures how we want to set up games on the server so that there's
a pretty common environment for each game to aide us when we inevitably have to
debug something.

General Process
===============

* Add a User for the Game
* Set up an ssh-key for that user
* Turn of password logins via ssh for that user
* Install the game
* Make sure they can run the server manually
* Lock down the game-user
* Write Startup / Tear Down scripts

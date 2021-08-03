#!/bin/sh
cd "$(dirname "$(readlink -f "$0")")" # cd to this directory
INTERP="/var/publications/python/Python-3.9.0/python"
$INTERP main.py


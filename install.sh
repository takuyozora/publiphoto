#!/bin/bash

if [ "$1" == "nautilus-action" ]; then
	mkdir -p "$HOME/.local/share/file-manager/actions/"
	cp "env/publiphoto-action.desktop" "$HOME/.local/share/file-manager/actions/"
	exit 0
fi

mkdir -p "/usr/share/publiphoto"

cp -R "src" "/usr/share/publiphoto/"
cp "publiphoto.py" "/usr/share/publiphoto/"

cp "env/publiphoto.desktop" "/usr/share/applications/"
cp "env/publiphoto" "/usr/bin/"


exit $?

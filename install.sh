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

for i in "po/*"; do
	if [ -d "$i" ]; then
		mkdir -p "/usr/share/locale/$i/LC_MESSAGES"
		cp "po/$i/LC_MESSAGES/publiphoto.mo" "/usr/share/locale/$i/LC_MESSAGES/publiphoto.mo"
	fi
done

mkdir -p "/usr/local/share/file-manager/actions"
cp "env/nautilus/publiphoto-action.desktop" "/usr/local/share/file-manager/actions"


exit $?

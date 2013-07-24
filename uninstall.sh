#!/bin/bash

if [ "$1" == "nautilus-action" ]; then
	rm "$HOME/.local/share/file-manager/actions/publiphoto-action.desktop"
	exit 0
fi

rm -rf "/usr/share/publiphoto"

rm "/usr/share/applications/publiphoto.desktop"
rm "/usr/bin/publiphoto"

rm "/usr/share/locale/*/LC_MESSAGES/publiphoto.mo"
rm "/usr/local/share/file-manager/actions/publiphoto-action.desktop"


exit $?

#!/usr/bin/env bash

json=$(./baza/surveys_to_json ./backend/tests/surveys-to-json/example.xlsx)
json_target=$(cat ./backend/tests/surveys-to-json/example.json)

if [ "$json" == "$json_target" ]; then
	exit 0
else
	exit 1
fi

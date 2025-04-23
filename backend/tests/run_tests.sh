#!/usr/bin/env bash

if ! (./backend/tests/surveys-to-json/test.sh &>/dev/null); then echo "ERROR: surveys-to-json"; exit 1; fi

exit 0

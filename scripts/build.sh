#!/bin/bash

function check_pyinstaller {
    if ! command -v pyinstaller &> /dev/null
    then
        echo "Pyinstaller could not be found. Please install it using 'pip install pyinstaller' or 'pipx install pyinstaller'"
        exit
    fi
}

check_pyinstaller

pyinstaller --onefile src/main.py

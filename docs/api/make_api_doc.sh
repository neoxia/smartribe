#!/bin/bash
FILENAME="apiary.apib"
DEST="../.."
rm "$DEST/$FILENAME"
for file in *.src; do
    cat $file >> ../../apiary.apib
    if [ $# -ne 0 ]; then
        echo "ERROR: cat >> $DEST/$FILENAME"
	exit 100
    fi
done
if [ $# -eq 0 ]; then
    echo "$DEST/$FILENAME successfully created"
fi

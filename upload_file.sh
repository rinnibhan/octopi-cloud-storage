#!/bin/sh

# to execute, run: source ./upload_file.sh UPLOAD_FILE USER_NAME [KEY_PATH]

UPLOAD_FILE="$1" #path to object to be uploaded
USER_NAME="$2" #name of user
KEY_PATH="$3" #(optional) path to service account keys (.json)

gsutil cp $UPLOAD_FILE gs://$USER_NAME-octopi-bucket
if ["$3"]
	then
		export GOOGLE_APPLICATION_CREDENTIALS=$KEY_PATH
fi

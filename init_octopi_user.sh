#!/bin/sh

# to execute, run: source ./init_octopi_user.sh USER_NAME

USER_NAME="$1" #name for new user (will be used in service account and bucket)
SERV_NAME="$USER_NAME-serv-acc" #name of service account for user
BUCKET_NAME="$USER_NAME-octopi-bucket" #name of bucket for user
SERV_KEY_FILE="../Oct_Storage/$USER_NAME-keys"

PROJECT_ID="soe-octopi" #project where service account will be added
ROLE_NAME="${USER_NAME//-/}_OctopiUser" #name of role for new user

# 1. create service account for new user
gcloud iam service-accounts create $SERV_NAME

# 2. create bucket for new user
gsutil mb -p $PROJECT_ID -b on gs://$BUCKET_NAME

# 3. create custom role for bucket
gcloud iam roles create $ROLE_NAME --project=$PROJECT_ID --title="$USER_NAME Octopi User" --description="A deployed Octopi service account, which can access all objects in a bucket within soe-octopi" --permissions=storage.objects.create,storage.objects.delete,storage.objects.get,storage.objects.list,storage.objects.update,storage.multipartUploads.create,storage.multipartUploads.abort,storage.multipartUploads.listParts,storage.multipartUploads.list --stage="ALPHA"

# 4. create .json file with service account keys
gcloud iam service-accounts keys create $SERV_KEY_FILE.json --iam-account=$SERV_NAME@$PROJECT_ID.iam.gserviceaccount.com

# 5. set current credentials to new service account
export GOOGLE_APPLICATION_CREDENTIALS="$SERV_KEY_FILE.json"

# 6. connect service account to bucket (with custom permissions)
gsutil iam ch serviceAccount:$SERV_NAME@$PROJECT_ID.iam.gserviceaccount.com:projects/$PROJECT_ID/roles/$ROLE_NAME gs://$BUCKET_NAME

echo "Set up new user with service account and bucket!"

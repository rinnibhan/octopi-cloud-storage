import os
from google.cloud import storage

class UploadCloudPar():

    def __init__(self, user_name, key_folder="/Users/rinnibhansali/Documents/Stanford/Research/Oct_Storage/", key_file="", bucket_name="", serv_acc_user="", project_id="soe-octopi"):
        self.user_name = user_name
        self.key_folder = key_folder
        self.key_file = key_file
        if len(key_file) == 0:
            self.key_file = user_name + "-keys.json"
        self.bucket_name = bucket_name
        if len(bucket_name) == 0:
            self.bucket_name = user_name+"-octopi-bucket"
        self.serv_acc_user = serv_acc_user
        if len(serv_acc_user) == 0:
            self.serv_acc_user = user_name+"-serv-acc"
        self.project_id = project_id
        # set service credentials:
        # set GOOGLE_APPLICATION_CREDENTIALS to point to the .json file containing the authentication keys for your service account
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.key_folder + self.key_file
        print(self.key_folder + self.key_file)

    # return GOOGLE_APPLICATION_CREDENTIALS
    def get_serv_credentials(self):
        return os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    # use the service account to upload to its bucket
    def upload_blob(self, destination_blob_name, source_file_name):
        # source_file_name: path to file/directory to upload
        # destination_blob_name = name to assign the uploaded object in the bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        # low-level information: which file is printing where
        # print(
        #     "File {} uploaded to {}.".format(
        #         source_file_name, destination_blob_name
        #     )
        # )

    # wrapper upload function
    def upload_wrapper(self, destination_name, source_file):
        self.upload_blob(destination_name, source_file)

if __name__ == '__main__':
    upload_obj = UploadCloudPar("rinni")

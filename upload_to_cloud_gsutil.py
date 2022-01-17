import os
from google.cloud import storage

class UploadCloudGs():

    def __init__(self, user_name, key_folder="/Users/rinnibhansali/Documents/Stanford/Sophomore/Research/Oct_Storage/", key_file="", bucket_name="", serv_acc_user="", project_id="soe-octopi"):
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

    # set GOOGLE_APPLICATION_CREDENTIALS to point to the .json file containing the authentication keys for your service account
    def set_serv_credentials(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.key_folder + self.key_file
        return

    # return GOOGLE_APPLICATION_CREDENTIALS
    def get_serv_credentials(self):
        return os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    # use the service account to upload to its bucket
    def upload_blob(self, destination_blob_name, source_file_name):
        # source_file_name: path to file/directory to upload
        # destination_blob_name = name to assign the uploaded object in the bucket
        dest_file_name = "gs://" + self.bucket_name + "/" + destination_blob_name
        print(source_file_name)
        upload_cmd = "gsutil -m cp -r "+ source_file_name + " " + dest_file_name
        os.system(upload_cmd)

    # wrapper upload function
    def upload_wrapper(self, destination_name, source_file):
        self.set_serv_credentials()
        self.upload_blob(destination_name, source_file)

if __name__ == '__main__':
    upload_obj = UploadCloudGs("rinni")
    # upload_obj.upload_wrapper("new_upload2","/Users/rinnibhansali/Documents/Stanford/Sophomore/Research/upload-test/test.txt")

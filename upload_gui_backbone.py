from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import glob
import os
import shutil

import upload_to_cloud

class App(QWidget):

    # initialize window
    def __init__(self, user_name="rinni"):
        super().__init__()
        self.title = 'Octopi File Upload'
        self.user_name = user_name # name of user
        self.file_paths = []  # paths of file(s)/folder to upload
        self.uploading_file = True  # true: uploading file(s); false: uploading a folder
        self.destination_folder = ""  # name of destination folder in bucket to upload to (if blank, upload directly into bucket)
        self.initUI()

    # design UI setup
    def initUI(self):
        # Create window
        self.setWindowTitle(self.title)

        # Layout set up
        final_layout = QVBoxLayout() # outermost layout
        file_manip_layout = QHBoxLayout() # file selection/upload layout
        file_layout = QVBoxLayout() # file selection
        upload_layout = QVBoxLayout() # upload layout
        dest_folder_layout = QHBoxLayout() # destination folder selection layout (within upload layout)
        up_button_layout = QHBoxLayout() # upload process layout (within upload layout)

        # Section to select file/folder
        # select file button
        self.file_button = QPushButton('Select File(s)', self)
        self.file_button.setToolTip('Select file(s) for upload')
        self.file_button.clicked.connect(self.pick_file)
        file_layout.addWidget(self.file_button)
        # OR label
        self.label = QLabel("OR", self)
        self.label.setAlignment(Qt.AlignCenter)
        file_layout.addWidget(self.label)
        # select folder button
        self.folder_button = QPushButton('Select Folder', self)
        self.folder_button.setToolTip('Select a folder for upload')
        self.folder_button.clicked.connect(self.pick_dir)
        file_layout.addWidget(self.folder_button)

        # Section to upload file/folder

        # Section to select destination folder
        # textbox to enter destination folder name
        self.upload_dest = QLineEdit()  # textbox
        self.upload_dest.returnPressed.connect(self.on_pushButtonOK_clicked)
        # OK button to choose destination folder
        self.pushButtonOK = QPushButton(self)
        self.pushButtonOK.setText("OK")
        self.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.pushButtonOK.setToolTip("Press to save destination name; otherwise, press 'return'")
        dest_folder_layout.addWidget(self.upload_dest)
        dest_folder_layout.addWidget(self.pushButtonOK)
        # destination folder label
        dest_label = QLabel("Destination Folder Name")
        dest_label.setFont(QFont('Arial', 13))
        dest_note = QLabel("**Leave blank to upload directly into bucket**")
        dest_note_font = QFont('Arial', 10)
        dest_note_font.setItalic(True)
        dest_note.setFont(dest_note_font)

        # Section to upload file to cloud
        # upload button
        self.upload_button = QPushButton('Upload', self)
        self.upload_button.setToolTip('Upload the chosen file(s)/folder')
        self.upload_button.clicked.connect(self.upload_to_bucket)
        # progress bar
        self.progress = QProgressBar()
        up_button_layout.addWidget(self.upload_button)
        up_button_layout.addWidget(self.progress)

        # checkbox to delete files after upload
        self.del_file_check = QCheckBox("Delete Files after Upload")
        self.del_file_check.setToolTip('If unchecked, uploaded files will be renamed with prefix "upload_"')

        upload_layout.addWidget(dest_label)
        upload_layout.addWidget(dest_note)
        upload_layout.addLayout(dest_folder_layout)
        upload_layout.addWidget(self.del_file_check)
        upload_layout.addLayout(up_button_layout)

        # name of current file being uploaded label
        self.curr_file_name = QLabel("")
        self.curr_file_name.setFont(QFont('Arial', 10))

        # Section for file manipulation
        file_manip_layout.addLayout(file_layout)
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.VLine)
        self.divider.setFrameShadow(QFrame.Raised)
        file_manip_layout.addWidget(self.divider)
        file_manip_layout.addLayout(upload_layout)

        # Final layout
        final_layout.addLayout(file_manip_layout)
        final_layout.addWidget(self.curr_file_name)
        self.setLayout(final_layout)

        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def on_pushButtonOK_clicked(self):
        self.destination_folder = self.upload_dest.text()

    @pyqtSlot()
    def pick_file(self):
        self.uploading_file = True
        dialog = QFileDialog()
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setDirectory("/") # TODO: change based on system
        file_paths = dialog.getOpenFileNames(None, "Select File(s)")
        self.file_paths = file_paths[0]
        return file_paths

    @pyqtSlot()
    def pick_dir(self):
        self.uploading_file = False
        dialog = QFileDialog()
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setDirectory("/")
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setOption(QFileDialog.ShowDirsOnly,True)
        dir_path = dialog.getExistingDirectory(None, "Select Folder")
        self.file_paths = [dir_path]
        return dir_path

    @pyqtSlot()
    def upload_to_bucket(self):
        if self.uploading_file:
            self.upload_file()
        else:
            self.upload_folder()

    @pyqtSlot()
    def after_upload_process(self, files_uploaded):
        if self.del_file_check.isChecked():
            if self.uploading_file:
                for file in files_uploaded:
                    os.remove(file)
                    self.curr_file_name.setText("Deleted local file: " + file)
            else:
                shutil.rmtree(self.file_paths[0])
                self.curr_file_name.setText("Deleted local directory: " + self.file_paths[0])
        else:
            if self.uploading_file:
                for file in files_uploaded:
                    file_name = file[file.rfind("/")+1:]
                    os.rename(file, file[:file.rfind("/")+1] + "uploaded_" + file_name)
                    self.curr_file_name.setText("Renamed local filue: " + file)
            else:
                top = self.file_paths[0]
                file_name = top[top.rfind("/") + 1:]
                os.rename(top, top[:top.rfind("/")+1] + "uploaded_" + file_name)

    @pyqtSlot()
    def upload_file(self):
        # destination_folder_name: name of "folder" in bucket to save files to
        upload_obj = upload_to_cloud.UploadCloud(self.user_name)
        num_files = len(self.file_paths)
        curr_file = 1
        files_uploaded = []
        for file_path in self.file_paths:
            if '/' in file_path:
                files_uploaded.append(file_path)
                self.curr_file_name.setText("Uploading " + file_path)
                self.update_prog(curr_file, num_files)
                curr_file += 1
                file_name = file_path[file_path.rfind("/"):]
                if len(self.destination_folder) == 0:
                    upload_obj.upload_wrapper(file_name, file_path)
                else:
                    upload_obj.upload_wrapper(self.destination_folder + file_name, file_path)
        self.after_upload_process(files_uploaded)

    @pyqtSlot()
    def upload_folder(self):
        upload_obj = upload_to_cloud.UploadCloud(self.user_name)
        dir_path = self.file_paths[0]
        top_dir = dir_path[dir_path.rfind("/"):] # top directory name
        num_files = 0
        # count number of total files
        for files in os.walk(dir_path):
            dir_files = files[2]
            for f in dir_files:
                if not f.startswith("."):
                    num_files += 1
        curr_file = 1
        # go through all files in dir_path
        files = []
        for filename in glob.iglob(dir_path + '**/**', recursive=True):
            if os.path.isfile(filename):
                files.append(filename)
                self.curr_file_name.setText("Uploading " + filename) # update current folder label
                self.update_prog(curr_file, num_files) # update progress bar
                curr_file += 1
                file_path = filename[filename.find(top_dir):]
                if len(self.destination_folder) == 0:
                    upload_obj.upload_wrapper(file_path[1:], filename)
                else:
                    upload_obj.upload_wrapper(self.destination_folder + file_path, filename)
        # do after-upload processing
        self.after_upload_process(files)

    def update_prog(self, curr_file, num_files):
        perc_comp = int(float(curr_file)/float(num_files) * 100)
        self.progress.setValue(perc_comp)
        self.progress.setTextVisible(True)
        self.progress.setFormat("File " + str(curr_file) + " of " + str(num_files))
        QApplication.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
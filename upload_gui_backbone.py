from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import glob
import os

import upload_to_cloud

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Octopi File Upload'
        self.initUI()

    def initUI(self):
        self.file_paths = []
        self.uploading_file = True  # true: uploading file(s); false: uploading a folder
        self.destination_folder = ""
        # Create window: title, size, location
        self.setWindowTitle(self.title)
        outer_layout = QHBoxLayout()

        file_layout = QVBoxLayout()
        # Add buttons to select file/folder
        self.file_button = QPushButton('Select File(s)', self)
        self.file_button.setToolTip('Select file(s) for upload')
        self.file_button.clicked.connect(self.pick_file)
        file_layout.addWidget(self.file_button)

        self.label = QLabel("OR", self)
        self.label.setAlignment(Qt.AlignCenter)
        file_layout.addWidget(self.label)

        self.folder_button = QPushButton('Select Folder', self)
        self.folder_button.setToolTip('Select a folder for upload')
        self.folder_button.clicked.connect(self.pick_dir)
        file_layout.addWidget(self.folder_button)

        upload_layout = QVBoxLayout()
        dest_folder_layout = QHBoxLayout()
        up_button_layout = QHBoxLayout()

        # Add textbox + button to enter name of destination folder
        self.upload_dest = QLineEdit()  # textbox
        self.upload_dest.returnPressed.connect(self.on_pushButtonOK_clicked)
        self.pushButtonOK = QPushButton(self) # button
        self.pushButtonOK.setText("OK")
        self.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)

        dest_folder_layout.addWidget(self.upload_dest)
        dest_folder_layout.addWidget(self.pushButtonOK)

        # Add button to upload file to cloud
        self.upload_button = QPushButton('Upload File', self)
        self.upload_button.setToolTip('Upload the chosen file')
        self.upload_button.clicked.connect(self.upload_to_bucket)
        up_button_layout.addWidget(self.upload_button)

        # set up upload layout
        label = QLabel("Destination Folder Name")
        label.setFont(QFont('Arial', 13))
        note = QLabel("**Leave blank to upload directly into bucket**")
        note_font = QFont('Arial',10)
        note_font.setItalic(True)
        note.setFont(note_font)

        upload_layout.addWidget(label)
        upload_layout.addWidget(note)
        upload_layout.addLayout(dest_folder_layout)
        upload_layout.addLayout(up_button_layout)

        outer_layout.addLayout(file_layout)
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.VLine)
        self.divider.setFrameShadow(QFrame.Raised)
        outer_layout.addWidget(self.divider)
        outer_layout.addLayout(upload_layout)
        self.setLayout(outer_layout)

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
        dialog.setDirectory("/")  # TODO: change based on system
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
    def upload_file(self):
        # destination_folder_name: name of "folder" in bucket to save files to
        upload_obj = upload_to_cloud.UploadCloud("rinni")
        num_files = len(self.file_paths)
        curr_file = 1
        for file_path in self.file_paths:
            if '/' in file_path:
                print("Uploading file " + str(curr_file) + " out of " + str(num_files) + " files")
                curr_file += 1
                file_name = file_path[file_path.rfind("/"):]
                if len(self.destination_folder) == 0:
                    upload_obj.upload_wrapper(file_name, file_path)
                else:
                    upload_obj.upload_wrapper(self.destination_folder + file_name, file_path)
        print("Done with upload!")

    @pyqtSlot()
    def upload_folder(self, dir_path = "-1", num_files = -1, curr_file = -1, og_dir = ""):
        # destination_folder_name: name of "folder" in bucket to save folder to
        upload_obj = upload_to_cloud.UploadCloud("rinni")
        # if in parent folder
        if num_files == -1: # if this is the top folder
            dir_path = self.file_paths[0]
            num_files = 0
            for files in os.walk(dir_path):
                dir_files = files[2]
                for f in dir_files:
                    if not f.startswith("."):
                        num_files += 1
            curr_file = 1
            og_dir = dir_path[dir_path.rfind("/"):]
        assert os.path.isdir(dir_path)
        for dir_file in glob.glob(dir_path + '/**'):
            if not os.path.isfile(dir_file): # if it's a nested directory
                self.upload_folder(dir_file, num_files, curr_file, og_dir)
            else:
                if '/' in dir_file:
                    print("Uploading file " + str(curr_file) + " out of " + str(num_files) + " files")
                    curr_file += 1
                    file_path = dir_file[dir_file.find(og_dir):]
                    if len(self.destination_folder) == 0:
                        upload_obj.upload_wrapper(file_path[1:], dir_file)
                    else:
                        upload_obj.upload_wrapper(self.destination_folder + file_path, dir_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
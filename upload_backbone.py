from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Octopi File Upload'
        self.initUI()

    def initUI(self):
        # Create window: title, size, location
        self.setWindowTitle(self.title)

        centerPoint = QDesktopWidget().availableGeometry().center()
        x_center = centerPoint.x()
        y_center = centerPoint.y()
        width = 250
        height = 100
        self.move(x_center - int(width/2), y_center - int(height/2)) # centers window
        self.resize(width,height)

        # Add button to select file
        self.file_button = QPushButton('Select File', self)
        self.file_button.setToolTip('Select a file to upload')
        self.file_button.move(int(width/4 - self.file_button.size().width()/2), int(height/3 - self.file_button.size().height()/2))
        self.file_button.clicked.connect(self.pick_file)

        self.file_path = ''

        # Add button to upload file to cloud
        self.upload_button = QPushButton('Upload File', self)
        self.upload_button.setToolTip('Upload the chosen file')
        self.upload_button.move(int(3*width/4 - self.upload_button.size().width()/2), int(height/3 - self.file_button.size().height()/2))
        self.upload_button.clicked.connect(self.upload_file)

        # Add progress bar for upload
        self.p_bar = QProgressBar(self)
        self.p_bar.setGeometry(int(width*0.1), int(height*0.8), int(width*0.8), int(height*0.1))

        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    @pyqtSlot()
    def pick_file(self):
        dialog = QFileDialog()
        file_path = dialog.getOpenFileName(None, "Select Folder")[0]
        self.file_path = file_path
        return file_path

    @pyqtSlot()
    def upload_file(self):
        file_path = self.file_path

        # TODO: upload file here

        # setting for loop to set value of progress bar
        for i in range(101):
            # slowing down the loop
            time.sleep(1)
            # setting value to progress bar
            self.p_bar.setValue(i)
        print('Uploading file!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
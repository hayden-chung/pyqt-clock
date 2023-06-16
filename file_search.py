import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import time
import os 

# ================ CLOCK =================== #

def sec_counter(hr, min, sec, alrm_time):
    while sec < 60:
        print(f'{hr} hr, {min} min, {sec} seconds')
        if (hr, min, sec) == alrm_time:
            print("ringringringringring")
            time.sleep(10)
        time.sleep(0.001)
        sec += 1
        os.system('cls')
    sec = 0
    return sec

def min_counter(hr, min, sec, alrm_time):
    while min < 60:
        sec = sec_counter(hr, min, sec, alrm_time)
        min += 1
    min = 0
    return min

def hr_counter(hr, min, sec, alrm_time):
    while hr < 24:
        min = min_counter(hr, min, sec, alrm_time)
        hr += 1
    


class Clock():
    def __init__(self, hr, min, sec):
        self.hr = hr
        self.min = min
        self.sec = 0
        self.alrm_time = (None, None, None)

    def start(self):
        hr_counter(self.hr, self.min, self.sec, self.alrm_time)
    
    def alarm(self, alrm_time):
        hr_counter(self.hr, self.min, self.sec, alrm_time)


# myclock = Clock(1, 0, 0)

# myclock.alarm((1, 2, 29))



# ===================== DISPAY ======================== #

class FileSearchThread(Clock):
    # The pyqtSignal is defined outside the __init__ method because it is a class attribute, not an instance attribute. 
    # It is defined at the class level and can be accessed by all instances of the class.

    def __init__(self, set_time):
        
        super().__init__()
        self.set_time = set_time        

    def run(self):
        results = self.find_files(self.file_name, self.root_directory)
        self.search_completed.emit(results)

    def find_files(self, file_name, root_directory):
        results = []
        total_files = 0
        searched_files = 0

        for root, dirs, files in os.walk(root_directory):
            total_files += len(files)

        for root, dirs, files in os.walk(root_directory):
            for file in files:
                if file_name in file:
                    results.append(os.path.join(root, file))
                searched_files += 1
                progress = int((searched_files / total_files) * 100)
                self.search_progress.emit(progress)

        return results


class FileSearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        win = QWidget()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()

        # Can you use layout?
        file_search = self.setWindowTitle("File Search")
        self.setGeometry(100, 100, 400, 350)
        # hbox1.addWidget(file_search)
        # hbox1.addStretch()

        file_name_text = self.sec = QLabel("Seconds:", self)
        self.input_label.setGeometry(10, 20, 120, 30)
        hbox1.addWidget(file_name_text)

        self.input_text = QLineEdit(self)
        self.input_text.setGeometry(130, 20, 200, 30)
        hbox1.addWidget(self.input_text)


        self.root_button = QPushButton("Select Root Folder", self)
        self.root_button.setGeometry(130, 70, 200, 30)
        self.root_button.clicked.connect(self.select_root_folder)
        hbox2.addWidget(self.root_button)
        hbox2.addStretch()

        search_button = self.search_button = QPushButton("Search", self)
        self.search_button.setGeometry(150, 120, 100, 30)
        self.search_button.clicked.connect(self.start_search)
        hbox1.addWidget(search_button)
        hbox1.addStretch()


        self.progress_label = QLabel("Progress:", self)
        self.progress_label.setGeometry(20, 170, 100, 30)
        hbox3.addWidget(self.progress_label)
        hbox3.addStretch()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(130, 170, 240, 30)
        self.progress_bar.setValue(0)
        hbox3.addWidget(self.progress_bar)
        hbox3.addStretch()

        self.result_label = QLabel("Found File Paths:", self)
        self.result_label.setGeometry(20, 220, 200, 30)


        self.result_text = QTextEdit(self)
        self.result_text.setGeometry(20, 250, 350, 80)
        self.result_text.setReadOnly(True)

        self.root_directory = ""

        self.file_search_thread = None

        vbox = QHBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        
        win.setLayout(vbox)
        win.show()
        sys.exit(app.exec_())

    def select_root_folder(self):
        root_directory = QFileDialog.getExistingDirectory(self, "Select Root Folder")
        if root_directory:
            self.root_directory = root_directory

    def start_search(self):
        file_name = self.input_text.text()

        if not file_name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a file name.")
            return

        if not self.root_directory:
            QMessageBox.warning(self, "Invalid Input", "Please select a root folder.")
            return

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_results(self, results):
        if results:
            self.result_text.setPlainText("\n".join(results))
        else:
            self.result_text.setPlainText("No files found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSearchWindow()


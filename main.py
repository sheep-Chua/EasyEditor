#создай тут фоторедактор Easy Editor!
import os
from PIL import Image, ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap

app = QApplication([])
main_window = QWidget()
main_layout = QHBoxLayout()

# Тут создаем все элементы

left_col = QVBoxLayout()
open = QPushButton("Открыть")
left_col.addWidget(open)
files = QListWidget()
left_col.addWidget(files)

right_col = QVBoxLayout()
image = QLabel("Картинка")
right_col.addWidget(image)
buttons = QHBoxLayout()
btn_left = QPushButton("Влево")
btn_right = QPushButton("Вправо")
btn_mirror = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")
buttons.addWidget(btn_left)
buttons.addWidget(btn_right)
buttons.addWidget(btn_mirror)
buttons.addWidget(btn_sharp)
buttons.addWidget(btn_bw)
right_col.addLayout(buttons)

# Тут функции
def is_image(fn):
    fn = fn.lower()
    exts = [".png", ".jpg", ".bmp", ".tiff"]
    for ext in exts:
        if fn.endswith(ext):
            return True
    return False        

wd = ""

class ImageProcessor():
    def __init__(self, fname):
        self.fname = fname
        self.image = None
    def load(self, fname=""):
        global wd
        if fname == "":
            full_path = os.path.join(wd, self.fname)
        else:
            full_path = fname
        self.image = Image.open(full_path)
        image.hide()
        mem = QPixmap(full_path)
        w = image.width()
        h = image.height()
        mem = mem.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(mem)
        image.show()
    def save(self):
        full_path = "C:\\tmp"
        if os.path.exists(full_path) == False or os.path.isdir(full_path) == False:
            os.mkdir(full_path)
        full_path = os.path.join(full_path, self.fname)
        self.image.save(full_path)
        self.load(full_path)
    def bw(self):
        if self.image is not None:
            self.image = self.image.convert("L")
            self.save()
    def rotate_left(self):
        if self.image is not None:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.save()
    def rotate_right(self):
        if self.image is not None:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.save()
    def sharp(self):
        if self.image is not None:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.save()
    def mirror(self):
        if self.image is not None:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.save()

imp = ImageProcessor("")

def clickFile():
    if files.currentRow() >= 0:
        imp.fname = files.currentItem().text()
        imp.load()
files.clicked.connect(clickFile)
def onOpen():
    global wd
    wd_tmp = QFileDialog.getExistingDirectory()
    if wd_tmp:
        wd = wd_tmp
        files.clear()
        fls = os.listdir(wd)
        for fn in fls:
            if is_image(fn):
                files.addItem(fn)
            mem = QPixmap()
            image.setPixmap(mem)
            imp.image = None
open.clicked.connect(onOpen)

btn_bw.clicked.connect(imp.bw)
btn_left.clicked.connect(imp.rotate_left)
btn_right.clicked.connect(imp.rotate_right)
btn_sharp.clicked.connect(imp.sharp)
btn_mirror.clicked.connect(imp.mirror)

main_layout.addLayout(left_col)
main_layout.addLayout(right_col)
main_window.setLayout(main_layout)
main_window.show()
app.exec_()
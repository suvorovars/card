import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import uic

api_server = "http://static-maps.yandex.ru/1.x/"


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = '37.677751'
        self.lat = '55.757718'
        self.delta = 0.02
        uic.loadUi('untitled.ui', self)
        self.update()
        self.btn.clicked.connect(self.run)
        self.map_file = "map.png"
        self.pixmap = QPixmap(self.map_file)
        self.lbl.setPixmap(self.pixmap)

    def update(self):
        params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(params['spn'])
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.lbl.setPixmap(self.pixmap)


    def run(self):
        self.lon = self.line1.text()
        self.lat = self.line2.text()
        self.update()


    def keyPressEvent(self, event):
        print(self.delta)
        if event.key() == Qt.Key_PageDown:
            print('1')
            if self.delta > 0.0005:
                self.delta -= 0.0005
                self.update()

        if event.key() == Qt.Key_PageUp:
            if self.delta < 10:
                self.delta += 0.0005
                self.update()
                print('2')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
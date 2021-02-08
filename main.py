import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import uic

api_server = "http://static-maps.yandex.ru/1.x/"


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.btn.clicked.connect(self.run)
        self.map_file = "map.png"
        self.pixmap = QPixmap(self.map_file)

        self.lbl.setPixmap(self.pixmap)

    def run(self):
        lon = self.line1.text()
        lat = self.line2.text()
        delta = "0.002"
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)

        self.lbl.setPixmap(self.pixmap)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
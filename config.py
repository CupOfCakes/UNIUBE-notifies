from apoio.front_end import Login
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
janela = Login()
janela.show()
app.exec()
import os.path
from os.path import exists
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QFrame
)
from PySide6.QtGui import QIntValidator
from apoio.edit_json import *
import re
from apoio.agendador import agendar, delete_agenda


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CONFIG")

        self.label_user = QLabel("RA:")
        self.input_user = QLineEdit()
        self.input_user.setValidator(QIntValidator())

        self.label_pass = QLabel("Senha:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.label_horario = QLabel("Horario para receber notificações diariamente:")
        self.horarios_input = QLineEdit()
        self.horarios_input.setPlaceholderText("Ex: 08:00,18:00")
        self.checkbox_horario = QCheckBox("Deseja receber notificações diarias no computador?")


        self.label_email = QLabel("Email:")
        self.input_email = QLineEdit()

        self.checkbox_email = QCheckBox("Deseja receber notificações da mensalidade por email?")

        self.label_aviso = QLabel("Nota:\n"
                                  "- sem as notificações automaticas o envio de email não funcionara\n"
                                  "- quando for salvar a agenda o programa pedira por privilegios de adm\n"
                                  "apos aceitar a pagina fechara e abrirar de novo e sera preciso recolocar\n"
                                  "seu dados\n"
                                  "-Todos os dados informados aqui são salvos em arquivos JSON\n"
                                  "eles não são enviados a terceiros, eles ficam salvos no seu computador")

        self.button_save = QPushButton("Salvar")
        self.button_save.clicked.connect(self.save_data)

        if os.path.exists("apoio/login_data.json"):
            with open("apoio/login_data.json", "r") as arquivo:
                dados = json.load(arquivo)

            self.input_user.setText(dados["RA"])
            self.horarios_input.setText(", ".join(dados["horarios"]))
            self.input_email.setText(dados["email"])
            self.checkbox_email.setChecked(dados["receber_email"])
            self.checkbox_horario.setChecked(dados["receber_not"])


        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)

        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)

        layout.addWidget(self.linha())
        layout.addSpacing(10)

        layout.addWidget(self.label_horario)
        layout.addWidget(self.horarios_input)
        layout.addWidget(self.checkbox_horario)

        layout.addWidget(self.linha())
        layout.addSpacing(10)

        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.checkbox_email)

        layout.addSpacing(10)

        layout.addWidget(self.label_aviso)

        layout.addSpacing(10)

        layout.addWidget(self.button_save)
        self.setLayout(layout)

    def save_data(self):
        ra = self.input_user.text().strip()
        senha = self.input_pass.text().strip()
        email = self.input_email.text().strip()
        receber_email = self.checkbox_email.isChecked()
        horarios = [h.strip() for h in self.horarios_input.text().split(",") if h.strip()]
        receber_not = self.checkbox_horario.isChecked()

        if not self.validar_horario(horarios):
            QMessageBox.warning(self, "Erro", "Horários inválidos.Use o formato HH:MM.")
            return

        if not ra or not senha:
            QMessageBox.warning(self, "Erro", "Preencha o RA e Senha")
            return

        if not receber_email and email:
            QMessageBox.warning(self, "Erro", "Se quiser receber email informe um ou desabilite a opção")
            return

        if not receber_not and horarios:
            QMessageBox.warning(self, "Erro", "Se quiser receber notificações informe um horario ou desabilite a opção")
            return

        if receber_not:
            agendar(horarios)

        if os.path.exists("apoio/login_data.json") and not receber_not:
            with open("apoio/login_data.json", "r") as arquivo:
                dados = json.load(arquivo)

            delete_agenda(dados["horarios"])

        salvar_login(ra, senha, email, receber_email, horarios, receber_not)
        QMessageBox.information(self, "Sucesso", "Dados salvos com sucesso")
        self.close()

    @staticmethod
    def validar_horario(horarios):
        pattern = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
        return all(pattern.match(h.strip()) for h in horarios)

    @staticmethod
    def linha():
        linha = QFrame()
        linha.setFrameShape(QFrame.HLine)
        linha.setFrameShadow(QFrame.Sunken)
        return linha


class ErroRA(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERRO CONFIG")

        self.label_explic = QLabel("Sua senha ou RA não esta correto, por favor registre novamente")

        self.label_user = QLabel("RA:")
        self.input_user = QLineEdit()
        self.input_user.setValidator(QIntValidator())

        with open("apoio/login_data.json", "r") as arquivo:
            dados = json.load(arquivo)

        self.input_user.setText(dados["RA"])

        self.label_pass = QLabel("Senha:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.button_save = QPushButton("Salvar")
        self.button_save.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(self.label_explic)
        layout.addSpacing(10)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)

        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)

        layout.addWidget(Login.linha())
        layout.addSpacing(10)

        layout.addWidget(self.button_save)
        self.setLayout(layout)

    def save(self):
        ra = self.input_user.text().strip()
        senha = self.input_pass.text().strip()

        if not ra or not senha:
            QMessageBox.warning(self, "Erro", "Preencha o RA e Senha")
            return

        salvar_login_erro(ra, senha)
        QMessageBox.information(self, "Sucesso", "Dados salvos com sucesso")
        self.close()


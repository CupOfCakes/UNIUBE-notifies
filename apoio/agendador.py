import ctypes
import sys
import subprocess
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def agendar(horarios):
    if not is_admin():
        # Reexecuta o script como administrador
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    nome_base = "NotificacaoUNIUBE"
    caminho_script = os.path.abspath("NotificacaoFacul.pyw")

    for horario in horarios:
        nome_tarefa = f"{nome_base}_{horario.replace(':', '')}"
        comando = [
            "schtasks",
            "/Create",
            "/SC", "DAILY",
            "/TN", nome_tarefa,
            "/TR", f'"{sys.executable}""{caminho_script}"',
            "/ST", horario,
            "/F"
        ]

        try:
            resultado = subprocess.run(comando, capture_output=True, text=True)
            #print("STDOUT:", resultado.stdout)
            #print("STDERR:", resultado.stderr)
            resultado.check_returncode()
            #print(f"Agendado: {horario}")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao agendar {horario}: {e.stderr}")

def delete_agenda(horarios):
    if not is_admin():
        # Reexecuta o script como administrador
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    nome_base = "NotificacaoUNIUBE"

    for horario in horarios:
        nome_tarefa = f"{nome_base}_{horario.replace(':', '')}"
        comando = ["schtasks", "/Delete", "/TN", nome_tarefa, "/F"]

        try:
            subprocess.run(comando, check=True)
            #print(f"Tarefa {nome_tarefa} deletada!")
        except subprocess.CalledProcessError:
            print(f"Tarefa {nome_tarefa} não existia!")



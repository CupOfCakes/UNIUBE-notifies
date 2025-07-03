import os.path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime, timedelta
from apoio.edit_json import salvar_mensalidade
from dotenv import load_dotenv

def load_env():
    load_dotenv()

    return os.getenv("EMAIL_REMETENTE"), os.getenv("EMAIL_SENHA")

def status_mensalidade():
    estado_path = "apoio/mensalidade_data.json"
    if os.path.exists(estado_path):
        with open(estado_path, "r", encoding="utf-8") as f:
            estado = json.load(f)
    else:
        estado = {}
    return estado

def nova_mensalidade(mensalidade, limite):
    estado = status_mensalidade()

    if estado.get("ultima_mensalidad") != mensalidade or estado.get("vencimento") != limite:
        enviar_email(
            assunto = "Nova mensalidade disponível",
            corpo = f"Valor: {mensalidade}\nVencimento:{limite}",
        )

        estado = {
            "ultima_mensalidade": mensalidade,
            "vencimento": limite,
            "notificacao_enviada": True,
            "vencimento_alerta_enviado": False
        }

        salvar_mensalidade(estado["ultima_mensalidade"],
                           estado["vencimento"],
                           estado["notificacao_enviada"],
                           estado["vencimento_alerta_enviado"])


def vencimento_prox_mensalidade(mensalidade, limite):
    estado = status_mensalidade()

    if not estado.get("vencimento_alerta_enviado"):
        try:
            data_venc = datetime.strptime(limite, "%d/%m/%Y")
            hoje = datetime.now()
            if data_venc - hoje <= timedelta(days = 2):
                enviar_email(
                    assunto="Alerta: Vencimento da Mensalidade Próximo!",
                    corpo=f"Sua mensalidade de {mensalidade} vence em {limite}!",
                )

                estado["vencimento_alerta_enviado"] = True

                # Salvar de volta
                with open("apoio/mensalidade_data.json", "w") as arq:
                    json.dump(estado, arq, indent=4)

            else:
                print("dia paia")
        except Exception as e:
            print(f"Deu algum problema: {e}")


def enviar_email(assunto, corpo):
    remetente, senha  = load_env()

    with open("apoio/login_data.json", "r") as arquivo:
        dados = json.load(arquivo)

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = dados["email"]
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, dados["email"], msg.as_string())
        print("email enviado")


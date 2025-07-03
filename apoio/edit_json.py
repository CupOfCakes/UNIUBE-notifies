import json

def salvar_login(RA, senha, email, receber_email, horarios, receber_not):
    dados = {
        "RA":RA,
        "senha":senha,
        "email":email,
        "receber_email":receber_email,
        "horarios":horarios,
        "receber_not":receber_not
    }

    with open("apoio/login_data.json", "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

def salvar_mensalidade(ultima_mensalidade, vencimento, notificacao_enviada, vencimento_alerta_enviado):
    dados_mensalidade={
        "ultima_mensalidade": ultima_mensalidade,
        "vencimento": vencimento,
        "notificacao_enviada": notificacao_enviada,
        "vencimento_alerta_enviado": vencimento_alerta_enviado
    }

    with open("apoio/mensalidade_data.json", "w") as arquivo:
        json.dump(dados_mensalidade, arquivo, indent=4)


def salvar_login_erro(RA, senha):
    dados = {
        "RA":RA,
        "senha":senha
    }

    with open("apoio/login_data.json", "w") as arquivo:
        json.dump(dados, arquivo, indent=4)


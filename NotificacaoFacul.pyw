from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from winotify import Notification
from pygame import mixer
import time
import json
from apoio.front_end import Login, ErroRA
from PySide6.QtWidgets import QApplication
import sys
from apoio.envio_email import nova_mensalidade, vencimento_prox_mensalidade

#variaveis globais
app = QApplication(sys.argv)
ad_xpath = ['//*[@id="Botoes"]/a[2]', '//*[@id="acessar"]/button']

#funções
def pular_ads(navegador, xpath):
    while True:
        try:
            botao = WebDriverWait(navegador, 6). until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            botao.click()
        except(TimeoutException, ElementClickInterceptedException):
            break


def login():
    janela = Login()
    janela.show()

    app.exec()



def ler_login():
    try:
        with open("apoio/login_data.json", "r") as arquivo:
            dados = json.load(arquivo)
            return dados
    except FileNotFoundError:
        login()

        time.sleep(3)
        with open("apoio/login_data.json", "r") as arquivo:
            dados = json.load(arquivo)
            return dados

def login_erro():
        janela = ErroRA()
        janela.show()

        app.exec()


dados = ler_login()

# configura o navegador
options = Options()
options.add_argument("--headless=new")  # Modo headless
options.add_argument('--window-size=1920,1080')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/91.0.4472.124 Safari/537.36")

# Inicializa o navegador
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=options)

# abre e loga no ava
navegador.get("https://ava.uniube.br/login/")

while True:
    navegador.find_element(By.XPATH, '//*[@id="usuarioLogin"]').send_keys(dados['RA'])
    navegador.find_element(By.XPATH, '//*[@id="senhaView"]').send_keys(dados['senha'])
    navegador.find_element(By.XPATH, '//*[@id="loginPage"]/div[3]/form/div[3]/div[1]/button').click()

    try:
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="erro"]'))
        )
        login_erro()
        dados = ler_login()
        time.sleep(2)
    except TimeoutException:
        break

try:
    navegador.find_element('xpath', '//*[@id="DIV_ANDAMENTO"]/div/div/div/div[2]/div[2]/button/span').click()
except:
    pass

for xpath in ad_xpath:
    pular_ads(navegador, xpath)


# pega o valor da mensalidade a pagar e data limite
try:
    mensalidade = navegador.find_element(By.XPATH, '//*[@id="info_financeiro_content"]/span').text
    limite = navegador.find_element(By.XPATH, '//*[@id="info_financeiro"]/div[2]/div/span[1]').text

    NMens = Notification(app_id="UNIUBE", title="Mensalidade Uniube", msg=f"valor:{mensalidade}\nvencimento:{limite}", )

    NMens.add_actions(label="ir ao site", launch="https://ava.uniube.br/login/")

    NMens.show()
    time.sleep(1)
    Bmensalidade = True

except:
    Bmensalidade = False


# pega os comunicados e soma
ComunicadoUniube = int(navegador.find_element(By.XPATH, '//*[@id="info_comunicacao"]/div[2]/div[1]/span[2]').text)
ComunicadoCurso = int(navegador.find_element(By.XPATH, '//*[@id="info_comunicacao"]/div[2]/div[2]/span[2]').text)

try:
    ComunicadoTiraDuvidas = int(navegador.find_element(By.XPATH, '//*[@id="info_comunicacao"]/div[2]/div[3]/span[2]').text)
except:
    ComunicadoTiraDuvidas = 0

comunicacoes = ComunicadoUniube + ComunicadoTiraDuvidas + ComunicadoCurso

if comunicacoes != 0:
    NComu = Notification(app_id="UNIUBE", title="Comunicados", msg=f"Novos comunicados: {comunicacoes}")
    NComu.add_actions(label="ir ao site", launch="https://ava.uniube.br/login/")
    NComu.show()
    time.sleep(1)

# pega os comunicados do sae e soma
SaeComplementar = int(navegador.find_element(By.XPATH, '//*[@id="info_sae"]/div[2]/div[1]/span[2]').text)
SaeFBParcial = int(navegador.find_element(By.XPATH, '//*[@id="info_sae"]/div[2]/div[1]/span[2]').text)
SaeFinalizado = int(navegador.find_element(By.XPATH, '//*[@id="info_sae"]/div[2]/div[1]/span[2]').text)

sae = SaeComplementar + SaeFinalizado + SaeFBParcial

if sae != 0:
    NSae = Notification(app_id="UNIUBE", title="SAE", msg=f"Comunicados do SAE: {sae}")
    NSae.add_actions(label="ir ao site", launch="https://ava.uniube.br/login/")
    NSae.show()
    time.sleep(1)

# pega os arquivos e questões não visualizados
try:
    arquivos = int(navegador.find_element(By.XPATH, '//*[@id="info_arquivos"]/div[2]/span[1]').text)
except:
    arquivos = 0

QuestD = int(navegador.find_element(By.XPATH, '//*[@id="info_acqa"]/div[2]/span[1]').text)
QuestO = int(navegador.find_element(By.XPATH, '//*[@id="info_acqf"]/div[2]/span[1]').text)

if (arquivos + QuestD + QuestO) != 0:
    NNew = Notification(app_id="UNIUBE", title="Arquivos e Questões", msg=f"Novos arquivos: {arquivos}\n"
                                                                          f"Questões fechadas: {QuestO}\n"
                                                                          f"Questões Abertas: {QuestD}")
    NNew.add_actions(label="ir ao site", launch="https://ava.uniube.br/login/")
    NNew.show()
    time.sleep(1)


# informações das aulas
try:
    aula1 = navegador.find_element(By.XPATH, '//*[@id="info_aulas_hoje"]/div[2]/div[2]/div[1]/h2').text
    sala1 = navegador.find_element(By.XPATH, '//*[@id="info_aulas_hoje"]/div[2]/div[2]/div[2]/div[1]/span').text

    try:
        navegador.find_element('xpath', '//*[@id="prox_aula"]/i').click()
    
        aula2 = navegador.find_element(By.XPATH, '//*[@id="info_aulas_hoje"]/div[2]/div[3]/div[1]/h2').text
        sala2 = navegador.find_element(By.XPATH, '//*[@id="info_aulas_hoje"]/div[2]/div[3]/div[2]/div[1]/span').text
    
        NAul = Notification(app_id="UNIUBE", title="Aulas hoje", msg=f"1 horario: {aula1}\n"
                                                                     f"{sala1}\n"
                                                                     f"2 horario: {aula2}\n"
                                                                     f"{sala2}\n")
    except:
        NAul = Notification(app_id="UNIUBE", title="Aulas hoje", msg=f"1 horario: {aula1}\n"
                                                                     f"{sala1}\n")

    NAul.add_actions(label="ir ao site", launch="https://ava.uniube.br/login/")
    NAul.show()

except:
    pass

if dados["receber_email"] and Bmensalidade:
    nova_mensalidade(mensalidade, limite)
    vencimento_prox_mensalidade(mensalidade, limite)

# roda um som
mixer.init()
mixer.music.load(r"apoio/HK notify.mp3") #se o arquivo de audio não estiver na mesma pasta deste arquivo, coloque o caminho do audio
mixer.music.play()

while mixer.music.get_busy():
    pass

# UNIUBE-notify

Este software em Python automatiza tarefas relacionadas ao portal da UNIUBE. 

# Como funiona
*Automação de Login:* Faz login na sua conta da UNIUBE utilizando suas credenciais de forma segura.

*Web Scraping:* Realiza scraping no portal para coletar informações específicas

*Notificações:* Utiliza o winotify para alertar o usuário sobre:
- Aulas do dia.
- Novas mensagens recebidas.
- Alerta de pendências financeiras.
- Novos arquivos e questões onlines lançados.
- Comunicados.

Esse software serve para facilitar a vida dos estudante da UNIUBE

# 🚀 Funcionalidades
- Interface amigável, sem necessidade de conhecimento em código.
- Dados do usuário são armazenados localmente em `.json`, sem risco de vazamento.
- Ao ativar notificações diárias, o sistema agenda tarefas no **Agendador de Tarefas do Windows** (por isso pede permissão de administrador).


# 🛠️ Tecnologias
Codigo feito em python (backend e frontend)

GUI feita em `PySide6`

# 📦 Bibliotecas Utilizadas e Comandos de Instalação
| Biblioteca         | Instalação                      |
|--------------------|----------------------------------|
| Selenium           | `pip install selenium`          |
| WebDriver Manager  | `pip install webdriver-manager` |
| Winotify           | `pip install winotify`          |
| PySide6            | `pip install PySide6`           |
| pygame             | `pip install pygame`            |
| dotenv             | `pip install python-dotenv`     |

# 📌 Configuração Passo a Passo

para o funcionamento do envio de emails é necessario o email do remetente e a senha, olhe o arquivo "manual de email automaticos" para ajudar a criar o email

1. Criar o E-mail (Recomendado: Gmail ou Outlook)
✔ Gmail
Acesse https://accounts.google.com/signup

Preencha com um nome tipo:
notificador.sistema@gmail.com ou meusistema.bot@gmail.com

Crie uma senha forte.

Finalize o cadastro.

⚙️ 2. Habilitar o Acesso de Aplicativos Menos Seguros (Gmail)
⚠️ Importante pro seu sistema conseguir logar com o e-mail.

Vá em https://myaccount.google.com/security

Ative a verificação em duas etapas

Depois de ativar, vá em:

css
Copiar
Editar
Segurança > Senhas de App > Gerar nova senha
Escolha "Outro", digite algo tipo “meusistema” e gere a senha.

É mais seguro que liberar "aplicativos menos seguros", porque essa senha não expõe a sua senha real.

3. Adicionar ao codigo, no arquivo env coloque as credencias deste novo email
EMAIL_REMETENTE=email criado
EMAIL_SENHA=senha gerada


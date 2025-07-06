# UNIUBE-notify

This Python software automates tasks related to the UNIUBE portal. 

# How it works
*Login Automation:* Logs into your UNIUBE account using your credentials in a secure way.

*Web Scraping:* Scrape the portal to collect specific information

*Notifications:* Uses winotify to alert the user about:
- Classes of the day.
- New messages received.
- Alerts about financial issues.
- New files and online questions launched.
- Announcements.

This software is designed to make life easier for UNIUBE students

# Features
- User-friendly interface, no coding skills required.
- User data is stored locally in `.json`, with no risk of leakage.
- When you activate daily notifications, the system schedules tasks in **Windows Task Scheduler** (that's why it asks for administrator permission).


# 🛠️ Technologies
Python code (backend and frontend)

GUI made in `PySide6`

# 📦 Libraries Used and Installation Commands
| Library | Installation |
|--------------------|----------------------------------|
| Selenium | `pip install selenium` |
| WebDriver Manager | `pip install webdriver-manager` |
| Winotify | `pip install winotify` |
| PySide6 | `pip install PySide6` |
| pygame | `pip install pygame` |
| dotenv | `pip install python-dotenv` |

# 📌 Step-by-step configuration

in order to send emails, you need the sender's email address and password, see the file "manual de email automaticos" to help you create the email.

1. Create the email (Recommended: Gmail or Outlook)
✔ Gmail
Go to https://accounts.google.com/signup

Fill in a name like:
notificador.sistema@gmail.com or meusistema.bot@gmail.com

Create a strong password.

Finish registration.

⚙️ 2. Enable Access from Less Secure Applications (Gmail)
⚠️ Important for your system to be able to log in with the e-mail.

Go to https://myaccount.google.com/security

Activate two-step verification

Once enabled, go to

css
Copy
Edit
Security > App passwords > Generate new password
Choose "Other", type in something like "my system" and generate the password.

It's more secure than releasing "less secure apps", because this password doesn't expose your real password.

3. Add to the code, in the env file, the credentials for this new email
EMAIL_REMETENTE=email created
EMAIL_SENHA=generated password

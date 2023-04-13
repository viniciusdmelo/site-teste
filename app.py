import os

import gspread
import requests
from flask import Flask, request
from tchan import ChannelScraper
from oauth2client.service_account import ServiceAccountCredentials

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1zI16LZUgnR-1Xr3MqsjdV6wtyYNMiPpVuxdUVoXYuA4")
sheet = planilha.worksheet("Resultados")

app = Flask(__name__)

def ultimas_promocoes():
  scraper = ChannelScraper()
  contador = 0
  resultado = []
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    resultado.append(f"{message.created_at} {texto}")
    if contador == 10:
      return resultado

menu = """
<br>
<a href="/">Página inicial</a> |
<a href="/promocoes"> Promoções</a> |
<a href="/sobre">Sobre</a> |
<a href="/contato">Contato</a> |
<a href="/dedoduro">Dedo duro</a>
<br>
<br>
"""

@app.route("/")
def index():
   return menu + "Olá, mundo! Esse é o meu site de teste. Prazer, sou Vinícius."

@app.route("/sobre")
def sobre():
   return menu + "Este é um site de teste feito durante a aula de Algoritmos de Automação"

@app.route("/contato")
def contato():
   return menu + """
   Você pode encontrar em contato comigo pelo @viniciusdmelo nas redes sociais <br>
   <a href="https://www.linkedin.com/in/viniciusdmelo/">LinkedIn</a> | 
   <a href="https://www.facebook.com/viniciusdmelo">Facebook</a> | 
   <a href="http://instagram.com/viniciusdmelo">Instagram</a> | 
   <a href="https://twitter.com/viniciusdmelo">Twitter</a>
   """

@app.route("/promocoes")
def promocoes():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  for promocao in ultimas_promocoes():
    conteudo += f"<li>{promocao}</li>"
  return conteudo + "</ul>"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. \n\nResposta: ({resposta.status_code}) - {resposta.text}"

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {
    "chat_id": chat_id,
    "text": f"Você enviou a mensagem: <b>{message}</b>",
    "parse_mode": "HTML",
  }
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  print(resposta.text)
  return "ok"

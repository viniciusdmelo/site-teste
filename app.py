from flask import Flask

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
<a href="/">Página inicial</a> |
<a href="/promocoes"> Promoções |
<a href="/sobre">Sobre</a> |
<a href="/contato">Contato</a>
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
   return menu + "Você pode encontrar em contato comigo pelo @viniciusdmelo nas redes sociais"

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

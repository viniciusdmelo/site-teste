from flask import Flask

app = Flask(__name__)

menu = """
<a href="/">Página incial</a> |
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

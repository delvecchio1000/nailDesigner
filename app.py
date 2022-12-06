from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# ------------------------------------------------------------------
teste = "teste"

load_dotenv()

app = Flask(__name__)

# SEGURANÇA NOS FORMULÁRIOS!
# Passo 1 no terminal digite: python, enter;
# Passo 2 no terminal digite: import secrets, enter;
# Passo 3 no terminal digite: secrets.token_hex(16), enter;
# Passo 4 no terminal: copie o código gerado pelo python;
# Passo 5 no terminal: cole o código como está na linha abaixo do Passo 6.
# Passo 6 no terminal digite: exit(), enter. Isto sairá do python.
app.config['SECRET_KEY'] = '4538a6e04545f4353866fd02d02c6992'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA")
}

app.config.update(mail_settings)
mail = Mail(app)


class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )
        msg = Message(subject=f'{formContato.nome} visitou sua página "Nail Designer" e '
                              f'enviou uma mensagem utilizando a área de contato',
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=['delvecchio1000@gmail.com', app.config.get("MAIL_USERNAME")],
                      body=f'''
            {formContato.nome} enviou a seguinte mensagem:

            {formContato.mensagem}
            
            Para entrar em contato com {formContato.nome} use esse e-mail: {formContato.email},
                '''
                      )
        mail.send(msg)
        flash('Mensagem enviada com sucesso!')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
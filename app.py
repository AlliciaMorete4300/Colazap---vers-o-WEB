from flask import Flask, render_template, redirect, request,session,url_for,jsonify
from conexao import Conexao
from hashlib import sha256
from usuario import Usuario
from chat import Chat
from contato import Contato



app=Flask(__name__)
app.secret_key = 'berinjela'


messages = []

@app.route("/", methods=["POST","GET"])
def pagina_index():
  #  if request.method == 'POST':
  #       message = request.form['message']
        # if message:
        #    messages.append(('Usuário', message))
        return render_template('index.html')# messages=messages)


@app.route("/cadastrar", methods=["POST","GET"])
def pagina_cadastrar():
      usuario = Usuario()
      if request.method == "GET":
        return render_template ("cadastrar.html")
      else:
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        senha = request.form["senha"]
      
      usuario = Usuario()
      if usuario.cadastrar(nome, telefone, senha) ==True:
          return "Cadastro efetuado com sucesso 🌠"
      else:
        return render_template("cadastrar.html")
      
# @app.route("/cadastrar_via_ajax", methods=["POST"])
# def post_cadastro_ajax():
#     dados = request.get_json() #pega os dados que foram enviados

#     nome = dados["telefone"]
#     telefone = dados["telefone"]
#     senha = dados["senha"]

#     usuario = Usuario()

#     if usuario.cadastrar(nome, telefone,senha) == True:
#         return jsonify({'mensagem':'Cadastro OK'}), 200
#     else:
#          return jsonify({'mensagem':'Erro'}), 500

@app.route("/chat")
def pagina_chat():
    usuario = Usuario()
    if "usuario.logado" in session:
      return render_template("chat.html")
    else:
        return redirect("/cadastrar")
    
    
@app.route ("/login", methods=["GET"])
def pagina_login():
    return render_template("login.html")


@app.route ("/login", methods=["POST"])
def pagina_login_post():
   
        
        telefone = request.form["telefone"]
        senha = request.form["senha"]

        usuario = Usuario()

        usuario.logar(telefone, senha)

        if usuario.logado == True:
            session['usuario_logado'] = {"nome":usuario.nome, "telefone":usuario.telefone}
            return render_template("chat.html")
        else:
            return redirect("/login")
        
@app.route("/retorna_usuarios")
def retorna_usuarios():
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)
    
    contatos = chat.retornar_contatos()

    return jsonify(contatos),200


@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    destinatario = Contato("", tel_destinatario)

    mensagens = chat.verificar_mensagem(0, destinatario)
    return jsonify(mensagens), 200



@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    dados= request.get_json()
    tel_destinatario = dados["telefone"]
    mensagem = dados["mensagem"]
    
    
    tel_remetente = session["usuario_logado"]["telefone"]
    nome_remetente = session["usuario_logado"]["nome"]

    chat = Chat(tel_remetente, nome_remetente)

    contato= Contato("", tel_destinatario)
    # tel_remetente = Contato("", tel_remetente )

   
    chat = chat.enviar_mensagem(mensagem, contato)

    return jsonify({}), 200


app.run(debug=True)
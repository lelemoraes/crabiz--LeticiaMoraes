# Importações necessárias do Flask e dos módulos personalizados
from flask import Flask, render_template, request, jsonify, redirect, session
from usuario import Usuario
from chat import Chat
from contato import Contato
from mensagem import Mensagem
from conexao import Conexao

# Inicialização da aplicação Flask
app = Flask(__name__)

# Chave secreta para gerar o segredo de sessão
app.secret_key = "batatinhafrita123"

# Rota para a página de cadastro
@app.route("/", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == 'GET':
        return render_template("cadastro.html")
    else:
        # Recebendo os dados do formulário de cadastro em formato JSON
        dados_cadastro = request.get_json()

        # Extraindo os dados do JSON
        nome = dados_cadastro['nome']
        tel = dados_cadastro['tel']
        senha = dados_cadastro['senha']

        # Instanciando um objeto Usuario e chamando o método cadastrar para adicionar o usuário ao banco de dados
        usuario = Usuario()
        if usuario.cadastrar(tel, nome, senha) == True:
            return jsonify({'mensagem':''}), 200
        else:
            return jsonify({'mensagem':'Erro ao cadastrar!'}), 500

# Rota para a página de login
@app.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        # Verificando as credenciais de login
        usuario = Usuario()
        tel = request.form["tel"]
        senha = request.form["senha"]

        # Chamando o método logar para verificar as credenciais
        usuario.logar(tel, senha)

        # Se o login for bem-sucedido, redireciona para a página do chat, caso contrário, redireciona de volta para a página de login
        if usuario.logado == True:
            session['usuario_logado'] = {"nome":usuario.nome,
                                        "telefone":usuario.tel}
            return redirect("/chat")
        else:
            return redirect("/login")

# Rota para a página do chat
@app.route("/chat")
def pag_chat():
    # Verifica se o usuário está logado na sessão, se sim, renderiza a página do chat, caso contrário, redireciona para a página de login
    if "usuario_logado" in session:
        return render_template("chat.html")
    else:
        return redirect("")

# Rota para obter a lista de usuários
@app.route("/get/usuarios")
def api_get_usuarios():
    # Obtém o nome e o telefone do usuário logado na sessão
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    
    # Instancia um objeto Chat para interagir com os contatos e mensagens
    chat = Chat(nome_usuario, telefone_usuario)

    # Chama o método retorna_contatos() para obter a lista de contatos do usuário
    contatos = chat.retorna_contatos()

    # Retorna a lista de contatos em formato JSON
    return jsonify(contatos), 200

# Rota para obter as mensagens de um determinado destinatário
@app.route('/get/mensagens/<tel_destinatario>')
def api_get_mensagens(tel_destinatario):
    # Obtém o nome e o telefone do usuário logado na sessão
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    
    # Instancia um objeto Chat para interagir com os contatos e mensagens
    chat = Chat(nome_usuario, telefone_usuario)

    # Cria um objeto Contato com o telefone do destinatário
    contato_destinatario = Contato("", tel_destinatario)

    # Chama o método verificar_mensagem() para obter a lista de mensagens com o destinatário especificado
    lista_de_mensagens = chat.verificar_mensagem(0, contato_destinatario)

    # Retorna a lista de mensagens em formato JSON
    return jsonify(lista_de_mensagens), 200

# Rota para o envio de mensagem via AJAX
@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem_ajax():
    if request.method == "POST":
        # Recebe os dados da requisição AJAX
        dados = request.json
        destinatario = dados["destinatario"]
        mensagem = dados["mensagem"]

        # Obtém o nome e o telefone do usuário logado na sessão
        nome_usuario = session["usuario_logado"]["nome"]
        telefone_usuario = session["usuario_logado"]["telefone"]
        
        # Instancia um objeto Chat para interagir com os contatos e mensagens
        chat = Chat(nome_usuario, telefone_usuario)
        # Cria um objeto Contato com o telefone do destinatário
        contato_destinatario = Contato("", destinatario)
        envia = chat.enviar_mensagem(mensagem,contato_destinatario)
        return jsonify({"status": "Mensagem enviada com sucesso"}), 200
    else:
       
        return jsonify({"status": "Erro ao enviar mensagem"}), 5000




app.run(debug=True)

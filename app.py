from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from auth import token_obrigatorio, gerar_token 
from flask_cors import CORS 
import os
from dotenv import load_dotenv
import json
from flasgger import Swagger 

load_dotenv() 

app = Flask(__name__)

# versão do openapi
app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}

swagger = Swagger(app, template_file='openapi.yaml')

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app, origins="*")   

ADM_USUARIO = os.getenv("ADM_USUARIO")
ADM_SENHA = os.getenv("ADM_SENHA")

# Firebase config
if os.getenv("VERCEL"):
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_CREDENTIALS")))
else:
    cred = credentials.Certificate("firebase.json") 

firebase_admin.initialize_app(cred) 
db = firestore.client()


# ------------------ ROTAS ------------------ #

@app.route("/", methods=['GET'])
def root():
    return jsonify({
        "api": "academia",
        "version": "1.0",
        "Author": "Ana e Lívia" 
    }), 200


# LOGIN
@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()

    if not dados:
        return jsonify({"error": "Envie os dados para login"}), 400
    
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    print(f"Usuário: {usuario}, Senha: {senha}")

    if not usuario or not senha:
        return jsonify({"error": "Usuário e senha obrigatórios!"}), 400
    

    
    if usuario == ADM_USUARIO and senha == ADM_SENHA:
        token = gerar_token(usuario) 
        return jsonify({
            "message": "Login realizado com sucesso!",
            "token": token
        }), 200
    
    return jsonify({"error": "Usuário ou senha inválidos!"}), 401


# CADASTRO
@app.route("/cadastro", methods=['POST'])
@token_obrigatorio
def cadastro():
    dados = request.get_json()

    if not dados:
        return jsonify({"Erro": "Envie os dados para o cadastro."}), 400

    nome = dados.get("nome")
    cpf = dados.get("cpf")
    status = dados.get("status", "ativo")

    if not nome or not cpf:
        return jsonify({"Erro": "Nome e CPF são obrigatórios."}), 400

    # gerar ID depois da validação
    contador_ref = db.collection("contador").document("controle_id")
    contador_doc = contador_ref.get()

    ultimo_id = contador_doc.to_dict().get("ultimo_id", 0)
    novo_id = ultimo_id + 1

    contador_ref.update({"ultimo_id": novo_id})

    novo_aluno = {
        "id": novo_id,
        "nome": nome,
        "cpf": cpf,
        "status": status
    }

    db.collection("alunos").add(novo_aluno)

    return jsonify({
        "mensagem": "Aluno cadastrado com sucesso!",
        "aluno": novo_aluno
    }), 201


# LISTAR TODOS
@app.route("/alunos", methods=['GET'])
def listar_alunos():
    alunos_ref = db.collection("alunos").stream()

    lista = []
    for doc in alunos_ref:
        aluno = doc.to_dict()
        lista.append(aluno)

    return jsonify(lista), 200


# CONSULTAR POR ID
@app.route("/alunos/<int:id>", methods=['GET'])
def consultar_por_id(id):
    doc = db.collection("alunos").where("id", "==", id).stream()

    if doc:
        for aluno in doc:
            return jsonify(aluno.to_dict()),200 
        

    return jsonify({"erro": "Aluno não encontrado."}), 404


# CONSULTAR POR CPF
@app.route("/alunos/cpf/<string:cpf>", methods=['GET'])
def consultar_por_cpf(cpf):
    alunos_ref = db.collection("alunos").stream()

    for doc in alunos_ref:
        aluno = doc.to_dict()
        if aluno.get("cpf") == cpf:
            return jsonify(aluno), 200

    return jsonify({"erro": "Aluno não encontrado."}), 404


# EDITAR
@app.route("/alunos/<string:id>", methods=['PUT'])
@token_obrigatorio
def editar_aluno(id):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados para a edição."}), 400

    doc_ref = db.collection("alunos").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"erro": "Aluno não encontrado."}), 404

    doc_ref.update(dados)

    return jsonify({
        "mensagem": "Dados editados com sucesso!"
    }), 200


# EXCLUIR
@app.route("/alunos/<string:id>", methods=['DELETE'])
@token_obrigatorio
def excluir_aluno(id):
    doc_ref = db.collection("alunos").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"erro": "Aluno não encontrado."}), 404

    doc_ref.delete()

    return jsonify({
        "mensagem": "Aluno excluído com sucesso!"
    }), 200


# ------------------ ERROS ------------------ #

@app.errorhandler(404)
def erro404(error):
    return jsonify({"error": "Rota não encontrada"}), 404


@app.errorhandler(500)
def erro500(error):
    return jsonify({"error": "Servidor interno com falhas!"}), 500


# RUN
if __name__ == "__main__":
    app.run(debug=True)
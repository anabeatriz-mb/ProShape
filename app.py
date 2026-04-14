from flask import Flask, jsonify, request
import random
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

#versão do openapi
app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}
#chamar o openapi para o codigo 
swagger = Swagger(app, template_file='openapi.yaml')

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app, origins="*")   

ADM_USUARIO = os.getenv("ADM_USUARIO")
ADM_SENHA = os.getenv("ADM_SENHA")

if os.getenv("VERCEL"):
    #online na vercel
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_CREDENTIALS")))
else:
    #local
    cred= credentials.Certificate("firebase.json") 
    
# carregar as credenciais do firebase
firebase_admin.initialize_app(cred) 

#conectar ao firestore
db = firestore.client()

alunos = []


#rota boas vindas
@app.route("/", methods=['GET'])
def root():
    return jsonify({
        "api": "academia",
        "version":"1.0",
        "Author": "Ana e Lívia" 
    }),200


#rota login
@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    if not dados:
        return jsonify({"error":"Envie os dados para login"}), 400
    
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"error":"Usuário e senha obrigatórios!"}), 400
    
    if usuario == ADM_USUARIO and senha == ADM_SENHA:
        token = gerar_token(usuario) 
        return jsonify({"message":"Login realizado com sucesso!", "token": token}), 200
    
    return jsonify({"error": "Usuário ou senha inválidos!"})


#rota para cadastrar um novo aluno
@app.route("/cadastro", methods=['POST'])
@token_obrigatorio
def cadastro():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "Envie os dados para o cadastro."}), 400
    nome = dados.get("nome")
    cpf = dados.get("cpf")

    if not nome or not cpf:
        return jsonify({"Erro": "Nome e CPF são obrigatórios."}), 400
    
    for aluno in alunos:
        if aluno["cpf"] == cpf:
            return jsonify({"erro": "CPF já cadastrado."}), 400

    novo_aluno = {
        "id": len(alunos) + 1,
        "nome": nome,
        "cpf": cpf
    }

    alunos.append(novo_aluno)

    return jsonify({
        "mensagem": "Aluno cadastrado com sucesso!",
        "aluno": novo_aluno
    }), 201
    
#rotas para consulta de alunos
#todos
@app.route("/alunos", methods=['GET'])
def listar_alunos():
    return jsonify(alunos),200

#por id
@app.route("/alunos/<int:id>", methods=['GET'])
def consultar_por_id(id):
    for aluno in alunos:
        if aluno["id"] == id:
            return jsonify(aluno), 200
    return jsonify({"erro": "Aluno não encontrado."}), 404 

#por cpf
@app.route("/alunos/cpf/<string:cpf>", methods=['GET'])
def consultar_por_cpf(cpf):
    for aluno in alunos:
        if aluno["cpf"] == cpf:
            return jsonify(aluno), 200

    return jsonify({"erro": "Aluno não encontrado."}), 404

#rota para edição de aluno - PATCH alteração parcial
@app.route("/alunos/<int:id>", methods=['PUT'])
@token_obrigatorio
def editar_aluno(id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie os dados para a edição."}), 400

    for aluno in alunos:
        if aluno["id"] == id:
            aluno.update(dados)
            return jsonify({
                "mensagem": "Dados editados com sucesso!",
                "aluno": aluno
            }), 200

    return jsonify({"erro": "Aluno não encontrado."}), 404 

#rota para exclusão de alunos
@app.route("/alunos/<int:id>", methods=['DELETE'])
@token_obrigatorio
def excluir_aluno(id):
    for aluno in alunos:
        if aluno["id"] == id:
            alunos.remove(aluno)
            return jsonify({"mensagem": "Aluno excluído com sucesso!"}), 200
    return jsonify({"erro": "Aluno não encontrado."}), 404  


#rotas de tratamento de erro
@app.errorhandler(404)
def erro404(error):
    return jsonify({"error":"Rota não encontrada"}),404 

@app.errorhandler(500)
def erro500(error):
    return jsonify({"error":"Servidor interno com falhas!"}),500


if __name__ == "__main__":
    app.run(debug=True)

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from acesso_bd import acesso_bd

app = Flask(__name__)
CORS(app)

conn = mysql.connector.connect(
    host=f"{acesso_bd["host"]}",
    database=f"{acesso_bd["database"]}",
    user=f"{acesso_bd["user"]}",
    password=f"{acesso_bd["password"]}"
)

# PÁGINA PRINCIPAL
@app.route("/")
def homepage():
    return jsonify({"mensagem": "API de MF DEPÓSITOS online!"})

# VISUALIZAÇÃO DE PRODUTOS
@app.route("/produtos", methods=["GET"])
def visualizar_produtos():
    sql = conn.cursor(dictionary=True)
    consulta = "SELECT * FROM produtos"
    sql.execute(consulta)
    lista_produtos = sql.fetchall()
    sql.close()
    return jsonify(lista_produtos)

# VISUALIZAÇÃO DE PRODUTOS POR NOME/MARCA
@app.route("/produtos", methods=["GET"])
def visualizar_produto_por_nome_marca():
    informacoes_do_front = request.get_json()
    busca = informacoes_do_front.get("busca")
    sql = conn.cursor(dictionary=True)
    consulta = f"SELECT * FROM produtos WHERE nome LIKE '%" + "%s%" + "' OR marca LIKE '%" + "%s"+ "%'"
    itens = (busca, busca)
    sql.execute(consulta, itens)
    lista_produtos = sql.fetchall()
    sql.close()
    return jsonify(lista_produtos)

# CADASTRO DE PRODUTOS
@app.route("/produtos", methods=["POST"])
def cadastrar_produtos():
    informacoes_do_front = request.get_json()
    nome = informacoes_do_front.get("nome")
    marca = informacoes_do_front.get("marca")
    unidade = informacoes_do_front.get("unidade")
    valor = informacoes_do_front.get("valor")
    qtde = informacoes_do_front.get("qtde")
    sql = conn.cursor(dictionary=True)
    consulta = f"INSERT INTO produtos (nome, marca, unidade, valor, qtde) VALUES (%s, %s, %s, %s, %s)"
    itens = (nome, marca, unidade, valor, qtde)
    sql.execute(consulta, itens)
    conn.commit()
    sql.close()
    
    return jsonify({"mensagem": "Produto cadastrado com sucesso"}), 201

if __name__ == "__main__":
    app.run(debug=True)
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def db_connection():
    try:
        conn = sqlite3.connect("financeiro.sqlite")
        return conn
    except sqlite3.Error as e:
        print("Falha na conexão com o SQLite:", str(e))
        return None

@app.route('/users', methods=['GET', 'POST'])
def users_geral():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM users")
        users = [
            {
                'id': row[0],
                'nome': row[1],
                'ganhos': row[2],
                'despesas': row[3]
            }
            for row in cursor.fetchall()
        ]
        return jsonify(users)

    if request.method == 'POST':
        new_name = request.form['nome']
        new_earnings = request.form['ganhos']
        new_spents = request.form['despesas']
        sql = """INSERT INTO users (nome, ganhos, despesas)
                 VALUES (?, ?, ?)"""
        cursor.execute(sql, (new_name, new_earnings, new_spents))
        conn.commit()
        return f"User com o id: {cursor.lastrowid} criado com sucesso"

    return None

@app.route('/user/<int:id>', methods=['GET', 'PUT'])
def user(id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM users where id=?", (id,))
        row = cursor.fetchone()
        if row is not None:
            user = {
                'id': row[0],
                'nome': row[1],
                'ganhos': row[2],
                'despesas': row[3]
            }
            return jsonify(user), 200
        return "Usuário não encontrado", 404

    if request.method == 'PUT':
        coluna_atualizar = request.form.get('coluna')

        if coluna_atualizar not in ('ganhos', 'despesas'):
            return "Coluna inválida", 400

        novo_valor = (request.form.get('valor'))  # Obter o valor a ser somado como float
        sql = f"""UPDATE users
                  SET {coluna_atualizar} = {coluna_atualizar} + ?
                  WHERE id = ?"""
        cursor.execute(sql, (novo_valor, id))
        conn.commit()

        cursor.execute("SELECT * FROM users where id=?", (id,))
        row = cursor.fetchone()
        if row is not None:
            user = {
                'id': row[0],
                'nome': row[1],
                'ganhos': row[2],
                'despesas': row[3]
            }
            return jsonify(user), 200
        return "Usuário não encontrado", 404

if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)

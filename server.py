from flask import Flask, jsonify, request
from flask_cors import CORS
from auditoria import auditar_notas 
import banco # Importando o nosso novo módulo!

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Garante que a tabela seja criada assim que o servidor ligar
banco.criar_tabela()

@app.route("/")
def home():
    return jsonify({"status": "online", "mensagem": "API conectada ao SQLite!"})

@app.route("/api/auditoria", methods=["GET", "POST"])
def gerenciar_auditoria():
    conexao = banco.conectar_banco()
    cursor = conexao.cursor()
    
    # 1. Se for o React enviando uma nota nova (POST)
    if request.method == "POST":
        nova_nota = request.json
        nova_nota["status"] = "Pendente"
        
        # Passamos a nota pela nossa máquina de auditoria isolada para saber o status final
        resultado = auditar_notas([nova_nota], limite=400.00)
        nota_processada = resultado[0]
        
        # Inserimos a nota no Banco de Dados usando SQL
        cursor.execute(
            "INSERT INTO notas (item, valor, status) VALUES (?, ?, ?)",
            (nota_processada["item"], nota_processada["valor"], nota_processada["status"])
        )
        conexao.commit()
        
    # 2. Independente de ser GET ou POST, sempre buscamos o histórico salvo
    cursor.execute("SELECT * FROM notas")
    notas_salvas = [dict(linha) for linha in cursor.fetchall()]
    conexao.close()
    
    # 3. Devolvemos os dados reais do banco para o Frontend
    return jsonify(notas_salvas)

# Rota exclusiva para DELETAR uma nota específica pelo ID
@app.route("/api/auditoria/<int:id>", methods=["DELETE"])
def deletar_nota(id):
    conexao = banco.conectar_banco()
    cursor = conexao.cursor()
    
    # O comando SQL que apaga a linha onde o id for igual ao número recebido
    cursor.execute("DELETE FROM notas WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    
    return jsonify({"status": "sucesso", "mensagem": "Nota deletada!"})

# Rota exclusiva para ATUALIZAR (Editar) uma nota existente
@app.route("/api/auditoria/<int:id>", methods=["PUT"])
def editar_nota(id):
    conexao = banco.conectar_banco()
    cursor = conexao.cursor()
    
    # Recebemos os novos dados que o utilizador digitou no React
    nota_editada = request.json
    nota_editada["status"] = "Pendente"
    
    # Passamos a nota pela auditoria novamente para ver se o novo valor altera o status
    resultado = auditar_notas([nota_editada], limite=400.00)
    nota_processada = resultado[0]
    
    # O comando SQL que ATUALIZA (UPDATE) a linha na base de dados
    cursor.execute('''
        UPDATE notas 
        SET item = ?, valor = ?, status = ?
        WHERE id = ?
    ''', (nota_processada["item"], nota_processada["valor"], nota_processada["status"], id))
    
    conexao.commit()
    conexao.close()
    
    return jsonify({"status": "sucesso", "mensagem": "Nota atualizada!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
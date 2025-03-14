# pdv/modelos/database.py
import sqlite3

DATABASE_NAME = "recibos.db"

def criar_banco_dados():
    """Cria o banco de dados e as tabelas se não existirem."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                endereco TEXT,
                telefone TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                preco REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recibos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                endereco TEXT,
                telefone TEXT,
                itens TEXT,
                taxa REAL,
                total REAL,
                data TEXT
            )
        """)

        conexao.commit()
        print("Banco de dados criado ou existente.")
    except sqlite3.Error as e:
        print(f"Erro ao criar banco de dados: {e}")
    finally:
        if conexao:
            conexao.close()

def adicionar_cliente(nome, endereco, telefone):
    """Adiciona um novo cliente ao banco de dados."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO clientes (nome, endereco, telefone) VALUES (?, ?, ?)", (nome, endereco, telefone))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar cliente: {e}")
    finally:
        if conexao:
            conexao.close()

def adicionar_produto(nome, preco):
    """Adiciona um novo produto ao banco de dados."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar produto: {e}")
    finally:
        if conexao:
            conexao.close()

def alterar_preco_produto(nome_produto, novo_preco):
    """Altera o preço de um produto existente."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("UPDATE produtos SET preco = ? WHERE nome = ?", (novo_preco, nome_produto))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao alterar preço do produto: {e}")
    finally:
        if conexao:
            conexao.close()

def obter_clientes():
    """Retorna uma lista de nomes de clientes."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM clientes")
        clientes = [cliente[0] for cliente in cursor.fetchall()]
        return clientes
    except sqlite3.Error as e:
        print(f"Erro ao obter clientes: {e}")
        return []
    finally:
        if conexao:
            conexao.close()

def obter_produtos():
    """Retorna uma lista de nomes de produtos."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM produtos")
        produtos = [produto[0] for produto in cursor.fetchall()]
        return produtos
    except sqlite3.Error as e:
        print(f"Erro ao obter produtos: {e}")
        return []
    finally:
        if conexao:
            conexao.close()

def obter_dados_cliente(nome_cliente):
    """Retorna os dados de um cliente pelo nome."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("SELECT endereco, telefone FROM clientes WHERE nome = ?", (nome_cliente,))
        dados = cursor.fetchone()
        return dados
    except sqlite3.Error as e:
        print(f"Erro ao obter dados do cliente: {e}")
        return None
    finally:
        if conexao:
            conexao.close()

def obter_preco_produto(nome_produto):
    """Retorna o preço de um produto pelo nome."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("SELECT preco FROM produtos WHERE nome = ?", (nome_produto,))
        preco = cursor.fetchone()[0]
        return preco
    except sqlite3.Error as e:
        print(f"Erro ao obter preço do produto: {e}")
        return None
    finally:
        if conexao:
            conexao.close()

def adicionar_recibo(cliente, endereco, telefone, itens, taxa, total, data):
    """Adiciona um novo recibo ao banco de dados."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO recibos (cliente, endereco, telefone, itens, taxa, total, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (cliente, endereco, telefone, str(itens), taxa, total, data))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar recibo: {e}")
    finally:
        if conexao:
            conexao.close()

def obter_recibos_por_periodo(data_inicio, data_fim):
    """Retorna os recibos dentro de um período específico."""
    try:
        conexao = sqlite3.connect(DATABASE_NAME)
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT DATE(data), COUNT(*), SUM(total)
            FROM recibos
            WHERE DATE(data) BETWEEN ? AND ?
            GROUP BY DATE(data)
        """, (data_inicio, data_fim))
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao obter recibos por período: {e}")
        return []
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    criar_banco_dados()
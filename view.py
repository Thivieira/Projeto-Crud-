import sqlite3 as lite

# Lista de produtos com código, nome, custo e venda
produtos = [
    ("c101", "batata completa", 7.35, 25),
    ("c102", "adc batata", 3.67, 16),
    ("c103", "banana da terra", 5, 14),
    ("c104", "queijo coalho", 4.4, 15),
    ("c105", "pda simples", 5.5, 25),
    ("c106", "pda picanha/ mignon", 13.16, 38),
    ("c107", "pda contra/ ancho", 10.25, 33),
    ("c108", "pda coração", 13.5, 33),
    ("c109", "pda sobrecoxa", 7.22, 30),
    ("c110", "pda toscana", 7.11, 25),
    ("c111", "brasa burguer", 12.65, 42),
    ("c112", "brasa ribbs", 12.65, 43),
    ("c113", "bandeja picanha/mion", 22.25, 55),
    ("c114", "bandeja contra/ancho", 14.99, 45),
    ("c115", "bandeja toscana", 6.32, 31),
    ("c116", "bandeja sobrecoxa", 7.22, 33),
    ("c117", "bandeja coração", 13.25, 43),
    ("c118", "pão doce", 5, 23),
    ("b119", "agua", 2, 5),
    ("b120", "mate", 3.4, 6),
    ("b121", "refrigerante", 3.69, 7),
    ("b122", "heineken", 6.36, 12)
]

# Conectar ao banco de dados SQLite
conn = lite.connect('dados.db')

# Inserir os produtos na tabela produtos
with conn:
    cur = conn.cursor()
    # Criar a tabela produtos se ela não existir
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            codigo_produto TEXT PRIMARY KEY,
            nome_produto TEXT,
            valor_custo REAL,
            valor_venda REAL
        )
    """)
    # Loop através da lista de produtos e inserir cada um na tabela
    for produto in produtos:
        cur.execute("INSERT INTO produtos (codigo_produto, nome_produto, valor_custo, valor_venda) VALUES (?, ?, ?, ?)", produto)
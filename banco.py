import sqlite3 as lite

con = lite.connect('dados.db')

with con: 
  cur = con.cursor()
  cur.execute("""
              CREATE TABLE IF NOT EXISTS transacoes (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  codigo_produto TEXT,
                  nome_produto TEXT,
                  data_pagamento DATE,
                  mes_pagamento DATE,
                  valor_custo TEXT,
                  valor_venda TEXT,                 
                  FOREIGN KEY (codigo_produto) REFERENCES produtos (codigo_produto)
              )
              """)
  
  
import sqlite3 as lite
import os
import sys

appdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

con = lite.connect(os.path.join(appdir, 'dados.db'))

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
  
  
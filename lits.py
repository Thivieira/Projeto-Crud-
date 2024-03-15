import sqlite3
from tkinter import messagebox
from tkinter import simpledialog




# Função para inserir transação com os detalhes do produto
def inserir_com_detalhes(codigo_produto, data_pagamento, mes_pagamento):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('dados.db')
    cur = conn.cursor()

    # Consultar o produto na tabela produtos
    cur.execute("SELECT * FROM produtos WHERE codigo_produto=?", (codigo_produto,))
    produto = cur.fetchone()

    if produto:
        # Recuperar os detalhes do produto
        nome_produto = produto[1]
        valor_custo = produto[2]
        valor_venda = produto[3]

        # Inserir a transação na tabela transacoes
        cur.execute("INSERT INTO transacoes (codigo_produto, nome_produto, data_pagamento, mes_pagamento, valor_custo, valor_venda) VALUES (?, ?, ?, ?, ?, ?)",
                    (codigo_produto, nome_produto, data_pagamento, mes_pagamento, valor_custo, valor_venda))
        # Commit para salvar as alterações
        conn.commit()

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.",icon='info')
    else:
        messagebox.showinfo("ERROR","Produto não encontrado.",icon='error')

    # Fechar a conexão com o banco de dados
    conn.close()


def excluir_transacao(id_transacao):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('dados.db')
    cur = conn.cursor()

    # Excluir a transação com o ID da transação fornecido
    cur.execute("DELETE FROM transacoes WHERE id=?", (id_transacao,))

    # Verificar se alguma linha foi afetada pela exclusão
    if cur.rowcount > 0:
        messagebox.showinfo("Sucesso","Transação excluída com sucesso.",icon='info')
    else:
        messagebox.showinfo("Sucesso","Nenhuma transação encontrada com o ID da transação fornecido.",icon='info')


    # Commit para salvar as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()
    
def atualizar(label_total_custo, label_total_venda):
    # Solicitar ao usuário que insira o mês das transações
    mes_selecionado = simpledialog.askstring("Selecionar Mês", "Por favor, insira o mês no formato YYYY-MM:")
    if mes_selecionado:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('dados.db')
        cur = conn.cursor()

        # Consultar todas as transações do mês selecionado
        cur.execute("SELECT valor_custo, valor_venda FROM transacoes WHERE mes_pagamento=?", (mes_selecionado,))
        transacoes_mes = cur.fetchall()

        # Calcular os totais de valor_custo e valor_venda
        total_valor_custo = sum(transacao[0] for transacao in transacoes_mes)
        total_valor_venda = sum(transacao[1] for transacao in transacoes_mes)

        # Exibir os totais em uma label abaixo do Treeview
        label_total_custo.config(text=f"Total de custo no mês {mes_selecionado}: {total_valor_custo}")
        label_total_custo.place(x=10, y=300)
        label_total_venda.config(text=f"Total de venda no mês {mes_selecionado}: {total_valor_venda}")
        label_total_venda.place(x=10, y=320)

        # Fechar a conexão com o banco de dados
        conn.close()
        
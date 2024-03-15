from tkinter import *
import sqlite3
from tkinter import ttk
from tkcalendar import DateEntry
from lits import inserir_com_detalhes, excluir_transacao
from tkinter import messagebox

# cores
co0 = "#f0f3f5"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # letra
co5 = "#e06636"  # - profit
co6 = "#038cfc"  # azul
co7 = "#ef5350"  # vermelha
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # sky blue
co10 = '#e0a752' # honey

def obter_lista_produtos_do_bd():
    conn = sqlite3.connect('dados.db')
    cur = conn.cursor()
    cur.execute("SELECT codigo_produto, nome_produto FROM produtos")
    lista_produtos = cur.fetchall()
    conn.close()

    # Dividir a lista de produtos em duas colunas
    metade = len(lista_produtos) // 2
    coluna1 = lista_produtos[:metade]
    coluna2 = lista_produtos[metade:]

    # Formatando os itens para exibir em cada coluna
    texto_coluna1 = "\n".join([f"{item[0]} - {item[1]}" for item in coluna1])
    texto_coluna2 = "\n".join([f"{item[0]} - {item[1]}" for item in coluna2])

    return texto_coluna1, texto_coluna2
       
def atualizar_treeview():
    cur.execute("SELECT * FROM transacoes")

    for item in tree.get_children():
        tree.delete(item)

    for linha in cur.fetchall():
        tree.insert('', 'end', values=linha)

    cur.execute("SELECT valor_custo, valor_venda FROM transacoes")

    transacoes_mes = cur.fetchall()

    total_valor_custo = sum(float(transacao[0]) for transacao in transacoes_mes)
    total_valor_venda = sum(float(transacao[1]) for transacao in transacoes_mes)

    label_total_custo.config(text=f"Total de custo : {total_valor_custo}")
    label_total_venda.config(text=f"Total de venda : {total_valor_venda}")
     # Obter os textos formatados para cada coluna
    texto_coluna1, texto_coluna2 = obter_lista_produtos_do_bd()

    # Atualizar o texto dos labels correspondentes
    label_lista_produtos_coluna1.config(text=texto_coluna1)
    label_lista_produtos_coluna2.config(text=texto_coluna2)

def verificar_e_limpar_bd():
    # Verificar se há itens no banco de dados
    cur.execute("SELECT COUNT(*) FROM transacoes")
    count = cur.fetchone()[0]
    if count > 0:
        # Se houver itens, perguntar ao usuário se deseja limpar a lista
        if messagebox.askokcancel("Limpar Lista", "Há itens no banco de dados. Deseja limpá-los?"):
            # Se o usuário confirmar, limpar os itens da Treeview
            for item in tree.get_children():
                tree.delete(item)
            
            # Limpar os dados do banco de dados
            cur.execute("DELETE FROM transacoes")
            conn.commit()
            
            # Reiniciar a sequência do SQLite para a tabela 'transacoes'
            cur.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'transacoes'")
            conn.commit()
            
            # Atualizar os totais para 0
            label_total_custo.config(text="Total de custo : 0")
            label_total_venda.config(text="Total de venda : 0")
    else:
        messagebox.showinfo("Banco de Dados Vazio", "Não há itens no banco de dados.")

        
def inserir():
    codigo_produto = e_codigo.get()
    data_pagamento = e_data.get_date().strftime('%Y-%m-%d')
    mes_pagamento = e_data.get_date().strftime('%Y-%m')
    inserir_com_detalhes(codigo_produto, data_pagamento, mes_pagamento)
    atualizar_treeview()

def deletar():
    selected_item = tree.selection()
    if selected_item:
        id_transacao = tree.item(selected_item)['values'][0]
        excluir_transacao(id_transacao)
        atualizar_treeview()
    else:
        messagebox.showinfo("ERROR", "Nenhuma transação selecionada para excluir.", icon='error')

janela = Tk()
janela.title("")
janela.geometry('1200x453')
janela.configure(background=co9)

frame_cima = Frame(janela, width=310, height=50, bg=co2, relief="flat")
frame_cima.grid(row=0, column=0)

frame_baixo = Frame(janela, width=310, height=403, bg=co1, relief="flat")
frame_baixo.grid(row=1, column=0, sticky=NSEW, padx=0, pady=1)

frame_direita = Frame(janela, width=588, height=403, bg=co1, relief="flat")
frame_direita.grid(row=0, column=1, rowspan=2, padx=1, pady=0, sticky=NSEW)

app_nome = Label(frame_cima, text='Formulário De Gastos', anchor=NW, font=('Ivy 13 bold'), bg=co2, fg=co1, relief="flat")
app_nome.place(x=10, y=20)

l_codigo = Label(frame_baixo, text='Codigo Do Produto *', anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4, relief="flat")
l_codigo.place(x=10, y=70)
e_codigo = Entry(frame_baixo, width=45, justify="left", relief="solid")
e_codigo.place(x=15, y=100)
##label produtos
label_lista_produtos_coluna1 = Label(frame_direita, text="", font=('Ivy 10 bold'), bg=co1, fg=co7, relief="flat", justify=LEFT)
label_lista_produtos_coluna1.place(x=300, y=255)

label_lista_produtos_coluna2 = Label(frame_direita, text="", font=('Ivy 10 bold'), bg=co1, fg=co7, relief="flat", justify=LEFT)
label_lista_produtos_coluna2.place(x=600, y=255)

l_data = Label(frame_baixo, text='Data*', anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4, relief="flat")
l_data.place(x=10, y=130)
e_data = DateEntry(frame_baixo, width=12, background='darkblue', foreground='white', borderwidth=2)
e_data.place(x=15, y=160)

conn = sqlite3.connect('dados.db')
cur = conn.cursor()

query = "SELECT * FROM transacoes"
cur.execute(query)
colunas = [col[0] for col in cur.description]

cur.execute("SELECT * FROM transacoes")
dados_transacoes = cur.fetchall()

label_total_venda = Label(frame_direita, text="", font=('Ivy 10 bold'), bg=co1, fg=co4, relief="flat")
label_total_venda.place(x=10, y=370)

def inserir():
    codigo_produto = e_codigo.get()
    data_pagamento = e_data.get_date().strftime('%Y-%m-%d')
    mes_pagamento = e_data.get_date().strftime('%Y-%m')
    inserir_com_detalhes(codigo_produto, data_pagamento, mes_pagamento)
    atualizar_treeview()

def deletar():
    selected_item = tree.selection()
    if selected_item:
        id_transacao = tree.item(selected_item)['values'][0]
        excluir_transacao(id_transacao)
        atualizar_treeview()
    else:
        messagebox.showinfo("ERROR", "Nenhuma transação selecionada para excluir.", icon='error')

tree = ttk.Treeview(frame_direita, columns=colunas, show="headings")

vsb = ttk.Scrollbar(frame_direita, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(frame_direita, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

tree.grid(column=0, row=0, sticky='nsew')
vsb.grid(column=1, row=0, sticky='ns')
hsb.grid(column=0, row=1, sticky='ew')

for col in colunas:
    tree.heading(col, text=col.title(), anchor=CENTER)
    tree.column(col, width=80, anchor=CENTER)

for dado in dados_transacoes:
    tree.insert('', 'end', values=dado)

for col in colunas:
    tree.heading(col, text=col.title(), anchor=CENTER)
    tree.column(col, width=max(70, len(col) * 10))

b_inserir = Button(frame_baixo, text='Inserir', width=10, font=('Ivy 9 bold'), bg=co6, fg=co1, relief="raised", overrelief='ridge', command=inserir)
b_inserir.place(x=15, y=200)

b_atualizar = Button(frame_baixo, text='Limpar', width=10, font=('Ivy 9 bold'), bg=co10, fg=co1, relief="raised", overrelief='ridge', command=verificar_e_limpar_bd)
b_atualizar.place(x=105, y=200)

b_deletar = Button(frame_baixo, text='Deletar', width=10, font=('Ivy 9 bold'), bg=co7, fg=co1, relief="raised", overrelief='ridge', command=deletar)
b_deletar.place(x=195, y=200)

label_total_custo = Label(frame_direita, text="", font=('Ivy 10 bold'), bg=co1, fg=co4, relief="flat")
label_total_custo.place(x=10, y=340)

atualizar_treeview()

janela.mainloop()

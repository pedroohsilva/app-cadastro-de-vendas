import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Criar janela principal
janela = tk.Tk()
janela.title("Cadastro de Vendas")
janela.geometry("600x400")

# Conexão e criação de tabela
conn = sqlite3.connect('cadastro.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        quantidade INTEGER
    )
''')
conn.commit()
conn.close()

# Navegação entre frames
frame_cadastro = tk.Frame(janela)
frame_visualizacao = tk.Frame(janela)

for frame in (frame_cadastro, frame_visualizacao):
    frame.grid(row=0, column=0, sticky='nsew')

# Funções de navegação e manipulação de dados
def cadastrar_produto():
    nome = entrada_nome.get()
    preco = entrada_preco.get()
    quantidade = entrada_quantidade.get()

    if not nome or not preco or not quantidade:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    try:
        preco = float(preco)
        quantidade = int(quantidade)
        conn = sqlite3.connect('cadastro.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO produto (nome, preco, quantidade) VALUES (?, ?, ?)', (nome, preco, quantidade))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
        entrada_nome.delete(0, tk.END)
        entrada_preco.delete(0, tk.END)
        entrada_quantidade.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser número decimal e quantidade um inteiro.")

def carregar_produtos():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('cadastro.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produto')
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def mostrar_frame(frame):
    frame.tkraise()
    if frame == frame_visualizacao:
        carregar_produtos()

def mostrar_ajuda():
    mensagem = (
        "📌 Projeto: Cadastro de Vendas\n"
        "👥 Autor: Pedro Henrique Alves da Silva\n"
        "💡 Descrição: Aplicação simples com interface Tkinter e banco SQLite para cadastrar e visualizar venda de produtos."
    )
    messagebox.showinfo("Ajuda", mensagem)

# Menu de navegação
menu_barra = tk.Menu(janela)

menu_navegacao = tk.Menu(menu_barra, tearoff=0)
menu_navegacao.add_command(label="Cadastro de Produtos", command=lambda: mostrar_frame(frame_cadastro))
menu_navegacao.add_command(label="Visualizar Produtos", command=lambda: mostrar_frame(frame_visualizacao))
menu_barra.add_cascade(label="Navegação", menu=menu_navegacao)

menu_ajuda = tk.Menu(menu_barra, tearoff=0)
menu_ajuda.add_command(label="Sobre", command=mostrar_ajuda)
menu_barra.add_cascade(label="Ajuda", menu=menu_ajuda)

janela.config(menu=menu_barra)

# Tela de cadastro de produtos
tk.Label(frame_cadastro, text="Nome do Produto:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entrada_nome = tk.Entry(frame_cadastro, width=30)
entrada_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_cadastro, text="Preço:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entrada_preco = tk.Entry(frame_cadastro, width=30)
entrada_preco.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame_cadastro, text="Quantidade:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entrada_quantidade = tk.Entry(frame_cadastro, width=30)
entrada_quantidade.grid(row=2, column=1, padx=10, pady=10)

botao_cadastrar = tk.Button(frame_cadastro, text="Cadastrar Produto", command=cadastrar_produto)
botao_cadastrar.grid(row=3, column=1, pady=20, sticky="e")

# Tela de visualização de produtos
tree = ttk.Treeview(frame_visualizacao, columns=("ID", "Nome", "Preço", "Quantidade"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Preço", text="Preço")
tree.heading("Quantidade", text="Quantidade")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Mostrar tela de cadastro ao iniciar
mostrar_frame(frame_cadastro)

janela.mainloop()

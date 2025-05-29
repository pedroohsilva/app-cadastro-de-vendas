import tkinter as tk
import sqlite3

# Criar janela principal
janela = tk.Tk()
janela.title("Cadastro de Vendas")
janela.geometry("360x260")

# Nome do Produto
label_nome_produto = tk.Label(janela, text="Nome do Produto:")
label_nome_produto.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entrada_nome_produto = tk.Entry(janela, width=30)
entrada_nome_produto.grid(row=0, column=1, padx=10, pady=10)

# Quantidade
label_quantidade = tk.Label(janela, text="Quantidade:")
label_quantidade.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entrada_quantidade = tk.Entry(janela, width=30)
entrada_quantidade.grid(row=1, column=1, padx=10, pady=10)

# Preço
label_preco = tk.Label(janela, text="Preço:")
label_preco.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entrada_preco = tk.Entry(janela, width=30)
entrada_preco.grid(row=2, column=1, padx=10, pady=10)

# Data
label_data = tk.Label(janela, text="Data (DD/MM/YYYY):")
label_data.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entrada_data = tk.Entry(janela, width=30)
entrada_data.grid(row=3, column=1, padx=10, pady=10)

# Função que insere os dados no banco
def inserir_dados():
    conn = sqlite3.connect('cadastro.db')
    cursor = conn.cursor()

    # Inserir produto
    cursor.execute('''
        INSERT INTO produto (nome, preco) VALUES (:nome, :preco)
    ''', {
        'nome': entrada_nome_produto.get(),
        'preco': float(entrada_preco.get())
    })

    produto_id = cursor.lastrowid  # Pega o ID do produto inserido

    # Inserir venda com produto_id referenciado
    cursor.execute('''
        INSERT INTO venda (data, quantidade, produto_id) VALUES (:data, :quantidade, :produto_id)
    ''', {
        'data': entrada_data.get(),
        'quantidade': int(entrada_quantidade.get()),
        'produto_id': produto_id
    })

    conn.commit()
    conn.close()

# Frame para botões
frame_botoes = tk.Frame(janela)
frame_botoes.grid(row=4, column=0, columnspan=2, pady=(10, 0))

# Botões empilhados
botao_enviar = tk.Button(frame_botoes, text="Cadastrar", width=20, command=inserir_dados)
botao_enviar.pack(pady=5)

botao_exportar_excel = tk.Button(frame_botoes, text="Exportar para Excel", width=20)
botao_exportar_excel.pack(pady=5)

# Iniciar loop da interface
janela.mainloop()

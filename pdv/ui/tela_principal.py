import tkinter as tk
from tkinter import ttk
import pdv.modelos.database as banco_de_dados
import pdv.util.printer as impressora
from tkinter import messagebox

class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Recibos")
        self.geometry("1280x720")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

        self.frame_cadastro = tk.Frame(self)
        self.frame_cadastro.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.frame_cadastro.columnconfigure(0, weight=1)
        self.frame_cadastro.columnconfigure(1, weight=1)
        self.frame_cadastro.columnconfigure(2, weight=1)

        self.botao_cadastrar_cliente = tk.Button(self.frame_cadastro, text="Cadastrar Cliente", command=self.cadastrar_cliente, bg="#4caf50", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_cadastrar_cliente.grid(row=0, column=0, padx=10)

        self.botao_cadastrar_produto = tk.Button(self.frame_cadastro, text="Cadastrar Produto", command=self.cadastrar_produto, bg="#2196f3", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_cadastrar_produto.grid(row=0, column=1, padx=10)

        self.botao_alterar_preco_produto = tk.Button(self.frame_cadastro, text="Alterar Preço Produto", command=self.alterar_preco_produto, bg="#ff9800", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_alterar_preco_produto.grid(row=0, column=2, padx=10)

        self.frame_cliente = tk.Frame(self)
        self.frame_cliente.grid(row=1, column=0, sticky="new", padx=10, pady=5)

        tk.Label(self.frame_cliente, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.cliente_combobox = ttk.Combobox(self.frame_cliente, values=banco_de_dados.obter_clientes())
        self.cliente_combobox.grid(row=0, column=1, sticky="ew")
        self.cliente_combobox.bind("<<ComboboxSelected>>", self.selecionar_cliente)

        tk.Label(self.frame_cliente, text="Endereço:").grid(row=1, column=0, sticky="w")
        self.endereco_entry = tk.Entry(self.frame_cliente)
        self.endereco_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(self.frame_cliente, text="Telefone:").grid(row=2, column=0, sticky="w")
        self.telefone_entry = tk.Entry(self.frame_cliente)
        self.telefone_entry.grid(row=2, column=1, sticky="ew")

        self.frame_produto = tk.Frame(self)
        self.frame_produto.grid(row=1, column=1, sticky="new", padx=10, pady=5)

        tk.Label(self.frame_produto, text="Produto:").grid(row=0, column=0, sticky="w")
        self.produto_combobox = ttk.Combobox(self.frame_produto, values=banco_de_dados.obter_produtos())
        self.produto_combobox.grid(row=0, column=1, sticky="ew")
        self.produto_combobox.bind("<<ComboboxSelected>>", self.selecionar_produto)

        tk.Label(self.frame_produto, text="Preço:").grid(row=1, column=0, sticky="w")
        self.preco_entry = tk.Entry(self.frame_produto)
        self.preco_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(self.frame_produto, text="Quantidade:").grid(row=2, column=0, sticky="w")
        self.quantidade_entry = tk.Entry(self.frame_produto)
        self.quantidade_entry.grid(row=2, column=1, sticky="ew")

        self.adicionar_produto_button = tk.Button(self.frame_produto, text="Adicionar Produto", command=self.adicionar_produto_lista, bg="#42a5f5", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
        self.adicionar_produto_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.frame_itens = tk.Frame(self)
        self.frame_itens.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        tk.Label(self.frame_itens, text="Itens:").grid(row=0, column=0, sticky="w")
        self.itens_listbox = tk.Listbox(self.frame_itens, height=5, width=60)
        self.itens_listbox.grid(row=1, column=0, sticky="ew")

        self.frame_taxa = tk.Frame(self)
        self.frame_taxa.grid(row=3, column=0, sticky="new", padx=10, pady=5)

        tk.Label(self.frame_taxa, text="Taxa de Entrega:").grid(row=0, column=0, sticky="w")
        self.taxa_entry = tk.Entry(self.frame_taxa)
        self.taxa_entry.grid(row=0, column=1, sticky="ew")

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.grid(row=3, column=1, sticky="ne", padx=10, pady=5)

        self.imprimir_button = tk.Button(self.frame_botoes, text="Imprimir Recibo", command=self.imprimir_recibo)
        self.imprimir_button.grid(row=0, column=0)

        self.frame_recibo = tk.Frame(self)
        self.frame_recibo.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.recibo_text = tk.Text(self.frame_recibo, height=10)
        self.recibo_text.grid(row=0, column=0, sticky="nsew")

        self.balanceamento_button = tk.Button(self.frame_cadastro, text="Balanceamento", command=self.janela_balanceamento, bg="#9c27b0", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.balanceamento_button.grid(row=0, column=3, padx=10) # Coluna 3

        self.itens = []

    def cadastrar_cliente(self):
        # Criar uma nova janela para o cadastro de cliente
        janela_cadastro_cliente = tk.Toplevel(self)
        janela_cadastro_cliente.title("Cadastro de Cliente")

        # Adicionar campos de entrada para os dados do cliente
        tk.Label(janela_cadastro_cliente, text="Nome:").grid(row=0, column=0, sticky="w")
        nome_entry = tk.Entry(janela_cadastro_cliente)
        nome_entry.grid(row=0, column=1)

        tk.Label(janela_cadastro_cliente, text="Endereço:").grid(row=1, column=0, sticky="w")
        endereco_entry = tk.Entry(janela_cadastro_cliente)
        endereco_entry.grid(row=1, column=1)

        tk.Label(janela_cadastro_cliente, text="Telefone:").grid(row=2, column=0, sticky="w")
        telefone_entry = tk.Entry(janela_cadastro_cliente)
        telefone_entry.grid(row=2, column=1)

        # Adicionar um botão "Salvar" para salvar os dados do cliente
        def salvar_cliente():
            nome = nome_entry.get()
            endereco = endereco_entry.get()
            telefone = telefone_entry.get()

            try:
                banco_de_dados.inserir_cliente(nome, endereco, telefone)
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                janela_cadastro_cliente.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")

        salvar_button = tk.Button(janela_cadastro_cliente, text="Salvar", command=salvar_cliente)

    def cadastrar_produto(self):
        # Criar uma nova janela para o cadastro de produto
        janela_cadastro_produto = tk.Toplevel(self)
        janela_cadastro_produto.title("Cadastro de Produto")

        # Adicionar campos de entrada para os dados do produto
        tk.Label(janela_cadastro_produto, text="Nome:").grid(row=0, column=0, sticky="w")
        nome_entry = tk.Entry(janela_cadastro_produto)
        nome_entry.grid(row=0, column=1)

        tk.Label(janela_cadastro_produto, text="Preço:").grid(row=1, column=0, sticky="w")
        preco_entry = tk.Entry(janela_cadastro_produto)
        preco_entry.grid(row=1, column=1)

        # Adicionar um botão "Salvar" para salvar os dados do produto
        def salvar_produto():
            nome = nome_entry.get()
            preco = preco_entry.get()

            try:
                if not nome:
                    raise ValueError("O nome do produto não pode estar vazio.")
                if not preco:
                    raise ValueError("O preço do produto não pode estar vazio.")
                if not preco.replace('.', '', 1).isdigit(): # permite apenas um ponto decimal
                    raise ValueError("O preço do produto deve ser um número válido.")

                banco_de_dados.inserir_produto(nome, preco)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                janela_cadastro_produto.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")

    def alterar_preco_produto(self):
        # Criar uma nova janela para alterar o preço do produto
        janela_alterar_preco = tk.Toplevel(self)
        janela_alterar_preco.title("Alterar Preço do Produto")

        # Adicionar campos de entrada para selecionar o produto e inserir o novo preço
        tk.Label(janela_alterar_preco, text="Produto:").grid(row=0, column=0, sticky="w")
        produtos = banco_de_dados.obter_produtos()
        produto_combobox = ttk.Combobox(janela_alterar_preco, values=produtos)
        produto_combobox.grid(row=0, column=1)

        tk.Label(janela_alterar_preco, text="Novo Preço:").grid(row=1, column=0, sticky="w")
        novo_preco_entry = tk.Entry(janela_alterar_preco)
        novo_preco_entry.grid(row=1, column=1)

        # Adicionar um botão "Salvar" para salvar o novo preço do produto
        def salvar_novo_preco():
            produto_nome = produto_combobox.get()
            novo_preco = novo_preco_entry.get()
            banco_de_dados.atualizar_preco_produto(produto_nome, novo_preco)
            janela_alterar_preco.destroy()

        salvar_button = tk.Button(janela_alterar_preco, text="Salvar", command=salvar_novo_preco)
        salvar_button.grid(row=2, column=1)

    def selecionar_cliente(self, event):
        cliente_nome = self.cliente_combobox.get()
        cliente_dados = banco_de_dados.obter_dados_cliente(cliente_nome)
        if cliente_dados:
            self.endereco_entry.delete(0, tk.END)
            self.endereco_entry.insert(0, cliente_dados['endereco'])
            self.telefone_entry.delete(0, tk.END)
            self.telefone_entry.insert(0, cliente_dados)
   
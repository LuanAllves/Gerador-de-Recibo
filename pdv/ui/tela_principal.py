# pdv/ui/tela_principal.py
import tkinter as tk
from tkinter import ttk
import pdv.modelos.database as db
from pdv.ui import tela_cadastro_cliente, tela_cadastro_produto, tela_alterar_preco_produto, tela_balanceamento
from pdv.util import printer
import pdv.ui.tela_principal as tela_principal

class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        db.criar_banco_dados() # Crie o banco de dados na inicialização
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

        self.botao_cadastrar_cliente = tk.Button(self.frame_cadastro, text="Cadastrar Cliente", command=self.abrir_tela_cadastro_cliente, bg="#4caf50", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_cadastrar_cliente.grid(row=0, column=0, padx=10)

        self.botao_cadastrar_produto = tk.Button(self.frame_cadastro, text="Cadastrar Produto", command=self.abrir_tela_cadastro_produto, bg="#2196f3", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_cadastrar_produto.grid(row=0, column=1, padx=10)

        self.botao_alterar_preco_produto = tk.Button(self.frame_cadastro, text="Alterar Preço Produto", command=self.abrir_tela_alterar_preco_produto, bg="#ff9800", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.botao_alterar_preco_produto.grid(row=0, column=2, padx=10)

        self.frame_cliente = tk.Frame(self)
        self.frame_cliente.grid(row=1, column=0, sticky="new", padx=10, pady=5)

        tk.Label(self.frame_cliente, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.cliente_combobox = ttk.Combobox(self.frame_cliente, values=db.obter_clientes())
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
        self.produto_combobox = ttk.Combobox(self.frame_produto, values=db.obter_produtos())
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

        self.balanceamento_button = tk.Button(self.frame_cadastro, text="Balanceamento", command=self.abrir_tela_balanceamento, bg="#9c27b0", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, padx=20, pady=10)
        self.balanceamento_button.grid(row=0, column=3, padx=10) # Coluna 3

        self.itens = []

    def abrir_tela_cadastro_cliente(self):
        tela_cadastro_cliente.TelaCadastroCliente(self)

    def abrir_tela_cadastro_produto(self):
        tela_cadastro_produto.TelaCadastroProduto(self)

    def abrir_tela_alterar_preco_produto(self):
        tela_alterar_preco_produto.TelaAlterarPreco
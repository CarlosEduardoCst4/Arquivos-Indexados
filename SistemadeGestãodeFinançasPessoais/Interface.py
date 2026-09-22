from tkinter import Tk, Frame, Label, Entry, Button, StringVar
from tkinter import ttk

class App:
    def __init__(self, root, repo_bancos, repo_pessoas, repo_categorias, repo_contas, repo_transacoes):
        self.root = root
        self.root.title("Gestão de Finanças Pessoais")

        # guarda os repositórios já criados no Main.py
        self.repo_bancos = repo_bancos
        self.repo_pessoas = repo_pessoas
        self.repo_categorias = repo_categorias
        self.repo_contas = repo_contas
        self.repo_transacoes = repo_transacoes

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        aba_bancos = Frame(notebook)
        notebook.add(aba_bancos, text="Bancos")
        self.montar_tela_bancos(aba_bancos)

        aba_pessoas = Frame(notebook)
        notebook.add(aba_pessoas, text="Pessoas")
        self.montar_tela_pessoas(aba_pessoas)

        aba_categorias = Frame(notebook)
        notebook.add(aba_categorias, text="Categorias")
        self.montar_tela_categorias(aba_categorias)

        aba_contas = Frame(notebook)
        notebook.add(aba_contas, text="Contas")
        self.montar_tela_contas(aba_contas)

        aba_transacoes = Frame(notebook)
        notebook.add(aba_transacoes, text="Transações")
        self.montar_tela_transacoes(aba_transacoes)

    def montar_tela_bancos(self, container):
        Label(container, text="Descrição:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_descricao_banco = Entry(container)
        self.entry_descricao_banco.grid(row=0, column=1, padx=5, pady=5)

        Button(container, text="Incluir", command=self.incluir_banco).grid(row=0, column=2, padx=5)

        self.tabela_bancos = ttk.Treeview(container, columns=("codigo", "descricao"), show="headings")
        self.tabela_bancos.heading("codigo", text="Código")
        self.tabela_bancos.heading("descricao", text="Descrição")
        self.tabela_bancos.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        self.atualizar_tabela_bancos()

    def incluir_banco(self):
        descricao = self.entry_descricao_banco.get()
        self.repo_bancos.incluir(descricao)
        self.entry_descricao_banco.delete(0, "end")
        self.atualizar_tabela_bancos()

    def atualizar_tabela_bancos(self):
        for item in self.tabela_bancos.get_children():
            self.tabela_bancos.delete(item)
        for banco in self.repo_bancos.listar():
            self.tabela_bancos.insert("", "end", values=(banco.cod_banco, banco.descricao))

    def montar_tela_pessoas(self, container):
        Label(container, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome_pessoa = Entry(container)
        self.entry_nome_pessoa.grid(row=0, column=1, padx=5, pady=5)

        Button(container, text="Incluir", command=self.incluir_pessoa).grid(row=0, column=2, padx=5)

        self.tabela_pessoas = ttk.Treeview(container, columns=("codigo", "nome"), show="headings")
        self.tabela_pessoas.heading("codigo", text="Código")
        self.tabela_pessoas.heading("nome", text="Nome")
        self.tabela_pessoas.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        self.atualizar_tabela_pessoas()

    def incluir_pessoa(self):
        nome = self.entry_nome_pessoa.get().strip()
        if not nome:
            return
        self.repo_pessoas.incluir(nome)
        self.entry_nome_pessoa.delete(0, "end")
        self.atualizar_tabela_pessoas()

    def atualizar_tabela_pessoas(self):
        for item in self.tabela_pessoas.get_children():
            self.tabela_pessoas.delete(item)
        for pessoa in self.repo_pessoas.listar():
            self.tabela_pessoas.insert("", "end", values=(pessoa.codigo, pessoa.nome))

    def montar_tela_categorias(self, container):
        Label(container, text="Descrição:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_descricao_categoria = Entry(container)
        self.entry_descricao_categoria.grid(row=0, column=1, padx=5, pady=5)

        Button(container, text="Incluir", command=self.incluir_categoria).grid(row=0, column=2, padx=5)

        self.tabela_categorias = ttk.Treeview(container, columns=("codigo", "descricao"), show="headings")
        self.tabela_categorias.heading("codigo", text="Código")
        self.tabela_categorias.heading("descricao", text="Descrição")
        self.tabela_categorias.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        self.atualizar_tabela_categorias()

    def incluir_categoria(self):
        descricao = self.entry_descricao_categoria.get().strip()
        if not descricao:
            return
        self.repo_categorias.incluir(descricao)
        self.entry_descricao_categoria.delete(0, "end")
        self.atualizar_tabela_categorias()

    def atualizar_tabela_categorias(self):
        for item in self.tabela_categorias.get_children():
            self.tabela_categorias.delete(item)
        for cat in self.repo_categorias.listar():
            self.tabela_categorias.insert("", "end", values=(cat.codigoCat, cat.descricao))

    def montar_tela_contas(self, container):
        Label(container, text="Descrição:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_descricao_conta = Entry(container, width=25)
        self.entry_descricao_conta.grid(row=0, column=1, padx=5, pady=5)

        Label(container, text="Banco:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_banco_conta = ttk.Combobox(container, state="readonly", width=25)
        self.combo_banco_conta.grid(row=1, column=1, padx=5, pady=5)

        Label(container, text="Pessoa:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_pessoa_conta = ttk.Combobox(container, state="readonly", width=25)
        self.combo_pessoa_conta.grid(row=2, column=1, padx=5, pady=5)

        Label(container, text="Saldo inicial:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_saldo_conta = Entry(container, width=25)
        self.entry_saldo_conta.grid(row=3, column=1, padx=5, pady=5)

        Button(container, text="Incluir", command=self.incluir_conta).grid(row=1, column=2, padx=5)

        self.tabela_contas = ttk.Treeview(container, columns=("codigo", "descricao", "banco", "pessoa", "saldo"), show="headings")
        for col, titulo in [("codigo", "Código"), ("descricao", "Descrição"), ("banco", "Banco"), ("pessoa", "Pessoa"), ("saldo", "Saldo")]:
            self.tabela_contas.heading(col, text=titulo)
        self.tabela_contas.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        self.atualizar_combo_banco_conta()
        self.atualizar_combo_pessoa_conta()
        self.atualizar_tabela_contas()

    def atualizar_combo_banco_conta(self):
        self.bancos_disponiveis = self.repo_bancos.listar()
        self.combo_banco_conta["values"] = [b.descricao for b in self.bancos_disponiveis]

    def atualizar_combo_pessoa_conta(self):
        self.pessoas_disponiveis = self.repo_pessoas.listar()
        self.combo_pessoa_conta["values"] = [p.nome for p in self.pessoas_disponiveis]

    def incluir_conta(self):
        idx_banco = self.combo_banco_conta.current()
        idx_pessoa = self.combo_pessoa_conta.current()
        if idx_banco == -1 or idx_pessoa == -1:
            return
        try:
            saldo = float(self.entry_saldo_conta.get())
        except ValueError:
            return

        cod_banco = self.bancos_disponiveis[idx_banco].cod_banco
        cod_pessoa = self.pessoas_disponiveis[idx_pessoa].codigo
        descricao = self.entry_descricao_conta.get().strip()

        self.repo_contas.incluir(cod_banco, cod_pessoa, descricao, saldo)
        self.entry_descricao_conta.delete(0, "end")
        self.entry_saldo_conta.delete(0, "end")
        self.atualizar_tabela_contas()

    def atualizar_tabela_contas(self):
        for item in self.tabela_contas.get_children():
            self.tabela_contas.delete(item)
        for conta in self.repo_contas.listar():
            banco = self.repo_bancos.buscar(conta.codBanco)
            pessoa = self.repo_pessoas.buscar(conta.codPessoa)
            self.tabela_contas.insert("", "end", values=(conta.codConta, conta.descricao, banco.descricao, pessoa.nome, f"R$ {conta.saldo:.2f}"))

    def montar_tela_transacoes(self, container):
        Label(container, text="Categoria:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_categoria_trans = ttk.Combobox(container, state="readonly", width=25)
        self.combo_categoria_trans.grid(row=0, column=1, padx=5, pady=5)

        Label(container, text="Conta:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_conta_trans = ttk.Combobox(container, state="readonly", width=25)
        self.combo_conta_trans.grid(row=1, column=1, padx=5, pady=5)

        Label(container, text="Data (AAAA-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_data_trans = Entry(container, width=25)
        self.entry_data_trans.grid(row=2, column=1, padx=5, pady=5)

        Label(container, text="Valor:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_valor_trans = Entry(container, width=25)
        self.entry_valor_trans.grid(row=3, column=1, padx=5, pady=5)

        Label(container, text="Tipo:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.combo_tipo_trans = ttk.Combobox(container, state="readonly", width=25, values=["Débito", "Crédito"])
        self.combo_tipo_trans.grid(row=4, column=1, padx=5, pady=5)

        Button(container, text="Lançar", command=self.incluir_transacao).grid(row=1, column=2, padx=5)

        self.tabela_transacoes = ttk.Treeview(container, columns=("codigo", "data", "categoria", "conta", "tipo", "valor"), show="headings")
        for col, titulo in [("codigo", "Código"), ("data", "Data"), ("categoria", "Categoria"), ("conta", "Conta"), ("tipo", "Tipo"), ("valor", "Valor")]:
            self.tabela_transacoes.heading(col, text=titulo)
        self.tabela_transacoes.grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

        self.atualizar_combo_categoria_trans()
        self.atualizar_combo_conta_trans()
        self.atualizar_tabela_transacoes()

    def atualizar_combo_categoria_trans(self):
        self.categorias_disponiveis = self.repo_categorias.listar()
        self.combo_categoria_trans["values"] = [c.descricao for c in self.categorias_disponiveis]

    def atualizar_combo_conta_trans(self):
        self.contas_disponiveis = self.repo_contas.listar()
        self.combo_conta_trans["values"] = [c.descricao for c in self.contas_disponiveis]

    def incluir_transacao(self):
        idx_cat = self.combo_categoria_trans.current()
        idx_conta = self.combo_conta_trans.current()
        tipo_selecionado = self.combo_tipo_trans.get()
        if idx_cat == -1 or idx_conta == -1 or tipo_selecionado == "":
            return
        try:
            valor = float(self.entry_valor_trans.get())
        except ValueError:
            return

        cod_categoria = self.categorias_disponiveis[idx_cat].codigoCat
        cod_conta = self.contas_disponiveis[idx_conta].codConta
        data = self.entry_data_trans.get().strip()
        tipo = "D" if tipo_selecionado == "Débito" else "C"

        self.repo_transacoes.incluir(cod_categoria, cod_conta, data, valor, tipo)
        self.entry_data_trans.delete(0, "end")
        self.entry_valor_trans.delete(0, "end")
        self.atualizar_combo_conta_trans()
        self.atualizar_tabela_transacoes()

    def atualizar_tabela_transacoes(self):
        for item in self.tabela_transacoes.get_children():
            self.tabela_transacoes.delete(item)
        for t in self.repo_transacoes.listar():
            categoria = self.repo_categorias.buscar(t.codCategoria)
            conta = self.repo_contas.buscar(t.codConta)
            self.tabela_transacoes.insert("", "end", values=(t.codTransacao, t.data, categoria.descricao, conta.descricao, t.DebitoCredito, f"R$ {t.valor:.2f}"))
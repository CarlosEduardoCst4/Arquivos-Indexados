import json
import os

class ContasBancarias:
    def __init__(self, codConta, codBanco, codPessoa, descricao, saldo):
        self.codConta = codConta
        self.codBanco = codBanco
        self.codPessoa = codPessoa
        self.descricao = descricao
        self.saldo = saldo

    def to_dict(self):
        return {
            "codConta": self.codConta,
            "codBanco": self.codBanco,
            "codPessoa": self.codPessoa,
            "descricao": self.descricao,
            "saldo": self.saldo,
        }

    @staticmethod
    def from_dict(d):
        return ContasBancarias(d["codConta"], d["codBanco"], d["codPessoa"], d["descricao"], d["saldo"])
    

class Cb:
    def __init__(self, codigo, posicao):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inclusao(self, k, endereco):
        novo = Cb(k, endereco)
        if self.raiz is None:
            self.raiz = novo
            return
        atual = self.raiz
        pai = None
        while atual is not None:
            pai = atual
            if k < atual.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita
        if k < pai.codigo:
            pai.esquerda = novo
        else:
            pai.direita = novo

    def busca_na_arvore(self, k):
        atual = self.raiz
        while atual is not None:
            if k == atual.codigo:
                return atual.posicao
            elif k < atual.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def listar_codigos(self):
        codigos = []
        self._em_ordem(self.raiz, codigos)
        return codigos

    def _em_ordem(self, no, codigos):
        if no is not None:
            self._em_ordem(no.esquerda, codigos)
            codigos.append(no.codigo)
            self._em_ordem(no.direita, codigos)

    def limpar(self):
        self.raiz = None

class RepositorioContasBancarias:
    ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "contas.jsonl")

    def __init__(self, repo_bancos, repo_pessoas):
        self.arvore = ArvoreBinaria()
        self.proximo_codigo = 1
        self.repo_bancos = repo_bancos
        self.repo_pessoas = repo_pessoas
        self._carregar_indice()

    def _carregar_indice(self):
        os.makedirs(os.path.dirname(self.ARQUIVO), exist_ok=True)
        if not os.path.exists(self.ARQUIVO):
            return
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            while True:
                pos = arq.tell()
                linha = arq.readline()
                if linha == "":
                    break
                d = json.loads(linha)
                self.arvore.inclusao(d["codConta"], pos)
                if d["codConta"] >= self.proximo_codigo:
                    self.proximo_codigo = d["codConta"] + 1

    def incluir(self, codBanco, codPessoa, descricao, saldoInicial):
        conta = ContasBancarias(self.proximo_codigo, codBanco, codPessoa, descricao, saldoInicial)
        with open(self.ARQUIVO, "a", encoding="utf-8") as arq:
            pos = arq.tell()
            arq.write(json.dumps(conta.to_dict()) + "\n")
        self.arvore.inclusao(conta.codConta, pos)
        self.proximo_codigo += 1
        return conta

    def buscar(self, codigo):
        pos = self.arvore.busca_na_arvore(codigo)
        if pos is None:
            return None
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            arq.seek(pos)
            return ContasBancarias.from_dict(json.loads(arq.readline()))

    def listar(self):
        return [self.buscar(c) for c in self.arvore.listar_codigos()]

    def atualizar_saldo(self, codConta, novoSaldo):
        contas = self.listar()
        for c in contas:
            if c.codConta == codConta:
                c.saldo = novoSaldo
        self._regravar(contas)

    def _regravar(self, contas):
        self.arvore.limpar()
        with open(self.ARQUIVO, "w", encoding="utf-8") as arq:
            for c in contas:
                pos = arq.tell()
                arq.write(json.dumps(c.to_dict()) + "\n")
                self.arvore.inclusao(c.codConta, pos)

    def ler_codigo_conta(self, mensagem="Código da conta; "):
        while True:
            codigo = int(input(mensagem))
            conta = self.buscar(codigo)
            if conta is None:
                print("Código naõ encontrado. Tente novamnete.")
                continue
            banco = self.repo_bancos.buscar(conta.codBanco)
            pessoa = self.repo_pessoas.buscar(conta.codPessoa)
            print(f"Conta: {conta.descricao} | Banco: {banco.descricao} | Titular: {pessoa.nome}")
            return conta.codConta

    def menu(self):
        while True:
            print("\n=== CONTAS BANCÁRIAS ===")
            print("1 - Cadastar")
            print("2 - Listar")
            print("0 - Voltar")
            opcao = input("Opção: ").strip()
            match opcao:
                case "1":
                    cod_banco = self.repo_bancos.ler_codigo_banco("Cod_Banco: ")
                    cod_pessoa = self.repo_pessoas.ler_codigo_pessoa("Cod_Pessoa: ")
                    decricao = input("Descrição daconta: ").strip()
                    saldo_inicial = float(input("Saldo inicial: "))
                    conta = self.incluir(cod_banco, cod_pessoa, decricao, saldo_inicial)
                    print(f"Conta cadastrada com código {conta.codConta}.")
                case "2":
                    contas = self.listar()
                    if not contas:
                        print("Nenhuma conta cadastarda.")
                    for c in contas:
                        banco = self.repo_bancos.buscar(c.codBanco)
                        pessoa = self.repo_pessoas.buscar(c.codPessoa)
                        print(f"{c.codConta} - {c.descricao} | Banco: {banco.descricao} | Titular: {pessoa.nome} | Saldo: R$ {c.saldo:.2f}")
                case "0":
                    break
                case _:
                    print("Opção invalida.")
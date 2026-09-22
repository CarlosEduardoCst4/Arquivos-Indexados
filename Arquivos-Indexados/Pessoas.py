import json
import os

class Pessoa:
    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome}

    @staticmethod
    def from_dict(d):
        return Pessoa(d["codigo"], d["nome"])

class Po:
    def __init__(self, codigo, posicao):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:

    def __init__(self):
        self.raiz = None

    def inclusao(self, k, endereco):
        novo = Po(k, endereco)
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

    def listar_codigo(self):
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


class RepositorioPessoas:
    ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "pessoas.jsonl")

    def __init__(self):
        self.arvore = ArvoreBinaria()
        self.proximo_codigo = 1
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
                self.arvore.inclusao(d["codigo"], pos)
                if d["codigo"] >= self.proximo_codigo:
                    self.proximo_codigo = d["codigo"] + 1

    def incluir(self, nome):
        pessoa = Pessoa(self.proximo_codigo, nome)
        with open(self.ARQUIVO, "a", encoding="utf-8") as arq:
            pos = arq.tell()
            arq.write(json.dumps(pessoa.to_dict()) + "\n")
            self.arvore.inclusao(pessoa.codigo, pos)
            self.proximo_codigo += 1
            return pessoa

    def buscar(self, codigo):
        pos = self.arvore.busca_na_arvore(codigo)
        if pos is None:
            return None
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            arq.seek(pos)
            return Pessoa.from_dict(json.loads(arq.readline()))

    def listar(self):
        return [self.buscar(c) for c in self.arvore.listar_codigo()]

    def ler_codigo_pessoa(self, mensagem="Código da Pessoa: "):
        while True:
            codigo = int(input(mensagem))
            pessoa = self.buscar(codigo)
            if pessoa is None:
                print("Código não encontrado. Tente novamente. ")
                continue
            print(f"Pessoa: {pessoa.nome}")
            return pessoa.codigo

    def menu(self):
        while True:
            print("\n=== PESSOAS ===")
            print("1 - Cadastrar")
            print("2 - Listar")
            print("0 - Voltar")
            opcao = input("Opção: ").strip()
            match opcao:
                case "1":
                    nome = input("Nome: ").strip()
                    if not nome:
                        print("Nome não pode ser vazio.")
                        continue
                    p = self.incluir(nome)
                    print(f"Cadastrada com código {p.codigo}.")
                case "2":
                    pessoas = self.listar()
                    if not pessoas:
                        print("Nenhuma pessoa cadastrada.")
                    else:
                        for p in pessoas:
                            print(f"{p.codigo} - {p.nome}")
                case "0":
                    break
                case _:
                    print("Opção invalida.")

import json
import os

class Transacoes:
    def __init__(self, codTransacao, codCategoria, codConta,  data, valor, DebitoCredito):
        self.codTransacao = codTransacao
        self.codCategoria = codCategoria
        self.codConta = codConta
        self.data = data
        self.valor = valor
        self.DebitoCredito = DebitoCredito

    def to_dict(self):
        return {
            "codigoTrans": self.codTransacao,
            "codCategoria": self.codCategoria,
            "codConta": self.codConta,
            "data": self.data,
            "valor": self.valor,
            "debitoCredito": self.DebitoCredito
        }

    @staticmethod
    def from_dict(d):
        return Transacoes(d["codigoTrans"], d["codCategoria"], d["codConta"], d["data"], d["valor"], d["debitoCredito"])
    
class Tr:
    def __init__(self, codigo, posicao):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:

    def __init__(self):
        self.raiz = None

    def inclusao(self, k, endereco):
        novo = Tr(k, endereco)
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

class RepositorioTransacoes:
    ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "transacoes.jsonl")

    def __init__(self, repo_categorias, repo_contas):
        self.arvore = ArvoreBinaria()
        self.proximo_codigo = 1
        self.repo_categorias = repo_categorias
        self.repo_contas = repo_contas
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
                self.arvore.inclusao(d["codigoTrans"], pos)
                if d["codigoTrans"] >= self.proximo_codigo:
                    self.proximo_codigo = d["codigoTrans"] + 1

    def incluir(self, codCategoria, codConta, data, valor, debitoCredito):
        trans = Transacoes(self.proximo_codigo, codCategoria, codConta, data, valor, debitoCredito)
        with open(self.ARQUIVO, "a", encoding="utf-8") as arq:
            pos =arq.tell()
            arq.write(json.dumps(trans.to_dict()) + "\n")
        self.arvore.inclusao(trans.codTransacao, pos)
        self.proximo_codigo += 1

        conta = self.repo_contas.buscar(codConta)
        if debitoCredito == "C":
            novo_saldo = conta.saldo + valor
        else:
            novo_saldo = conta.saldo - valor
        self.repo_contas.atualizar_saldo(codConta, novo_saldo)
        return trans

    def buscar(self, codigo):
        pos = self.arvore.busca_na_arvore(codigo)
        if pos is None:
            return None
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            arq.seek(pos)
            return Transacoes.from_dict(json.loads(arq.readline()))

    def listar(self):
        return [self.buscar(c) for c in self.arvore.listar_codigos()]

    def excluir(self, codigoTransacao):
        trans = self.buscar(codigoTransacao)
        if trans is None:
            return False

        conta = self.repo_contas.buscar(trans.codConta)
        if trans.DebitoCredito == "C":
            saldo_estornado = conta.saldo - trans.valor
        else:
            saldo_estornado = conta.saldo + trans.valor
        self.repo_contas.atualizar_saldo(trans.codConta, saldo_estornado)

        restantes = [t for t in self.listar() if t.codTransacao != codigoTransacao]
        self._regravar(restantes)
        return True

    def _regravar(self, transacoes):
        self.arvore.limpar()
        with open(self.ARQUIVO, "w", encoding="utf-8") as arq:
            for t in transacoes:
                pos = arq.tell()
                arq.write(json.dumps(t.to_dict()) + "\n")
                self.arvore.inclusao(t.codTransacao, pos)

    def extrato_por_periodo(self, data_ini, data_fim):
        transacoes = [t for t in self.listar() if data_ini <= t.data <= data_fim]
        if not transacoes:
            print("Nenhuma transação no periodo.")
            return

        saldo_periodo = 0
        print(f"\n--- TRANSAÇÕES DE {data_ini} A {data_fim} ---")
        for t in transacoes:
            categoria = self.repo_categorias.buscar(t.codCategoria)
            conta = self.repo_contas.buscar(t.codConta)
            banco = self.repo_contas.repo_bancos.buscar(conta.codBanco)
            sinal = "+" if t.DebitoCredito == "C" else "-"
            saldo_periodo += t.valor if t.DebitoCredito == "C" else -t.valor
            print(f"{t.codTransacao} | {t.data} | {categoria.descricao} | Banco: {banco.descricao} | {sinal}R$ {t.valor:.2f}")

    def menu(self):
        while True:
            print("\n=== TRANSAÇÕES ===")
            print("1 - Lançar transação")
            print("2 - Listar todas")
            print("3 - Excluir transação")
            print("0 - Voltar")
            opcao = input("Opção: ").strip()
            match opcao:
                case "1":
                    codCategoria = self.repo_categorias.ler_codigo_categoria("codCategoria: ")
                    codConta = self.repo_contas.ler_codigo_conta("codConta: ")
                    data = input("Data (AAAA-MM-DD): ").strip()
                    valor = float(input("Valor: "))
                    tipo = ""
                    while tipo not in ("D", "C"):
                        tipo = input("Débito ou Crédito? (D/C): ").strip().upper()
                    trans = self.incluir(codCategoria, codConta, data, valor, tipo)
                    print(f"Transação {trans.codTransacao} lançada. Saldo da conta atualizado.")
                case "2":
                    transacoes = self.listar()
                    if not transacoes:
                        print("Nenhuma transação cadastrada.")
                    for t in transacoes:
                        categoria = self.repo_categorias.buscar(t.codCategoria)
                        conta = self.repo_contas.buscar(t.codConta)
                        banco = self.repo_contas.repo_bancos.buscar(conta.codBanco)
                        print(f"{t.codTransacao} | {t.data} | {categoria.descricao} | Banco: {banco.descricao} | {t.DebitoCredito} | R$ {t.valor:.2f}")
                case "3":
                    codigo = int(input("Código da transação a excluir: "))
                    if self.excluir(codigo):
                        print("Transação excluida e saldo estornado.")
                    else:
                        print("Código não encontrado.")
                case "0":
                    break
                case _:
                    print("Opção inválida.")
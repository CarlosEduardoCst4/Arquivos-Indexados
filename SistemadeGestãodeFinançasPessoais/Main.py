from Pessoas import RepositorioPessoas
from Bancos import RepositorioBancos
from CategoriaGastos import RepositorioCategoriaGasto
from ContasBancarias import RepositorioContasBancarias
from Transacoes import RepositorioTransacoes
from Interface import App
from tkinter import Tk

def relatorio_saldos(repo_contas):
    contas = repo_contas.listar()
    if not contas:
        return
    total = 0
    for c in contas:
        banco = repo_contas.repo_bancos.buscar(c.codBanco)
        pessoa = repo_contas.repo_pessoas.buscar(c.codPessoa)
        print(f"{c.codConta} - {c.descricao} | Banco: {banco.descricao} | Titular: {pessoa.nome} | Saldo: R$ {c.saldo:.2f}")
        total += c.saldo

def main():
    repo_pessoas = RepositorioPessoas()
    repo_bancos = RepositorioBancos()
    repo_categoriaGastos = RepositorioCategoriaGasto()
    repo_contaBancaria = RepositorioContasBancarias(repo_bancos, repo_pessoas)
    repo_transacoes = RepositorioTransacoes(repo_categoriaGastos, repo_contaBancaria)

    root = Tk()
    app = App(root, repo_bancos, repo_pessoas, repo_categoriaGastos, repo_contaBancaria, repo_transacoes)
    root.mainloop()

if __name__ == "__main__":
    main()  
from Pessoas import RepositorioPessoas
from Bancos import RepositorioBancos
from CategoriaGastos import RepositorioCategoriaGasto
from ContasBancarias import RepositorioContasBancarias
from Transacoes import RepositorioTransacoes

def relatorio_saldos(repo_contas):
    contas = repo_contas.listar()
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    total = 0
    print("\n=== SALDOS DAS CONTAS ===")
    for c in contas:
        banco = repo_contas.repo_bancos.buscar(c.codBanco)
        pessoa = repo_contas.repo_pessoas.buscar(c.codPessoa)
        print(f"{c.codConta} - {c.descricao} | Banco: {banco.descricao} | Titular: {pessoa.nome} | Saldo: R$ {c.saldo:.2f}")
    total += c.saldo
    print(f"Saldo geral: R$ {total:.2f}")
 

def main():
    repo_pessoas = RepositorioPessoas()
    repo_bancos = RepositorioBancos()
    repo_categoriaGastos = RepositorioCategoriaGasto()
    repo_contaBancaria = RepositorioContasBancarias(repo_bancos, repo_pessoas)
    repo_transacoes = RepositorioTransacoes(repo_categoriaGastos, repo_contaBancaria)

    while True:
        print("\n=== SISTEMA DE GESTÃO DE FINANÇAS PESSOAIS ===")
        print("1 - Pessoas ( Cadastrar / Listar )")
        print("2 - Bancos")
        print("3 - Categoria dos Gastos")
        print("4 - Contas Bancarias")
        print("5 - Transações (Lançar / Listar / Excluir)")
        print("6 - Extrato por periodo")
        print("7 - Saldos de todas as contas")
        print("0 - Sair")

        opcao = input("Opção: ").strip()
        match opcao:
            case "1":
                repo_pessoas.menu()
            case "2":
                repo_bancos.menu()
            case "3":
                repo_categoriaGastos.menu()
            case "4":
                repo_contaBancaria.menu()
            case "5":
                repo_transacoes.menu()
            case "6":
                data_init = input("Data inicial (AAAA-MM-DD): ").strip()
                data_fim = input("Data final (AAAA-MM-DD): ").strip()
                repo_transacoes.extrato_por_periodo(data_init, data_fim)
            case "7":
                relatorio_saldos(repo_contaBancaria)
            case "0":
                print("Até Logo!")
                break
            case _:
                print("Opção invélida.")

if __name__ == "__main__":
    main()
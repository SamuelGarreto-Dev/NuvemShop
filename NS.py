from defs import GerenciadorProdutos
import tkinter.messagebox as messagebox


def main():
    # Preencha com suas informações locais do PostgreSQL
    dbname = '----'
    user = '----'
    password = '----'
    host = 'localhost'
    port = 0000

    # Crie uma instância do GerenciadorProdutos com as informações de conexão
    gerenciador = GerenciadorProdutos(dbname, user, password, host, port)

    while True:
        print("\nMenu:")
        print("1. Cadastrar Produto")
        print("2. Alterar Produto")
        print("3. Excluir Produto")
        print("4. Visualizar Produtos")
        print("5. Sair")

        escolha = input("Escolha a opção desejada (1-5): ")

        try:
            if escolha == '1':
                nome = input("Digite o nome do produto: ")
                preco = float(input("Digite o preço do produto: "))
                quantidade = int(input("Digite a quantidade do produto: "))
                gerenciador.cadastrar_produto(nome, preco, quantidade)
                
            elif escolha == '2':
                nome = input("Digite o nome do produto que deseja alterar: ")
                preco = float(input("Digite o novo preço do produto (ou pressione Enter para manter o mesmo): "))
                quantidade = int(input("Digite a nova quantidade do produto (ou pressione Enter para manter a mesma): "))
                gerenciador.alterar_produto(nome, preco, quantidade)
                
            elif escolha == '3':
                nome = input("Digite o nome do produto que deseja excluir: ")
                gerenciador.excluir_produto(nome)
                
            elif escolha == '4':
                gerenciador.visualizar_produtos()
                
            elif escolha == '5':
                print("Saindo do programa. Até mais!")
                break
            
            else:
                print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")
                messagebox.showerror("Erro", "Opção inválida. Por favor, escolha uma opção de 1 a 5.")
                
        except ValueError as e:
            print(f"Erro: {e}. Certifique-se de inserir um valor numérico correto.")
            messagebox.showerror("Erro", f"Erro: {e}. Certifique-se de inserir um valor numérico correto.")
            
        except Exception as e:
            print(f"Erro inesperado: {e}")
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()


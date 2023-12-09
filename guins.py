import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from defs import GerenciadorProdutos

class InterfaceGrafica:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Produtos")

        # Defina um tamanho padrão para a janela principal
        self.master.geometry("1000x600")

        # Preencha com suas informações locais do PostgreSQL
        dbname = '----'
        user = '----'
        password = '----'
        host = 'localhost'
        port = 0000

        # Crie uma instância do GerenciadorProdutos com as informações de conexão
        self.gerenciador = GerenciadorProdutos(dbname, user, password, host, port)

        self.create_widgets()

    def create_widgets(self):
        # Adicione um estilo ao Treeview
        style = ttk.Style()
        style.theme_use("clam")  # Você pode experimentar outros temas disponíveis
        style.configure("Treeview", background="#D3D3D3", fieldbackground="#D3D3D3", foreground="black")
        style.map("Treeview", background=[('selected', '#347083')])

        # Use Labelframes para organizar os elementos
        frame_cadastro = ttk.Labelframe(self.master, text="Cadastro de Produto")
        frame_cadastro.pack(pady=10, padx=10)

        self.label_nome = tk.Label(frame_cadastro, text="Nome do Produto:")
        self.label_nome.grid(row=0, column=0, pady=5)
        self.entry_nome = tk.Entry(frame_cadastro)
        self.entry_nome.grid(row=0, column=1, pady=5)

        self.label_preco = tk.Label(frame_cadastro, text="Preço do Produto:")
        self.label_preco.grid(row=1, column=0, pady=5)
        self.entry_preco = tk.Entry(frame_cadastro)
        self.entry_preco.grid(row=1, column=1, pady=5)

        self.label_quantidade = tk.Label(frame_cadastro, text="Quantidade do Produto:")
        self.label_quantidade.grid(row=2, column=0, pady=5)
        self.entry_quantidade = tk.Entry(frame_cadastro)
        self.entry_quantidade.grid(row=2, column=1, pady=5)

        self.button_cadastrar = tk.Button(frame_cadastro, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.button_cadastrar.grid(row=3, columnspan=2, pady=10)

        self.button_alterar = tk.Button(frame_cadastro, text="Alterar Produto", command=self.alterar_produto)
        self.button_alterar.grid(row=4, columnspan=2, pady=10)

        self.button_excluir = tk.Button(frame_cadastro, text="Excluir Produto", command=self.excluir_produto)
        self.button_excluir.grid(row=5, columnspan=2, pady=10)

        # Adicione espaçamento
        ttk.Separator(self.master, orient="horizontal").pack(fill="x", pady=10)

        # Use Labelframe para a visualização de produtos
        frame_visualizacao = ttk.Labelframe(self.master, text="Visualização de Produtos")
        frame_visualizacao.pack(pady=10, padx=10)

        self.button_visualizar = tk.Button(frame_visualizacao, text="Visualizar Produtos", command=self.visualizar_produtos)
        self.button_visualizar.pack(pady=10)

        self.button_sair = tk.Button(self.master, text="Sair", command=self.master.destroy)
        self.button_sair.pack(pady=5)

    def cadastrar_produto(self):
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        quantidade = int(self.entry_quantidade.get())

        # Adicione a verificação de produto já cadastrado
        if self.gerenciador.verificar_produto(nome):
            print("Produto já cadastrado.")
        else:
            self.gerenciador.cadastrar_produto(nome, preco, quantidade)
            print(f"Produto {nome} cadastrado com sucesso.")

    def alterar_produto(self):
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        quantidade = int(self.entry_quantidade.get())

        # Adicione a verificação de produto existente
        if self.gerenciador.verificar_produto(nome):
            self.gerenciador.alterar_produto(nome, preco, quantidade)
            print(f"Produto {nome} alterado com sucesso.")
        else:
            print(f"Produto {nome} não encontrado. Utilize a opção de cadastrar para incluir um novo produto.")

    def excluir_produto(self):
        nome = self.entry_nome.get()
        # Adicione a verificação de produto existente
        if self.gerenciador.verificar_produto(nome):
            self.gerenciador.excluir_produto(nome)
            print(f"Produto {nome} excluído com sucesso.")
        else:
            print(f"Produto {nome} não encontrado.")

    def visualizar_produtos(self):
        try:
            # Criar uma nova janela (toplevel) para exibir os produtos
            visualizacao_window = tk.Toplevel(self.master)
            visualizacao_window.title("Produtos Cadastrados")

            # Defina um tamanho padrão para a janela de visualização de produtos
            visualizacao_window.geometry("1000x600")

            # Criar uma treeview para exibir os produtos
            tree = ttk.Treeview(visualizacao_window, columns=('Nome', 'Preço', 'Quantidade'), show='headings')
            tree.heading('Nome', text='Nome', anchor='center')
            tree.heading('Preço', text='Preço', anchor='center')
            tree.heading('Quantidade', text='Quantidade', anchor='center')

            # Obter os produtos do gerenciador e exibi-los na treeview
            produtos = self.gerenciador.visualizar_produtos()
            if not produtos:
                messagebox.showinfo("Informação", "Nenhum produto cadastrado.")
                return

            for produto in produtos:
                tree.insert('', 'end', values=produto)

            tree.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()

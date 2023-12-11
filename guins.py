import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from defs import GerenciadorProdutos

class InterfaceGrafica:
    def __init__(self, master):
        self.master = tk.Tk()
        self.master.title("Gerenciador de Produtos")

        # Defina um tamanho padrão para a janela principal
        self.master.geometry("330x500")

        # Preencha com suas informações locais do PostgreSQL
        dbname = 'NuvemShop'
        user = 'samuel'
        password = '0000'
        host = 'localhost'
        port = 5432

        # Crie uma instância do GerenciadorProdutos com as informações de conexão
        self.gerenciador = GerenciadorProdutos(dbname, user, password, host, port)

        # Aplique um tema moderno usando ttkbootstrap
        self.style = Style(theme="darkly")  # Escolha um tema diferente se desejar

        self.create_widgets()

    def create_widgets(self):
        # Frame para o cadastro de produtos
        frame_cadastro = ttk.Frame(self.master)
        frame_cadastro.grid(row=0, pady=10, padx=10, sticky="nsew")

        self.label_nome = ttk.Label(frame_cadastro, text="Nome do Produto:")
        self.label_nome.grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.entry_nome = ttk.Entry(frame_cadastro)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        self.label_preco = ttk.Label(frame_cadastro, text="Preço do Produto:")
        self.label_preco.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.entry_preco = ttk.Entry(frame_cadastro)
        self.entry_preco.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.label_quantidade = ttk.Label(frame_cadastro, text="Quantidade do Produto:")
        self.label_quantidade.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.entry_quantidade = ttk.Entry(frame_cadastro)
        self.entry_quantidade.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.button_cadastrar = ttk.Button(frame_cadastro, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.button_cadastrar.grid(row=3, columnspan=2, pady=10)

        self.button_alterar = ttk.Button(frame_cadastro, text="Alterar Produto", command=self.alterar_produto)
        self.button_alterar.grid(row=4, columnspan=2, pady=10)

        self.button_excluir = ttk.Button(frame_cadastro, text="Excluir Produto", command=self.excluir_produto)
        self.button_excluir.grid(row=5, columnspan=2, pady=10)

        ttk.Separator(self.master, orient="horizontal").grid(row=1, pady=20, sticky="ew")

        # Frame para a visualização de produtos
        frame_visualizacao = ttk.Frame(self.master)
        frame_visualizacao.grid(row=2, pady=10, padx=10, sticky="nsew")

        self.button_visualizar = ttk.Button(frame_visualizacao, text="Visualizar Produtos", command=self.visualizar_produtos)
        self.button_visualizar.pack(pady=20)

        ttk.Button(self.master, text="Sair", command=self.master.destroy).grid(row=3, pady=10)

        # Configuração do layout para ocupar todo o espaço disponível
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def cadastrar_produto(self):
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        quantidade = int(self.entry_quantidade.get())

        if self.gerenciador.verificar_produto(nome):
            messagebox.showwarning("Aviso", "Produto já cadastrado.")
        else:
            self.gerenciador.cadastrar_produto(nome, preco, quantidade)
            messagebox.showinfo("Sucesso", f"Produto {nome} cadastrado com sucesso.")

    def alterar_produto(self):
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        quantidade = int(self.entry_quantidade.get())

        if self.gerenciador.verificar_produto(nome):
            self.gerenciador.alterar_produto(nome, preco, quantidade)
            messagebox.showinfo("Sucesso", f"Produto {nome} alterado com sucesso.")
        else:
            messagebox.showwarning("Aviso", f"Produto {nome} não encontrado.")

    def excluir_produto(self):
        nome = self.entry_nome.get()

        if self.gerenciador.verificar_produto(nome):
            self.gerenciador.excluir_produto(nome)
            messagebox.showinfo("Sucesso", f"Produto {nome} excluído com sucesso.")
        else:
            messagebox.showwarning("Aviso", f"Produto {nome} não encontrado.")

    def visualizar_produtos(self):
        try:
            visualizacao_window = tk.Toplevel(self.master)
            visualizacao_window.title("Produtos Cadastrados")
            visualizacao_window.geometry("1000x600")

            tree = ttk.Treeview(visualizacao_window, columns=('Nome', 'Preço', 'Quantidade'), show='headings')
            tree.heading('Nome', text='Nome', anchor='center')
            tree.heading('Preço', text='Preço', anchor='center')
            tree.heading('Quantidade', text='Quantidade', anchor='center')

            produtos = self.gerenciador.visualizar_produtos()
            if not produtos:
                messagebox.showinfo("Informação", "Nenhum produto cadastrado.")
                return

            for produto in produtos:
                tree.insert('', 'end', values=produto)

            tree.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    app = InterfaceGrafica(None)
    app.master.mainloop()

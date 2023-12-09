import psycopg2
from psycopg2 import sql
import tkinter.messagebox as messagebox

class GerenciadorProdutos:
    def __init__(self, dbname, user, password, host, port):
        # Conectar ao banco de dados PostgreSQL
        self.conn = psycopg2.connect(
            dbname='----',
            user='----',
            password='----',
            host = 'localhost',
            port = 0000
        )
        self.criar_tabela()

    def verificar_produto(self, nome):
        """Verifica se um produto já está cadastrado."""
        query = "SELECT nome FROM produtos WHERE nome = %s;"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (nome,))
            return cursor.fetchone() is not None


    def criar_tabela(self):
        # Criar uma tabela de produtos se não existir
        query = '''
        CREATE TABLE IF NOT EXISTS produtos (
            nome TEXT PRIMARY KEY,
            preco REAL,
            quantidade INTEGER
        );
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()

    def cadastrar_produto(self, nome, preco, quantidade):
        if not self.produto_existe(nome):
            # Inserir o produto na tabela
            query = "INSERT INTO produtos VALUES (%s, %s, %s);"
            with self.conn.cursor() as cursor:
                cursor.execute(query, (nome, preco, quantidade))
                self.conn.commit()
            messagebox.showinfo("Informação", "Produto cadastrado com sucesso!")
            return
        else:
            messagebox.showinfo("Erro", f"Produto {nome} já cadastrado. Utilize a opção de alterar para modificar as informações.")
            return

    def alterar_produto(self, nome, preco=None, quantidade=None):
        if self.produto_existe(nome):
            # Atualizar informações do produto na tabela
            query = "UPDATE produtos SET preco=%s, quantidade=%s WHERE nome=%s;"
            with self.conn.cursor() as cursor:
                cursor.execute(query, (preco, quantidade, nome))
                self.conn.commit()
            messagebox.showerror("Informação",f"Informações do produto {nome} alteradas com sucesso!")
            print(f"Informações do produto {nome} alteradas com sucesso!")
            
        else:
            messagebox.showerror("Erro", f"Produto {nome} não encontrado. Utilize a opção de cadastrar para incluir um novo produto.")
            print(f"Produto {nome} não encontrado. Utilize a opção de cadastrar para incluir um novo produto.")
            
    def excluir_produto(self, nome):
        if self.produto_existe(nome):
            # Excluir o produto da tabela
            query = "DELETE FROM produtos WHERE nome=%s;"
            with self.conn.cursor() as cursor:
                cursor.execute(query, (nome,))
                self.conn.commit()
                
            messagebox.showerror("Informação", f"Produto {nome} excluído com sucesso!")
            print(f"Produto {nome} excluído com sucesso!")
        else:
            messagebox.showerror("Erro", f"Produto {nome} não encontrado.")
            print(f"Produto {nome} não encontrado.")
    
    def visualizar_produtos(self):
        # Selecionar todos os produtos na tabela
        query = "SELECT * FROM produtos;"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            produtos = cursor.fetchall()

        if not produtos:
            return None
        else:
            return produtos

        
    def produto_existe(self, nome):
        # Verificar se o produto existe na tabela
        query = "SELECT * FROM produtos WHERE nome=%s;"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (nome,))
            return cursor.fetchone() is not None


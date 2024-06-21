import customtkinter
from tkinter import messagebox
import psycopg as sql

def tela_cadastro_produto(dashboard, connection):
    cadastro_janela = customtkinter.CTk()
    cadastro_janela.title("Cadastro de Produto")
    cadastro_janela.geometry("600x400")

    def voltar_ao_dashboard():
        cadastro_janela.destroy()
        dashboard.deiconify()

    def cadastrar_produto():
        descricao = entrada_descricao.get()
        valor = entrada_valor.get()
        quantidade = entrada_quantidade.get()
        fornecedor_codigo = entrada_fornecedor_codigo.get()

        try:
            cursor = connection.cursor()
            query = """INSERT INTO tb_produtos (pro_descricao, pro_valor, pro_quantidade, tb_fornecedores_for_codigo) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (descricao, valor, quantidade, fornecedor_codigo))
            connection.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao cadastrar produto", str(e))

    label_descricao = customtkinter.CTkLabel(cadastro_janela, text="Descrição do Produto:")
    label_descricao.pack(padx=10, pady=5)

    entrada_descricao = customtkinter.CTkEntry(cadastro_janela, placeholder_text="Digite a descrição do produto")
    entrada_descricao.pack(padx=10, pady=5)

    label_valor = customtkinter.CTkLabel(cadastro_janela, text="Valor do Produto:")
    label_valor.pack(padx=10, pady=5)

    entrada_valor = customtkinter.CTkEntry(cadastro_janela, placeholder_text="Digite o valor do produto")
    entrada_valor.pack(padx=10, pady=5)

    label_quantidade = customtkinter.CTkLabel(cadastro_janela, text="Quantidade do Produto:")
    label_quantidade.pack(padx=10, pady=5)

    entrada_quantidade = customtkinter.CTkEntry(cadastro_janela, placeholder_text="Digite a quantidade do produto")
    entrada_quantidade.pack(padx=10, pady=5)

    label_fornecedor_codigo = customtkinter.CTkLabel(cadastro_janela, text="Código do Fornecedor:")
    label_fornecedor_codigo.pack(padx=10, pady=5)

    entrada_fornecedor_codigo = customtkinter.CTkEntry(cadastro_janela, placeholder_text="Digite o código do fornecedor")
    entrada_fornecedor_codigo.pack(padx=10, pady=5)

    botao_cadastrar = customtkinter.CTkButton(cadastro_janela, text="Cadastrar Produto", command=cadastrar_produto)
    botao_cadastrar.pack(padx=10, pady=10)

    botao_voltar = customtkinter.CTkButton(cadastro_janela, text="Voltar ao Dashboard", command=voltar_ao_dashboard)
    botao_voltar.pack(padx=10, pady=10)

    cadastro_janela.mainloop()

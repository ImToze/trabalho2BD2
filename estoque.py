import customtkinter
from tkinter import messagebox, ttk
import psycopg as sql

def tela_estoque(dashboard, connection):
    estoque_janela = customtkinter.CTk()
    estoque_janela.title("Gerenciar Estoque")
    estoque_janela.geometry("800x800")

    def voltar_ao_dashboard():
        estoque_janela.destroy()
        dashboard.deiconify()

    def carregar_produtos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = connection.cursor()
            query = "SELECT pro_codigo, pro_descricao, pro_quantidade, pro_valor FROM tb_produtos"
            cursor.execute(query)
            produtos = cursor.fetchall()
            for produto in produtos:
                tree.insert("", "end", values=produto)
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", str(e))

    def atualizar_preco():
        produto_id = entrada_id.get()
        novo_preco = entrada_novo_preco.get()
        try:
            cursor = connection.cursor()
            query = "UPDATE tb_produtos SET pro_valor = %s WHERE pro_codigo = %s"
            cursor.execute(query, (novo_preco, produto_id))
            connection.commit()
            messagebox.showinfo("Sucesso", "Preço atualizado com sucesso!")
            carregar_produtos()
        except Exception as e:
            messagebox.showerror("Erro ao Atualizar Preço", str(e))

    def atualizar_quantidade():
        produto_id = entrada_id.get()
        quantidade_adicionada = int(entrada_nova_quantidade.get())
        try:
            cursor = connection.cursor()
            query = "SELECT pro_quantidade FROM tb_produtos WHERE pro_codigo = %s"
            cursor.execute(query, (produto_id,))
            quantidade_atual = cursor.fetchone()[0]
            nova_quantidade = quantidade_atual + quantidade_adicionada
            query = "UPDATE tb_produtos SET pro_quantidade = %s WHERE pro_codigo = %s"
            cursor.execute(query, (nova_quantidade, produto_id))
            connection.commit()
            messagebox.showinfo("Sucesso", "Quantidade atualizada com sucesso!")
            carregar_produtos()
        except Exception as e:
            messagebox.showerror("Erro ao Atualizar Quantidade", str(e))

    label_id = customtkinter.CTkLabel(estoque_janela, text="ID do Produto:")
    label_id.pack(padx=10, pady=5)

    entrada_id = customtkinter.CTkEntry(estoque_janela, placeholder_text="Digite o ID do produto")
    entrada_id.pack(padx=10, pady=5)

    label_novo_preco = customtkinter.CTkLabel(estoque_janela, text="Novo Preço:")
    label_novo_preco.pack(padx=10, pady=5)

    entrada_novo_preco = customtkinter.CTkEntry(estoque_janela, placeholder_text="Digite o novo preço")
    entrada_novo_preco.pack(padx=10, pady=5)

    botao_atualizar_preco = customtkinter.CTkButton(estoque_janela, text="Atualizar Preço", command=atualizar_preco)
    botao_atualizar_preco.pack(padx=10, pady=10)

    label_nova_quantidade = customtkinter.CTkLabel(estoque_janela, text="Nova Quantidade:")
    label_nova_quantidade.pack(padx=10, pady=5)

    entrada_nova_quantidade = customtkinter.CTkEntry(estoque_janela, placeholder_text="Digite a nova quantidade")
    entrada_nova_quantidade.pack(padx=10, pady=5)

    botao_atualizar_quantidade = customtkinter.CTkButton(estoque_janela, text="Atualizar Quantidade", command=atualizar_quantidade)
    botao_atualizar_quantidade.pack(padx=10, pady=10)

    columns = ("ID", "Descrição", "Quantidade", "Preço")
    tree = ttk.Treeview(estoque_janela, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(padx=10, pady=10, expand=True, fill="both")

    botao_carregar = customtkinter.CTkButton(estoque_janela, text="Carregar Produtos", command=carregar_produtos)
    botao_carregar.pack(padx=10, pady=10)

    botao_voltar = customtkinter.CTkButton(estoque_janela, text="Voltar ao Dashboard", command=voltar_ao_dashboard)
    botao_voltar.pack(padx=10, pady=10)

    carregar_produtos()

    estoque_janela.mainloop()

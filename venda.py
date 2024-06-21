import customtkinter
from tkinter import messagebox, ttk
import psycopg as sql

def tela_realizar_venda(dashboard, connection, usuario):
    venda_janela = customtkinter.CTk()
    venda_janela.title("Realizar Venda")
    venda_janela.geometry("600x600")

    def voltar_ao_dashboard():
        venda_janela.destroy()
        dashboard.deiconify()
        
    usuario_funcionario_mapeamento = {
        'joao_silva': 1,
        'maria_oliveira': 2,
        'carlos_souza': 3,
        'ana_pereira': 4,
        'lucas_lima': 5,
        'fernanda_alves': 6,
    }

    def buscar_produto():
        produto_cod = entrada_produto.get()
        quantidade = int(entrada_quantidade.get())
        try:
            cursor = connection.cursor()
            query = "SELECT pro_descricao, pro_valor FROM tb_produtos WHERE pro_codigo = %s"
            cursor.execute(query, (produto_cod,))
            resultado = cursor.fetchall()

            if resultado:
                produto = resultado[0]
                produto_info = {"nome": produto[0], "quantidade": quantidade, "preco": produto[1] * quantidade}
                adicionar_produto_lista(produto_info)
            else:
                messagebox.showwarning("Produto não encontrado", "Nenhum produto encontrado com o código fornecido.")
        except Exception as e:
            messagebox.showerror("Erro de Busca", str(e))

    def adicionar_produto_lista(produto_info):
        tree.insert("", "end", values=(produto_info["nome"], produto_info["quantidade"], f'R$ {produto_info["preco"]:.2f}'))
        calcular_total()

    def calcular_total():
        total = 0.0
        for child in tree.get_children():
            total += float(tree.item(child, "values")[2][3:])
        label_total.configure(text=f"Total: R$ {total:.2f}")

    def finalizar_venda():
        try:
            cursor = connection.cursor()
            funcionario_codigo = usuario_funcionario_mapeamento.get(usuario)
            if not funcionario_codigo:
                raise Exception("Código do funcionário não encontrado para o usuário do banco.")

            total_venda = sum(float(tree.item(child, "values")[2][3:]) for child in tree.get_children())

            query_venda = """INSERT INTO tb_vendas (ven_horario, ven_valor_total, tb_funcionarios_fun_codigo) VALUES (CURRENT_TIMESTAMP, %s, %s) RETURNING ven_codigo"""
            cursor.execute(query_venda, (total_venda, funcionario_codigo))
            venda_codigo = cursor.fetchone()[0]

            for child in tree.get_children():
                produto = tree.item(child, "values")
                produto_nome = produto[0]
                quantidade_vendida = int(produto[1])
              #  valor_parcel = float(produto[2][3:])
                query_item = """INSERT INTO tb_itens (ite_codigo, ite_quantidade, ite_valor_parcel, tb_produtos_pro_codigo, tb_vendas_ven_codigo) VALUES (%s, %s, %s, (SELECT pro_codigo FROM tb_produtos WHERE pro_descricao=%s), %s)"""
                #cursor.execute(query_item, (quantidade_vendida, valor_parcel, produto_nome, venda_codigo))
                cursor.execute(query_item, (venda_codigo, produto[1], float(produto[2][3:]), produto[0], venda_codigo))

                query_atualiza_produto = """UPDATE tb_produtos SET pro_quantidade = pro_quantidade - %s WHERE pro_descricao = %s"""
                cursor.execute(query_atualiza_produto, (quantidade_vendida, produto_nome))

            
            connection.commit()

            messagebox.showinfo("Venda Finalizada", "Venda realizada com sucesso!")
            venda_janela.destroy()
            dashboard.deiconify()  
        except sql.errors.InsufficientPrivilege as e:
            messagebox.showerror("Erro ao Finalizar", f"Permissão insuficiente: {str(e)}")
        except sql.OperationalError as e:
            messagebox.showerror("Erro ao Finalizar", f"Erro de operação: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro ao Finalizar", f"Erro inesperado: {str(e)}")

    label_produto = customtkinter.CTkLabel(venda_janela, text="Buscar Produto:")
    label_produto.pack(padx=10, pady=5)

    entrada_produto = customtkinter.CTkEntry(venda_janela, placeholder_text="Digite o código do produto")
    entrada_produto.pack(padx=10, pady=5)

    label_quantidade = customtkinter.CTkLabel(venda_janela, text="Quantidade:")
    label_quantidade.pack(padx=10, pady=5)

    entrada_quantidade = customtkinter.CTkEntry(venda_janela, placeholder_text="Digite a quantidade")
    entrada_quantidade.pack(padx=10, pady=5)

    botao_buscar = customtkinter.CTkButton(venda_janela, text="Buscar", command=buscar_produto)
    botao_buscar.pack(padx=10, pady=5)

    columns = ("Produto", "Quantidade", "Preço Total")
    tree = ttk.Treeview(venda_janela, columns=columns, show="headings")
    tree.heading("Produto", text="Produto")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço Total", text="Preço Total")
    tree.pack(padx=10, pady=10)

    label_total = customtkinter.CTkLabel(venda_janela, text="Total: R$ 0.00")
    label_total.pack(padx=10, pady=5)

    botao_finalizar = customtkinter.CTkButton(venda_janela, text="Finalizar Venda", command=finalizar_venda)
    botao_finalizar.pack(padx=10, pady=5)

    botao_voltar = customtkinter.CTkButton(venda_janela, text="Voltar ao Dashboard", command=voltar_ao_dashboard)
    botao_voltar.pack(padx=10, pady=5)

    venda_janela.mainloop()

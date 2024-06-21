import customtkinter
from venda import tela_realizar_venda
from produto import tela_cadastro_produto
from estoque import tela_estoque  

def abrir_dashboard(janela_login, connection, usuario):
    janela_login.withdraw()

    dashboard = customtkinter.CTk()
    dashboard.title("Dashboard")
    dashboard.geometry("600x400")

    texto_dashboard = customtkinter.CTkLabel(dashboard, text=f"Bem-vindo ao Dashboard, {usuario}")
    texto_dashboard.pack(padx=10, pady=10)

    def abrir_tela_venda():
        dashboard.withdraw()
        tela_realizar_venda(dashboard, connection, usuario)

    def abrir_tela_cadastro_produto():
        dashboard.withdraw()
        tela_cadastro_produto(dashboard, connection)

    def abrir_tela_estoque():
        dashboard.withdraw()
        tela_estoque(dashboard, connection)

    botao_venda = customtkinter.CTkButton(dashboard, text="Realizar Venda", command=abrir_tela_venda)
    botao_venda.pack(padx=10, pady=10)

    botao_cadastro_produto = customtkinter.CTkButton(dashboard, text="Cadastrar Produto", command=abrir_tela_cadastro_produto)
    botao_cadastro_produto.pack(padx=10, pady=10)

    botao_estoque = customtkinter.CTkButton(dashboard, text="Gerenciar Estoque", command=abrir_tela_estoque)
    botao_estoque.pack(padx=10, pady=10)

    def fechar_dashboard():
        connection.close()
        dashboard.destroy()
        janela_login.deiconify()

    botao_sair = customtkinter.CTkButton(dashboard, text="Sair", command=fechar_dashboard)
    botao_sair.pack(padx=10, pady=10)

    dashboard.mainloop()

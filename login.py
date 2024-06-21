import customtkinter
from tkinter import messagebox
from main import abrir_dashboard
import psycopg

def login():
    usuario_texto = usuario.get()
    senha_texto = senha.get()
    
    try:
        conn = psycopg.connect(
            dbname="trabalho2BD2",
            user=usuario_texto,
            password=senha_texto,
            host="localhost",
            port="5432"
        )
        abrir_dashboard(janela, conn, usuario_texto)
    except psycopg.OperationalError:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos")

janela = customtkinter.CTk()
janela.title("Login System")
janela.geometry("500x400")
janela.maxsize(width=700, height=500)
janela.minsize(width=400, height=300)

texto = customtkinter.CTkLabel(janela, text="Entrar")
texto.pack(padx=10, pady=10)

usuario = customtkinter.CTkEntry(janela, placeholder_text="Digite o seu usuário")
usuario.pack(padx=10, pady=10)
senha = customtkinter.CTkEntry(janela, placeholder_text="Digite sua senha", show="*")
senha.pack(padx=10, pady=10)

botao = customtkinter.CTkButton(janela, text="Login", command=login)
botao.pack(padx=10, pady=10)

janela.mainloop()

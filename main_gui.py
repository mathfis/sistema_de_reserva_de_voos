#/main_gui.py

import tkinter as tk
from tkinter import ttk, messagebox

# imports do backend
from biblioteca.avioes import Aviao
from biblioteca.usuarios import Usuario
from biblioteca.voos import GerenciadorVoos


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Reserva de Voos")
        self.geometry("900x600")
        self.resizable(False,False)
        self.configure(bg="blue")

        # Armazenamento de Dados do back-end
        self.gerenciador_voos = None
        self.lista_avioes = []
        self.usuario_logado = None

        # Dicionario de Telas
        self.frames = {}
        for F in (TelaLogin, TelaCadastro, TelaPainel):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column= 0, sticky="nsew")
        
        self.mostrar_tela("TelaLogin")
    
    def mostrar_tela(self, nome_tela):
        """Traz a tela especificada para frente."""
        frame = self.frames[nome_tela]
        frame.tkraise()


class TelaLogin(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")

        tk.Label(self, text="Login de Passageiro", font=("Arial", 22, "bold"), bg="blue").pack(pady=40)

        form = tk.Frame(self, bg="blue")
        form.pack()

        tk.Label(form, text="CPF:", font=("Arial", 12), bg="blue").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.cpf_entry = tk.Entry(form, width=30)
        self.cpf_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Senha (simulada):", font=("Arial", 12), bg="blue").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.senha_entry = tk.Entry(form, show="*", width=30)
        self.senha_entry.grid(row=1, column=1, pady=5)

        btns = tk.Frame(self, bg="blue")
        btns.pack(pady=30)

        tk.Button(btns, text="Entrar", width=15, command=self.fazer_login).grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Cadastrar", width=15,
                  command=lambda: master.mostrar_tela("TelaCadastro")).grid(row=0, column=1, padx=10)

    def fazer_login(self):
        """Por enquanto, apenas simula login."""
        cpf = self.cpf_entry.get().strip()
        if not cpf:
            messagebox.showwarning("Aviso", "Por favor, insira o CPF.")
            return
        messagebox.showinfo("Login", f"Login simulado para o CPF: {cpf}")
        self.master.mostrar_tela("TelaPainel")


    def fazer_login(self):
        """Por enquanto, apenas simula login."""
        cpf = self.cpf_entry.get().strip()
        if not cpf:
            messagebox.showwarning("Aviso", "Por favor, insira o CPF.")
            return
        messagebox.showinfo("Login", f"Login simulado para o CPF: {cpf}")
        self.master.mostrar_tela("TelaPainel")



class TelaCadastro(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")

        tk.Label(self, text="Cadastro de Novo Passageiro", font=("Arial", 22, "bold"), bg="blue").pack(pady=40)
        form = tk.Frame(self, bg="blue")
        form.pack()

        campos = [
            ("CPF:", "cpf"), ("Nome:", "nome"),
            ("Data de Nascimento (DD/MM/AAAA):", "data"),
            ("E-mail:", "email")
        ]
        self.entries = {}

        for i, (label_text, campo) in enumerate(campos):
            tk.Label(form, text=label_text, font=("Arial", 12), bg="blue").grid(row=i, column=0, sticky="e", padx=10, pady=5)
            entry = tk.Entry(form, width=35)
            entry.grid(row=i, column=1, pady=5)
            self.entries[campo] = entry

        tk.Button(self, text="Salvar Cadastro", width=20, command=self.salvar_cadastro).pack(pady=30)
        tk.Button(self, text="Voltar ao Login", width=20,
                  command=lambda: master.mostrar_tela("TelaLogin")).pack()

    def salvar_cadastro(self):
        dados = {k: e.get().strip() for k, e in self.entries.items()}
        if not all(dados.values()):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return
        messagebox.showinfo("Cadastro", "Cadastro simulado com sucesso!")
        self.master.mostrar_tela("TelaLogin")

    

class TelaPainel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")
        tk.Label(self, text="Painel do Usuário", font=("Arial", 22, "bold"), bg="blue").pack(pady=40)

        tk.Button(self, text="Visualizar Voos", width=20, command=self.ir_voos).pack(pady=10)
        tk.Button(self, text="Minhas Reservas", width=20, command=self.ir_reservas).pack(pady=10)
        tk.Button(self, text="Sair", width=20,
                  command=lambda: master.mostrar_tela("TelaLogin")).pack(pady=40)

    def ir_voos(self):
        messagebox.showinfo("Navegação", "Tela de voos ainda não implementada.")

    def ir_reservas(self):
        messagebox.showinfo("Navegação", "Tela de reservas ainda não implementada.")


if __name__ == "__main__":
    print("Bloco __main__ executado! Inicializando interface...")
    app = App()
    app.mainloop()

    
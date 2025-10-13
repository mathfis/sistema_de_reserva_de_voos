#/main_gui.py

import tkinter as tk
from tkinter import ttk, messagebox

# imports do backend
from biblioteca.avioes import Aviao, carregar_avioes
from biblioteca.usuarios import Usuario, carregar_usuarios,salvar_usuarios, salvar_usuario_unico
from biblioteca.voos import GerenciadorVoos


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Reserva de Voos")
        self.geometry("900x600")
        self.resizable(False,False)
        self.configure(bg="blue")

        # Armazenamento de Dados do back-end
        self.lista_avioes = carregar_avioes()  
        self.gerenciador_voos = GerenciadorVoos()  
        self.gerenciador_voos.carregar_voos(self.lista_avioes) 
        self.voo_selecionado = None
        self.usuario_logado = None
        
        # Dicionario de Telas
        self.frames = {}
        for F in (TelaLogin, TelaCadastro, TelaPainel, TelaVoos, TelaAssentos):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column= 0, sticky="nsew")
        
        self.mostrar_tela("TelaLogin")
    
    def mostrar_tela(self, nome_tela):
        """Traz a tela especificada para frente."""
        frame = self.frames[nome_tela]
        frame.tkraise()

        # Atualizar informações quando o painel for mostrado
        if nome_tela == "TelaPainel" and self.usuario_logado:
            self.frames["TelaPainel"].atualizar_info_usuario()


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
        cpf_digitado = ''.join(ch for ch in self.cpf_entry.get().strip() if ch.isdigit())
        senha_digitada = self.senha_entry.get().strip()

        if not cpf_digitado or not senha_digitada:
            messagebox.showwarning("Aviso", "Por favor, insira o CPF.")
            return
        
        try:
            usuarios  = carregar_usuarios()
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de usuários não encontrado")
            return

###### alteração        
        usuario_encontrado = None
        for usuario in usuarios:
            cpf_armazenado = ''.join(ch for ch in usuario.cpf if ch.isdigit())
            if cpf_digitado == cpf_armazenado:
                usuario_encontrado = usuario
                break

        if usuario_encontrado:
            if usuario_encontrado.senha == senha_digitada:
                self.master.usuario_logado = usuario_encontrado
                messagebox.showinfo("Bem-vindo!", f"Login bem-sucedido, {usuario_encontrado.nome}")
                self.master.mostrar_tela("TelaPainel")
            else:
                # NOVA MENSAGEM DE ERRO DE SENHA
                messagebox.showerror("Erro de Login", "Senha incorreta. Por favor, insira a senha correta.")
                
                # MANTÉM CPF E LIMPA SENHA
                self.cpf_entry.delete(0, tk.END)
                self.cpf_entry.insert(0, self.cpf_entry.get())  # Mantém CPF digitado
                self.senha_entry.delete(0, tk.END)  # Limpa campo senha
                self.senha_entry.focus_set()  # Foca no campo senha para nova tentativa
        else:
            messagebox.showerror("Erro de Login", "CPF não encontrado. Faça o cadastro primeiro.")


class TelaCadastro(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")

        tk.Label(self, text="Cadastro de Novo Passageiro", font=("Arial", 22, "bold"), bg="blue").pack(pady=40)
        form = tk.Frame(self, bg="blue")
        form.pack()

        campos = [
            ("CPF:", "cpf"), ("Nome:", "nome"),
            ("Data de Nascimento (DD/MM/AAAA):", "data"),
            ("E-mail:", "email"),
            ("Senha:", "senha")
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
        """Cria e salva novo usuário real no backend."""

        # Captura e valida campos
        dados = {k: e.get().strip() for k, e in self.entries.items()}
        if not all(dados.values()):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        cpf = dados["cpf"]
        nome = dados["nome"]
        data_nasc = dados["data"]
        email = dados["email"]
        senha = dados["senha"]

        try:
            usuarios = carregar_usuarios()
        except FileNotFoundError:
            usuarios = []

        # Verifica se CPF já existe
        for u in usuarios:
            if u.cpf == cpf:
                messagebox.showwarning("Atenção", "CPF já cadastrado. Faça login.")
                self.master.mostrar_tela("TelaLogin")
                return

        # Cria o novo objeto Usuario
        novo_usuario = Usuario(cpf, nome, data_nasc, email, senha)

        # Adiciona e salva
        try:
            salvar_usuario_unico(novo_usuario)
        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
            self.master.mostrar_tela("TelaLogin")
            return


        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.master.mostrar_tela("TelaLogin")


class TelaPainel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")
        tk.Label(self, text="Painel do Usuário", font=("Arial", 22, "bold"), bg="blue").pack(pady=40)

        # Frame para informações do usuário
        info_frame = tk.Frame(self, bg="blue")
        info_frame.pack(pady=10)

        # Labels para informações do usuário
        self.label_nome = tk.Label(info_frame, text="Nome: ", font=("Arial", 12), bg="blue")
        self.label_nome.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        self.label_cpf = tk.Label(info_frame, text="CPF: ", font=("Arial", 12), bg="blue")
        self.label_cpf.grid(row=1, column=0, sticky="w", padx=10, pady=2)
        
        self.label_email = tk.Label(info_frame, text="Email: ", font=("Arial", 12), bg="blue")
        self.label_email.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        # Frame para reservas
        reservas_frame = tk.Frame(self, bg="blue")
        reservas_frame.pack(pady=10)
        
        tk.Label(reservas_frame, text="Reservas Ativas:", font=("Arial", 12, "bold"), bg="blue").pack()
        
        # Listbox para mostrar reservas
        self.lista_reservas = tk.Listbox(reservas_frame, width=50, height=6)
        self.lista_reservas.pack(pady=5)


        # Inserção dos Botões de Ação na base da tela
        tk.Button(self, text="Visualizar Voos", width=20, command=self.ir_voos).pack(pady=10)
        tk.Button(self, text="Minhas Reservas", width=20, command=self.ir_reservas).pack(pady=10)
        tk.Button(self, text="Sair", width=20,
                  command=lambda: master.mostrar_tela("TelaLogin")).pack(pady=40)

    # Método para atualizar informações do usuário
    def atualizar_info_usuario(self):
        if self.master.usuario_logado:
            usuario = self.master.usuario_logado
            self.label_nome.config(text=f"Nome: {usuario.nome}")
            self.label_cpf.config(text=f"CPF: {usuario.cpf}")
            self.label_email.config(text=f"Email: {usuario.email}")

    def ir_voos(self):
        """Navega para a tela de seleção de voos"""
        self.master.mostrar_tela("TelaVoos")
    
    def ir_reservas(self):
        messagebox.showinfo("Navegação", "Tela de reservas ainda não implementada.")


class TelaVoos(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")
        
        tk.Label(self, text="Seleção de Voos Disponíveis", 
                font=("Arial", 22, "bold"), bg="blue").pack(pady=20)
        
        # Frame para instruções
        instrucoes_frame = tk.Frame(self, bg="blue")
        instrucoes_frame.pack(pady=10)
        tk.Label(instrucoes_frame, text="Selecione um voo para ver os assentos disponíveis:", 
                font=("Arial", 12), bg="blue").pack()
        
        # Frame principal para lista de voos
        main_frame = tk.Frame(self, bg="blue")
        main_frame.pack(pady=20, fill="both", expand=True)
        
        # Lista de voos com scrollbar
        lista_frame = tk.Frame(main_frame, bg="blue")
        lista_frame.pack(pady=10)
        
        # Cabeçalho da lista
        cabecalho_frame = tk.Frame(lista_frame, bg="lightgray")
        cabecalho_frame.pack(fill="x", padx=20)
        
        tk.Label(cabecalho_frame, text="Voo", width=8, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=2)
        tk.Label(cabecalho_frame, text="Origem", width=15, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=2)
        tk.Label(cabecalho_frame, text="Destino", width=15, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=2)
        tk.Label(cabecalho_frame, text="Data/Hora", width=20, font=("Arial", 10, "bold")).grid(row=0, column=3, padx=2)
        tk.Label(cabecalho_frame, text="Avião", width=12, font=("Arial", 10, "bold")).grid(row=0, column=4, padx=2)
        tk.Label(cabecalho_frame, text="Ação", width=10, font=("Arial", 10, "bold")).grid(row=0, column=5, padx=2)
        
        # Frame scrollable para os voos
        container_frame = tk.Frame(lista_frame, bg="blue")
        container_frame.pack(fill="both", expand=True, padx=20)
        
        self.canvas = tk.Canvas(container_frame, bg="blue", height=200)
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="blue")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Carregar voos
        self.carregar_voos()
        
        # Botões de ação
        botoes_frame = tk.Frame(self, bg="blue")
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="Voltar ao Painel", 
                 width=20, command=self.voltar_painel).pack(pady=10)
    
    def carregar_voos(self):
        """Carrega e exibe a lista de voos disponíveis"""
        # Limpar frame existente
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Obter lista de voos do gerenciador
        voos = self.master.gerenciador_voos.listar_voos()
        
        if not voos:
            # Se não há voos, mostrar mensagem
            tk.Label(self.scrollable_frame, text="Nenhum voo disponível no momento", 
                    font=("Arial", 12), bg="blue", fg="white").pack(pady=20)
            return
        
        # Exibir cada voo
        for i, voo in enumerate(voos):
            frame_voo = tk.Frame(self.scrollable_frame, bg="white", relief="raised", bd=1)
            frame_voo.pack(fill="x", padx=5, pady=2)
            
            # Informações do voo
            tk.Label(frame_voo, text=voo.voo_id, width=8, anchor="w", bg="white").grid(row=0, column=0, padx=2, pady=5)
            tk.Label(frame_voo, text=voo.origem, width=15, anchor="w", bg="white").grid(row=0, column=1, padx=2, pady=5)
            tk.Label(frame_voo, text=voo.destino, width=15, anchor="w", bg="white").grid(row=0, column=2, padx=2, pady=5)
            tk.Label(frame_voo, text=voo.data_hora, width=20, anchor="w", bg="white").grid(row=0, column=3, padx=2, pady=5)
            tk.Label(frame_voo, text=voo.aviao.aviao_id, width=12, anchor="w", bg="white").grid(row=0, column=4, padx=2, pady=5)
            
            # Botão selecionar
            tk.Button(frame_voo, text="Selecionar", width=8,
                     command=lambda v=voo: self.selecionar_voo(v)).grid(row=0, column=5, padx=2, pady=5)
    
    def selecionar_voo(self, voo):
        """Seleciona um voo e navega para seleção de assentos"""
        # Armazenar voo selecionado no master (App)
        self.master.voo_selecionado = voo
        
        # Mostrar mensagem informativa
        messagebox.showinfo("Voo Selecionado", 
                           f"Voo {voo.voo_id} selecionado!\n"
                           f"{voo.origem} → {voo.destino}\n"
                           f"Avião: {voo.aviao.aviao_id}\n"
                           f"Próximo: selecione seu assento")
        
        # Navegar para tela de assentos
        self.master.frames["TelaAssentos"].atualizar_info_voo(voo)
        self.master.mostrar_tela("TelaAssentos")
    
    def voltar_painel(self):
        """Volta para o painel do usuário"""
        self.master.mostrar_tela("TelaPainel")


    # def __init__(self, master):
    #     super().__init__(master, bg="blue")
        
    #     tk.Label(self, text="Seleção de Voos Disponíveis", 
    #             font=("Arial", 22, "bold"), bg="blue").pack(pady=40)
        
    #     # Frame para lista de voos (será preenchido na próxima modificação)
    #     self.frame_voos = tk.Frame(self, bg="blue")
    #     self.frame_voos.pack(pady=20, fill="both", expand=True)
        
    #     tk.Label(self.frame_voos, text="Lista de voos aparecerá aqui", 
    #             font=("Arial", 14), bg="blue").pack(pady=50)
        
    #     # Botões de ação
    #     botoes_frame = tk.Frame(self, bg="blue")
    #     botoes_frame.pack(pady=30)
        
    #     tk.Button(botoes_frame, text="Selecionar Voo (Teste)", 
    #              width=20, command=self.selecionar_voo_teste).pack(pady=10)
    #     tk.Button(botoes_frame, text="Voltar ao Painel", 
    #              width=20, command=self.voltar_painel).pack(pady=10)
    
    # def selecionar_voo_teste(self):
    #     """Método temporário para teste de navegação"""
    #     messagebox.showinfo("Seleção de Voo", 
    #                        "Funcionalidade de seleção será implementada na próxima etapa!")
    
    # def voltar_painel(self):
    #     """Volta para o painel do usuário"""
    #     self.master.mostrar_tela("TelaPainel")


# ADICIONAR no main_gui.py - NOVA CLASSE TelaAssentos (placeholder)
class TelaAssentos(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")
        
        tk.Label(self, text="Seleção de Assentos", 
                font=("Arial", 22, "bold"), bg="blue").pack(pady=20)
        
        # Informações do voo selecionado
        self.label_voo_info = tk.Label(self, text="", font=("Arial", 14), bg="blue")
        self.label_voo_info.pack(pady=10)
        
        # Placeholder para layout de assentos
        tk.Label(self, text="Layout de assentos será implementado na próxima etapa", 
                font=("Arial", 12), bg="blue").pack(pady=20)
        
        # Botões de ação
        botoes_frame = tk.Frame(self, bg="blue")
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="Voltar para Voos", 
                 width=20, command=self.voltar_voos).pack(pady=10)
        tk.Button(botoes_frame, text="Confirmar Reserva", 
                 width=20, command=self.confirmar_reserva).pack(pady=10)
    
    def atualizar_info_voo(self, voo):
        """Atualiza as informações do voo selecionado"""
        if voo:
            info_text = f"Voo: {voo.voo_id} | {voo.origem} → {voo.destino} | {voo.data_hora}"
            self.label_voo_info.config(text=info_text)
    
    def voltar_voos(self):
        """Volta para a tela de seleção de voos"""
        self.master.mostrar_tela("TelaVoos")
    
    def confirmar_reserva(self):
        """Placeholder para confirmação de reserva"""
        messagebox.showinfo("Reserva", "Funcionalidade de reserva será implementada na próxima etapa")


if __name__ == "__main__":
    print("Bloco __main__ executado! Inicializando interface...")
    app = App()
    app.mainloop()


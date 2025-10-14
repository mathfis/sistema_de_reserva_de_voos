#/main_gui.py

import tkinter as tk
from tkinter import ttk, messagebox

# imports do backend
from biblioteca.avioes import carregar_avioes
from biblioteca.usuarios import Usuario, carregar_usuarios,salvar_usuarios, salvar_usuario_unico
from biblioteca.voos import GerenciadorVoos


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Reserva de Voos")
        self.geometry("900x600")
        self.resizable(True,True)
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

        # Frame para reservas (ATUALIZADO)
        reservas_frame = tk.Frame(self, bg="blue")
        reservas_frame.pack(pady=10)
        
        tk.Label(reservas_frame, text="Minhas Reservas Ativas:", font=("Arial", 12, "bold"), bg="blue").pack()
        
        # Listbox para mostrar reservas
        self.lista_reservas = tk.Listbox(reservas_frame, width=60, height=4)
        self.lista_reservas.pack(pady=5)
        
        # Botão para gerenciar reservas
        tk.Button(reservas_frame, text="Gerenciar Todas as Reservas", width=25,
                  command=self.ir_reservas, bg="#3498db", fg="white").pack(pady=5)
        
        # Frame para referência (IMPORTANTE para o método atualizar_preview_reservas)
        self.lista_reservas_frame = reservas_frame


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
            self.atualizar_preview_reservas()

    def ir_voos(self):
        """Navega para a tela de seleção de voos"""
        self.master.mostrar_tela("TelaVoos")
    
    def ir_reservas(self):
        """Navega para tela de minhas reservas"""
        # Criar janela de reservas
        janela_reservas = tk.Toplevel(self)
        janela_reservas.title("Minhas Reservas")
        janela_reservas.geometry("600x400")
        janela_reservas.configure(bg="white")
        
        tk.Label(janela_reservas, text="Minhas Reservas Ativas", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        # Frame para lista de reservas
        frame_lista = tk.Frame(janela_reservas, bg="white")
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Cabeçalho
        cabecalho_frame = tk.Frame(frame_lista, bg="lightgray")
        cabecalho_frame.pack(fill="x")
        
        tk.Label(cabecalho_frame, text="Voo", width=10, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=2)
        tk.Label(cabecalho_frame, text="Assento", width=8, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=2)
        tk.Label(cabecalho_frame, text="Origem/Destino", width=20, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=2)
        tk.Label(cabecalho_frame, text="Data/Hora", width=15, font=("Arial", 10, "bold")).grid(row=0, column=3, padx=2)
        tk.Label(cabecalho_frame, text="Valor", width=10, font=("Arial", 10, "bold")).grid(row=0, column=4, padx=2)
        tk.Label(cabecalho_frame, text="Ação", width=10, font=("Arial", 10, "bold")).grid(row=0, column=5, padx=2)
        
        # Container scrollable
        container = tk.Frame(frame_lista, bg="white")
        container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(container, bg="white", height=250)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Carregar reservas do usuário
        self.carregar_minhas_reservas(scrollable_frame, janela_reservas)
        
        # Botão fechar
        tk.Button(janela_reservas, text="Fechar", command=janela_reservas.destroy,
                font=("Arial", 10), bg="red", fg="white", width=15).pack(pady=10)

    def carregar_minhas_reservas(self, parent, janela_pai):
        """Carrega e exibe as reservas do usuário logado"""
        if not self.master.usuario_logado:
            tk.Label(parent, text="Nenhum usuário logado", font=("Arial", 12), bg="white").pack(pady=20)
            return
        
        usuario = self.master.usuario_logado
        reservas_ativas = [r for r in usuario.reservas if r.get('status') == 'confirmada']
        
        if not reservas_ativas:
            tk.Label(parent, text="Nenhuma reserva ativa", font=("Arial", 12), bg="white").pack(pady=20)
            return
        
        for i, reserva in enumerate(reservas_ativas):
            voo_id = reserva['voo_id']
            assento_id = reserva['assento_id']
            assento_info = reserva.get('assento_info', {})
            
            # Buscar informações completas do voo
            voo = self.master.gerenciador_voos.obter_voo(voo_id)
            
            frame_reserva = tk.Frame(parent, bg="white", relief="raised", bd=1)
            frame_reserva.pack(fill="x", padx=5, pady=2)
            
            # Informações da reserva
            tk.Label(frame_reserva, text=voo_id, width=10, anchor="w", bg="white").grid(row=0, column=0, padx=2, pady=5)
            tk.Label(frame_reserva, text=assento_id, width=8, anchor="w", bg="white").grid(row=0, column=1, padx=2, pady=5)
            
            if voo:
                origem_destino = f"{voo.origem} -> {voo.destino}"
                tk.Label(frame_reserva, text=origem_destino, width=20, anchor="w", bg="white").grid(row=0, column=2, padx=2, pady=5)
                tk.Label(frame_reserva, text=voo.data_hora, width=15, anchor="w", bg="white").grid(row=0, column=3, padx=2, pady=5)
            else:
                tk.Label(frame_reserva, text="Voo não encontrado", width=20, anchor="w", bg="white").grid(row=0, column=2, padx=2, pady=5)
                tk.Label(frame_reserva, text="N/A", width=15, anchor="w", bg="white").grid(row=0, column=3, padx=2, pady=5)
            
            valor = assento_info.get('valor', 0)
            tk.Label(frame_reserva, text=f"R$ {valor:.2f}", width=10, anchor="w", bg="white").grid(row=0, column=4, padx=2, pady=5)
            
            # Botão cancelar
            tk.Button(frame_reserva, text="Cancelar", width=8,
                    command=lambda v=voo_id, a=assento_id, j=janela_pai: self.cancelar_reserva(v, a, j),
                    bg="red", fg="white", font=("Arial", 8)).grid(row=0, column=5, padx=2, pady=5)

    def cancelar_reserva(self, voo_id, assento_id, janela_pai):
        """Cancela uma reserva específica"""
        if not self.master.usuario_logado:
            messagebox.showerror("Erro", "Usuário não logado")
            return
        
        usuario = self.master.usuario_logado
        voo = self.master.gerenciador_voos.obter_voo(voo_id)
        
        if not voo:
            messagebox.showerror("Erro", f"Voo {voo_id} não encontrado")
            return
        
        # Confirmar cancelamento
        resposta = messagebox.askyesno(
            "Confirmar Cancelamento",
            f"Cancelar reserva do assento {assento_id} no voo {voo_id}?\n"
            f"{voo.origem} -> {voo.destino}\n\n"
            "Esta ação não pode ser desfeita."
        )
        
        if not resposta:
            return
        
        try:
            # Cancelar no sistema do usuário
            usuario.cancelar_reserva(voo_id, assento_id)
            
            # Remover do sistema do voo
            if hasattr(voo, 'assentos_reservados') and assento_id in voo.assentos_reservados:
                if voo.assentos_reservados[assento_id] == usuario.cpf:
                    del voo.assentos_reservados[assento_id]
            
            # Atualizar status na lista de reservas do voo
            if hasattr(voo, 'reservas'):
                for reserva in voo.reservas:
                    if (isinstance(reserva, dict) and 
                        reserva.get('usuario_cpf') == usuario.cpf and 
                        reserva.get('assento_id') == assento_id):
                        reserva['status'] = 'cancelada'
            
            # Salvar alterações
            self.master.gerenciador_voos.salvar_voos()
            
            # Salvar usuários atualizados
            todos_usuarios = carregar_usuarios()
            usuario_atualizado = False
            
            for i, u in enumerate(todos_usuarios):
                if u.cpf == usuario.cpf:
                    todos_usuarios[i] = usuario
                    usuario_atualizado = True
                    break
            
            if not usuario_atualizado:
                todos_usuarios.append(usuario)
            
            salvar_usuarios(todos_usuarios)
            
            messagebox.showinfo("Sucesso", f"Reserva do assento {assento_id} cancelada com sucesso!")
            
            # Fechar janela de reservas e recarregar
            janela_pai.destroy()
            self.ir_reservas()  # Reabre com lista atualizada
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao cancelar reserva: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

    def atualizar_preview_reservas(self):
        """Atualiza a preview de reservas no painel principal"""
        # Limpa a listbox
        self.lista_reservas.delete(0, tk.END)
        
        if self.master.usuario_logado:
            usuario = self.master.usuario_logado
            reservas_ativas = [r for r in usuario.reservas if r.get('status') == 'confirmada']
            
            for reserva in reservas_ativas[:3]:  # Mostra até 3 reservas
                voo_id = reserva['voo_id']
                assento_id = reserva['assento_id']
                voo = self.master.gerenciador_voos.obter_voo(voo_id)
                
                if voo:
                    texto = f"Voo {voo_id}: {voo.origem} -> {voo.destino} - Assento {assento_id}"
                else:
                    texto = f"Voo {voo_id} - Assento {assento_id}"
                
                self.lista_reservas.insert(tk.END, texto)
            
            if len(reservas_ativas) > 3:
                self.lista_reservas.insert(tk.END, f"... e mais {len(reservas_ativas) - 3} reservas")
            
            if not reservas_ativas:
                self.lista_reservas.insert(tk.END, "Nenhuma reserva ativa")


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
        
        # Lista de voos com barra de rolagem
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
                           f"{voo.origem} -> {voo.destino}\n"
                           f"Avião: {voo.aviao.aviao_id}\n"
                           f"Próximo: selecione seu assento")
        
        # Navegar para tela de assentos
        self.master.frames["TelaAssentos"].atualizar_tela()
        self.master.mostrar_tela("TelaAssentos")
    
    def voltar_painel(self):
        """Volta para o painel do usuário"""
        self.master.mostrar_tela("TelaPainel")


class TelaAssentos(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.assentos_frame = None
        self.assento_selecionado = None
        self.criar_widgets()
        
    def criar_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="Seleção de Assentos", 
                        font=('Arial', 16, 'bold'), bg='white')
        titulo.pack(pady=10)
        
        # Informações do voo
        if self.master.voo_selecionado:
            info_text = f"Voo: {self.master.voo_selecionado.voo_id} | " \
                    f"{self.master.voo_selecionado.origem} -> {self.master.voo_selecionado.destino}"
            info_label = tk.Label(main_frame, text=info_text, 
                                font=('Arial', 12), bg='white')
            info_label.pack(pady=5)
        
        # Container principal com scrollbar
        container_frame = tk.Frame(main_frame, bg='white')
        container_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Canvas e Scrollbar
        canvas = tk.Canvas(container_frame, bg='white', height=300)  # Altura fixa para scroll
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        
        # Frame de rolagem dentro do canvas
        self.assentos_frame = tk.Frame(canvas, bg='white')
        self.assentos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Criar window no canvas
        canvas.create_window((0, 0), window=self.assentos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empacotar canvas e barra de rolagem
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para legenda
        self.criar_legenda(main_frame)
        
        # Status da seleção
        self.status_label = tk.Label(main_frame, text="Nenhum assento selecionado", 
                                font=('Arial', 10), bg='white', fg='gray')
        self.status_label.pack(pady=5)

        # Botões de navegação (código existente mantido)
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Voltar ao Painel", command=self.voltar_painel,
                font=('Arial', 10), bg='red', fg='white', padx=15).grid(row=0, column=0, padx=10)
        
        tk.Button(btn_frame, text="Ver Outros Voos", command=self.voltar_voos,
                font=('Arial', 10), bg='orange', fg='white', padx=15).grid(row=0, column=1, padx=10)
        
        self.btn_confirmar = tk.Button(btn_frame, text="Confirmar Reserva", 
                                    command=self.confirmar_reserva, state=tk.DISABLED,
                                    font=('Arial', 10), bg='green', fg='white', padx=15)
        self.btn_confirmar.grid(row=0, column=2, padx=10)
        
        # Carregar assentos
        self.carregar_assentos()
        
    def criar_legenda(self, parent):
        legenda_frame = tk.Frame(parent, bg='white')
        legenda_frame.pack(pady=10)
        
        legendas = [
            ("Livre", "lightgreen"),
            ("Ocupado", "red"), 
            ("Selecionado", "#3498db"),
            ("Emergência", "orange"),
            ("Bloqueado", "lightgray")
        ]
        
        for i, (texto, cor) in enumerate(legendas):
            frame = tk.Frame(legenda_frame, bg='white')
            frame.grid(row=0, column=i, padx=10)
            
            tk.Label(frame, text="■", fg=cor, font=('Arial', 14), bg='white').pack(side=tk.LEFT)
            tk.Label(frame, text=texto, font=('Arial', 9), bg='white').pack(side=tk.LEFT, padx=2)
    
    def carregar_assentos(self):
        if not self.master.voo_selecionado:
            return


        # Limpar assentos anteriores
        for widget in self.assentos_frame.winfo_children():
            widget.destroy()
        
        # Obter layout do avião
        aviao = self.master.voo_selecionado.aviao
        layout = aviao.gerar_layout()
        
        # Organizar assentos por fileira
        fileiras = {}
        for assento_id, info in layout.items():
            fileira = assento_id[:-1]  # Remove letra (ex: "1A" -> "1")
            if fileira not in fileiras:
                fileiras[fileira] = []
            fileiras[fileira].append((assento_id, info))
        
        # Ordenar fileiras numericamente
        fileiras_ordenadas = sorted(fileiras.items(), key=lambda x: int(x[0]))
        
        # Criar grid de assentos
        for row_idx, (fileira, assentos) in enumerate(fileiras_ordenadas):
            # Label da fileira
            tk.Label(self.assentos_frame, text=fileira, font=('Arial', 10, 'bold'), 
                    bg='white', width=3).grid(row=row_idx, column=0, padx=5, pady=2)
            
            # Ordenar assentos por coluna (A, B, C, D, E, F)
            assentos_ordenados = sorted(assentos, key=lambda x: x[0][-1])
            
            for col_idx, (assento_id, info) in enumerate(assentos_ordenados, 1):
                self.criar_botao_assento(assento_id, info, row_idx, col_idx)
    
    def criar_botao_assento(self, assento_id, info, row, col):
        # Determinar cor baseado no status
        if info.get('bloqueado', False):
            cor = "lightgray"  # Cinza - bloqueado
            estado = tk.DISABLED
        elif self.assento_esta_reservado(assento_id):
            cor = "red"  # Vermelho - ocupado
            estado = tk.DISABLED
        elif info.get('emergencia', False):
            cor = "orange"  # Laranja - emergência
            estado = tk.NORMAL
        else:
            cor = "lightgreen"  # Verde - livre
            estado = tk.NORMAL
        
        btn = tk.Button(self.assentos_frame, text=assento_id, 
                       font=('Arial', 9), bg=cor, fg='white',
                       width=4, height=1, state=estado,
                       command=lambda a=assento_id, i=info: self.selecionar_assento(a, i))
        btn.grid(row=row, column=col, padx=2, pady=2)
    
    def assento_esta_reservado(self, assento_id):
        """Verifica se assento já está reservado no voo - CORREÇÃO COMPLETA"""
        if not self.master.voo_selecionado:
            return False
        
        # Verificar no sistema de reservas do voo
        voo = self.master.voo_selecionado
        
        # Verificar em assentos_reservados
        if hasattr(voo, 'assentos_reservados') and assento_id in voo.assentos_reservados:
            return True
            
        # Verificar em reservas
        if hasattr(voo, 'reservas'):
            for reserva in voo.reservas:
                if isinstance(reserva, dict) and reserva.get('assento_id') == assento_id:
                    return True
                elif hasattr(reserva, 'assento') and reserva.assento == assento_id:
                    return True
        
        return False
    
    def selecionar_assento(self, assento_id, assento_info):
        """Manipula seleção de assento"""
        self.assento_selecionado = assento_id
        self.btn_confirmar.config(state=tk.NORMAL)
        self.status_label.config(text=f"Assento selecionado: {assento_id}")
        
        print(f"Assento selecionado: {assento_id} - {assento_info}")

    def voltar_painel(self):
        """Volta diretamente para o painel do usuário """
        self.master.mostrar_tela("TelaPainel")

    def voltar_voos(self):
        self.master.mostrar_tela("TelaVoos")

    def atualizar_info_voo(self, voo):
        """Atualiza informações do voo na tela"""
        self.master.voo_selecionado = voo
        self.atualizar_tela()

    def atualizar_tela(self):
        """Atualiza a tela quando navegada"""
        self.assento_selecionado = None
        self.btn_confirmar.config(state=tk.DISABLED)
        self.status_label.config(text="Nenhum assento selecionado")
        self.carregar_assentos()

    def confirmar_reserva(self):

        if not self.assento_selecionado:
            messagebox.showwarning("Aviso", "Selecione um assento antes de confirmar.")
            return
            
        usuario = self.master.usuario_logado
        voo = self.master.voo_selecionado
        assento_id = self.assento_selecionado
        
        try:
            # Reservar no sistema do voo
            sucesso = voo.reservar_assento(usuario, assento_id)
            
            if sucesso:
                # Reservar no sistema do usuário
                layout = voo.aviao.gerar_layout()
                assento_info = layout.get(assento_id)
                usuario.criar_reserva(voo.voo_id, assento_id, assento_info)
                
                # Atualizar o voo no gerenciador
                self.master.gerenciador_voos.voos[voo.voo_id] = voo
                
                # Salvar alterações em AMBOS os sistemas
                self.master.gerenciador_voos.salvar_voos()
                
                # Salvar TODOS os usuários
                todos_usuarios = carregar_usuarios()
                
                usuario_atualizado = False
                for i, u in enumerate(todos_usuarios):
                    if u.cpf == usuario.cpf:
                        todos_usuarios[i] = usuario
                        usuario_atualizado = True
                        break
                
                if not usuario_atualizado:
                    todos_usuarios.append(usuario)
                
                salvar_usuarios(todos_usuarios)
                
                messagebox.showinfo("Sucesso", 
                                f"Reserva confirmada!\n"
                                f"Assento: {assento_id}\n"
                                f"Voo: {voo.voo_id}\n"
                                f"Valor: R$ {assento_info.get('valor', 0):.2f}")
                
                # 4. Atualizar visualização
                self.carregar_assentos()
                self.assento_selecionado = None
                self.btn_confirmar.config(state=tk.DISABLED)
                self.status_label.config(text="Reserva confirmada! Selecione novo assento ou volte ao painel.")
                
                # Atualizar painel do usuário
                self.master.frames["TelaPainel"].atualizar_info_usuario()
                
            else:
                messagebox.showerror("Erro", "Não foi possível reservar o assento. Tente outro.")
                
        except ValueError as e:
            messagebox.showerror("Erro na reserva", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            


if __name__ == "__main__":
    print("=== SISTEMA DE RESERVAS - STATUS FINAL ===")
    
    # Carregar dados
    avioes = carregar_avioes()
    usuarios = carregar_usuarios()
    gerenciador = GerenciadorVoos()
    gerenciador.carregar_voos(avioes)
    
    print(f"Aviões: {len(avioes)}")
    print(f"Usuários: {len(usuarios)}") 
    print(f"Voos: {len(gerenciador.voos)}")
    
    # Mostrar reservas ativas
    for usuario in usuarios:
        reservas_ativas = [r for r in usuario.reservas if r.get('status') == 'confirmada']
        if reservas_ativas:
            print(f"   {usuario.nome}: {len(reservas_ativas)} reserva(s)")
    
    app = App()
    app.mainloop()
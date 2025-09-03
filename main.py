# /main.py
# CLI Parcial
from biblioteca.usuarios import carregar_usuarios, salvar_usuarios, Usuario
from biblioteca.avioes import carregar_avioes, Aviao
from biblioteca.voos import Voo, GerenciadorVoos
import os
import sys

def menu_principal():
    """Menu principal do sistema"""
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE RESERVA DE VOOS")
        print("="*50)
        print("1. Cadastrar usuario")
        print("2. Listar usuarios cadastrados")
        print("3. Visualizar layout de aviao")
        print("4. Validar assento")
        print("5. Fazer login")
        print("6. Sair")
        print("="*50)
        
        opcao = input("Escolha uma opcao: ").strip()
        
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            visualizar_layout_aviao()
        elif opcao == "4":
            validar_assento()
        elif opcao == "5":
            fazer_login()
        elif opcao == "6":
            print("Saindo do sistema...")
            break
        else:
            print("X Opcao invalida. Tente novamente.")

def fazer_login():
    """Faz login de usuário"""
    print("\n" + "="*50)
    print("LOGIN")
    print("="*50)
    
    try:
        cpf = input("CPF: ").strip()
        usuarios = carregar_usuarios()
        
        usuario_encontrado = None
        for usuario in usuarios:
            if usuario.cpf == cpf:
                usuario_encontrado = usuario
                break
        
        if usuario_encontrado:
            print(f"Bem-vindo, {usuario_encontrado.nome}!")
            menu_usuario(usuario_encontrado)
        else:
            print("X Usuário não encontrado.")
            
    except Exception as e:
        print(f"X Erro no login: {e}")

def menu_usuario(usuario):
    """Menu do usuário logado"""
    gerenciador_voos = GerenciadorVoos()
    gerenciador_avioes = carregar_avioes()
    
    while True:
        print("\n" + "="*50)
        print(f"USUÁRIO: {usuario.nome}")
        print("="*50)
        print("1. Visualizar voos disponíveis")
        print("2. Visualizar assentos de um voo")
        print("3. Fazer reserva")
        print("4. Cancelar reserva")
        print("5. Modificar reserva")
        print("6. Minhas reservas")
        print("7. Logout")
        print("="*50)
        
        opcao = input("Escolha uma opcao: ").strip()
        
        if opcao == "1":
            visualizar_voos_disponiveis()
        elif opcao == "2":
            visualizar_assentos_voo(usuario)
        elif opcao == "3":
            fazer_reserva(usuario, gerenciador_voos, gerenciador_avioes)
        elif opcao == "4":
            cancelar_reserva(usuario, gerenciador_voos)
        elif opcao == "5":
            modificar_reserva(usuario, gerenciador_voos, gerenciador_avioes)
        elif opcao == "6":
            minhas_reservas(usuario)
        elif opcao == "7":
            print("Logout realizado.")
            break
        else:
            print("X Opcao invalida. Tente novamente.")

def visualizar_voos_disponiveis():
    """Visualiza voos disponíveis"""
    print("\n" + "="*50)
    print("VOOS DISPONÍVEIS")
    print("="*50)
    
    try:
        gerenciador = GerenciadorVoos()
        gerenciador.carregar_voos(carregar_avioes())
        voos = gerenciador.listar_voos()
        
        if not voos:
            print("Nenhum voo disponível.")
            return
        
        for voo in voos:
            print(f"Voo {voo.voo_id}: {voo.origem} -> {voo.destino} - {voo.data_hora}")
            
    except Exception as e:
        print(f"X Erro ao carregar voos: {e}")

def visualizar_assentos_voo(usuario):
    """Visualiza assentos de um voo específico"""
    print("\n" + "="*50)
    print("ASSENTOS DO VOO")
    print("="*50)
    
    try:
        voo_id = input("ID do voo: ").strip()
        gerenciador = GerenciadorVoos()
        gerenciador.carregar_voos(carregar_avioes())
        voo = gerenciador.obter_voo(voo_id)
        
        if not voo:
            print("X Voo não encontrado.")
            return
        
        assentos = voo.listar_assentos()
        layout = voo.aviao.gerar_layout()
        
        print(f"Voo {voo_id}: {voo.origem} -> {voo.destino}")
        print("Assentos:")
        
        for assento, status in assentos.items():
            info_assento = layout.get(assento, {})
            classe = info_assento.get('classe', 'desconhecida')
            posicao = info_assento.get('posicao', 'desconhecida')
            emergencia = " (EMERGÊNCIA)" if info_assento.get('emergencia', False) else ""
            
            if status == 'reservado':
                if assento in [r['assento_id'] for r in usuario.reservas if r['status'] == 'confirmada']:
                    status_display = "RESERVADO POR VOCÊ"
                else:
                    status_display = "RESERVADO"
            else:
                status_display = "DISPONÍVEL"
            
            print(f"  {assento}: {classe} - {posicao}{emergencia} - {status_display}")
            
    except Exception as e:
        print(f"X Erro ao visualizar assentos: {e}")

def fazer_reserva(usuario, gerenciador_voos, gerenciador_avioes):
    """Faz reserva de assento"""
    print("\n" + "="*50)
    print("FAZER RESERVA")
    print("="*50)
    
    try:
        voo_id = input("ID do voo: ").strip()
        assento_id = input("Número do assento: ").strip().upper()
        
        gerenciador_voos.carregar_voos(gerenciador_avioes)
        voo = gerenciador_voos.obter_voo(voo_id)
        
        if not voo:
            print("X Voo não encontrado.")
            return
        
        # Verificar se usuário já tem reserva neste voo
        for reserva in usuario.reservas:
            if reserva['voo_id'] == voo_id and reserva['status'] == 'confirmada':
                print("X Você já tem uma reserva neste voo.")
                return
        
        # Obter informações do assento para validação
        layout = voo.aviao.gerar_layout()
        assento_info = layout.get(assento_id)
        
        if not assento_info:
            print("X Assento inválido.")
            return
        
        # Fazer reserva
        try:
            # Usar o método do usuário para criar reserva com informações do assento
            usuario.criar_reserva(voo_id, assento_id, assento_info)
            
            # Atualizar o voo com a reserva
            if voo.reservar_assento(usuario, assento_id):
                gerenciador_voos.salvar_voos()
                salvar_usuarios(carregar_usuarios())  # Atualizar lista de usuários
                print("✅ Reserva realizada com sucesso!")
            else:
                # Reverter reserva no usuário se falhar no voo
                usuario.cancelar_reserva(voo_id, assento_id)
                print("X Não foi possível realizar a reserva.")
                
        except ValueError as e:
            print(f"X {e}")
            
    except Exception as e:
        print(f"X Erro ao fazer reserva: {e}")

def cancelar_reserva(usuario, gerenciador_voos):
    """Cancela reserva de assento"""
    print("\n" + "="*50)
    print("CANCELAR RESERVA")
    print("="*50)
    
    try:
        voo_id = input("ID do voo: ").strip()
        assento_id = input("Número do assento: ").strip().upper()
        
        gerenciador_voos.carregar_voos(carregar_avioes())
        voo = gerenciador_voos.obter_voo(voo_id)
        
        if not voo:
            print("X Voo não encontrado.")
            return
        
        # Verificar se usuário tem reserva neste voo e assento
        tem_reserva = False
        for reserva in usuario.reservas:
            if (reserva['voo_id'] == voo_id and 
                reserva['assento_id'] == assento_id and 
                reserva['status'] == 'confirmada'):
                tem_reserva = True
                break
        
        if not tem_reserva:
            print("X Reserva não encontrada.")
            return
        
        # Cancelar reserva
        if voo.cancelar_reserva(usuario, assento_id):
            usuario.cancelar_reserva(voo_id, assento_id)
            gerenciador_voos.salvar_voos()
            salvar_usuarios(carregar_usuarios())
            print("✅ Reserva cancelada com sucesso!")
        else:
            print("X Não foi possível cancelar a reserva.")
            
    except Exception as e:
        print(f"X Erro ao cancelar reserva: {e}")

def modificar_reserva(usuario, gerenciador_voos, gerenciador_avioes):
    """Modifica reserva de assento"""
    print("\n" + "="*50)
    print("MODIFICAR RESERVA")
    print("="*50)
    
    try:
        voo_id_antigo = input("ID do voo atual: ").strip()
        assento_id_antigo = input("Número do assento atual: ").strip().upper()
        
        voo_id_novo = input("ID do novo voo: ").strip()
        assento_id_novo = input("Número do novo assento: ").strip().upper()
        
        # Primeiro cancela a reserva antiga
        gerenciador_voos.carregar_voos(gerenciador_avioes)
        voo_antigo = gerenciador_voos.obter_voo(voo_id_antigo)
        
        if voo_antigo and voo_antigo.cancelar_reserva(usuario, assento_id_antigo):
            usuario.cancelar_reserva(voo_id_antigo, assento_id_antigo)
            
            # Depois faz a nova reserva
            voo_novo = gerenciador_voos.obter_voo(voo_id_novo)
            if voo_novo:
                layout = voo_novo.aviao.gerar_layout()
                assento_info = layout.get(assento_id_novo)
                
                if assento_info:
                    usuario.criar_reserva(voo_id_novo, assento_id_novo, assento_info)
                    if voo_novo.reservar_assento(usuario, assento_id_novo):
                        gerenciador_voos.salvar_voos()
                        salvar_usuarios(carregar_usuarios())
                        print("✅ Reserva modificada com sucesso!")
                        return
        
        print("X Não foi possível modificar a reserva.")
        
    except Exception as e:
        print(f"X Erro ao modificar reserva: {e}")

def minhas_reservas(usuario):
    """Mostra reservas do usuário"""
    print("\n" + "="*50)
    print("MINHAS RESERVAS")
    print("="*50)
    
    reservas_ativas = [r for r in usuario.reservas if r['status'] == 'confirmada']
    
    if not reservas_ativas:
        print("Nenhuma reserva ativa.")
        return
    
    for i, reserva in enumerate(reservas_ativas, 1):
        print(f"{i}. Voo: {reserva['voo_id']} - Assento: {reserva['assento_id']}")

def cadastrar_usuario():
    """Cadastra um novo usuario"""
    print("\n" + "="*50)
    print("CADASTRO DE USUARIO")
    print("="*50)
    
    try:
        cpf = input("CPF: ").strip()
        nome = input("Nome completo: ").strip()
        data_nascimento = input("Data nascimento (DD/MM/AAAA): ").strip()
        email = input("Email: ").strip()
        
        usuario = Usuario(cpf, nome, data_nascimento, email)
        
        # Carregar usuarios existentes e adicionar novo
        usuarios = carregar_usuarios()
        usuarios.append(usuario)
        salvar_usuarios(usuarios)
        
        print(f"\n✅ Usuario {nome} cadastrado com sucesso!")
        
    except ValueError as e:
        print(f"\nX Erro no cadastro: {e}")
    except Exception as e:
        print(f"\nX Erro inesperado: {e}")

def listar_usuarios():
    """Lista todos os usuarios cadastrados"""
    print("\n" + "="*50)
    print("USUARIOS CADASTRADOS")
    print("="*50)
    
    try:
        usuarios = carregar_usuarios()
        
        if not usuarios:
            print("Nenhum usuario cadastrado.")
            return
        
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. CPF: {usuario.cpf}, Nome: {usuario.nome}, Email: {usuario.email}")
            
    except Exception as e:
        print(f"X Erro ao carregar usuarios: {e}")

def visualizar_layout_aviao():
    """Visualiza o layout de assentos de um aviao"""
    print("\n" + "="*50)
    print("LAYOUT DE AVIAO")
    print("="*50)
    
    try:
        avioes = carregar_avioes()
        
        if not avioes:
            print("Nenhum aviao cadastrado.")
            return
        
        print("Avioes disponiveis:")
        for i, aviao in enumerate(avioes, 1):
            print(f"{i}. {aviao.aviao_id} - {aviao.modelo}")
        
        try:
            escolha = int(input("\nEscolha o numero do aviao: ")) - 1
            if escolha < 0 or escolha >= len(avioes):
                print("X Opcao invalida!")
                return
        except ValueError:
            print("X Digite um numero valido!")
            return
        
        aviao = avioes[escolha]
        layout = aviao.gerar_layout()
        
        print(f"\nLayout do Aviao {aviao.aviao_id} ({aviao.modelo}):")
        print("Assento | Classe      | Posição   | Emergência | Valor")
        print("-" * 55)
        
        for assento, info in sorted(layout.items()):
            emergencia = "Sim" if info['emergencia'] else "Não"
            print(f"{assento:<7} | {info['classe']:<11} | {info['posicao']:<9} | {emergencia:<10} | R$ {info['valor']:.2f}")
            
    except Exception as e:
        print(f"X Erro ao visualizar layout: {e}")

def validar_assento():
    """Valida se um assento existe em um aviao"""
    print("\n" + "="*50)
    print("VALIDACAO DE ASSENTO")
    print("="*50)
    
    try:
        avioes = carregar_avioes()
        
        if not avioes:
            print("Nenhum aviao cadastrado.")
            return
        
        print("Avioes disponiveis:")
        for i, aviao in enumerate(avioes, 1):
            print(f"{i}. {aviao.aviao_id} - {aviao.modelo}")
        
        try:
            escolha = int(input("\nEscolha o numero do aviao: ")) - 1
            if escolha < 0 or escolha >= len(avioes):
                print("X Opcao invalida!")
                return
        except ValueError:
            print("X Digite um numero valido!")
            return
        
        aviao = avioes[escolha]
        assento = input("Digite o numero do assento (ex: 1A): ").strip().upper()
        
        if aviao.validar_assento(assento):
            layout = aviao.gerar_layout()
            info = layout[assento]
            emergencia = " (EMERGÊNCIA)" if info['emergencia'] else ""
            print(f"✅ Assento {assento}: VÁLIDO - {info['classe']} - {info['posicao']}{emergencia} - R$ {info['valor']:.2f}")
        else:
            print(f"X Assento {assento}: INVÁLIDO")
            
    except Exception as e:
        print(f"X Erro ao validar assento: {e}")

def configurar_ambiente():
    """Configura o ambiente criando diretorios necessarios"""
    if not os.path.exists('dados'):
        os.makedirs('dados')
    
    # Criar arquivo de avioes de exemplo se nao existir
    if not os.path.exists('dados/avioes.txt'):
        with open('dados/avioes.txt', 'w', encoding='utf-8') as f:
            f.write("BOEING-001;B737;30;6\n")
            f.write("AIRBUS-001;A320;28;6\n")
    
    # Criar arquivo de voos de exemplo se nao existir
    if not os.path.exists('dados/voos.txt'):
        with open('dados/voos.txt', 'w', encoding='utf-8') as f:
            f.write("V001;BOEING-001;Sao Paulo;Rio de Janeiro;2024-01-15 08:00\n")
            f.write("V002;AIRBUS-001;Rio de Janeiro;Brasilia;2024-01-16 14:30\n")

if __name__ == "__main__":
    configurar_ambiente()
    menu_principal()
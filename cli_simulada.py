#cli_simulada.py
import sys
import os
import time
from biblioteca.usuarios import carregar_usuarios, salvar_usuarios, Usuario
from biblioteca.avioes import carregar_avioes, Aviao, salvar_avioes
from biblioteca.voos import Voo, GerenciadorVoos

def cli_simulada():
    """Executa uma interação simulada completa do sistema"""
    print("="*60)
    print("SIMULAÇÃO CLI DO SISTEMA DE RESERVA DE VOOS")
    print("="*60)
    
    # Configurar ambiente
    configurar_ambiente()
    
    # 1. Cadastrar usuários
    print("\n1. CADASTRANDO USUÁRIOS...")
    try:
        usuarios = [
            Usuario("52998224725", "João Silva", "15/05/1990", "joao@email.com"),
            Usuario("11122233344", "Maria Souza", "01/01/2010", "maria@email.com")
        ]
        salvar_usuarios(usuarios)
        print("✅ Usuários cadastrados e salvos")
    except Exception as e:
        print(f"❌ Erro no cadastro: {e}")
        return
    
    # 2. Configurar aviões e voos
    print("\n2. CONFIGURANDO AVIÕES E VOOS...")
    try:
        avioes = carregar_avioes()
        if not avioes:
            avioes = [
                Aviao("BOEING-001", "B737", 30, 6),
                Aviao("AIRBUS-001", "A320", 28, 6)
            ]
            salvar_avioes(avioes)
            print("✅ Aviões criados: Boeing 737 e Airbus A320")
        else:
            print("✅ Aviões carregados do arquivo")
        
        gerenciador_voos = GerenciadorVoos()
        gerenciador_voos.carregar_voos(avioes)
        if not gerenciador_voos.voos:
            voo1 = Voo("V001", avioes[0], "São Paulo", "Rio de Janeiro", "2024-03-15 08:00")
            voo2 = Voo("V002", avioes[1], "Rio de Janeiro", "Brasília", "2024-03-16 14:30")
            gerenciador_voos.adicionar_voo(voo1)
            gerenciador_voos.adicionar_voo(voo2)
            print("✅ Voos criados: V001 (SP-RJ) e V002 (RJ-BSB)")
        else:
            print("✅ Voos carregados do arquivo")
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return
    
    # 3. Testar login
    print("\n3. TESTANDO LOGIN...")
    try:
        usuarios_carregados = carregar_usuarios()
        if usuarios_carregados:
            print(f"✅ {len(usuarios_carregados)} usuário(s) carregado(s)")
            for usuario in usuarios_carregados:
                idade = usuario.calcular_idade()
                status = "MAIOR" if usuario.eh_maior_de_idade() else "MENOR"
                print(f"   - {usuario.nome}: {idade} anos ({status})")
        else:
            print("❌ Nenhum usuário carregado")
            return
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return
    
    # 4. Visualizar layout de avião
    print("\n4. VISUALIZANDO LAYOUT DE AVIÃO...")
    try:
        if avioes:
            aviao = avioes[0]
            layout = aviao.gerar_layout()
            print(f"✅ Layout do {aviao.modelo} com {len(layout)} assentos")
            exemplos = ["1A", "1F", "5C", "15A", "15F", "30A", "30F"]
            for assento in exemplos:
                if assento in layout:
                    info = layout[assento]
                    emergencia = " (EMERGÊNCIA)" if info['emergencia'] else ""
                    print(f"   {assento}: {info['classe']} - {info['posicao']}{emergencia} - R$ {info['valor']:.2f}")
    except Exception as e:
        print(f"❌ Erro ao visualizar layout: {e}")
    
    # 5. Testar reservas
    print("\n5. TESTANDO RESERVAS...")
    try:
        gerenciador_voos.carregar_voos(avioes)
        voo = gerenciador_voos.obter_voo("V001")
        if voo and usuarios_carregados:
            usuario_maior = usuarios_carregados[0]
            layout = voo.aviao.gerar_layout()
            assento_info = layout.get("5C")
            usuario_maior.criar_reserva("V001", "5C", assento_info)
            if voo.reservar_assento(usuario_maior, "5C"):
                gerenciador_voos.salvar_voos()
                usuarios = carregar_usuarios()
                usuarios[0] = usuario_maior
                salvar_usuarios(usuarios)
                print("   ✅ Reserva 5C realizada com sucesso!")
            else:
                print("   ❌ Falha na reserva")
        else:
            print("   ❌ Voo ou usuários não encontrados")
    except Exception as e:
        print(f"   ❌ Erro na reserva: {e}")
    
    # 6. Testar regra de emergência com menor
    print("\n6. TESTANDO REGRA DE EMERGÊNCIA...")
    try:
        if len(usuarios_carregados) > 1:
            usuario_menor = usuarios_carregados[1]
            voo = gerenciador_voos.obter_voo("V001")
            layout = voo.aviao.gerar_layout()
            assento_emergencia = "1A"
            assento_info = layout.get(assento_emergencia)
            try:
                usuario_menor.criar_reserva("V001", assento_emergencia, assento_info)
                print("   ❌ ERRO: Deveria ter bloqueado!")
            except ValueError:
                print("   ✅ Correto: menor bloqueado em assento de emergência")
    except Exception as e:
        print(f"   ❌ Erro no teste de emergência: {e}")
    
    # 7. Visualizar voos
    print("\n7. VISUALIZANDO VOOS DISPONÍVEIS...")
    try:
        voos = gerenciador_voos.listar_voos()
        for voo in voos:
            print(f"   - Voo {voo.voo_id}: {voo.origem} → {voo.destino} - {voo.data_hora}")
    except Exception as e:
        print(f"   ❌ Erro ao visualizar voos: {e}")
    
    # 8. Cancelar reserva
    print("\n8. TESTANDO CANCELAMENTO DE RESERVA...")
    try:
        usuario = usuarios_carregados[0]
        voo = gerenciador_voos.obter_voo("V001")
        reservas_ativas = [r for r in usuario.reservas if r['status'] == 'confirmada']
        if reservas_ativas:
            reserva = reservas_ativas[0]
            if voo.cancelar_reserva(usuario, reserva['assento_id']):
                usuario.cancelar_reserva(reserva['voo_id'], reserva['assento_id'])
                gerenciador_voos.salvar_voos()
                usuarios = carregar_usuarios()
                usuarios[0] = usuario
                salvar_usuarios(usuarios)
                print("   ✅ Reserva cancelada com sucesso!")
    except Exception as e:
        print(f"   ❌ Erro no cancelamento: {e}")
    
    # 9. Modificar reserva
    print("\n9. TESTANDO MODIFICAÇÃO DE RESERVA...")
    try:
        usuario = usuarios_carregados[0]
        voo = gerenciador_voos.obter_voo("V001")
        layout = voo.aviao.gerar_layout()
        usuario.criar_reserva("V001", "7B", layout.get("7B"))
        voo.reservar_assento(usuario, "7B")
        usuario.modificar_reserva("V001", "7B", "V001", "7C", layout.get("7C"))
        voo.cancelar_reserva(usuario, "7B")
        voo.reservar_assento(usuario, "7C")
        gerenciador_voos.salvar_voos()
        usuarios = carregar_usuarios()
        usuarios[0] = usuario
        salvar_usuarios(usuarios)
        print("   ✅ Reserva modificada para 7C")
    except Exception as e:
        print(f"   ❌ Erro na modificação: {e}")
    
    # 10. Resumo final
    print("\n10. RESUMO FINAL...")
    try:
        usuarios_finais = carregar_usuarios()
        gerenciador_voos.carregar_voos(avioes)
        voos_finais = gerenciador_voos.listar_voos()
        print(f"   ✅ {len(usuarios_finais)} usuário(s) no sistema")
        print(f"   ✅ {len(voos_finais)} voo(s) configurado(s)")
        for usuario in usuarios_finais:
            reservas_ativas = [r for r in usuario.reservas if r['status'] == 'confirmada']
            if reservas_ativas:
                print(f"   {usuario.nome} tem {len(reservas_ativas)} reserva(s) ativa(s)")
                for reserva in reservas_ativas:
                    print(f"     - Voo {reserva['voo_id']}, Assento {reserva['assento_id']}")
            else:
                print(f"   {usuario.nome} não tem reservas ativas")
    except Exception as e:
        print(f"   ❌ Erro no resumo: {e}")
    
    print("\n" + "="*60)
    print("SIMULAÇÃO CONCLUÍDA!")
    print("="*60)

def configurar_ambiente():
    """Configura o ambiente criando diretórios necessários"""
    if not os.path.exists('dados'):
        os.makedirs('dados')
    if not os.path.exists('dados/avioes.txt'):
        with open('dados/avioes.txt', 'w', encoding='utf-8') as f:
            f.write("BOEING-001;B737;30;6\n")
            f.write("AIRBUS-001;A320;28;6\n")
    if not os.path.exists('dados/voos.txt'):
        with open('dados/voos.txt', 'w', encoding='utf-8') as f:
            f.write("V001;BOEING-001;Sao Paulo;Rio de Janeiro;2024-03-15 08:00\n")
            f.write("V002;AIRBUS-001;Rio de Janeiro;Brasilia;2024-03-16 14:30\n")

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print("Iniciando simulação CLI...")
    time.sleep(1)
    cli_simulada()
    print("\nPara executar o sistema interativo, use: python main.py")

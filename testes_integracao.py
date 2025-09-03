#/teste_integracao.py

import os
import shutil

from biblioteca.avioes_old import carregar_avioes
from biblioteca.usuarios import Usuario, carregar_usuarios, salvar_usuarios
from biblioteca.voos import GerenciadorVoos


def executar_testes_integracao():
    """Executa todos os testes implementados de forma incremental"""
    resultados = []
    testes_executados = []
    
    # Teste 1: Configuração do Ambiente
    if configurar_ambiente_teste.__code__.co_code != b'd\x00S\x00':
        try:
            sucesso = configurar_ambiente_teste()
            resultados.append(sucesso)
            testes_executados.append("Configuração do Ambiente")
        except Exception as e:
            print(f"Erro na configuração do ambiente: {e}")
            resultados.append(False)
            testes_executados.append("Configuração do Ambiente")
    
    # Teste 2: Restauração do Ambiente  
    if restaurar_ambiente.__code__.co_code != b'd\x00S\x00':
        try:
            sucesso = restaurar_ambiente()
            resultados.append(sucesso)
            testes_executados.append("Restauração do Ambiente")
        except Exception as e:
            print(f"Erro na restauração do ambiente: {e}")
            resultados.append(False)
            testes_executados.append("Restauração do Ambiente")
    
    # Teste 3: Reserva Integrada
    if testar_reserva_integrada.__code__.co_code != b'd\x00S\x00':
        try:
            sucesso = testar_reserva_integrada()
            resultados.append(sucesso)
            testes_executados.append("Reserva Integrada (Voo → Usuario → Aviao)")
        except Exception as e:
            print(f"Erro no teste de reserva integrada: {e}")
            resultados.append(False)
            testes_executados.append("Reserva Integrada (Voo → Usuario → Aviao)")
    
    # Teste 4: Cancelamento Integrado
    if testar_cancelamento_integrado.__code__.co_code != b'd\x00S\x00':
        try:
            sucesso = testar_cancelamento_integrado()
            resultados.append(sucesso)
            testes_executados.append("Cancelamento Integrado")
        except Exception as e:
            print(f"Erro no teste de cancelamento: {e}")
            resultados.append(False)
            testes_executados.append("Cancelamento Integrado")
    
    # Teste 5: Regras de Negócio
    if testar_regras_negocio.__code__.co_code != b'd\x00S\x00':
        try:
            sucesso = testar_regras_negocio()
            resultados.append(sucesso)
            testes_executados.append("Regras de Negócio (assentos emergência)")
        except Exception as e:
            print(f"Erro no teste de regras: {e}")
            resultados.append(False)
            testes_executados.append("Regras de Negócio (assentos emergência)")
    
    # Teste 6: Persistência Cruzada
    if testar_persistencia_cruzada.__code__.co_code != b'd\x00S\x00':
        try:
            sucesso = testar_persistencia_cruzada()
            resultados.append(sucesso)
            testes_executados.append("Persistência Cruzada entre arquivos")
        except Exception as e:
            print(f"Erro no teste de persistência: {e}")
            resultados.append(False)
            testes_executados.append("Persistência Cruzada entre arquivos")
    
    # Teste 7: Concorrência Básica
    if testar_concorrencia_basica_simples.__code__.co_code != b'd\x00S\x00':
        try:
            sucesso = testar_concorrencia_basica_simples()
            resultados.append(sucesso)
            testes_executados.append("Controle de Concorrência Básica")
        except Exception as e:
            print(f"Erro no teste de concorrência: {e}")
            resultados.append(False)
            testes_executados.append("Controle de Concorrência Básica")
    
    return resultados, testes_executados

def configurar_ambiente_teste():
    """Configura ambiente para testes criando arquivos necessários"""
    print("Configurando ambiente de teste...")
    
    try:
        # Criar diretório dados se não existir
        os.makedirs('dados', exist_ok=True)
        
        # Fazer backup dos arquivos originais se existirem
        if os.path.exists('dados/usuarios.txt'):
            shutil.copy2('dados/usuarios.txt', 'dados/usuarios_backup.txt')
        if os.path.exists('dados/avioes.txt'):
            shutil.copy2('dados/avioes.txt', 'dados/avioes_backup.txt')
        if os.path.exists('dados/voos.txt'):
            shutil.copy2('dados/voos.txt', 'dados/voos_backup.txt')
        
        # Criar arquivos de teste limpos
        with open('dados/avioes.txt', 'w', encoding='utf-8') as f:
            f.write("B737;Boeing 737;30;6\n")
        
        with open('dados/usuarios.txt', 'w', encoding='utf-8') as f:
            f.write("")  # Arquivo vazio
        
        with open('dados/voos.txt', 'w', encoding='utf-8') as f:
            f.write("V001;B737;SP;RJ;2024-01-15 08:00\n")
        
        print("Ambiente de teste configurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar ambiente: {e}")
        return False

def restaurar_ambiente():
    """Restaura ambiente original a partir dos backups"""
    print("Restaurando ambiente original...")
    
    try:
        # Dicionário de backups para restaurar
        backups = {
            'usuarios_backup.txt': 'usuarios.txt',
            'avioes_backup.txt': 'avioes.txt', 
            'voos_backup.txt': 'voos.txt'
        }
        
        restaurou = False
        
        for backup, original in backups.items():
            backup_path = os.path.join('dados', backup)
            original_path = os.path.join('dados', original)
            
            if os.path.exists(backup_path):
                # Restaurar backup
                shutil.copy2(backup_path, original_path)
                os.remove(backup_path)
                restaurou = True
                print(f"Restaurado: {original}")
            elif os.path.exists(original_path):
                # Remover arquivo de teste se não houver backup
                os.remove(original_path)
                print(f"Removido: {original}")
        
        # Remover arquivo de lock se existir
        lock_path = os.path.join('dados', 'voos.txt.lock')
        if os.path.exists(lock_path):
            os.remove(lock_path)
            print("Removido arquivo de lock")
        
        if restaurou:
            print("Ambiente restaurado com sucesso!")
            return True
        else:
            print("Nenhum backup encontrado para restaurar")
            return True
            
    except Exception as e:
        print(f"Erro ao restaurar ambiente: {e}")
        return False

def testar_reserva_integrada():
    """Testa reserva integrada entre Voo → Usuario → Aviao"""
    print("Executando teste de reserva integrada...")
    
    try:
        # Configurar ambiente primeiro
        if not configurar_ambiente_teste():
            return False
        
        # Carregar dados de teste
        avioes = carregar_avioes()
        usuarios = carregar_usuarios()
        
        if not avioes:
            print("Nenhum avião carregado")
            return False
        
        print(f"Avião carregado: {avioes[0].aviao_id}")
        
        # Criar gerenciador de voos e carregar voo de teste
        gerenciador = GerenciadorVoos()
        gerenciador.carregar_voos(avioes[0])
        voo = gerenciador.obter_voo("V001")
        
        if not voo:
            print("Voo V001 não encontrado")
            return False
        
        print(f"Voo encontrado: {voo.voo_id}")
        
        # Criar usuário de teste
        usuario = Usuario("52998224725", "Teste Integrado", "01/01/1990", "teste@email.com")
        usuarios.append(usuario)
        salvar_usuarios(usuarios)
        
        print(f"Usuário criado: {usuario.nome}, CPF: {usuario.cpf}")
        
        # Verificar se assento é válido no avião
        assento_valido = voo.aviao.validar_assento("1A")
        print(f"Assento 1A válido: {assento_valido}")
        
        # Verificar se assento já está reservado
        assentos_reservados = getattr(voo, 'assentos_reservados', {})
        print(f"Assentos já reservados: {assentos_reservados}")
        
        # Fazer reserva
        print("Tentando reservar assento 1A...")
        sucesso = voo.reservar_assento(usuario, "1A")
        print(f"Resultado da reserva: {sucesso}")
        
        if not sucesso:
            print("Falha na reserva do assento 1A")
            return False
        
        # Verificações pós-reserva
        print(f"Reservas do usuário: {usuario.reservas}")
        print(f"Assentos reservados no voo: {voo.assentos_reservados}")
        
        if len(usuario.reservas) != 1:
            print("Reserva não criada no usuário")
            return False
        
        if "1A" not in voo.assentos_reservados:
            print("Assento não reservado no voo")
            return False
        
        if voo.assentos_reservados["1A"] != usuario.cpf:
            print("CPF do usuário não registrado na reserva")
            return False
        
        print("Reserva integrada realizada com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro no teste de reserva integrada: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Restaurar ambiente independente do resultado
        restaurar_ambiente()

def testar_cancelamento_integrado():
    """Testa cancelamento integrado - Versão inicial"""
    print("Executando teste de cancelamento integrado...")
    # Esta função será implementada posteriormente
    # Testará cancelamento entre módulos
    return False  # Retorno temporário

def testar_regras_negocio():
    """Testa regras de negócio - Versão inicial"""
    print("Executando teste de regras de negócio...")
    # Esta função será implementada posteriormente
    # Testará regras como menores em assentos emergência
    return False  # Retorno temporário

def testar_persistencia_cruzada():
    """Testa persistência cruzada - Versão inicial"""
    print("Executando teste de persistência cruzada...")
    # Esta função será implementada posteriormente
    # Testará consistência entre arquivos
    return False  # Retorno temporário

def testar_concorrencia_basica_simples():
    """Testa concorrência básica - Versão inicial"""
    print("Executando teste de concorrência básica...")
    # Esta função será implementada posteriormente
    # Testará mecanismos de lock e concorrência
    return False  # Retorno temporário


# Executa e mostra resultados
if __name__ == "__main__":
    print("Iniciando testes de integração...")
    print("=" * 50)
    
    try:
        # Executar testes
        resultados, testes_executados = executar_testes_integracao()
        
        # Mostrar resultados
        if resultados and testes_executados:
            print("\nRESULTADOS DOS TESTES:")
            print("=" * 50)
            for i, (teste, resultado) in enumerate(zip(testes_executados, resultados), 1):
                status = "OK" if resultado else "FALHOU"
                print(f"Teste {i}: {teste} - {status}")
            
            print(f"\nTotal: {sum(resultados)}/{len(resultados)} testes passaram")
        else:
            print("Nenhum teste implementado ainda.")
            
    except TypeError:
        print("Função executar_testes_integracao() não retorna valores esperados.")
        print("Implemente a função para retornar (resultados, testes_executados)")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
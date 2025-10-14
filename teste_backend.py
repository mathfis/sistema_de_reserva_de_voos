#!/usr/bin/env python3
"""
Sistema de Teste Backend para Sistema de Reserva de Voos
Testa todas as funcionalidades do backend: usuários, aviões, voos e reservas
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# Adiciona o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from biblioteca.usuarios import Usuario, carregar_usuarios, salvar_usuarios
from biblioteca.avioes import Aviao, carregar_avioes, salvar_avioes
from biblioteca.voos import Voo, GerenciadorVoos

class TestBackend:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.dados_dir = os.path.join(self.temp_dir, "dados")
        os.makedirs(self.dados_dir)
        print(f"📁 Diretório de teste: {self.temp_dir}")
    
    def setup_test_environment(self):
        """Configura ambiente de teste com dados iniciais"""
        # Criar arquivos de dados de teste com nomes específicos
        with open(os.path.join(self.dados_dir, "avioes_teste.txt"), "w", encoding="utf-8") as f:
            f.write("A320;Airbus A320;30;6\n")
            f.write("B737;Boeing 737;32;6\n")
        
        with open(os.path.join(self.dados_dir, "usuarios_teste.txt"), "w", encoding="utf-8") as f:
            f.write("123.456.789-00;João Silva;15/05/1990;joao@email.com;senha123;\n")
            f.write("987.654.321-00;Maria Santos;20/08/2005;maria@email.com;senha456;\n")
        
        with open(os.path.join(self.dados_dir, "voos_teste.txt"), "w", encoding="utf-8") as f:
            f.write("VG1001;A320;São Paulo;Rio de Janeiro;2025-03-15 08:00;\n")
            f.write("VG1002;B737;Rio de Janeiro;Brasília;2025-03-15 14:30;\n")
    
    def test_usuarios(self):
        """Testa funcionalidades relacionadas a usuários"""
        print("\n" + "="*50)
        print("🧪 TESTANDO MÓDULO DE USUÁRIOS")
        print("="*50)
        
        # Teste 1: Criação de usuário válido
        try:
            usuario1 = Usuario("52998224725", "Teste Silva", "15/05/1990", "teste@email.com", "senha123")
            print("✅ Usuário criado com sucesso")
            print(f"   CPF formatado: {usuario1.cpf}")
            print(f"   Maior de idade: {usuario1.eh_maior_de_idade()}")
        except Exception as e:
            print(f"❌ Erro na criação de usuário: {e}")
        
        # Teste 2: Criação de usuário com CPF inválido
        try:
            usuario_invalido = Usuario("123", "Teste Inválido", "01/01/2000", "teste@email.com", "senha")
            print("❌ CPF inválido deveria ter gerado erro")
        except ValueError as e:
            print(f"✅ CPF inválido corretamente rejeitado: {e}")
        
        # Teste 3: Validação de idade
        try:
            usuario_menor = Usuario("11122233344", "Menor Teste", "20/08/2010", "menor@email.com", "senha", validar=False)
            idade = usuario_menor.calcular_idade()
            maior_idade = usuario_menor.eh_maior_de_idade()
            print(f"✅ Validação de idade: {idade} anos, Maior: {maior_idade}")
        except Exception as e:
            print(f"❌ Erro na validação de idade: {e}")
        
        
        # Teste 4: Persistência de usuários
        try:
            usuarios = [
                Usuario("52998224725", "User 1", "01/01/1990", "user1@email.com", "senha1"),
                Usuario("98765432100", "User 2", "01/01/2005", "user2@email.com", "senha2")
            ]
            
            # Salvar em arquivo de teste
            with open(os.path.join(self.dados_dir, "usuarios_teste.txt"), "w", encoding="utf-8") as f:
                for usuario in usuarios:
                    reservas_str = ','.join([f"{r['voo_id']}-{r['assento_id']}" for r in usuario.reservas if r.get('status') == 'confirmada'])
                    linha = f"{usuario.cpf};{usuario.nome};{usuario.data_nascimento};{usuario.email};{usuario.senha};{reservas_str}\n"
                    f.write(linha)
            
            # Carregar do arquivo de teste
            usuarios_carregados = []
            with open(os.path.join(self.dados_dir, "usuarios_teste.txt"), "r", encoding="utf-8") as file:
                for linha in file:
                    linha = linha.strip()
                    if linha:
                        partes = linha.split(';')
                        if len(partes) >= 4:
                            cpf = partes[0]
                            nome = partes[1]
                            data_nascimento = partes[2]
                            email = partes[3]
                            senha = partes[4] if len(partes) > 4 else ""
                            usuario = Usuario(cpf, nome, data_nascimento, email, senha, validar=False)
                            usuarios_carregados.append(usuario)
            
            print(f"Persistência: {len(usuarios_carregados)} usuários carregados")
        except Exception as e:
            print(f"Erro na persistência: {e}")
    
    def test_avioes(self):
        """Testa funcionalidades relacionadas a aviões"""
        print("\n" + "="*50)
        print("✈️ TESTANDO MÓDULO DE AVIÕES")
        print("="*50)
        
        # Teste 1: Criação de avião
        try:
            aviao = Aviao("A320", "Airbus A320", 30, 6)
            print(f"✅ Avião criado: {aviao.modelo}")
            print(f"   Fileiras: {aviao.fileiras}, Assentos por fileira: {aviao.assentos_por_fileira}")
        except Exception as e:
            print(f"❌ Erro na criação de avião: {e}")
        
        # Teste 2: Geração de layout
        try:
            layout = aviao.gerar_layout()
            print(f"✅ Layout gerado: {len(layout)} assentos")
            
            # Verificar alguns assentos específicos
            exemplos = ["1A", "1F", "15A", "15F", "30A", "30F"]
            for assento in exemplos:
                if assento in layout:
                    info = layout[assento]
                    print(f"   {assento}: {info['classe']}, {info['posicao']}, Emergência: {info['emergencia']}")
        except Exception as e:
            print(f"❌ Erro na geração de layout: {e}")
        
        # Teste 3: Validação de assentos
        try:
            valido = aviao.validar_assento("1A")
            invalido = aviao.validar_assento("31A")
            print(f"✅ Validação de assentos: '1A'={valido}, '31A'={invalido}")
        except Exception as e:
            print(f"❌ Erro na validação de assentos: {e}")
    
    def test_voos(self):
        """Testa funcionalidades relacionadas a voos"""
        print("\n" + "="*50)
        print("🎫 TESTANDO MÓDULO DE VOOS")
        print("="*50)
        
        # Configurar ambiente
        aviao = Aviao("A320", "Airbus A320", 30, 6)
        usuario_maior = Usuario("12345678900", "Maior Idade", "01/01/1990", "maior@email.com", "senha", validar=False)
        usuario_menor = Usuario("98765432100", "Menor Idade", "01/01/2010", "menor@email.com", "senha", validar=False)
        
        # Teste 1: Criação de voo
        try:
            voo = Voo("VG1001", aviao, "São Paulo", "Rio de Janeiro", "2025-03-15 08:00")
            print(f"✅ Voo criado: {voo.voo_id}")
            print(f"   Rota: {voo.origem} → {voo.destino}")
        except Exception as e:
            print(f"❌ Erro na criação de voo: {e}")
            return
        
        # Teste 2: Listagem de assentos
        try:
            assentos = voo.listar_assentos()
            print(f"✅ Listagem de assentos: {len(assentos)} assentos no total")
            livres = [a for a, s in assentos.items() if s == 'livre']
            print(f"   Assentos livres: {len(livres)}")
        except Exception as e:
            print(f"❌ Erro na listagem de assentos: {e}")
        
        # Teste 3: Reserva de assento válida
        try:
            sucesso = voo.reservar_assento(usuario_maior, "5C")
            if sucesso:
                print("✅ Reserva de assento bem-sucedida")
            else:
                print("❌ Falha na reserva de assento")
        except Exception as e:
            print(f"❌ Erro na reserva: {e}")
        
        # Teste 4: Tentativa de reserva duplicada
        try:
            sucesso = voo.reservar_assento(usuario_maior, "5C")
            if not sucesso:
                print("✅ Duplicata corretamente rejeitada")
            else:
                print("❌ Duplicata deveria ter sido rejeitada")
        except Exception as e:
            print(f"✅ Duplicata corretamente rejeitada com erro: {e}")
        
        # Teste 5: Tentativa de reserva em assento de emergência por menor
        try:
            layout = aviao.gerar_layout()
            assento_emergencia = "1A"  # Assento de emergência
            if layout[assento_emergencia]['emergencia']:
                voo.reservar_assento(usuario_menor, assento_emergencia)
                print("❌ Menor deveria ser bloqueado em assento de emergência")
            else:
                print("⚠️  Assento de emergência não identificado corretamente")
        except ValueError as e:
            print(f"✅ Menor corretamente bloqueado em emergência: {e}")
        
        # Teste 6: Cancelamento de reserva
        try:
            sucesso = voo.cancelar_reserva(usuario_maior, "5C")
            if sucesso:
                print("✅ Cancelamento de reserva bem-sucedido")
            else:
                print("❌ Falha no cancelamento")
        except Exception as e:
            print(f"❌ Erro no cancelamento: {e}")
        
        # Teste 7: Serialização do voo
        try:
            serializado = voo.to_string()
            print(f"✅ Serialização: {serializado}")
        except Exception as e:
            print(f"❌ Erro na serialização: {e}")
    
    def test_gerenciador_voos(self):
        """Testa o gerenciador de voos com persistência"""
        print("\n" + "="*50)
        print("TESTANDO GERENCIADOR DE VOOS")
        print("="*50)
        
        # Configurar dados de teste
        avioes = [
            Aviao("A320", "Airbus A320", 30, 6),
            Aviao("B737", "Boeing 737", 32, 6)
        ]
        
        # Teste 1: Criação e configuração do gerenciador
        try:
            # Use o arquivo de teste específico
            gerenciador = GerenciadorVoos(os.path.join(self.dados_dir, "voos_teste.txt"))
            gerenciador.carregar_voos(avioes)
            print(f"Gerenciador criado: {len(gerenciador.voos)} voos carregados")
        except Exception as e:
            print(f"Erro na criação do gerenciador: {e}")
            return
        
        # Teste 2: Adição de novo voo
        try:
            novo_voo = Voo("VG1003", avioes[0], "São Paulo", "Salvador", "2025-03-16 10:00")
            gerenciador.adicionar_voo(novo_voo)
            print(f"✅ Novo voo adicionado: {len(gerenciador.voos)} voos no total")
        except Exception as e:
            print(f"❌ Erro ao adicionar voo: {e}")
        
        # Teste 3: Busca de voos
        try:
            resultados = gerenciador.buscar_voos(origem="São Paulo")
            print(f"✅ Busca por origem: {len(resultados)} voos encontrados")
            
            resultados_data = gerenciador.buscar_voos(data="2025-03-15")
            print(f"✅ Busca por data: {len(resultados_data)} voos encontrados")
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
        
        # Teste 4: Persistência
        try:
            gerenciador.salvar_voos()
            print("✅ Persistência de voos bem-sucedida")
            
            # Verificar se arquivo foi criado
            if os.path.exists(os.path.join(self.dados_dir, "voos_teste.txt")):
                with open(os.path.join(self.dados_dir, "voos_teste.txt"), "r", encoding="utf-8") as f:
                    linhas = f.readlines()
                    print(f"✅ Arquivo salvo com {len(linhas)} voos")
        except Exception as e:
            print(f"❌ Erro na persistência: {e}")
    
    def test_cenarios_complexos(self):
        """Testa cenários complexos e casos limite"""
        print("\n" + "="*50)
        print("🔬 TESTANDO CENÁRIOS COMPLEXOS")
        print("="*50)
        
        aviao = Aviao("A320", "Airbus A320", 30, 6)
        usuario1 = Usuario("11111111111", "Usuário 1", "01/01/1990", "user1@email.com", "senha1", validar=False)
        usuario2 = Usuario("22222222222", "Usuário 2", "01/01/1995", "user2@email.com", "senha2", validar=False)
        
        # Cenário 1: Múltiplos usuários no mesmo voo
        try:
            voo = Voo("VG2001", aviao, "São Paulo", "Rio de Janeiro", "2025-03-20 08:00")
            
            # Usuário 1 reserva assento
            voo.reservar_assento(usuario1, "10A")
            usuario1.criar_reserva("VG2001", "10A", aviao.gerar_layout().get("10A"))
            
            # Usuário 2 reserva assento diferente
            voo.reservar_assento(usuario2, "10B")
            usuario2.criar_reserva("VG2001", "10B", aviao.gerar_layout().get("10B"))
            
            # Verificar status
            assentos = voo.listar_assentos()
            reservados = [a for a, s in assentos.items() if s == 'reservado']
            
            print(f"✅ Cenário múltiplos usuários: {len(reservados)} assentos reservados")
            
        except Exception as e:
            print(f"❌ Erro no cenário múltiplos usuários: {e}")
        
        # Cenário 2: Modificação de reserva
        try:
            voo2 = Voo("VG2002", aviao, "Rio de Janeiro", "São Paulo", "2025-03-21 18:00")
            
            # Usuário faz reserva inicial
            voo2.reservar_assento(usuario1, "15C")
            usuario1.criar_reserva("VG2002", "15C", aviao.gerar_layout().get("15C"))
            
            # Usuário modifica reserva
            usuario1.cancelar_reserva("VG2002", "15C")
            voo2.cancelar_reserva(usuario1, "15C")
            
            voo2.reservar_assento(usuario1, "15D")
            usuario1.criar_reserva("VG2002", "15D", aviao.gerar_layout().get("15D"))
            
            print("✅ Cenário modificação: Reserva modificada com sucesso")
            
        except Exception as e:
            print(f"❌ Erro no cenário modificação: {e}")
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTES COMPLETOS DO BACKEND")
        print("="*60)
        
        try:
            self.setup_test_environment()
            self.test_usuarios()
            self.test_avioes() 
            self.test_voos()
            self.test_gerenciador_voos()
            self.test_cenarios_complexos()
            
            print("\n" + "="*60)
            print("🎉 TODOS OS TESTES FORAM CONCLUÍDOS!")
            print("="*60)
            
        except Exception as e:
            print(f"\n💥 ERRO CRÍTICO DURANTE OS TESTES: {e}")
        
        finally:
            # Limpeza
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print(f"🧹 Diretório de teste limpo: {self.temp_dir}")

if __name__ == "__main__":
    tester = TestBackend()
    tester.run_all_tests()
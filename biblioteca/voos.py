# /biblioteca/voos.py

from datetime import datetime
import os
import time

class Voo:
    def __init__(self, voo_id, aviao, origem, destino, data_hora):
        self.voo_id = voo_id
        self.aviao = aviao
        self.origem = origem
        self.destino = destino
        self.data_hora = data_hora
        self.assentos_reservados = {}  # assento_id: usuario_cpf
        self.reservas = []

    def reservar_assento(self, usuario, assento_id):
        """
        Reserva um assento para o usuário
        Retorna True se a reserva foi bem-sucedida
        """
        # Verifica se o assento é válido no avião
        if not self.aviao.validar_assento(assento_id):
            raise ValueError("Assento {} inválido para este avião".format(assento_id))
        
        # ✅ CORREÇÃO CRÍTICA: Verificar se o usuário já tem QUALQUER reserva neste voo
        for reservado_cpf in self.assentos_reservados.values():
            if reservado_cpf == usuario.cpf:
                raise ValueError(
                    f"Usuário já possui uma reserva neste voo. Cada passageiro pode ter apenas um assento por voo.")

        # Verifica se o assento já está reservado
        if assento_id in self.assentos_reservados:
            return False
        
        # Obtém informações do assento para validação
        layout = self.aviao.gerar_layout()
        assento_info = layout.get(assento_id)
        
        if assento_info:
            # Verifica regra de idade para assentos de emergência
            if assento_info.get('emergencia', False) and hasattr(usuario, 'eh_maior_de_idade') and not usuario.eh_maior_de_idade():
                raise ValueError("Menores de 18 anos não podem reservar assentos de emergência")
            
            # Verifica se o assento está bloqueado
            if assento_info.get('bloqueado', False):
                raise ValueError("Assento {} indisponível".format(assento_id))
        
        # Registrar reserva no sistema do voo
        self.assentos_reservados[assento_id] = usuario.cpf
        
        # Também registrar no sistema de reservas do voo
        self.confirmar_reserva(usuario.cpf, assento_id)

        return True

    def confirmar_reserva(self, usuario_cpf: str, assento_id: str):
        """
        Registra a reserva no voo, associando o CPF do usuário ao assento.
        """
        if not hasattr(self, "reservas"):
            self.reservas = []

        registro = {
            "usuario_cpf": usuario_cpf,
            "assento_id": assento_id,
            "data_reserva": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "status": "confirmada"
        }

        self.reservas.append(registro)

    def cancelar_reserva(self, usuario, assento_id):
        """
        Cancela a reserva de um assento
        Retorna True se o cancelamento foi bem-sucedido
        """
        # Verifica se o assento está reservado para este usuário
        if assento_id not in self.assentos_reservados:
            return False
        
        if self.assentos_reservados[assento_id] != usuario.cpf:
            return False
        
        # Remove a reserva
        del self.assentos_reservados[assento_id]
        return True
    
    def listar_assentos(self):
        """
        Retorna o status de todos os assentos do avião
        Formato: {assento_id: status}
        Status: 'livre', 'reservado'
        """
        status_assentos = {}
        layout = self.aviao.gerar_layout()
        
        for assento_id in layout.keys():
            if assento_id in self.assentos_reservados:
                status_assentos[assento_id] = 'reservado'
            else:
                status_assentos[assento_id] = 'livre'
        
        return status_assentos
    
    def to_string(self):
        """Converte o voo para string no formato de arquivo"""
        base = "{};{};{};{};{}".format(self.voo_id, self.aviao.aviao_id, self.origem, self.destino, self.data_hora)
        
        # ✅ ADICIONAR: Incluir assentos reservados na serialização
        if self.assentos_reservados:
            reservas_str = ",".join([f"{assento}:{cpf}" for assento, cpf in self.assentos_reservados.items()])
            base += f";{reservas_str}"

        return base
    
    @classmethod
    def from_string(cls, linha, avioes_list):
        """Cria um objeto Voo a partir de uma string do arquivo - VERSÃO CORRIGIDA"""
        dados = linha.strip().split(';')
        
        # ✅ CORREÇÃO: Aceitar de 5 a 6 campos (com ou sem reservas)
        if len(dados) < 5:
            raise ValueError("Formato de linha inválido - mínimo 5 campos requeridos")
            
        voo_id, aviao_id, origem, destino, data_hora = dados[:5]
        
        # Encontrar o avião correspondente
        aviao_encontrado = None
        for aviao in avioes_list:
            if aviao.aviao_id == aviao_id:
                aviao_encontrado = aviao
                break
        
        if not aviao_encontrado:
            print(f"⚠️  Avião {aviao_id} não encontrado para voo {voo_id}")
            return None  # ✅ CORREÇÃO: Retorna None em vez de erro
        
        voo = cls(voo_id, aviao_encontrado, origem, destino, data_hora)

        # ✅ CORREÇÃO MELHORADA: Carregar assentos reservados se existirem (campo 6)
        if len(dados) > 5 and dados[5].strip():
            reservas_str = dados[5].strip()
            print(f"📝 Carregando reservas para voo {voo_id}: {reservas_str}")
            
            for reserva in reservas_str.split(','):
                if ':' in reserva:
                    try:
                        assento_id, usuario_cpf = reserva.split(':', 1)
                        voo.assentos_reservados[assento_id] = usuario_cpf
                        print(f"   ✅ Reserva carregada: {assento_id} → {usuario_cpf}")
                    except ValueError as e:
                        print(f"⚠️  Formato de reserva inválido: {reserva} - {e}")
                else:
                    print(f"⚠️  Formato de reserva inválido (sem ':'): {reserva}")

        return voo

# Gerenciador de voos com persistência
class GerenciadorVoos:
    def __init__(self, caminho_arquivo="dados/voos.txt"):
        self.caminho_arquivo = caminho_arquivo
        self.voos = {}
        self.lock_file = caminho_arquivo + ".lock"
    
    def carregar_voos(self, avioes_list):
        """Carrega voos do arquivo com controle de concorrência - VERSÃO CORRIGIDA"""
        while os.path.exists(self.lock_file):
            time.sleep(0.1)
        
        try:
            with open(self.lock_file, 'w') as f:
                f.write("locked")
            
            if not os.path.exists(self.caminho_arquivo):
                print("📁 Arquivo de voos não encontrado")
                return
            
            self.voos = {}
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                for i, linha in enumerate(f, 1):
                    linha = linha.strip()
                    if not linha:  # Pula linhas vazias
                        continue
                        
                    try:
                        voo = Voo.from_string(linha, avioes_list)
                        if voo:  # ✅ CORREÇÃO: Só adiciona se não for None
                            self.voos[voo.voo_id] = voo
                            print(f"✅ Voo carregado: {voo.voo_id}")
                        else:
                            print(f"❌ Voo não carregado (avião não encontrado)")
                            
                    except ValueError as e:
                        print(f"❌ Erro na linha {i}: {e} - Linha: {linha}")
                        
            print(f"📊 Total de voos carregados: {len(self.voos)}")
                        
        finally:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)


    def salvar_voos(self):
        """Salva voos no arquivo com controle de concorrência"""
        while os.path.exists(self.lock_file):
            time.sleep(0.1)  # Espera se o arquivo estiver bloqueado
        
        try:
            # Cria arquivo lock
            with open(self.lock_file, 'w') as f:
                f.write("locked")
            
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
            
            with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
                for voo in self.voos.values():
                    f.write(voo.to_string() + '\n')
                    
        finally:
            # Remove arquivo lock
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
    
    def adicionar_voo(self, voo):
        """Adiciona um novo voo"""
        self.voos[voo.voo_id] = voo
        self.salvar_voos()
    
    def obter_voo(self, voo_id):
        """Obtém um voo pelo ID"""
        return self.voos.get(voo_id)
    
    def listar_voos(self):
        """Retorna lista de todos os voos"""
        return list(self.voos.values())
    
    def buscar_voos(self, origem=None, destino=None, data=None):
        """Busca voos por critérios"""
        resultados = []
        
        for voo in self.voos.values():
            if origem and voo.origem.lower() != origem.lower():
                continue
            if destino and voo.destino.lower() != destino.lower():
                continue
            if data and not voo.data_hora.startswith(data):
                continue
            resultados.append(voo)
        
        return resultados


# Exceções personalizadas
class ErroReservaAssento(Exception):
    pass

class AssentoJaReservadoError(ErroReservaAssento):
    pass

class AssentoInvalidoError(ErroReservaAssento):
    pass


if __name__ == '__main__':
    # Teste mínimo completo da classe Voo
    print("=== TESTE MÍNIMO VOO ===")
    
    # Mocks simplificados COMPATÍVEIS
    class AviaoMock:
        def __init__(self): 
            self.aviao_id = "A320-001"
            self.assentos = ["1A", "1B"]
        
        def validar_assento(self, assento): 
            return assento in self.assentos
        
        def obter_assentos(self): 
            return self.assentos
        
        def gerar_layout(self):
            return {
                "1A": {"posicao": "janela", "classe": "econômica", "emergencia": True, "valor": 150.00, "bloqueado": False},
                "1B": {"posicao": "meio", "classe": "econômica", "emergencia": False, "valor": 150.00, "bloqueado": False}
            }
    
    class UsuarioMock:
        def __init__(self): 
            self.cpf = "123.456.789-00"
            self.idade = 25
        
        def eh_maior_de_idade(self):
            return True
        
        def criar_reserva(self, voo_id, assento_id, valor=None):
            return True
        
        def cancelar_reserva(self, voo_id, assento_id):
            return True
    
    # Teste rápido
    aviao = AviaoMock()
    usuario = UsuarioMock()
    voo = Voo("V001", aviao, "SP", "RJ", "2024-01-15 08:00")
    
    # Testa tudo em sequência mínima
    print("Assentos inicial:", voo.listar_assentos())
    
    # Teste de reserva
    try:
        resultado = voo.reservar_assento(usuario, "1A")
        print("Reserva do assento 1A:", "Sucesso" if resultado else "Falha")
    except Exception as e:
        print("Erro na reserva:", e)
    
    print("Após reserva:", voo.listar_assentos())
    
    # Teste de cancelamento
    try:
        resultado = voo.cancelar_reserva(usuario, "1A")
        print("Cancelamento do assento 1A:", "Sucesso" if resultado else "Falha")
    except Exception as e:
        print("Erro no cancelamento:", e)
    
    print("Após cancelamento:", voo.listar_assentos())
    print("Serialização:", voo.to_string())
    
    print("=== FIM TESTE ===")
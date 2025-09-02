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
    
    def reservar_assento(self, usuario, assento_id):
        """
        Reserva um assento para o usuário
        Retorna True se a reserva foi bem-sucedida
        """
        # Verifica se o assento é válido no avião
        if not self.aviao.validar_assento(assento_id):
            raise ValueError("Assento {} inválido para este avião".format(assento_id))
        
        # Verifica se o assento já está reservado
        if assento_id in self.assentos_reservados:
            return False
        
        # Cria a reserva no usuário
        if usuario.criar_reserva(self.voo_id, assento_id):
            self.assentos_reservados[assento_id] = usuario.cpf
            return True
        
        return False
    
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
        
        # Cancela a reserva no usuário
        if usuario.cancelar_reserva(self.voo_id, assento_id):
            del self.assentos_reservados[assento_id]
            return True
        
        return False
    
    def listar_assentos(self):
        """
        Retorna o status de todos os assentos do avião
        Formato: {assento_id: status}
        Status: 'livre', 'reservado'
        """
        status_assentos = {}
        todos_assentos = self.aviao.obter_assentos()
        
        for assento in todos_assentos:
            if assento in self.assentos_reservados:
                status_assentos[assento] = 'reservado'
            else:
                status_assentos[assento] = 'livre'
        
        return status_assentos
    
    def to_string(self):
        """Converte o voo para string no formato de arquivo"""
        return "{};{};{};{};{}".format(self.voo_id, self.aviao.aviao_id, self.origem, self.destino, self.data_hora)
    
    @classmethod
    def from_string(cls, linha, aviao):
        """Cria um objeto Voo a partir de uma string do arquivo"""
        dados = linha.strip().split(';')
        if len(dados) != 5:
            raise ValueError("Formato de linha inválido")
        
        voo_id, aviao_id, origem, destino, data_hora = dados
        
        # Verifica se o avião corresponde
        if aviao.aviao_id != aviao_id:
            raise ValueError("ID do avião não corresponde")
        
        return cls(voo_id, aviao, origem, destino, data_hora)


# Gerenciador de voos com persistência
class GerenciadorVoos:
    def __init__(self, caminho_arquivo="dados/voos.txt"):
        self.caminho_arquivo = caminho_arquivo
        self.voos = {}
        self.lock_file = caminho_arquivo + ".lock"
    
    def carregar_voos(self, gerenciador_avioes):
        """Carrega voos do arquivo com controle de concorrência"""
        while os.path.exists(self.lock_file):
            time.sleep(0.1)  # Espera se o arquivo estiver bloqueado
        
        try:
            # Cria arquivo lock
            with open(self.lock_file, 'w') as f:
                f.write("locked")
            
            if not os.path.exists(self.caminho_arquivo):
                return
            
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    try:
                        voo = Voo.from_string(linha, gerenciador_avioes)
                        self.voos[voo.voo_id] = voo
                    except ValueError as e:
                        print("Erro ao carregar voo: {}".format(e))
                        
        finally:
            # Remove arquivo lock
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

#TESTAGEM
if __name__ == '__main__':
    # Teste mínimo completo da classe Voo
    print("=== TESTE MÍNIMO VOO ===")
    
    # Mocks simplificados
    class AviaoMock:
        def __init__(self): self.aviao_id = "A320-001"; self.assentos = ["1A", "1B"]
        def validar_assento(self, assento): return assento in self.assentos
        def obter_assentos(self): return self.assentos
    
    class UsuarioMock:
        def __init__(self): self.cpf = "123.456.789-00"
        def criar_reserva(self, voo_id, assento): return True
        def cancelar_reserva(self, voo_id, assento): return True
    
    # Teste rápido
    aviao = AviaoMock()
    usuario = UsuarioMock()
    voo = Voo("V001", aviao, "SP", "RJ", "2024-01-15 08:00")
    
    # Testa tudo em sequência mínima
    print("Assentos inicial:", voo.listar_assentos())
    voo.reservar_assento(usuario, "1A")
    print("Após reserva 1A:", voo.listar_assentos())
    voo.cancelar_reserva(usuario, "1A")
    print("Após cancelamento:", voo.listar_assentos())
    print("Serialização:", voo.to_string())
    
    print("=== FIM TESTE ===")
#biblioteca/usuarios.py

import os
from datetime import datetime

class Usuario:
    def __init__(self, cpf: str, nome: str, data_nascimento: str, email: str,senha:str, validar: bool = True):
        self.cpf = self.validar_cpf(cpf) if validar else cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email
        self.senha = senha
        self.reservas = []
        
    @staticmethod
    def validar_cpf(cpf: str) -> str:
        """Validação simplificada: apenas formata e verifica se tem 11 dígitos"""
        cpf_limpo = ''.join(char for char in cpf if char.isdigit())
        
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        
        # Verifica se não é uma sequência repetida (ex: 111.111.111-11)
        if all(digito == cpf_limpo[0] for digito in cpf_limpo):
            raise ValueError("CPF não pode ter todos os dígitos iguais")
    
        # Saída formatada
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    
    def criar_reserva(self, voo_id: str, assento_id: str, assento_info: dict = None):
        # Verificar se já existe reserva ativa neste voo
        for reserva in self.reservas:
            if (reserva['voo_id'] == voo_id and 
                reserva['status'] == 'confirmada'):
                raise ValueError(f"Você já tem uma reserva no voo {voo_id}")
        
        # Verificar regra de idade para assentos de emergência
        is_emergencia = False
        
        if assento_info and 'emergencia' in assento_info:
            is_emergencia = assento_info['emergencia']
        else:
            # Verificar pelo ID do assento (prefixo 'E' ou fileiras de emergência)
            is_emergencia = assento_id.upper().startswith('E')
        
        if is_emergencia and not self.eh_maior_de_idade():
            raise ValueError("Assento de emergência não permitido para menores de 18 anos")
        
        # Verificar se já existe reserva ativa para este assento
        for reserva in self.reservas:
            if (reserva['voo_id'] == voo_id and 
                reserva['assento_id'] == assento_id and 
                reserva['status'] == 'confirmada'):
                raise ValueError(f"Já existe reserva ativa para voo {voo_id}, assento {assento_id}")
        
        # Cria nova reserva
        reserva = {
            'voo_id': voo_id,
            'assento_id': assento_id,
            'assento_info': assento_info,
            'data_reserva': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'status': 'confirmada'
        }
        
        self.reservas.append(reserva)
        return True
        
    def cancelar_reserva(self, voo_id: str, assento_id: str):
        """Cancela uma reserva do usuário"""
        for reserva in self.reservas:
            if (reserva['voo_id'] == voo_id and 
                reserva['assento_id'] == assento_id and 
                reserva['status'] == 'confirmada'):
                
                reserva['status'] = 'cancelada'
                reserva['data_cancelamento'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                return True
        
        raise ValueError(f"Reserva não encontrada para Voo: {voo_id}, Assento: {assento_id}")
    
    def modificar_reserva(self, voo_id_antigo: str, assento_id_antigo: str, 
                         voo_id_novo: str, assento_id_novo: str, assento_info_novo: dict = None):
        """Modifica uma reserva existente"""
        self.cancelar_reserva(voo_id_antigo, assento_id_antigo)
        self.criar_reserva(voo_id_novo, assento_id_novo, assento_info_novo)
        return True

    def calcular_idade(self) -> int:
        """Calcula a idade do usuário"""
        partes_data = self.data_nascimento.split('/')
        if len(partes_data) != 3:
            raise ValueError("Data de nascimento deve estar no formato DD/MM/AAAA")
        
        try:
            dia = int(partes_data[0])
            mes = int(partes_data[1])
            ano = int(partes_data[2])
        except ValueError:
            raise ValueError("Data de nascimento deve conter apenas números")
        
        hoje = datetime.now()
        idade = hoje.year - ano
        
        if (hoje.month, hoje.day) < (mes, dia):
            idade -= 1
            
        if idade < 0:
            raise ValueError("Data de nascimento não pode ser no futuro")
            
        return idade

    def eh_maior_de_idade(self) -> bool:
        """Retorna True se o usuário tiver 18 anos ou mais"""
        return self.calcular_idade() >= 18

def carregar_usuarios() -> list:
    """Carrega usuários do arquivo texto"""
    usuarios = []
    
    try:
        with open('dados/usuarios.txt', 'r', encoding='utf-8') as file:
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
                        
                        # Carregar reservas se existirem
                        if len(partes) > 5 and partes[5]:
                            for reserva_str in partes[5].split(','):
                                if '-' in reserva_str:
                                    voo_id, assento_id = reserva_str.split('-', 1)
                                    usuario.reservas.append({
                                        'voo_id': voo_id,
                                        'assento_id': assento_id,
                                        'status': 'confirmada',
                                        'data_reserva': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                    })
                        
                        usuarios.append(usuario)
                        
    except FileNotFoundError:
        return []
    
    return usuarios

def salvar_usuarios(usuarios: list):
    """Salva lista de usuários no arquivo texto"""
    try:
        with open('dados/usuarios.txt', 'a'):
            pass
    except FileNotFoundError:
        os.makedirs('dados', exist_ok=True)
    
    with open('dados/usuarios.txt', 'w', encoding='utf-8') as file:
        for usuario in usuarios:
            reservas_str = ','.join([
                f"{r['voo_id']}-{r['assento_id']}"
                for r in usuario.reservas
                if r.get('status') == 'confirmada'
                ])
            linha = f"{usuario.cpf};{usuario.nome};{usuario.data_nascimento};{usuario.email};{usuario.senha};{reservas_str}\n"
            file.write(linha)


def salvar_usuario_unico(novo_usuario: Usuario):
    """Adiciona um novo usuário ao arquivo, se ainda não existir."""
    os.makedirs('dados', exist_ok=True)
    caminho = 'dados/usuarios.txt'

    # Garante que o arquivo existe
    if not os.path.exists(caminho):
        with open(caminho, 'w', encoding='utf-8') as f:
            pass

    # Verifica duplicidade de CPF
    usuarios_existentes = carregar_usuarios()
    for u in usuarios_existentes:
        if u.cpf == novo_usuario.cpf:
            raise ValueError(f"O usuário com CPF {u.cpf} já está cadastrado.")

    # Serializa o novo usuário
    reservas_str = ','.join([
        f"{r['voo_id']}-{r['assento_id']}"
        for r in novo_usuario.reservas
        if r.get('status') == 'confirmada'
    ])
    
    linha = f"{novo_usuario.cpf};{novo_usuario.nome};{novo_usuario.data_nascimento};{novo_usuario.email};{novo_usuario.senha}\n"

    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(linha)
# biblioteca/avioes.py
class Aviao:
    def __init__(self, aviao_id: str, modelo: str, fileiras: int, assentos_por_fileira: int):
        self.aviao_id = aviao_id
        self.modelo = modelo
        self.fileiras = fileiras
        self.assentos_por_fileira = assentos_por_fileira
    
    def gerar_layout(self) -> dict:
        """
        Gera o layout de assentos conforme especificação da AD1.
        Retorna dicionário onde chaves são assentos (ex: "1A", "30F") e valores
        são dicionários com "posicao", "classe", "emergencia", "valor" e "bloqueado".
        """
        layout = {}
        letras = [chr(65 + i) for i in range(self.assentos_por_fileira)]
        
        # Definir assentos de emergência (fileiras 1, 15 e 30, assentos das extremidades)
        assentos_emergencia = []
        for fileira_emergencia in [1, 15, 30]:
            if fileira_emergencia <= self.fileiras:
                assentos_emergencia.append(f"{fileira_emergencia}{letras[0]}")  # Primeira letra (A)
                assentos_emergencia.append(f"{fileira_emergencia}{letras[-1]}")  # Última letra (F)
        
        for fileira in range(1, self.fileiras + 1):
            for letra in letras:
                assento_id = f"{fileira}{letra}"
                
                # Definir posição conforme regras da AD1
                if letra == letras[0] or letra == letras[-1]:
                    posicao = "janela"
                elif letra == letras[1] or letra == letras[-2]:
                    posicao = "meio"
                else:
                    posicao = "corredor"
                
                # Definir classe conforme fileira (exemplo da AD1)
                if fileira <= 5:
                    classe = "primeira"
                    valor = 500.00
                elif fileira <= 10:
                    classe = "executiva"
                    valor = 300.00
                else:
                    classe = "econômica"
                    valor = 150.00
                
                # Verificar se é assento de emergência
                emergencia = assento_id in assentos_emergencia
                
                layout[assento_id] = {
                    "posicao": posicao,
                    "classe": classe,
                    "emergencia": emergencia,
                    "valor": valor,
                    "bloqueado": False  # Por padrão, não bloqueado
                }
        
        return layout
    
    def validar_assento(self, assento_id: str) -> bool:
        """Valida se um assento existe no layout do avião"""
        return assento_id in self.gerar_layout()


def carregar_avioes(arquivo: str = "dados/avioes.txt") -> list:
    """Carrega aviões do arquivo texto no formato especificado"""
    avioes = []
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) == 4:
                        aviao_id, modelo, fileiras, assentos_por_fileira = partes
                        aviao = Aviao(
                            aviao_id=aviao_id,
                            modelo=modelo,
                            fileiras=int(fileiras),
                            assentos_por_fileira=int(assentos_por_fileira)
                        )
                        avioes.append(aviao)
    except FileNotFoundError:
        # Arquivo não existe, retorna lista vazia
        return []
    
    return avioes


def salvar_avioes(avioes: list, arquivo: str = "dados/avioes_teste.txt"):
    # importante para testagem
    """Salva lista de aviões em arquivo texto no formato especificado"""
    with open(arquivo, 'w', encoding='utf-8') as f:
        for aviao in avioes:
            linha = f"{aviao.aviao_id};{aviao.modelo};{aviao.fileiras};{aviao.assentos_por_fileira}\n"
            f.write(linha)
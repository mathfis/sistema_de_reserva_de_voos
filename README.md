# ✈️ Sistema de Reserva de Voos
AD1 – Programação com Interfaces Gráficas (PIG) – 2025.2

Instituição: Fundação CECIERJ / Consórcio CEDERJ
Curso: Tecnologia em Sistemas de Computação
Disciplina: Programação com Interfaces Gráficas (EAD05030)
_____________
## 📘 Visão Geral

Este projeto implementa um sistema de reservas de assentos em voos comerciais, utilizando programação orientada a objetos em Python.
Na AD1, foi desenvolvido o backend completo, com persistência em arquivos texto e interface em linha de comando (CLI).
Na AD2, este sistema servirá como base para o desenvolvimento da interface gráfica (frontend) usando tkinter.

## Estrutura do Projeto

```graphql
AD1_PIG_2025-2/
│
├── biblioteca/
│   ├── __pycache__/              # Cache automático do Python
│   ├── avioes.py                 # Classe Aviao + funções de persistência
│   ├── usuarios.py               # Classe Usuario + regras de reserva e idade
│   └── voos.py                   # Classes Voo e GerenciadorVoos
│
├── dados/
│   ├── avioes.txt                # Banco de dados de aeronaves
│   ├── usuarios.txt              # Banco de dados de passageiros
│   └── voos.txt                  # Banco de dados de voos
│
├── cli_simulada.py               # Simulação automatizada de uso do sistema
├── main.py                       # Interface CLI interativa (menu principal)
├── explicacao_do_projeto.txt     # Documento descritivo das classes e lógica
└── README.md                     # (este arquivo)
```
## ⚙️ Execução
### 🔹 Requisitos

Python 3.8 ou superior

Sistema operacional Linux (recomendado) ou Windows

Nenhuma dependência externa (usa apenas módulos padrão do Python)

### 🔹 Execução Interativa (CLI)

Para usar o sistema manualmente, execute:

```bash
python main.py
```
O programa exibirá o menu principal com as opções de:

- Cadastro de usuário;
- Login;
- Visualização de voos e assentos;
- Reserva, cancelamento e modificação de assentos.

### 🔹 Execução Automática (Simulada)

Para testar o sistema de ponta a ponta:

```bash
python cli_simulada.py
```
A simulação executa automaticamente:

1. Criação de usuários

2. Criação de aviões e voos

3. Teste de login e regras de idade

4. Visualização de layout

5. Reserva e cancelamento de assentos

6. Modificação de reserva

7. Relatório final de status

## 🧠 Principais Componentes
### ✈️ Aviao – (arquivo biblioteca/avioes.py)

- Representa uma aeronave e gera o layout completo de assentos.
- Gera posições, classes e valores automaticamente.
- Define assentos de emergência e bloqueios.
- Valida existência de assentos.
- Permite salvar e carregar lista de aviões em arquivo texto.

### 👤 Usuario – (arquivo biblioteca/usuarios.py)

- Modela um passageiro e suas reservas.
- Valida CPF e idade.
- Cria, modifica e cancela reservas.
- Impede menores de 18 anos de ocuparem assentos de emergência.
- Armazena reservas persistentes em dados/usuarios.txt.

### 🛫 Voo – (arquivo biblioteca/voos.py)

- Gerencia um voo individual e suas reservas.
- Valida assentos e controla status (livre/reservado).
- Associa cada reserva a um usuário (CPF).
- Possui serialização e leitura de arquivo texto.

###📋 GerenciadorVoos

- Gerencia a coleção completa de voos.
- Carrega e salva voos com controle de concorrência (.lock).
- Permite buscar, adicionar e listar voos.

### 💻 main.py

- Interface principal em linha de comando.
- Exibe menus interativos.
- Executa todas as operações do sistema.

    É o ponto de entrada principal do programa.

### 🔁 cli_simulada.py

- Executa um teste automatizado de ponta a ponta do sistema.
    Serve para validar a consistência da lógica antes da integração com o frontend Tkinter.

### 💾 Estrutura dos Arquivos de Dados
| Arquivo          | Formato                                         | Exemplo                                                       |
| ---------------- | ----------------------------------------------- | ------------------------------------------------------------- |
| **avioes.txt**   | `aviao_id;modelo;fileiras;assentos_por_fileira` | `BOEING-001;B737;30;6`                                        |
| **voos.txt**     | `voo_id;aviao_id;origem;destino;data_hora`      | `V001;BOEING-001;São Paulo;Rio de Janeiro;2024-03-15 08:00`   |
| **usuarios.txt** | `cpf;nome;data_nascimento;email;reservas`       | `529.982.247-25;João Silva;15/05/1990;joao@email.com;V001-7C` |

    As reservas são armazenadas como pares voo_id-assento, separados por vírgulas.

### 🧱 Organização por Camadas

| Camada                | Responsável             | Arquivos                     |
| --------------------- | ----------------------- | ---------------------------- |
| **Interface (CLI)**   | Interação com o usuário | `main.py`, `cli_simulada.py` |
| **Lógica de Negócio** | Regras e operações      | `biblioteca/*.py`            |
| **Persistência**      | Armazenamento em texto  | `dados/*.txt`                |


## 🚀 Próximos Passos (AD2)

Na AD2, será implementada uma interface gráfica (Tkinter) conectada diretamente às funções e classes existentes:

- Reutilizar Usuario, Aviao, Voo e GerenciadorVoos.
- Manter os arquivos de dados .txt como base de persistência.
- Implementar as telas:
- Login / Cadastro
- Painel do usuário
- Seleção de voo e assento
- Confirmação de pagamento

## 🧪 Testes e Validação

Para validar o sistema:
- Execute python cli_simulada.py para rodar todos os testes automáticos.
- Verifique a saída final de “SIMULAÇÃO CONCLUÍDA!” sem erros.

## 🧑‍💻 Autoria e Contexto

Projeto desenvolvido como parte da avaliação da disciplina Programação com Interfaces Gráficas (EAD05030)
    Professores: Dianne Medeiros e Luís Henrique Costa
    Período: 2º semestre de 2025

Implementação: <b>por Matheus Lara</b>
 [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/laramatheus/) [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mathfis)

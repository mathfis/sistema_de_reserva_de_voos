# ✈️ Sistema de Reserva de Voos
AD2 – Programação com Interfaces Gráficas (PIG) – 2025.2

Instituição: Fundação CECIERJ / Consórcio CEDERJ  
Curso: Tecnologia em Sistemas de Computação  
Disciplina: Programação com Interfaces Gráficas (EAD05030)  
_____________

## 📘 Visão Geral

Este projeto implementa um **sistema de reservas de assentos em voos comerciais**, utilizando **Python e orientação a objetos**.  

Na **AD1**, foi desenvolvido o **backend completo**, com persistência em arquivos texto e interface em linha de comando (CLI).  
Na **AD2**, está sendo implementada a **interface gráfica (frontend)** em **Tkinter**, que permitirá ao usuário interagir visualmente com o sistema.

---

## 💡 Estágio Atual (AD2)

O sistema gráfico está **100% operacional** — já é possível **navegar entre as telas principais** e validar os **fluxos visuais**.  
Nenhuma parte ainda acessa o backend, mas toda a estrutura está pronta para receber integração.

### 🧭 Estrutura atual

```graphql
App (tk.Tk)
│
├── TelaLogin
│ ├── Campo CPF
│ ├── Campo Senha
│ ├── Botões: Entrar / Cadastrar
│
├── TelaCadastro
│ ├── Campos: CPF, Nome, Data, Email
│ ├── Botões: Salvar / Voltar
│
└── TelaPainel
├── Botões: Visualizar Voos / Minhas Reservas / Sair
```

### 🖼️ Fluxo de Navegação

```shell
[ TelaLogin ]
↓
[ TelaCadastro ] ←→ [ TelaPainel ]
```

---

## ✈️ Próximas Etapas (Planejamento de Implementação)

| Etapa | Tarefa | Backend Necessário? | Descrição |
|-------|---------|----------------------|------------|
| 2 | ✅ Autenticação real de usuário | ✅ | Ler `dados/usuarios.txt`, verificar CPF com `carregar_usuarios()` e permitir login real. |
| 3 | ✅ Cadastro real de novo usuário | ✅ | Criar novo `Usuario`, validar CPF e salvar com `salvar_usuarios()`. |
| 4 | 🛫 Tela de seleção de voos | ✅ | Listar voos de `GerenciadorVoos.listar_voos()` e exibir dados (origem, destino, data). |
| 5 | 💺 Tela de seleção de assentos | ✅ | Exibir layout do avião (`Aviao.gerar_layout()`), colorindo por status (livre/reservado/emergência). |
| 6 | 💳 Tela de confirmação de reserva | ✅ | Mostrar resumo (voo + assento + valor) e confirmar reserva (`Usuario.criar_reserva()` + `Voo.reservar_assento()`). |
| 7 | 📋 Tela “Minhas Reservas” | ✅ | Exibir reservas do usuário logado e permitir cancelar/modificar (`Usuario.cancelar_reserva()`). |
| 8 | 🎨 Refinamento visual | ❌ | Ajustar layout, cores, ícones e responsividade. |
| 9 | 🧪 Testes e Validação | ❌ | Testar fluxos (login, reserva, cancelamento, etc.). |

---

## 📊 Mapa de Progresso

| Categoria | Progresso |
|------------|------------|
| Estrutura base (Tkinter + navegação) | 🟢 100% |
| Login e cadastro visuais | 🟢 100% |
| Integração com backend (usuário, voos, assentos) | 🟡 0% |
| Layout visual de assentos | ⚪ 0% |
| Confirmação e persistência | ⚪ 0% |
| Testes e ajustes finais | ⚪ 0% |

---

## 🧩 Estrutura Final Planejada
```graphql
App (tk.Tk)
│
├── TelaLogin → autenticação via carregar_usuarios()
├── TelaCadastro → criação via salvar_usuarios()
├── TelaPainel → acesso a TelaVoos / TelaReservas
│
├── TelaVoos
│ ├── Lista de voos (origem, destino, data)
│ └── Seleção → TelaAssentos
│
├── TelaAssentos
│ ├── Layout visual (grid de botões)
│ ├── Cores: verde=livre, vermelho=ocupado, amarelo=emergência
│ └── Selecionar assento → TelaPagamento
│
├── TelaPagamento
│ ├── Resumo (voo + assento + valor)
│ └── Confirmação → salvar reserva
│
└── TelaReservas
├── Listagem de reservas do usuário
└── Cancelar / Alterar assento
```

---

## 🧱 Estrutura do Projeto (Backend + Frontend)

```graphql
sistema_de_reserva_de_voos/
│
├── biblioteca/
│   ├── avioes.py
│   ├── usuarios.py
│   └── voos.py
│
├── dados/
│   ├── avioes.txt
│   ├── usuarios.txt
│   └── voos.txt
│
├── cli_simulada.py 
├── main.py                 # CLI (AD1)
├── main_gui.py             # GUI (Tkinter – AD2)
└── README.md
```

## ⚙️ Execução (na CLI)

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

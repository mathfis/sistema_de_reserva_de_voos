# ROTEIRO DE TESTE FRONTEND
Checklist de Teste da Interface Gráfica

## 📋 PRÉ-REQUISITOS

- Python 3.8+ instalado

- Todos os arquivos do projeto na mesma pasta

- Arquivos de dados iniciais na pasta dados/

- Nenhum processo do sistema em execução

## 🔐 TESTE 1: FLUXO DE LOGIN E CADASTRO
### 1.1 Cadastro de Novo Usuário
- Executar: python main_gui.py

- Clicar em "Cadastrar"

- Preencher formulário com dados válidos:
```
    CPF: 333.444.555-66

    Nome: Ana Teste

    Data Nascimento: 25/12/1988

    Email: ana.teste@email.com

    Senha: teste123
```

- Clicar "Salvar Cadastro"

*VERIFICAR: Mensagem de sucesso e redirecionamento para login*

### 1.2 Tentativa de Cadastro com CPF Existente
- Repetir cadastro com mesmo CPF

*VERIFICAR: Mensagem de erro "CPF já cadastrado"*

###  1.3 Login Válido

- No login, inserir 
```
CPF: 333.444.555-66

Senha: teste123
```

- Clicar "Entrar"

*VERIFICAR: Acesso ao Painel do Usuário com informações corretas*

### 1.4 Login com Senha Incorreta

- Usar CPF correto com senha errada

*VERIFICAR: Mensagem de erro específica sobre senha*

*VERIFICAR: Campo senha limpo, campo CPF mantido*

###  1.5 Login com CPF Inexistente
- Usar CPF não cadastrado:
```
CPF: 999.888.777-66
```
*VERIFICAR: Mensagem sugerindo cadastro*

## 🏠 TESTE 2: PAINEL DO USUÁRIO
### 2.1 Informações do Usuário
- Fazer login com usuário cadastrado

*VERIFICAR: Nome, CPF e email exibidos corretamente*

*VERIFICAR: Lista de reservas vazia (para novo usuário)*

### 2.2 Navegação do Painel

- Clicar "Visualizar Voos"

*VERIFICAR: Tela de voos carrega*

- Voltar ao Painel

- Clicar "Minhas Reservas"

*VERIFICAR: Janela de reservas abre*

- Fechar janela de reservas

- Clicar "Sair"
*VERIFICAR: Retorno à tela de login*

## ✈️ TESTE 3: SELEÇÃO DE VOOS
### 3.1 Listagem de Voos

- Acessar "Visualizar Voos"

*VERIFICAR: Lista com todos os voos disponíveis*

*VERIFICAR: Colunas: Voo, Origem, Destino, Data/Hora, Avião, Ação*

## 3.2 Seleção de Voo
- Clicar "Selecionar" em qualquer voo

*VERIFICAR: Mensagem informativa sobre voo selecionado*

*VERIFICAR: Navegação automática para tela de assentos*

## 💺 TESTE 4: SELEÇÃO DE ASSENTOS
### 4.1 Visualização do Layout

*VERIFICAR: Informações do voo exibidas no topo*

*VERIFICAR: Grade de assentos organizada por fileiras*

*VERIFICAR: Legenda de cores compreensível*

*VERIFICAR: Scroll funcionando para muitos assentos*

### 4.2 Estados dos Assentos
*IDENTIFICAR: Assentos livres (verdes)*

*IDENTIFICAR: Assentos de emergência (laranja)*

*VERIFICAR: Assentos bloqueados (cinza) não clicáveis*

### 4.3 Seleção de Assento Válido
- Clicar em assento livre verde

*VERIFICAR: Botão "Confirmar Reserva" habilita*

*VERIFICAR: Status atualizado "Assento selecionado: X"*

## ✅ TESTE 5: RESERVA E CONFIRMAÇÃO
### 5.1 Confirmação de Reserva
- Com assento selecionado, clicar "Confirmar Reserva"

*VERIFICAR: Mensagem de sucesso com detalhes*

*VERIFICAR: Botão "Confirmar" desabilita*

*VERIFICAR: Assento muda para estado ocupado*

### 5.2 Verificação no Painel
- Voltar ao Painel do Usuário

*VERIFICAR: Reserva aparece na lista "Minhas Reservas"*

- Clicar "Minhas Reservas"

*VERIFICAR: Reserva listada com informações completas*

## 🚫 TESTE 6: CANCELAMENTO DE RESERVA
### 6.1 Cancelamento via Painel
- Na janela "Minhas Reservas", clicar "Cancelar" na reserva

*VERIFICAR: Confirmação de cancelamento*

- Confirmar cancelamento

*VERIFICAR: Mensagem de sucesso*

*VERIFICAR: Reserva removida da lista*

### 6.2 Verificação de Disponibilidade
- Voltar para seleção de assentos no mesmo voo

*VERIFICAR: Assento cancelado agora aparece como livre*

## 🔒 TESTE 7: VALIDAÇÕES E RESTRIÇÕES
### 7.1 Menor em Assento de Emergência
- Fazer login com usuário menor de idade (Maria Santos)

- Tentar reservar assento de emergência (1A, 1F, 15A, 15F, 30A, 30F)

*VERIFICAR: Mensagem de erro específica sobre idade*

### 7.2 Dupla Reserva no Mesmo Voo
- Com usuário logado, fazer uma reserva

- Tentar fazer segunda reserva no mesmo voo

*VERIFICAR: Mensagem de erro sobre limite de uma reserva por voo*

### 7.3 Assento Já Ocupado
- Com dois usuários diferentes, tentar reservar mesmo assento

*VERIFICAR: Segundo usuário recebe mensagem de assento indisponível*

## 🔄 TESTE 8: PERSISTÊNCIA DE DADOS
### 8.1 Persistência entre Sessões
- Fazer reservas com um usuário

- Fechar completamente a aplicação

- Reabrir aplicação e fazer login com mesmo usuário

*VERIFICAR: Reservas mantidas no painel*

### 8.2 Consistência de Dados
- Abrir arquivo usuarios.txt

*VERIFICAR: Reservas salvas no formato correto*

- Abrir arquivo voos.txt

*VERIFICAR: Reservas refletidas nos voos*

## 📱 TESTE 9: USABILIDADE E EXPERIÊNCIA
###  9.1 Navegação Intuitiva
*VERIFICAR: Fluxo lógico entre telas*

*VERIFICAR: Botões de navegação sempre visíveis*

*VERIFICAR: Feedback visual para todas as ações*

### 9.2 Mensagens ao Usuário
*VERIFICAR: Mensagens de erro claras e específicas*

*VERIFICAR: Mensagens de sucesso informativas*

*VERIFICAR: Confirmações para ações destrutivas*

### 9.3 Responsividade
- Redimensionar janela durante operação

*VERIFICAR: Layout se adapta corretamente*

*VERIFICAR: Scrollbars funcionam quando necessário*

## 🧪 TESTE 10: CASOS DE ERRO E RECUPERAÇÃO
### 10.1 Arquivos Corrompidos
- Corromper arquivo voos.txt (adicionar linha inválida)

- Iniciar aplicação

*VERIFICAR: Aplicação não crasha, erro tratado graciosamente*

### 10.2 Dados Inconsistentes
- Remover arquivo avioes.txt

- Iniciar aplicação

*VERIFICAR: Mensagem de erro apropriada*

*VERIFICAR: Funcionalidades não dependentes continuam*


# Autoria

Matheus Lara
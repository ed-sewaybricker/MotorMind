# MotorMind 🚗⚙️

Sistema de gerenciamento de motores desenvolvido com Django.

O objetivo do sistema é permitir o controle de inventário de motores, inspeções técnicas e administração de usuários, garantindo organização, rastreabilidade e controle operacional.

---

## 📌 Funcionalidades

### 👤 Autenticação
- Login com matrícula e senha
- Logout seguro
- Sistema de senha temporária (obrigação de troca no primeiro acesso ou reset)

---

### 🏭 Inventário de Motores
- Cadastro de motores com:
  - Modelo
  - Potência
  - Tensão
  - Corrente
  - RPM
  - Modo de fixação
  - Quantidade em estoque
- Edição e exclusão (admin)
- Visualização detalhada em modal
- Controle de quantidade com validação (não permite valores negativos)

---

### 🔍 Inspeções
- Criação de inspeções por administradores
- Atribuição de responsáveis
- Status:
  - PENDENTE
  - EM ANDAMENTO
  - CONCLUÍDO
- Funcionário pode:
  - Iniciar inspeção
  - Concluir inspeção
- Controle de acesso por permissão

---

### 🧑‍💼 Administração
- Cadastro de usuários
- Edição e remoção de usuários
- Promoção para administrador
- Reset de senha pelo administrador

---

## 🔐 Controle de Acesso

O sistema possui dois níveis principais:

- **Administrador (is_staff = True)**
  - Gerencia usuários
  - Gerencia motores
  - Cria inspeções

- **Funcionário**
  - Visualiza inventário
  - Gerencia suas inspeções atribuídas

---

## ⚙️ Tecnologias Utilizadas

- Python 3
- Django
- SQLite (banco de dados padrão)
- Bootstrap 5
- HTML5 + CSS3
- JavaScript (básico para UI)

---

## 🚀 Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/ed-sewaybricker/MotorMind.git
cd MotorMind
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

Ativar o ambiente:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar superusuário

```bash
python manage.py createsuperuser
```

### 6. Executar servidor

```bash
python manage.py runserver
```

Acesse no navegador: http://127.0.0.1:8000/

## 🔐 Regras importantes do sistema

- Quantidade de motores não pode ser negativa (validação no backend)
- Funcionários só podem interagir com suas próprias inspeções
- Apenas administradores podem criar/editar/excluir motores e usuários
- Inspeções seguem fluxo:
  - PENDENTE → EM ANDAMENTO → CONCLUÍDO
- Senha temporária força troca obrigatória no primeiro acesso

## 📁 Estrutura do projeto

```plaintext
projects/
│
├── models.py
├── views.py
├── urls.py
├── templates/
│   ├── dashboard.html
│   ├── inventario.html
│   ├── inspecoes.html
│   ├── login.html
│   └── administrador.html
│
├── manage.py
```

## 👨‍💻 Autores
Projeto desenvolvido por Eduardo Sewaybricker Zambreto Paixão, Jonathan Alisson Dos Santos, Matheus Dos Reis Pinto, Bruno Camargo Rosa, Felipe Yuji Yamada, Marcelo Diogo Gonsalez, Jhonatan David Arcanjo Da Silva e Matheus Augusto Alves

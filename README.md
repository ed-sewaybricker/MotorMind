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

O sistema possui três níveis principais:

- **Administrador**
  - Controle total do sistema

- **Staff**
  - Gerenciamento operacional
  - Usuários comuns
  - Inventário
  - Inspeções

- **Funcionário**
  - Visualização do inventário
  - Execução das inspeções atribuídas

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
MotorMind/
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── projects/
│   ├── migrations/
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── filtros.js
│   │
│   ├── templates/
│   │   ├── administrador.html
│   │   ├── alterar_senha.html
│   │   ├── dashboard.html
│   │   ├── inspecoes.html
│   │   ├── inventario.html
│   │   ├── login.html
│   │   └── master.html
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── auth_views.py
│   │   ├── dashboard_views.py
│   │   ├── administrador_views.py
│   │   ├── usuario_views.py
│   │   ├── fabricante_views.py
│   │   ├── tipo_motor_views.py
│   │   ├── local_views.py
│   │   ├── motor_views.py
│   │   └── inspecao_views.py
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── tests.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

### Organização das Views

Para facilitar a manutenção e escalabilidade do sistema, as views foram separadas por responsabilidade:

* `auth_views.py` → autenticação e gerenciamento de sessão
* `dashboard_views.py` → dashboard principal
* `administrador_views.py` → painel administrativo
* `usuario_views.py` → CRUD de usuários
* `fabricante_views.py` → CRUD de fabricantes
* `tipo_motor_views.py` → CRUD de tipos de motor
* `local_views.py` → CRUD de locais
* `motor_views.py` → inventário de motores
* `inspecao_views.py` → gerenciamento de inspeções


## 👨‍💻 Autores
Projeto desenvolvido por Eduardo Sewaybricker Zambreto Paixão, Jonathan Alisson Dos Santos, Matheus Dos Reis Pinto, Bruno Camargo Rosa, Felipe Yuji Yamada, Marcelo Diogo Gonsalez, Jhonatan David Arcanjo Da Silva e Matheus Augusto Alves

# 🏥 Marque_Bem – Sistema de Agendamento de Consultas e Exames

**Marque_Bem** é um sistema web criado com **Flask (Python)** e **SQLAlchemy**, com o objetivo de simular o fluxo de **agendamento de consultas e exames médicos**. O projeto foi desenvolvido como parte de um processo de **aprendizado e prática em desenvolvimento web completo**, incluindo back-end, front-end e banco de dados relacional.

> ⚠️ Este projeto está **em desenvolvimento ativo** e ainda há muito a ser feito. Ele **não está pronto para produção**, mas serve como um exercício prático de construção de aplicações reais com múltiplas tecnologias.

---

## 🎯 Objetivo

O principal objetivo do projeto é servir como uma base de aprendizado para:

- Desenvolvimento de aplicações web completas com **Python e Flask**
- Utilização de **ORM (SQLAlchemy)** para persistência de dados
- HTML, CSS e JavaScript na construção da interface
- Organização de um projeto em múltiplos arquivos e camadas
- Prática com **CRUD**, rotas, templates e formulários
- Futuramente, integrar APIs de notícias de saúde locais

---

## ✅ Funcionalidades Atuais

- Cadastro de exames e consultas médicas
- Listagem de agendamentos
- Edição e exclusão de registros
- Interface básica com HTML e CSS
- Banco de dados com SQLite via SQLAlchemy

---

## 🚧 Funcionalidades em Desenvolvimento

- [ ] Página inicial com resumo das atividades
- [ ] Estilização moderna e responsiva
- [ ] Validação de formulários (cliente e servidor)
- [ ] Sistema de autenticação (login e logout)
- [ ] Painel administrativo
- [ ] Integração com notícias locais da área da saúde
- [ ] Criação de testes automatizados
- [ ] Deploy em ambiente online (Render, Vercel, Heroku)

---

## 🛠️ Tecnologias Utilizadas

| Categoria      | Tecnologias                  |
|----------------|------------------------------|
| Linguagem      | Python 3                     |
| Framework Web  | Flask                        |
| Banco de Dados | SQLite + SQLAlchemy          |
| Front-End      | HTML5, CSS3, JavaScript      |
| Templates      | Jinja2 (com Flask)           |
| Organização    | MVC básico (rotas, modelos)  |

---

## ▶️ Como Executar o Projeto Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/GustavoHolanda16/Marque_Bem.git
cd Marque_Bem

```
### 2. Crie e ative um ambiente virtual 

```bash 
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```
### 3. Execute a aplicação

```bash
flask run
```

Estrutura do Projeto

Marque_Bem/
├── app/
│   ├── static/                   # Arquivos estáticos (CSS, JS)
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   ├── templates/                # Templates HTML (com Jinja2)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── exames.html
│   │   └── cadastrar_exames.html
│   ├── __init__.py               # Inicialização do app Flask
│   ├── routes.py                 # Rotas da aplicação
│   ├── models.py                 # Modelos do banco de dados
│   └── forms.py                  # (Opcional) Lógica de formulários
├── instance/
│   └── database.db               # Banco de dados SQLite
├── run.py                        # Script principal para rodar a aplicação
├── requirements.txt              # Dependências do projeto
└── README.md                     # Este arquivo

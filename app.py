from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Função para criar o banco de dados
def init_sqlite_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            cpf TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao iniciar a aplicação
init_sqlite_db()

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash('Senhas não conferem, tente novamente!', 'error')
            return render_template('cadastro.html')

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (nome, email, cpf, senha) VALUES (?, ?, ?, ?)', (nome, email, cpf, senha))
            conn.commit()
            conn.close()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('O email já está em uso, tente novamente com outro email.', 'error')
            return render_template('cadastro.html')

    return render_template('cadastro.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND senha = ?', (email, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas, tente novamente.', 'error')
            return render_template('login.html')

    return render_template('login.html')

# Rota para a página home (após o login)
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html', nome=session['user_name'])
    else:
        return redirect(url_for('login'))

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sessão.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

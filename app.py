from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela de usuários no SQLite (apenas uma vez)
def create_table():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        cpf TEXT NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

create_table()

# Rota para a página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cpf = request.form['cpf']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('As senhas não coincidem!')
            return redirect(url_for('register'))

        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (name, email, cpf, password) VALUES (?, ?, ?, ?)",
                         (name, email, cpf, password))
            conn.commit()
            conn.close()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Esse email já está cadastrado.')
            return redirect(url_for('register'))
        
    return render_template('register.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            flash('Login realizado com sucesso!')
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas. Tente novamente.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Página home (após login)
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

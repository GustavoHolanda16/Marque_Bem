from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Conexão com o banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criação da tabela de usuários
def create_table_users():
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

# Criação da tabela de exames
def create_table_exames():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS exames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cpf TEXT NOT NULL,
        nome_exame TEXT NOT NULL,
        feito INTEGER NOT NULL,
        resultado INTEGER NOT NULL
    )''')
    conn.commit()
    conn.close()

# Inicialização das tabelas
create_table_users()
create_table_exames()


# Rota padrão que redireciona para o login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Rota para cadastro de usuários
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


# Rota para login de usuários
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


# Rota para página inicial
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


# Rota para exibir os exames cadastrados
@app.route('/exames')
def exames():
    conn = get_db_connection()
    exames = conn.execute('SELECT * FROM exames').fetchall()
    conn.close()
    return render_template('exames.html', exames=exames)


# Rota para cadastrar novos exames
@app.route('/cadastrar_exames', methods=['GET', 'POST'])
def cadastrar_exames():
    if request.method == 'POST':
        name = request.form['name']
        cpf = request.form['cpf']
        nome_exame = request.form['exame']
        feito = 1 if 'feito' in request.form else 0
        resultado = 1 if 'resultado' in request.form else 0

        conn = get_db_connection()
        conn.execute("INSERT INTO exames (name, cpf, nome_exame, feito, resultado) VALUES (?, ?, ?, ?, ?)",
                     (name, cpf, nome_exame, feito, resultado))
        conn.commit()
        conn.close()
        flash('Exame cadastrado com sucesso!')
        return redirect(url_for('exames'))

    return render_template('cadastrar_exames.html')


# Rota para editar exames existentes
@app.route('/editar_exame/<int:id>', methods=['GET', 'POST'])
def editar_exame(id):
    conn = get_db_connection()
    exame = conn.execute('SELECT * FROM exames WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        cpf = request.form['cpf']
        nome_exame = request.form['exame']
        feito = 1 if 'feito' in request.form else 0
        resultado = 1 if 'resultado' in request.form else 0

        conn.execute('''
            UPDATE exames SET name = ?, cpf = ?, nome_exame = ?, feito = ?, resultado = ? WHERE id = ?
        ''', (name, cpf, nome_exame, feito, resultado, id))
        conn.commit()
        conn.close()
        flash('Exame atualizado com sucesso!')
        return redirect(url_for('exames'))

    conn.close()
    return render_template('editar_exame.html', exame=exame)


# Rota para deletar exames
@app.route('/deletar_exame/<int:id>')
def deletar_exame(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM exames WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Exame deletado com sucesso!')
    return redirect(url_for('exames'))


if __name__ == '__main__':
    app.run(debug=True)

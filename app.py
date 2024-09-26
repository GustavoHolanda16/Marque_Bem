from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'uma_chave_secreta_muito_forte'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelos de banco de dados usando SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relacionamento com Exames e Consultas
    exames = db.relationship('Exame', backref='user', lazy=True, cascade="all, delete-orphan")
    consultas = db.relationship('Consulta', backref='user', lazy=True, cascade="all, delete-orphan")

class Exame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    nome_exame = db.Column(db.String(100), nullable=False)
    feito = db.Column(db.Boolean, nullable=False, default=False)
    resultado = db.Column(db.Boolean, nullable=False, default=False)

    # Foreign Key para o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    tipo_consulta = db.Column(db.String(100), nullable=False)
    data_consulta = db.Column(db.String(20), nullable=False)
    realizada = db.Column(db.Boolean, nullable=False, default=False)

    # Foreign Key para o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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
            novo_usuario = User(name=name, email=email, cpf=cpf, password=password)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Esse email já está cadastrado.')
            return redirect(url_for('register'))

    return render_template('register.html')

# Rota para login de usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
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
    user_id = session.get('user_id')
    if user_id is None:
        flash('Você precisa estar logado para ver os exames.')
        return redirect(url_for('login'))

    exames = Exame.query.filter_by(user_id=user_id).all()
    return render_template('exames.html', exames=exames)

# Rota para cadastrar novos exames
@app.route('/cadastrar_exames', methods=['GET', 'POST'])
def cadastrar_exames():
    if request.method == 'POST':
        name = request.form['name']
        cpf = request.form['cpf']
        nome_exame = request.form['exame']
        feito = True if 'feito' in request.form else False
        resultado = True if 'resultado' in request.form else False

        user_id = session.get('user_id')
        if user_id is None:
            flash('Você precisa estar logado para cadastrar um exame.')
            return redirect(url_for('login'))

        novo_exame = Exame(name=name, cpf=cpf, nome_exame=nome_exame, feito=feito, resultado=resultado, user_id=user_id)
        db.session.add(novo_exame)
        db.session.commit()

        flash('Exame cadastrado com sucesso!')
        return redirect(url_for('exames'))

    return render_template('cadastrar_exames.html')

# Rota para exibir as consultas cadastradas
@app.route('/consultas')
def consultas():
    user_id = session.get('user_id')
    if user_id is None:
        flash('Você precisa estar logado para ver as consultas.')
        return redirect(url_for('login'))

    consultas = Consulta.query.filter_by(user_id=user_id).all()
    return render_template('consulta.html', consultas=consultas)

# Rota para cadastrar novas consultas
@app.route('/cadastrar_consultas', methods=['GET', 'POST'])
def cadastrar_consultas():
    if request.method == 'POST':
        name = request.form['name']
        cpf = request.form['cpf']
        tipo_consulta = request.form['consulta']
        data_consulta = request.form['data']
        realizada = True if 'realizada' in request.form else False

        user_id = session.get('user_id')
        if user_id is None:
            flash('Você precisa estar logado para cadastrar uma consulta.')
            return redirect(url_for('login'))

        nova_consulta = Consulta(name=name, cpf=cpf, tipo_consulta=tipo_consulta, data_consulta=data_consulta, realizada=realizada, user_id=user_id)
        db.session.add(nova_consulta)
        db.session.commit()

        flash('Consulta cadastrada com sucesso!')
        return redirect(url_for('consultas'))

    return render_template('marcar_consulta.html')

# Rota para editar exames existentes
@app.route('/editar_exame/<int:id>', methods=['GET', 'POST'])
def editar_exame(id):
    exame = Exame.query.get_or_404(id)

    if request.method == 'POST':
        exame.name = request.form['name']
        exame.cpf = request.form['cpf']
        exame.nome_exame = request.form['exame']
        exame.feito = True if 'feito' in request.form else False
        exame.resultado = True if 'resultado' in request.form else False

        db.session.commit()
        flash('Exame atualizado com sucesso!')
        return redirect(url_for('exames'))

    return render_template('editar_exame.html', exame=exame)

# Rota para deletar exames
@app.route('/deletar_exame/<int:id>')
def deletar_exame(id):
    exame = Exame.query.get_or_404(id)
    db.session.delete(exame)
    db.session.commit()
    flash('Exame deletado com sucesso!')
    return redirect(url_for('exames'))

# Rota para editar consultas existentes
@app.route('/editar_consulta/<int:id>', methods=['GET', 'POST'])
def editar_consulta(id):
    consulta = Consulta.query.get_or_404(id)

    if request.method == 'POST':
        consulta.name = request.form['name']
        consulta.cpf = request.form['cpf']
        consulta.tipo_consulta = request.form['consulta']
        consulta.data_consulta = request.form['data']
        consulta.realizada = True if 'realizada' in request.form else False

        db.session.commit()
        flash('Consulta atualizada com sucesso!')
        return redirect(url_for('consultas'))

    return render_template('editar_consulta.html', consulta=consulta)

# Rota para deletar consultas
@app.route('/deletar_consulta/<int:id>')
def deletar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    flash('Consulta deletada com sucesso!')
    return redirect(url_for('consultas'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.secret_key = 'mi_llave_secreta_super_pro'

# Configuración de la Base de Datos
db_path = os.path.join(os.path.dirname(__file__), 'comunidad.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la tabla
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    comentario = db.Column(db.Text, nullable=False) 

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# RUTAS

@app.route('/')
def index():
    personas = Usuario.query.all()
    # Enviamos los datos a la página
    return render_template('index.html', usuarios=personas)

@app.route('/unirse')
def pantalla_registro():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        nom = request.form.get('nombre')
        ema = request.form.get('email')
        com = request.form.get('comentario')
        
        if nom and ema and com:
            nuevo = Usuario(nombre=nom, email=ema, comentario=com)
            db.session.add(nuevo)
            db.session.commit()
            
            # 2. GUARDAR EN SESIÓN: Guardamos el ID del usuario recién registrado
            session['usuario_id'] = nuevo.id
            session['usuario_nombre'] = nuevo.nombre
            
            print(f"✅ ¡ÉXITO!: Idea de {nom} guardada.")
        else:
            print("⚠️ ADVERTENCIA: Formulario incompleto.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR AL GUARDAR: {e}")
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear() 
    print("👋 Sesión cerrada correctamente.")
    return redirect(url_for('index'))

@app.route('/consultas_admin_secretas')
def consultas():
    personas = Usuario.query.all()
    return render_template('consultas.html', usuarios=personas)

if __name__ == '__main__':
    app.run(debug=True)
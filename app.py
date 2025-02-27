from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://paola:hOGsKdODlZkzPT7s8u5TRugBfIhKhvVp@dpg-cuv3l3qn91rc73dslo8g-a.oregon-postgres.render.com/dbgg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Cliente(db.Model):
    __tablename__ = 'clientes'
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    telefono = db.Column(db.String)
    rfc = db.Column(db.String, primary_key=True)

    def to_dict(self):
        return{
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'telefono': self.telefono,
            'rfc': self.rfc,
        }
#Ruta raiz
@app.route('/')
def index():
    #trae todos los clientes
    clientes = Cliente.query.all()
    return render_template('index.html', clientes = clientes)
#Ruta crear clientes
@app.route('/clientes/new', methods=['GET', 'POST'])
def create_cliente():
    if request.method == 'POST':
        #Agregar cliente
        nombre = request.form['nombre']
        ap_paterno = request.form['ap_paterno']
        ap_materno = request.form['ap_materno']
        telefono = request.form['telefono']
        rfc = request.form['rfc']

        nvo_cliente =Cliente(nombre=nombre, ap_paterno=ap_paterno, ap_materno=ap_materno, telefono=telefono, rfc=rfc)

        db.session.add(nvo_cliente)
        db.session.commit()

        return redirect(url_for('index'))
    
    #Aqui sigue si es GET
    return render_template('create_cliente.html')
#Eliminar Alumno
@app.route('/clientes/delete/<string:rfc>')
def delete_cliente(rfc):
    cliente = Cliente.query.get(rfc)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
    return redirect(url_for('index'))

#Actualizar alumno
@app.route('/clientes/update/<string:rfc>', methods=['GET', 'POST'])
def update_cliente(rfc):
    cliente = Cliente.query.get(rfc)

#Verificar si existe el cliente
    if not cliente:
        return "Cliente no encontrado", 404

    if request.method == 'POST':
        cliente.nombre = request.form.get('nombre', cliente.nombre)
        cliente.ap_paterno = request.form.get('ap_paterno', cliente.ap_paterno)
        cliente.ap_materno = request.form.get('ap_materno', cliente.ap_materno)
        cliente.telefono = request.form.get('telefono', cliente.telefono)
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_cliente.html', cliente=cliente)

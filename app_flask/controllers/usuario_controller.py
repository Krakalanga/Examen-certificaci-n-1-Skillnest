import re
from flask import (
    render_template, request,
    redirect,  Flask, session, flash)
from app_flask.models.usuario import Usuario
from app_flask.models.viaje import Viaje

def rutas_usuario(app):


    @app.route('/registro', methods=['POST'])
    def registrar():
        data = {
            'nombre': request.form.get('nombre', '').strip(),
            'apellido': request.form.get('apellido', '').strip(),
            'email': request.form.get('email', '').strip(),
            'contraseña': request.form.get('contraseña', ''),
            'confirmar_contraseña': request.form.get('confirmar_contraseña', '')
        }

        #validar que no hayan campos vacios
        if not all(data.values()):
            flash('debes rellenar todos los campos!')
            return redirect('/')
        #validar formato email
        patron_email = r'^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$'

        if not re.match(patron_email, data['email']):
            flash('ingresa un correo valido!')
            return redirect('/')
        #validar contraseñas

        if data['contraseña'] != data['confirmar_contraseña']:
            flash('las contraseñas no coinciden')
            return redirect('/')

        #validar longitud contraseña
        if len(data['contraseña']) < 8:
            flash('la contraseña debe contener al menos 8 caracteres por seguridad!')
            return redirect('/')

        #validar que el correo ya este registrado
        if Usuario.buscar_por_email(data):
            flash('este correo ya está registrado!! prueba con otro')
            return redirect('/')
        #eliminar campo de confirmación
        data.pop('confirmar_contraseña')
        Usuario.crear_usuario(data)
        flash('Usuario registrado de manera exitosa!')
        return redirect('/')

    #INICIAR SESION
    @app.route('/login', methods=['POST'])
    def login():

        data = {
            'email': request.form.get('email', '').strip(),
            'contraseña': request.form.get('contraseña', '')
        }

        if not all(data.values()):
            flash('completa todos los campos')
            return redirect('/')
        usuario = Usuario.validar_usuario(data)

        if usuario:

            session.clear()
            session['usuario_id'] = usuario.id
            session['nombre'] = usuario.nombre

            return redirect('/dashboard')
        flash('Correo o contraseña incorrectos! :( ')
        return redirect('/')

    #home
    @app.route('/dashboard')
    def home():
        if 'usuario_id' not in session:
            return redirect('/')

        viajes = Viaje.obtener_todos()

        return render_template('home.html', viajes=viajes)

    #LOGOUT
    @app.route('/logout')
    def logout():
        session.clear()
        flash('sesión cerrada')
        return redirect('/')
    

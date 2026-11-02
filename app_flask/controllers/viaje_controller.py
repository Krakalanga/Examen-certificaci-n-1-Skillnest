
from flask import Blueprint, render_template, request, redirect, flash, session

from app_flask.models.viaje import Viaje
from app_flask.models.viajero import Viajero
from datetime import date

viaje_rutas = Blueprint('viaje', __name__)


# PAGINA PRINCIPAL
@viaje_rutas.route('/home')
def home():
    if 'usuario_id' not in session:
        return redirect('/')

    viajes = Viaje.obtener_todos()

    for viaje in viajes:
        print(viaje.id, viaje.destino, viaje.organizador_id)

    return render_template('home.html', viajes=viajes)


# FORMULARIO CREAR VIAJE
@viaje_rutas.route('/viaje/crear')
def formulario_crear():

    if 'usuario_id' not in session:
        return redirect('/')

    return render_template('crear_viaje.html', hoy=date.today().isoformat())


# CREAR VIAJE
@viaje_rutas.route('/viaje/crear', methods=['POST'])
def crear_viaje():

    if 'usuario_id' not in session:
        return redirect('/')

    data = {
        'destino': request.form.get('destino', '').strip(),
        'fecha_inicio': request.form.get('fecha_inicio', ''),
        'fecha_fin': request.form.get('fecha_fin', ''),
        'itinerario': request.form.get('itinerario', '').strip(),
        'organizador_id': session['usuario_id']
    }

    if not all(data.values()):
        flash('Completa todos los campos')
        return redirect('/viaje/crear')

    if data['fecha_inicio'] < date.today().isoformat():
        flash('La fecha de inicio no puede ser anterior a hoy')
        return redirect('/viaje/crear')

    if data['fecha_fin'] <= data['fecha_inicio']:
        flash('La fecha de finalización debe ser posterior a la de inicio')
        return redirect('/viaje/crear')

    Viaje.crear_viaje(data)

    flash('Viaje creado correctamente')
    return redirect('/home')


# DETALLES DEL VIAJE
@viaje_rutas.route('/viaje/<int:id>')
def detalle_viaje(id):

    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id({'id': id})

    if not viaje:
        flash('Viaje no encontrado')
        return redirect('/home')

    # Obtener participantes del viaje
    viajeros = Viajero.obtener_viajeros({
        'viaje_id': id
    })

    # Comprobar si el usuario actual está inscrito
    inscrito = Viajero.comprobar_union({
        'usuario_id': session['usuario_id'],
        'viaje_id': id
    })

    return render_template(
        'detalle_viaje.html',
        viaje=viaje,
        viajeros=viajeros,
        inscrito=inscrito
    )

# FORMULARIO EDITAR VIAJE
@viaje_rutas.route('/viaje/<int:id>/editar')
def formulario_editar(id):

    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id({'id': id})

    if not viaje:
        return redirect('/home')

    if viaje.organizador_id != session['usuario_id']:
        flash('No tienes permiso para editar este viaje')
        return redirect('/home')

    return render_template('editar_viaje.html', viaje=viaje)


# ACTUALIZAR VIAJE
@viaje_rutas.route('/viaje/<int:id>/editar', methods=['POST'])
def editar_viaje(id):

    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id({'id': id})

    if not viaje or viaje.organizador_id != session['usuario_id']:
        flash('No tienes permiso para realizar esta acción')
        return redirect('/home')

    data = {
        'id': id,
        'destino': request.form.get('destino', '').strip(),
        'fecha_inicio': request.form.get('fecha_inicio', ''),
        'fecha_fin': request.form.get('fecha_fin', ''),
        'itinerario': request.form.get('itinerario', '').strip()
    }

    if not all(data.values()):
        flash('Completa todos los campos')
        return redirect(f'/viaje/{id}/editar')

    if data['fecha_fin'] <= data['fecha_inicio']:
        flash('La fecha de finalización debe ser posterior a la de inicio')
        return redirect(f'/viaje/{id}/editar')

    Viaje.actualizar_viaje(data)

    flash('Viaje actualizado correctamente')
    return redirect(f'/viaje/{id}')


# ELIMINAR VIAJE
@viaje_rutas.route('/viaje/<int:id>/eliminar', methods=['POST'])
def eliminar_viaje(id):

    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id({'id': id})

    if not viaje or viaje.organizador_id != session['usuario_id']:
        flash('No tienes permiso para eliminar este viaje')
        return redirect('/home')

    Viaje.eliminar_viaje({'id': id})

    flash('Viaje eliminado correctamente')
    return redirect('/home')

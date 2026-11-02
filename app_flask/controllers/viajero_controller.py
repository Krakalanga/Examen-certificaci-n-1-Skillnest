
from flask import Blueprint, redirect, flash, session

from app_flask.models.viajero import Viajero
from app_flask.models.viaje import Viaje

viajero_rutas = Blueprint('viajero', __name__)


# UNIRSE A UN VIAJE
@viajero_rutas.route('/viaje/<int:id>/unirse', methods=['POST'])
def unirse(id):

    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id({'id': id})

    if not viaje:
        flash('El viaje no existe')
        return redirect('/home')

    usuario_id = session['usuario_id']

    if viaje.organizador_id == usuario_id:
        flash('Eres el organizador de este viaje')
        return redirect(f'/viaje/{id}')

    data = {
        'usuario_id': usuario_id,
        'viaje_id': id
    }

    if Viajero.comprobar_union(data):
        flash('Ya estás inscrito en este viaje')
        return redirect(f'/viaje/{id}')

    Viajero.unirse_viaje(data)

    flash('Te has unido al viaje correctamente')
    return redirect(f'/viaje/{id}')


# CANCELAR PARTICIPACION
@viajero_rutas.route('/viaje/<int:id>/cancelar', methods=['POST'])
def cancelar(id):

    if 'usuario_id' not in session:
        return redirect('/')

    data = {
        'usuario_id': session['usuario_id'],
        'viaje_id': id
    }

    viaje = Viaje.obtener_por_id({'id': id})

    if not viaje:
        flash('Viaje no encontrado')
        return redirect('/home')

    if viaje.organizador_id == session['usuario_id']:
        flash('El organizador no puede cancelar su propio viaje')
        return redirect(f'/viaje/{id}')

    if not Viajero.comprobar_union(data):
        flash('No estás inscrito en este viaje')
        return redirect(f'/viaje/{id}')

    Viajero.cancelar_union(data)

    flash('Has cancelado tu participación')
    return redirect(f'/viaje/{id}')


# MOSTRAR PARTICIPANTES
@viajero_rutas.route('/viaje/<int:id>/participantes')
def participantes(id):

    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id({'id': id})

    if not viaje:
        flash('Viaje no encontrado')
        return redirect('/home')

    viajeros = Viajero.obtener_viajeros({'viaje_id': id})

    return redirect(f'/viaje/{id}')

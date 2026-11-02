from app_flask.init import app
from flask import render_template
from app_flask.controllers.usuario_controller import rutas_usuario
from app_flask.controllers.viaje_controller import viaje_rutas
from app_flask.controllers.viajero_controller import viajero_rutas

app = app()
rutas_usuario(app)
app.register_blueprint(viaje_rutas)
app.register_blueprint(viajero_rutas)

@app.route('/')
def raiz():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from app_flask.config.mysqlconnection import connectToMySQL

db = 'viajes_usuario'


class Viajero:

    def __init__(self, data):
        self.id = data['id']
        self.usuario_id = data['usuario_id']
        self.viaje_id = data['viaje_id']
        self.fecha_union = data['fecha_union']

    # UNIRSE A UN VIAJE
    @classmethod
    def unirse_viaje(cls, data):

        query = """
            INSERT INTO viajeros (usuario_id, viaje_id)
            VALUES (%(usuario_id)s, %(viaje_id)s)
        """

        return connectToMySQL(db).query_db(query, data)

    # OBTENER VIAJEROS DE UN VIAJE
    @classmethod
    def obtener_viajeros(cls, data):

        query = """
            SELECT usuarios.id, usuarios.nombre, usuarios.apellido,
                   usuarios.email, viajeros.fecha_union
            FROM viajeros
            JOIN usuarios ON viajeros.usuario_id = usuarios.id
            WHERE viajeros.viaje_id = %(viaje_id)s
        """

        return connectToMySQL(db).query_db(query, data)

    # CANCELAR PARTICIPACION
    @classmethod
    def cancelar_union(cls, data):

        query = """
            DELETE FROM viajeros
            WHERE usuario_id = %(usuario_id)s
            AND viaje_id = %(viaje_id)s
        """

        return connectToMySQL(db).query_db(query, data)

    # COMPROBAR SI UN USUARIO ESTA UNIDO
    @classmethod
    def comprobar_union(cls, data):

        query = """
            SELECT *
            FROM viajeros
            WHERE usuario_id = %(usuario_id)s
            AND viaje_id = %(viaje_id)s
        """

        resultado = connectToMySQL(db).query_db(query, data)

        if resultado:
            return cls(resultado[0])

        return None

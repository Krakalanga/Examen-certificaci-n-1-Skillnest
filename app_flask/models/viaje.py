from app_flask.config.mysqlconnection import connectToMySQL

db = 'viajes_usuario'


class Viaje:

    def __init__(self, data):
        self.id = data['id']
        self.destino = data['destino']
        self.fecha_inicio = data['fecha_inicio']
        self.fecha_fin = data['fecha_fin']
        self.itinerario = data['itinerario']
        self.organizador_id = data['organizador_id']
        self.fecha_creacion = data['fecha_creacion']
        self.organizador_nombre = data.get('organizador_nombre', '')
        self.organizador_apellido = data.get('organizador_apellido', '')

    # CREAR VIAJE
    @classmethod
    def crear_viaje(cls, data):

        query = """
            INSERT INTO viajes
            (destino, fecha_inicio, fecha_fin, itinerario, organizador_id)
            VALUES
            (%(destino)s, %(fecha_inicio)s, %(fecha_fin)s,
             %(itinerario)s, %(organizador_id)s)
        """

        return connectToMySQL(db).query_db(query, data)

    # OBTENER TODOS LOS VIAJES
    @classmethod
    def obtener_todos(cls):
        query = """
            SELECT viajes.*,
                usuarios.nombre AS organizador_nombre,
                usuarios.apellido AS organizador_apellido
            FROM viajes
            JOIN usuarios ON viajes.organizador_id = usuarios.id
            ORDER BY viajes.fecha_creacion DESC
        """

        resultados = connectToMySQL(db).query_db(query)

        viajes = []

        if resultados:
            for viaje in resultados:
                viajes.append(cls(viaje))

        return viajes

    # BUSCAR VIAJE POR ID
    @classmethod
    def obtener_por_id(cls, data):

        query = """
            SELECT viajes.*,
                usuarios.nombre AS organizador_nombre,
                usuarios.apellido AS organizador_apellido
            FROM viajes
            JOIN usuarios ON viajes.organizador_id = usuarios.id
            WHERE viajes.id = %(id)s
        """

        resultado = connectToMySQL(db).query_db(query, data)

        if resultado:
            return cls(resultado[0])

        return None

    # ACTUALIZAR VIAJE
    @classmethod
    def actualizar_viaje(cls, data):

        query = """
            UPDATE viajes
            SET destino = %(destino)s,
                fecha_inicio = %(fecha_inicio)s,
                fecha_fin = %(fecha_fin)s,
                itinerario = %(itinerario)s
            WHERE id = %(id)s
        """

        return connectToMySQL(db).query_db(query, data)

    # ELIMINAR VIAJE
    @classmethod
    def eliminar_viaje(cls, data):

        query = """
            DELETE FROM viajes
            WHERE id = %(id)s
        """

        return connectToMySQL(db).query_db(query, data)

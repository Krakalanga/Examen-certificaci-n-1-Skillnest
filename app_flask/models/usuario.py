from app_flask.config.mysqlconnection import connectToMySQL
import bcrypt
db = 'viajes_usuario'

class Usuario():
    def __init__(self, data):
        self.nombre = data['nombre']
        self.id = data['id']
        self.apellido = data['apellido']
        self.email = data['email']
        self.contraseña = data['contraseña']
        self.created_at = data['fecha_registro']
    @classmethod
    def crear_usuario(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, contraseña, fecha_registro)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(contraseña)s, NOW())
        """
        data = data.copy()

        #hasheo de la contraseña

        contraseña = data['contraseña'].encode('utf-8')
        hashed = bcrypt.hashpw(contraseña, bcrypt.gensalt())

        data['contraseña'] = hashed.decode('utf-8')
        mysql = connectToMySQL(db)
        return mysql.query_db(query, data)

    @classmethod
    def buscar_por_email(cls, data):

        query = """
            SELECT * FROM usuarios
            WHERE email = %(email)s
        """

        resultado = connectToMySQL(db).query_db(query, data)

        if resultado:
            return cls(resultado[0])

        return None

    #validar usuario
    @classmethod
    def validar_usuario(cls, data):

        usuario = cls.buscar_por_email(data)

        if usuario:
            contraseña_ingresada = data['contraseña'].encode('utf-8')
            contraseña_hash = usuario.contraseña.encode('utf-8')

            if bcrypt.checkpw(contraseña_ingresada, contraseña_hash):
                return usuario

        return None
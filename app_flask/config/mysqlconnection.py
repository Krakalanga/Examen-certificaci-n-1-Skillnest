import pymysql.cursors 

class MySQLConnection: 
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                                    user = '', 
                                    password = '', # Acá van las credenciales que utilicen
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection
   
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                # En caso de alguna falla, regresa FALSE
                print("Hubo un error :(", e)
                return False
            finally:
                # cerramos conexión
                self.connection.close() 
# connectToMySQL recibe el nombre de la base de datos y genera una instancia de MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
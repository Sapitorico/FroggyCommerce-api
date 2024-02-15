class ModelUser():
    
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
        except Exception as e:
            raise Exception(f"Error al conectar con la base de datos: {str(e)}")
    
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
        except Exception as e:
            raise Exception(f"Error al conectar con la base de datos: {str(e)}")
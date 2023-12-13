import sqlite3
from flask import current_app

def vaciar_tabla():
    conn = None
    try:
        # Conectar a la base de datos
        with current_app.app_context():
            conn = sqlite3.connect(current_app.config['DATABASE'])
            cursor = conn.cursor()

            # Contar el número de registros en la tabla
            cursor.execute('SELECT COUNT(id) FROM clasificaciones')
            contador = cursor.fetchone()[0]

            # Si hay más de 10 registros, eliminar el más antiguo
            if contador > 10:
                cursor.execute('DELETE FROM clasificaciones WHERE id = (SELECT MIN(id) FROM clasificaciones)')

            # Confirmar los cambios
            conn.commit()
    except Exception as e:
        print(f'Ocurrió un error al vaciar la tabla: {e}')
    finally:
        if conn:
            # Cerrar la conexión solo si está definida
            conn.close()

def vaciar_tabla():
    try:
        # Conectar a la base de datos
        with current_app.app_context():
            conn = sqlite3.connect(current_app.config['DATABASE'])
            cursor = conn.cursor()

            # Vaciar la tabla
            cursor.execute('DELETE FROM clasificaciones')

            # Confirmar los cambios y cerrar la conexión
            conn.commit()
    except Exception as e:
        print(f'Ocurrió un error al vaciar la tabla: {e}')
    finally:
        if conn:
            conn.close()



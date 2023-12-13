from flask import render_template, request, redirect, url_for
from app import app
from .sentiment_analysis import analizar_sentimiento
import sqlite3
from .vaciar import vaciar_tabla

app.config['DATABASE'] = 'app/database.db'
# Conexión a la base de datos SQLite
conn = sqlite3.connect('app/database.db', check_same_thread=False)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clasificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL,
        probabilidad REAL NOT NULL,
        sentimiento TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form['texto']
        probabilidades = analizar_sentimiento(texto)
        sentimiento = ["Muy negativo", "Negativo", "Neutral", "Positivo", "Muy positivo"][probabilidades.argmax()]
        probabilidad_porcentaje = round(probabilidades.max().item() * 100, 2)

        # Guardar clasificación en la base de datos
        cursor.execute('INSERT INTO clasificaciones (texto, probabilidad, sentimiento) VALUES (?, ?, ?)',
                       (texto, probabilidad_porcentaje, sentimiento))
        conn.commit()

    # Obtener las últimas 10 clasificaciones
    cursor.execute('SELECT texto, probabilidad, sentimiento FROM clasificaciones ORDER BY id DESC LIMIT 10')
    clasificaciones = cursor.fetchall()

    return render_template('index.html', clasificaciones=clasificaciones)

@app.route('/vaciar', methods=['POST'])
def vaciar():
    vaciar_tabla()
    return redirect(url_for('index'))

@app.route('/vaciar_bd', methods=['POST'])
def vaciar_bd():
    vaciar_tabla()
    return redirect(url_for('index'))  # Redirige a la ruta 'index' después de vaciar la base de datos
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():  # Conectar a la base de datos
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="examen"
    )

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Nombre, Matricula, Edad, Grado FROM listadeestudiantes ORDER BY ID ASC")
    listadeestudiantes = cursor.fetchall()
    conn.close()
    return render_template("index.html", actividades=listadeestudiantes)

@app.route('/add', methods=['POST'])
def add():
    actividad = request.form.get('actividad', '').strip()
    Matricula = request.form.get('matricula', '').strip()
    Edad = request.form.get('edad', '').strip()  # Capturar Edad
    Grado = request.form.get('grado', '').strip()  # Capturar Grado

    if actividad and Matricula and Edad and Grado:  # Validar que no estén vacíos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO listadeestudiantes (Nombre, Matricula, Edad, Grado) VALUES (%s, %s, %s, %s)", 
                       (actividad, Matricula, Edad, Grado))
        conn.commit()
        conn.close()
    
    return redirect('/')

@app.route('/delete/<int:ID>')
def delete(ID):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM listadeestudiantes WHERE ID = %s", (ID,))
    conn.commit()
    
    # Renumerar los IDs
    cursor.execute("SET @count = 0")
    cursor.execute("UPDATE listadeestudiantes SET ID = @count:= @count + 1")
    cursor.execute("ALTER TABLE listadeestudiantes AUTO_INCREMENT = 1")
    conn.commit()
    
    conn.close()
    return redirect('/')

# Actualizar los datos de nombre, matricula, edad y grado
@app.route('/update_actividad/<int:ID>', methods=['POST'])
def update_actividad(ID):
    nuevo_nombre = request.form.get('nuevo_nombre', '').strip()
    nueva_matricula = request.form.get('nueva_matricula', '').strip()
    nueva_edad = request.form.get('nueva_edad', '').strip()  # Capturar nueva Edad
    nuevo_grado = request.form.get('nuevo_grado', '').strip()  # Capturar nuevo Grado

    if not nuevo_nombre or not nueva_matricula or not nueva_edad or not nuevo_grado:
        return redirect('/')  # Redirigir si falta algún campo

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE listadeestudiantes SET Nombre = %s, Matricula = %s, Edad = %s, Grado = %s WHERE ID = %s", 
                   (nuevo_nombre, nueva_matricula, nueva_edad, nuevo_grado, ID))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

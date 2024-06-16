from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='tg',
            passwd='tg',
            database='dev_testeos'
        )
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute('SELECT p.nombre_completo, ss.dni, ss.empresa, ss.puesto  FROM seguridad_social ss left join poblacion p on ss.dni = p.dni;')
            empleados = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('index.html', empleados=empleados)
        except Error as e:
            print(f"SQL Error: {e}")
            cur.close()
            conn.close()
            return "Error fetching data"
    else:
        return "Database connection failed"

@app.route('/update/<dni>', methods=['GET', 'POST'])
@app.route('/update/<dni>', methods=['GET', 'POST'])
def update(dni):
    if request.method == 'POST':
        cuantia = request.form['cuantia']
        conn = get_db_connection()
        if conn is not None:
            cur = conn.cursor()
            try:
                # Asegúrate de que la consulta SQL está correctamente formada
                cur.execute('UPDATE banco_social SET cuantia = cuantia + %s WHERE dni = %s;', (float(cuantia), dni))
                conn.commit()
                return redirect(url_for('index'))
            except Error as e:
                print(f"SQL Update Error: {e}")
                return f"Error updating data for DNI {dni}"
            finally:
                cur.close()
                conn.close()
        else:
            return "Database connection failed for update"
    else:
        # Renderiza la plantilla para el método GET, permitiendo ingresar una nueva cuantía
        return render_template('update.html', dni=dni)


if __name__ == '__main__':
    app.run(debug=True)

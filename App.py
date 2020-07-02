from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)


# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)


# Settings
app.secret_key = 'mysecretkey'


# INDEX
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    # print(data) # Impresion de la tupla
    return render_template('index.html', contacts=data)


# ADD CONTACT
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        matricula = request.form['matricula']
        edad = request.form['edad']

        # ESTABLECER CONEXION
        cur = mysql.connection.cursor()

        # CONSULTA
        cur.execute(
            'INSERT INTO contacts (fullname, phone, email, matricula, edad) VALUES (%s, %s, %s, %s, %s)', (fullname, phone, email, matricula, edad))
        
        # EJECUTAR CONSULTA
        mysql.connection.commit()

        # Mensaje entre ventanas
        flash('Contact Added Successfully')

        # Retorno a la misma pagina
        return redirect(url_for('Index'))


# EDIT CONTACT
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact=data[0])


# UPDATE CONTACT
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))


# DELETE CONTACT
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


# ONLINE DEBUG SERVER
if __name__ == '__main__':
    app.run(port=5000, debug=True)


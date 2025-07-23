from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'same_random_data'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'books'

mysql = MySQL(app)

@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books_and_novels")
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('index.html', books=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        Book_name = request.form['Book_name']
        Genre = request.form['Genre']
        Quantity = request.form['Quantity']
        Price = request.form['Price']
       
        cursor = mysql.connection.cursor()
        cursor.execute("""INSERT INTO books_and_novels(Book_name, Genre, Quantity, Price)
                        VALUES(%s, %s, %s, %s)
        """,(Book_name, Genre, Quantity, Price))
        mysql.connection.commit()
        flash("Successfully Added Book")
        return redirect(url_for('Index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        Book_name = request.form['Book_name']
        Genre = request.form['Genre']
        Quantity = request.form['Quantity']
        Price = request.form['Price']
        

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE books_and_novels
            SET Book_name=%s, Genre=%s, Quantity=%s, Price=%s WHERE id=%s
        """, (Book_name, Genre, Quantity, Price, id_data))
        mysql.connection.commit()
        flash("Book/Novel Updated Successfully!")
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM books_and_novels WHERE id = %s", (id_data,))
    mysql.connection.commit()
    flash("Book/Novel Deleted Successfully!")
    return redirect(url_for('Index'))

    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
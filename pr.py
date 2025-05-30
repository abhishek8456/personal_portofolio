from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'publication_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect('/submit')

@app.route('/submit', methods=['GET', 'POST'])
def submit_publication():
    if request.method == 'POST':
        data = (
            request.form['faculty_name'],
            request.form['department'],
            request.form['title'],
            request.form['pub_type'],
            request.form['publisher'],
            request.form['publication_year'],
            request.form['doi_or_link']
        )
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO publications (
                faculty_name, department, title, pub_type, 
                publisher, publication_year, doi_or_link
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, data)
        mysql.connection.commit()
        return redirect('/view')
    return render_template('submit_publication.html')

@app.route('/view')
def view_publications():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM publications ORDER BY submitted_on DESC")
    records = cur.fetchall()
    return render_template('view_publications.html', records=records)

@app.route('/admin')
def admin_dashboard():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM publications
        ORDER BY publication_year DESC, department
    """)
    records = cur.fetchall()
    return render_template('admin_dashboard.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
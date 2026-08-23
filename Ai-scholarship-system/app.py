from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
from reportlab.pdfgen import canvas
from predict import predict_scholarship

app = Flask(__name__)
app.secret_key = "scholarship_secret_key"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']
        year = request.form['year']
        cgpa = request.form['cgpa']
        income = request.form['income']
        community = request.form['community']

        conn = sqlite3.connect("database/scholarship.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            conn.close()
            return "Email already registered!"

        cursor.execute("""
        INSERT INTO students
        (fullname,email,password,department,year,cgpa,income,community)
        VALUES (?,?,?,?,?,?,?,?)
        """,
        (
            fullname,
            email,
            password,
            department,
            year,
            cgpa,
            income,
            community
        ))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("database/scholarship.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user'] = user[1]      # Full Name
            session['email'] = user[2]     # Email

            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')
# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        name=session['user']
    )


# ---------------- PROFILE ----------------
@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("database/scholarship.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE email=?",
        (session['email'],)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        student=student
    )


# ---------------- AI RECOMMENDATION ----------------
@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():

    if 'user' not in session:
        return redirect('/login')

    scholarship = None

    if request.method == 'POST':

        cgpa = float(request.form['cgpa'])
        income = float(request.form['income'])
        community = request.form['community']
        department = request.form['department']

        scholarship = predict_scholarship(
            cgpa,
            income,
            community,
            department
        )

        # Save recommendation for PDF
        session['scholarship'] = scholarship

    return render_template(
        'recommendation.html',
        scholarship=scholarship
    )


# ---------------- SCHOLARSHIPS ----------------
@app.route('/scholarships')
def scholarships():

    if 'user' not in session:
        return redirect('/login')

    return render_template('scholarships.html')


# ---------------- ABOUT ----------------
@app.route('/about')
def about():

    if 'user' not in session:
        return redirect('/login')

    return render_template('about.html')
    # ---------------- CHATBOT ----------------
@app.route('/chatbot')
def chatbot():

    if 'user' not in session:
        return redirect('/login')

    return render_template("chatbot.html")
    # ---------------- FORGOT PASSWORD ----------------
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form['email']
        new_password = request.form['password']

        conn = sqlite3.connect("database/scholarship.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE students SET password=? WHERE email=?",
            (new_password, email)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('forgot_password.html')


# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():

    conn = sqlite3.connect("database/scholarship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        students=students
    )
    # ---------------- DOWNLOAD PDF ----------------
@app.route('/download_pdf')
def download_pdf():

    if 'user' not in session:
        return redirect('/login')

    pdf_file = "Scholarship_Recommendation.pdf"

    c = canvas.Canvas(pdf_file)

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(120, 800, "AI Scholarship Recommendation")

    # Student Details
    c.setFont("Helvetica", 12)

    c.drawString(50, 760, f"Student Name : {session['user']}")
    c.drawString(50, 735, f"Email : {session['email']}")

    # Recommendation
    scholarship = session.get(
        'scholarship',
        'No Recommendation Generated'
    )

    c.drawString(50, 690, "Recommended Scholarship:")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 665, str(scholarship))

    # Footer
    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        610,
        "Generated by AI Scholarship Recommendation System"
    )

    c.drawString(
        50,
        590,
        "Thank you for using our application."
    )

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )
    # ---------------- CHANGE PASSWORD ----------------
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        old_password = request.form['old_password']
        new_password = request.form['new_password']

        conn = sqlite3.connect("database/scholarship.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (session['email'], old_password)
        )

        user = cursor.fetchone()

        if user:

            cursor.execute(
                "UPDATE students SET password=? WHERE email=?",
                (new_password, session['email'])
            )

            conn.commit()
            conn.close()

            return "✅ Password Changed Successfully! <br><br><a href='/dashboard'>Back to Dashboard</a>"

        conn.close()

        return "❌ Old Password is Incorrect!"

    return render_template("change_password.html")


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# ---------------- RUN APP ----------------
if __name__ == "__main__":

    app.run(
        debug=True
    )
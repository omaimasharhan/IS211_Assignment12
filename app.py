from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Define the correct username and password
correct_username = 'admin'
correct_password = 'password'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == correct_username and correct_password == password:
            # Store the username in the session to indicate the user is logged in
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Incorrect username or password')

    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in by verifying the username in the session
    if 'username' in session and session['username'] == correct_username:
        con = sqlite3.connect("hw12.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM Students")
        students_data = cur.fetchall()

        cur.execute("SELECT * FROM Quizzes")
        quizzes_data = cur.fetchall()

        return render_template('dashboard.html', students=students_data, quizzes=quizzes_data)
    else:
        return redirect(url_for('login'))

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        FirstName = request.form['first_name']
        LastName = request.form['last_name']

        if not FirstName or not LastName:
            error_message = 'Please provide both first name and last name.'
            return render_template('add_student.html', error=error_message)

        with sqlite3.connect("hw12.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Students (FirstName, LastName) VALUES (?,?)", (FirstName, LastName))

        return redirect(url_for('dashboard'))
    return render_template('add_student.html', error=None)


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        quiz_date = request.form['quiz_date']
        noq = int(request.form['noq'])

        with sqlite3.connect("hw12.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Quizzes (Subject, QuizDate, NumQuestions) VALUES (?, ?, ?)",
                        (subject, quiz_date, noq))

        return redirect(url_for('dashboard'))
    return render_template('add_quiz.html')



@app.route('/student/<student_id>')
def student_results(student_id):
    if 'username' in session and session['username'] == correct_username:
        with sqlite3.connect("hw12.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM StudentResults WHERE StudentID=?", (int(student_id),))
            results = cur.fetchall()
            if not results:
                return 'No Results'
            else:
                return render_template('student_results.html', results=results)
    else:
        return redirect(url_for('login'))


@app.route('/results/add', methods=['GET', 'POST'])
def add_quiz_result():
    if request.method == 'POST':
        student_id = request.form.get('student')
        quiz_id = request.form.get('quiz')
        score = request.form.get('score')

        if student_id and quiz_id and score:
            try:
                student_id = int(student_id)
                quiz_id = int(quiz_id)
                score = int(score)

                with sqlite3.connect("hw12.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO StudentResults (StudentID, QuizID, Score) VALUES (?,?,?)",
                                (student_id, quiz_id, score))

                return redirect(url_for('dashboard'))

            except ValueError:
                return "Invalid data format. Please enter valid values."

        else:
            return "Please fill out all fields."
    else:
        with sqlite3.connect("hw12.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Students")
            students_data = cur.fetchall()

            cur.execute("SELECT ID, Subject FROM Quizzes")
            quizzes_data = cur.fetchall()

        return render_template('add_result.html', students_data=students_data, quizzes_data=quizzes_data, error=None)

@app.route('/quiz/delete/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    with sqlite3.connect("hw12.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM Quizzes WHERE ID=?", (quiz_id,))
    return redirect(url_for('dashboard'))

@app.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    with sqlite3.connect("hw12.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM Students WHERE ID=?", (student_id,))
    return redirect(url_for('dashboard'))

@app.route('/results/delete/<int:result_id>', methods=['POST'])
def delete_result(result_id):
    with sqlite3.connect("hw12.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM StudentResults WHERE ID=?", (result_id,))
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

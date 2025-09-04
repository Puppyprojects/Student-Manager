from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "mysecretkey"


# Database configuration (replace with your MySQL username & password)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/student_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

# Home route
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']

    new_student = Student(name=name, age=age, grade=grade)
    db.session.add(new_student)
    db.session.commit()

    flash("✅ Student added successfully!", "success")
    return redirect('/')

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    flash("❌ Student deleted successfully!", "danger")
    return redirect('/')

# Update student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.grade = request.form['grade']
        db.session.commit()
        flash("✏️ Student updated successfully!", "info")
        return redirect('/')
    return render_template('update.html', student=student)


# Search students
@app.route('/search', methods=['GET', 'POST'])
def search_student():
    query = request.form.get('query')  # input from form
    if query:
        students = Student.query.filter(
            (Student.name.like(f"%{query}%")) | 
            (Student.grade.like(f"%{query}%"))
        ).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create the 'students' table if it doesn’t exist
    app.run(debug=True)


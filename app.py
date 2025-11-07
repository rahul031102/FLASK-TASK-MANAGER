from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Route for Home Page
@app.route("/", methods=["POST", "GET"])
def index():
    # Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"An error occurred: {e}"

    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id):
    # Find the task by ID
    task_to_delete = MyTask.query.get_or_404(id)

    try:
        # Delete the task from the database
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"There was an issue deleting the task: {e}"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = MyTask.query.get_or_404(id)

    if request.method == 'POST':
        # Get updated text from the form
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"There was an issue updating the task: {e}"
    else:
        # Render edit page (show current task text)
        return render_template('update.html', task=task)

if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

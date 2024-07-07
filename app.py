from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return self.text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        try:
            db.session.add(Todo(text=task_content))
            db.session.commit()
            return redirect("/")
        except Exception:
            return "There was an error"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:pk>/')
def delete(pk):
    task_to_delete = Todo.query.get_or_404(pk)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "There was an error"


@app.route('/update/<int:pk>/', methods=['GET', 'POST'])
def update(pk):
    task = Todo.query.get_or_404(pk)
    if request.method == 'POST':
        task.text = request.form['content']

        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            return "There was an error with updating"
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)


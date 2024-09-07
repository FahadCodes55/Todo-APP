from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder="template")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.todo_app'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking (optional)
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


# Manually push the application context
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # Show all todos
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    select_todo = Todo.query.filter_by(id=todo_id).first()
    select_todo.complete = not select_todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    select_todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(select_todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)

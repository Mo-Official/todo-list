from flask import Flask
from flask import render_template, redirect, request, url_for
import csv
from .csvUtils import CSVConnector

app = Flask(__name__, template_folder="./templates")
conn = CSVConnector("./tasks.csv")


@app.route("/", methods=["GET"])
def index():
    tasks = conn.get_tasks("*")
    return render_template("index.html", tasks=tasks)


@app.route("/tasks")
def get_tasks_ep():
    return {"tasks": conn.get_tasks()}


@app.route("/add")
def insert_task_ep():
    value = request.form.get("title", "New Title")
    conn.insert_task_db(value)
    return redirect(url_for("index"))


@app.route("/delete/<id>")
def delete_task_ep(id):
    conn.delete_task_db(id)
    return redirect(url_for("index"))


@app.route(
    "/update/<id>",
    methods=["POST"],
)
def update_task_ep(id):
    conn.update_task_db(id, request.json["value"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run("", debug=True)

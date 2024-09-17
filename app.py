from flask import Flask
from flask import render_template, redirect, request, url_for
import csv
from util.postgreUtils import PostgreConnector

app = Flask(__name__, template_folder="./templates")
conn = PostgreConnector("database.ini")
storage_path = "./storage/"


@app.route("/", methods=["GET"])
def index():
    tasks = conn.get_tasks("*")
    attachments = {}
    for task in tasks:
        attachments[task[0]] = [".txt", ".pdf", ".png"]
    return render_template("index.html", tasks=tasks, attachments=attachments)


@app.route("/tasks")
def get_tasks_ep():
    return {"tasks": conn.get_tasks()}


@app.route("/add")
def insert_task_ep():
    value = request.form.get("title", "New Title")
    conn.add_task(value)
    return redirect(url_for("index"))


@app.route("/delete/<id>")
def delete_task_ep(id):
    conn.delete_task(id)
    return redirect(url_for("index"))


@app.route(
    "/update/<id>",
    methods=["POST"],
)
def update_task_ep(id):
    conn.update_task(id, request.json["value"])
    return redirect(url_for("index"))


@app.route("/upload-attachment/<id>", methods=["POST"])
def upload_attachment(id):
    file = request.files["file"]
    file.save(storage_path + file.filename)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run("", debug=True)

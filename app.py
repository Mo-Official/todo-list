from flask import Flask
from flask import render_template, redirect, request, url_for
import csv

app = Flask(__name__, template_folder="./templates")
csv_path = "./tasks.csv"
csv_row_num = 0
def update_csv_row_num():
    with open(csv_path, "r") as fh:
        global csv_row_num
        csv_row_num = len(fh.readlines())
        
def update_task_db(id, value):
    lines = []
    with open(csv_path) as fh:
        lines : list[str] = fh.readlines()
        for i in range(len(lines)):
            try:
                parsed_line = lines[i].split(";")
                if parsed_line[0] == str(id):
                    parsed_line[1] = value +"\n"
                lines[i] = ";".join(parsed_line)
            except ValueError:
                continue
                
        global csv_row_num
        csv_row_num = len(lines)
    with open(csv_path, "w") as fh:
        fh.writelines(lines)
    
def insert_task_db(value):
    global csv_row_num
    if csv_row_num == 0:
        update_csv_row_num()
    csv_row_num += 1
    with open(csv_path, "a") as fh:
        fh.write(f"\n{csv_row_num};{value}")

def delete_task_db(id):
    global csv_row_num
    if csv_row_num == 0:
        update_csv_row_num()
    csv_row_num -= 1
    
    lines = []
    with open(csv_path) as fh:
        lines : list[str] = fh.readlines()
        for i in range(len(lines)):
            parsed_line = lines[i].split(";")
            if parsed_line[0] == str(id):
                lines.pop(i)
                break
            
    with open(csv_path, "w") as fh:
        if len(lines) > 0:
            lines[-1].removesuffix("\n")
        fh.writelines(lines)

def get_task(id):
    with open(csv_path) as fh:
        line = fh.readline().split(";")
        while line[0] != str(id):
            line = fh.readline().split(";")
        return (line[0], line[1].strip())

def get_tasks(search):
    with open(csv_path) as fh:
        if search == "*":
            lines =  fh.readlines()
            tasks = []
            for line in lines:
                try:
                    v1, v2 = line.split(";")
                    tasks.append((v1, v2))
                except ValueError:
                    continue
            return tasks
        return []
    

@app.route("/", methods=["GET"])
def index():
    tasks = get_tasks("*")
    return render_template("index.html", tasks=tasks)

@app.route("/add")
def insert_task_ep():
    value = request.form.get("title", "New Title")
    insert_task_db(value)
    return redirect(url_for("index"))

@app.route("/delete/<id>")
def delete_task_ep(id):
    delete_task_db(id)
    return redirect(url_for("index"))

@app.route("/update/<id>", methods=["POST"], )
def update_task_ep(id):
    update_task_db(id, request.json["value"])
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run("", debug=True)

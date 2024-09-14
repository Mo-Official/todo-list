from flask import Flask
from flask import render_template, redirect, request
import csv

app = Flask(__name__, template_folder="./templates")
csv_path = "./tasks.csv"
csv_row_num = 0
def update_csv_row_num():
    with open(csv_path, "r") as fh:
        global csv_row_num
        csv_row_num = len(fh.readlines())
        
def update_task(id, value):
    lines = []
    with open(csv_path) as fh:
        lines : list[str] = fh.readlines()
        for i in range(len(lines)):
            parsed_line = lines[i].split(";")
            if parsed_line[0] == str(id):
                parsed_line[1] = value +"\n"
            lines[i] = ";".join(parsed_line)
        global csv_row_num
        csv_row_num = len(lines)
    with open(csv_path, "w") as fh:
        fh.writelines(lines)
    
def add_task(value):
    global csv_row_num
    if csv_row_num == 0:
        update_csv_row_num()
    csv_row_num += 1
    with open(csv_path, "a") as fh:
        fh.write(f"\n{csv_row_num};{value}")

def delete_task(id):
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
        fh.writelines(lines)

def get_task(id):
    with open(csv_path) as fh:
        line = fh.readline().split(";")
        while line[0] != str(id):
            line = fh.readline().split(";")
        return line

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/add", methods=['POST'])
def add_task():
    pass

if __name__ == "__main__":
    app.run("", debug=True)

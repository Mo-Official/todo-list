class CSVConnector:
    def __init__(self, csv_path) -> None:
        self.csv_path = csv_path
        self.csv_row_num = 0

    def update_csv_row_num(self):
        with open(self.csv_path, "r") as fh:
            self.csv_row_num = len(fh.readlines())

    def update_task_db(self, id, value):
        lines = []
        with open(self.csv_path) as fh:
            lines: list[str] = fh.readlines()
            for i in range(len(lines)):
                try:
                    parsed_line = lines[i].split(";")
                    if parsed_line[0] == str(id):
                        parsed_line[1] = value + "\n"
                    lines[i] = ";".join(parsed_line)
                except ValueError:
                    continue
            self.update_csv_row_num()
        with open(self.csv_path, "w") as fh:
            fh.writelines(lines)

    def insert_task_db(self, value):
        self.update_csv_row_num()
        self.csv_row_num += 1
        with open(self.csv_path, "a") as fh:
            fh.write(f"\n{self.csv_row_num};{value}")

    def delete_task_db(self, id):
        self.update_csv_row_num()
        self.csv_row_num -= 1
        lines = []
        with open(self.csv_path) as fh:
            lines: list[str] = fh.readlines()
            for i in range(len(lines)):
                parsed_line = lines[i].split(";")
                if parsed_line[0] == str(id):
                    lines.pop(i)
                    break

        with open(self.csv_path, "w") as fh:
            if len(lines) > 0:
                lines[-1].removesuffix("\n")
            fh.writelines(lines)

    def get_task(self, id):
        with open(self.csv_path) as fh:
            line = fh.readline().split(";")
            while line[0] != str(id):
                line = fh.readline().split(";")
            return (line[0], line[1].strip())

    def get_tasks(self, search):
        with open(self.csv_path) as fh:
            if search == "*":
                lines = fh.readlines()
                tasks = []
                for line in lines:
                    try:
                        v1, v2 = line.split(";")
                        tasks.append((v1, v2))
                    except ValueError:
                        continue
                return tasks
            return []

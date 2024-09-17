CREATE TABLE Tasks (
        id SERIAL PRIMARY KEY,
        title TEXT
);

/* CREATE TABLE Attachments (
        id SERIAL PRIMARY KEY,
        name TEXT,
        hashedName TEXT,
                
        CONSTRAINT fk_task
         FOREIGN KEY(task_id) 
          REFERENCES Tasks(id)
) */
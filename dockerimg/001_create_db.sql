CREATE TABLE Tasks (
        id SERIAL PRIMARY KEY,
        username TEXT,
        title TEXT
        CONSTRAINT username_fk
        FOREIGN KEY(username) 
                REFERENCES Users(username)
);

CREATE TABLE Users (
        username TEXT PRIMARY KEY,
        password TEXT
)
CREATE TABLE Students (
    ID INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT
);

CREATE TABLE Quizzes (
    ID INTEGER PRIMARY KEY,
    Subject TEXT,
    NumQuestions INTEGER,
    QuizDate DATE
);

CREATE TABLE StudentResults (
    StudentID INTEGER,
    QuizID INTEGER,
    Score INTEGER,
    FOREIGN KEY(StudentID) REFERENCES Students(ID),
    FOREIGN KEY(QuizID) REFERENCES Quizzes(ID)
);



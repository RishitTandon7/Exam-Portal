CREATE TABLE Student_Answer (
    Answer_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Student_ID INT NOT NULL,
    Exam_ID INT NOT NULL,
    Question_ID INT NOT NULL,
    Option_ID INT NULL,
    Answer_Text TEXT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY (Exam_ID) REFERENCES Exam(Exam_ID),
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID),
    FOREIGN KEY (Option_ID) REFERENCES Options(Option_ID)
);

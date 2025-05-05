use exam_portal;
-- 1. Department 🏫
CREATE TABLE Department (
    Dept_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    HOD VARCHAR(100),
    No_of_Courses INT DEFAULT 0,
    Faculty_Count INT DEFAULT 0
);

-- 2. Faculty 👨🏫
CREATE TABLE Faculty (
    Faculty_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Dept_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- 3. Course 📚
CREATE TABLE Course (
    Course_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Credits INT CHECK (Credits > 0),
    Dept_ID INT,
    Faculty_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (Faculty_ID) REFERENCES Faculty(Faculty_ID)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- 4. Student 🧑🎓
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Course_ID INT,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- 5. Exam 📝
CREATE TABLE Exam (
    Exam_ID INT PRIMARY KEY AUTO_INCREMENT,
    Subject VARCHAR(100) NOT NULL,
    Date DATE NOT NULL,
    Duration INT CHECK (Duration > 0), -- Duration in minutes
    Faculty_ID INT,
    FOREIGN KEY (Faculty_ID) REFERENCES Faculty(Faculty_ID)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- 6. Question ❓
CREATE TABLE Question (
    Question_ID INT PRIMARY KEY AUTO_INCREMENT,
    Exam_ID INT,
    Type ENUM('MCQ', 'Descriptive', 'True/False') NOT NULL,
    Marks INT CHECK (Marks >= 0),
    Difficulty_Level ENUM('Easy', 'Medium', 'Hard'),
    FOREIGN KEY (Exam_ID) REFERENCES Exam(Exam_ID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 7. Options 🔢
CREATE TABLE Options (
    Option_ID INT PRIMARY KEY AUTO_INCREMENT,
    Question_ID INT,
    Option_Text TEXT NOT NULL,
    Is_Correct BOOLEAN DEFAULT FALSE,
    Option_Order INT CHECK (Option_Order > 0),
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 8. Result 📊
CREATE TABLE Result (
    Result_ID INT PRIMARY KEY AUTO_INCREMENT,
    Student_ID INT,
    Exam_ID INT,
    Score DECIMAL(5,2) CHECK (Score >= 0),
    Status ENUM('Pass', 'Fail') NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Exam_ID) REFERENCES Exam(Exam_ID)
        ON DELETE CASCADE ON UPDATE CASCADE
);
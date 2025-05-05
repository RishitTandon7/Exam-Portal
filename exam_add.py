import mysql.connector
from mysql.connector import Error

# Connect to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your host
            database='exam_portal',  # Replace with your database name
            user='root',  # Replace with your username
            password='root'  # Replace with your password
        )
        if connection.is_connected():
            print("Connected to MySQL")
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Create Questions table
def create_questions_table(connection):
    try:
        cursor = connection.cursor()
        
        # SQL to create the Questions table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Questions (
            question_id INT AUTO_INCREMENT PRIMARY KEY,
            exam_id INT NOT NULL,
            question_text TEXT NOT NULL,
            FOREIGN KEY (exam_id) REFERENCES Exam(exam_id)
        );
        """
        
        cursor.execute(create_table_query)
        print("Questions table created successfully.")
    except Error as e:
        print("Error while creating table:", e)
    finally:
        cursor.close()

# Main function
def main():
    # Create a connection to the database
    connection = create_connection()
    
    if connection:
        # Create the Questions table
        create_questions_table(connection)
        
        # Close the connection
        connection.close()

if __name__ == "__main__":
    main()

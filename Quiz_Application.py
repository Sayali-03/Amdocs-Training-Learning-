import pymysql
import csv

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="pass@word1",
        database="quizdb"
    )

def add_quiz():
    subject = input("Enter Subject: ")
    total_marks = int(input("Enter marks for each question: "))
    num_questions = int(input("Enter number of questions: "))

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO quizzes (subject, total_marks, num_questions) VALUES (%s, %s, %s)"
    cursor.execute(query, (subject, total_marks, num_questions))
    conn.commit()
    
    quiz_id = cursor.lastrowid 

    for i in range(num_questions):
        question = input(f"Enter question {i + 1}: ")

        option_1 = input(f"Enter option 1 for question {i + 1}: ")
        option_2 = input(f"Enter option 2 for question {i + 1}: ")
        option_3 = input(f"Enter option 3 for question {i + 1}: ")
        option_4 = input(f"Enter option 4 for question {i + 1}: ")
        correct_option = int(input(f"Enter the correct option number (1-4) for question {i + 1}: "))

        query = """
            INSERT INTO questions (quiz_id, question, option_1, option_2, option_3, option_4, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (quiz_id, question, option_1, option_2, option_3, option_4, correct_option))
        conn.commit()

    conn.close()
    print(f"Quiz for {subject} added successfully!")

def view_quiz():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizzes")
    quizzes = cursor.fetchall()

    print("\n=== Quiz List ===")
    if quizzes:
        for quiz in quizzes:
            print(f"ID: {quiz[0]}, Subject: {quiz[1]}, Marks per Question: {quiz[2]}, Total Questions: {quiz[3]}")
    else:
        print("No quizzes found!")

    conn.close()

def update_quiz():
    quiz_id = int(input("Enter quiz ID to update: "))
    num_extra_questions = int(input("Enter the number of extra questions to add: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizzes WHERE id=%s", (quiz_id,))
    quiz = cursor.fetchone()

    if quiz:
        for i in range(num_extra_questions):
            question = input(f"Enter extra question {i + 1}: ")

            option_1 = input(f"Enter option 1 for extra question {i + 1}: ")
            option_2 = input(f"Enter option 2 for extra question {i + 1}: ")
            option_3 = input(f"Enter option 3 for extra question {i + 1}: ")
            option_4 = input(f"Enter option 4 for extra question {i + 1}: ")

            correct_option = int(input(f"Enter the correct option number (1-4) for extra question {i + 1}: "))

            query = """
                INSERT INTO questions (quiz_id, question, option_1, option_2, option_3, option_4, correct_option)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (quiz_id, question, option_1, option_2, option_3, option_4, correct_option))
            conn.commit()

        print("Extra questions added successfully!")
    else:
        print("Quiz not found!")

    conn.close()


def delete_quiz():
    quiz_id = int(input("Enter quiz ID to delete: "))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE quiz_id=%s", (quiz_id,))
    conn.commit()
    cursor.execute("DELETE FROM quizzes WHERE id=%s", (quiz_id,))
    conn.commit()

    conn.close()
    print("Quiz deleted successfully!")

def export_quiz():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizzes")
    quizzes = cursor.fetchall()

    with open("quizzes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Subject", "Marks per Question", "Total Questions"])
        for quiz in quizzes:
            writer.writerow(quiz)

    conn.close()
    print("Quizzes exported to quizzes.csv!")

def search_quiz():
    print("\nSearch Quiz By:")
    print("1. Quiz ID")
    print("2. Subject")
    
    choice = input("Enter your choice (1/2): ")
    
    conn = get_connection()
    cursor = conn.cursor()

    if choice == "1":
        quiz_id = int(input("Enter quiz ID: "))
        query = "SELECT * FROM quizzes WHERE id = %s"
        cursor.execute(query, (quiz_id,))
        quiz = cursor.fetchone()

        if quiz:
            print("\n=== Quiz Found ===")
            print(f"ID: {quiz[0]}, Subject: {quiz[1]}, Marks per Question: {quiz[2]}, Total Questions: {quiz[3]}")

            cursor.execute("SELECT * FROM questions WHERE quiz_id = %s", (quiz_id,))
            questions = cursor.fetchall()
            print("\n=== Questions ===")
            for question in questions:
                print(f"Q: {question[2]}")
                print(f"1. {question[3]}")
                print(f"2. {question[4]}")
                print(f"3. {question[5]}")
                print(f"4. {question[6]}")
                print(f"Correct Option: {question[7]}")

        else:
            print("No quiz found with that ID.")

    elif choice == "2":
        subject = input("Enter subject to search: ")
        query = "SELECT * FROM quizzes WHERE subject LIKE %s"
        cursor.execute(query, (f"%{subject}%",))
        quizzes = cursor.fetchall()

        if quizzes:
            print("\n=== Quizzes Found ===")
            for quiz in quizzes:
                print(f"ID: {quiz[0]}, Subject: {quiz[1]}, Marks per Question: {quiz[2]}, Total Questions: {quiz[3]}")
                
                cursor.execute("SELECT * FROM questions WHERE quiz_id = %s", (quiz[0],))
                questions = cursor.fetchall()
                print("\n=== Questions ===")
                for question in questions:
                    print(f"Q: {question[2]}")
                    print(f"1. {question[3]}")
                    print(f"2. {question[4]}")
                    print(f"3. {question[5]}")
                    print(f"4. {question[6]}")
                    print(f"Correct Option: {question[7]}")
        else:
            print("No quizzes found with that subject.")

    else:
        print("Invalid choice! Please try again.")
    
    conn.close()


def main_menu():
    while True:
        print("\n=== QUIZ MANAGEMENT SYSTEM ===")
        print("1. Add Quiz")
        print("2. View Quizzes")
        print("3. Update Quiz")
        print("4. Delete Quiz")
        print("5. Search Quiz")
        print("6. Export Quizzes")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_quiz()

        elif choice == "2":
            view_quiz()

        elif choice == "3":
            update_quiz()

        elif choice == "4":
            delete_quiz()

        elif choice == "5":
            search_quiz()  

        elif choice == "6":
            export_quiz()

        elif choice == "7":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()

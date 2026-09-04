from .exceptions import LibraryError

from .services.library_service import LibraryService

from .storage.json_store import JsonStore


class LibraryApp:
    """
    Console UI.
    Business logic stays inside LibraryService.
    """

    def __init__(self):

        self.service = LibraryService(JsonStore("data"))

    # ==================================================
    # MAIN LOOP
    # ==================================================

    def run(self):

        while True:

            self.show_menu()

            choice = input("Enter your choice: ").strip()

            try:

                if choice == "1":
                    self.register_student()

                elif choice == "2":
                    self.add_book()

                elif choice == "3":
                    self.search_book()

                elif choice == "4":
                    self.issue_book()

                elif choice == "5":
                    self.return_book()

                elif choice == "6":
                    self.student_report()

                elif choice == "7":
                    self.book_availability_report()

                elif choice == "8":
                    self.book_history()

                elif choice == "9":
                    self.display_all_students()

                elif choice == "10":
                    self.display_all_books()

                elif choice == "11":

                    print(
                        "Thank you for using "
                        "Library Management System!"
                    )

                    break

                else:

                    print(
                        "Invalid choice. "
                        "Enter a number between 1 and 11."
                    )

            except LibraryError as error:

                print()
                print("Error:", error)

            except KeyboardInterrupt:
                print()
                print(
                    "Program stopped by user."
                )

                break

            except Exception as error:
                print()
                print("Unexpected error :", error)

    # ==================================================
    # MENU
    # ==================================================

    @staticmethod
    def show_menu():

        print()
        print("=" * 50)

        print("      LIBRARY MANAGEMENT SYSTEM")

        print("=" * 50)

        print("1. Student Registration")

        print("2. Add New Book")

        print("3. Search Book")

        print("4. Issue / Borrow Book")

        print("5. Return Book")

        print("6. Student Borrowing Report")

        print("7. Book Availability Report")

        print("8. Book Borrowing History")

        print("9. Display All Students")

        print("10. Display All Books")

        print("11. Exit")

        print("=" * 50)

    # ==================================================
    # 1. REGISTER STUDENT
    # ==================================================

    def register_student(self):

        student_id = input("Enter Student ID: ")

        student_name = input("Enter Student Name: ")

        student = self.service.register_student(student_id,student_name)
        print()
        print("Student Registration Successful!")

        print("Student ID:",student_id.strip().upper())

        print("Student Name:",student["name"])

        print("Membership: Active")

    # ==================================================
    # 2. ADD BOOK
    # ==================================================

    def add_book(self):

        book = self.service.add_book(

            input("Enter Book ID: "),

            input("Enter Book Name: "),

            input("Enter Author Name: "),

            input("Enter Rack Number: "),

            input("Enter Total Number of Books: ")
        )
        print()
        print("Book added successfully!")

        print("Book:",book["name"])

    # ==================================================
    # 3. SEARCH BOOK
    # ==================================================

    def search_book(self):

        results = self.service.search_books(

            input("Enter Book Name: "),

            input("Enter Author Name ""(Press Enter to Skip): ")
        )

        if not results:
            print()
            print("Book not found in the library.")

            return

        for book_id, book in results:

            issued = (book["total_books"]- book["available_books"])
            print()
            print("-----------------------------")

            print("Book ID        :",book_id)

            print("Book Name      :",book["name"])

            print("Author         :",book["author"])

            print("Rack Number    :",book["rack"])

            print("Total Books    :",book["total_books"])

            print("Issued Books   :",issued)

            print("Available Books:",book["available_books"])

            print(
                "Status         :",
                (
                    "AVAILABLE"
                    if book["available_books"] > 0
                    else "NOT AVAILABLE"
                )
            )

            print("-----------------------------")

    # ==================================================
    # 4. ISSUE BOOK
    # ==================================================

    def issue_book(self):

        student_id = input("Enter Student ID: ")

        current = self.service.current_borrowed(student_id)

        student_key = student_id.strip().upper()

        student_name = self.service.students[student_key]["name"]
        print()
        print("Student Name:",student_name)

        print("Currently Borrowed Books:", len(current))

        book_id = input("Enter Book ID: ")

        issue_date = input("Enter Issue Date (DD-MM-YYYY): ")

        book = self.service.issue_book(student_id,book_id,issue_date)
        print()
        print("Book issued successfully!")

        print("Book Name:",book["name"])

        print("Issue Date:",issue_date)

        print("Rack Number:",book["rack"])

        print("Available Books:",book["available_books"])

    # ==================================================
    # 5. RETURN BOOK
    # ==================================================

    def return_book(self):

        student_id = input("Enter Student ID: ")

        current = self.service.current_borrowed(student_id)

        if not current:

            print("This student has no books to return.")

            return
        print()
        print("Currently Borrowed Books:")

        for record in current:

            print("-",record["book_name"],"| Issue Date:",record["issue_date"])

        book_id = input("Enter Book ID to Return: ")

        return_date = input("Enter Return Date (DD-MM-YYYY): ")

        record = self.service.return_book(

            student_id,

            book_id,

            return_date
        )
        print()
        print("Book returned successfully!")

        print("Book Name:",record["book_name"])

        print("Return Date:",return_date)

    # ==================================================
    # 6. STUDENT REPORT
    # ==================================================

    def student_report(self):

        student_id, student, history = (
            self.service.student_report(
                input(
                    "Enter Student ID or Student Name: "
                )
            )
        )
        print()
        print("Student ID:",student_id)

        print("Student Name:",student["name"])

        print("BOOK HISTORY")

        print("-" * 40)

        for record in history:

            print("Book:",record["book_name"])

            print("Issue Date:",record["issue_date"])

            if record["return_date"] == "":

                print("Status: Currently Borrowed")

            else:

                print("Return Date:",record["return_date"])

            print("-" * 40)

        print("Total Borrowing Transactions:",len(history))

    # ==================================================
    # 7. BOOK AVAILABILITY
    # ==================================================

    def book_availability_report(self):

        print()
        print("=" * 40)

        print("BOOK AVAILABILITY REPORT")

        print("=" * 40)

        if not self.service.books:

            print("No books available.")

            return

        for book_id, book in (self.service.books.items()):

            issued = (book["total_books"]- book["available_books"])
            print()
            print("Book ID         :",book_id)

            print("Book Name       :",book["name"])

            print("Author          :",book["author"])

            print("Rack Number     :",book["rack"])

            print("Total Books     :",book["total_books"])

            print("Issued Books    :",issued)

            print("Available Books :",book["available_books"])

            print(
                "Status          :",
                (
                    "AVAILABLE"
                    if book["available_books"] > 0
                    else "NOT AVAILABLE"
                )
            )

    # ==================================================
    # 8. BOOK HISTORY
    # ==================================================

    def book_history(self):

        book_id, book, history, unique_students = (
            self.service.book_history(
                input("Enter Book Name: ")
            )
        )
        print()
        print("Book Name:",book["name"])

        print("Author:",book["author"])

        print("Rack Number:",book["rack"])

        print("Total Books:",book["total_books"])

        print("Available Books:",book["available_books"])
        print()
        print("BORROWING HISTORY")

        print("-" * 40)

        for record in history:

            print("Student:",record["student_name"])

            print("Issue Date:",record["issue_date"])

            if record["return_date"] == "":

                print("Status: Currently Borrowed")

            else:

                print("Return Date:",record["return_date"])

            print("-" * 40)

        print("Total Borrowing Transactions:",len(history))

        print("Number of Unique Students:",len(unique_students))

    # ==================================================
    # 9. DISPLAY ALL STUDENTS
    # ==================================================

    def display_all_students(self):
        print()
        print("=" * 40)

        print("ALL STUDENTS")

        print("=" * 40)

        if not self.service.students:

            print("No students registered.")

            return

        for student_id, student in (
            self.service.students.items()
        ):
            print()
            print("Student ID:",student_id)

            print("Name:",student["name"])

            print(
                "Membership:",
                (
                    "Active"
                    if student["membership"]
                    else "Inactive"
                )
            )

            print("-" * 35)

    # ==================================================
    # 10. DISPLAY ALL BOOKS
    # ==================================================

    def display_all_books(self):

        print()
        print( "=" * 40)

        print( "ALL BOOKS")

        print("=" * 40)

        if not self.service.books:

            print( "No books available.")

            return

        for book_id, book in (self.service.books.items() ):
            print()
            print("Book ID:",book_id)

            print("Book Name:",book["name"])

            print("Author:",book["author"])

            print("Rack:",book["rack"])

            print("Total Books:",book["total_books"])

            print("Available Books:",book["available_books"])

            print("-" * 35 )
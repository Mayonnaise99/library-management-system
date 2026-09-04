from ..exceptions import (BookNotFoundError,BookUnavailableError,BorrowLimitError,DuplicateRecordError,
    StudentNotFoundError,ValidationError,)

from ..validators import (date_dd_mm_yyyy,positive_int,required_text,)


class LibraryService:

    MAX_BORROWED_BOOKS = 3
    def __init__(self, store):

        self.store = store

        self.students = self.store.load("students.json",{})

        self.books = self.store.load("books.json",{})

        self.borrow_records = self.store.load("borrow_records.json",[])

        self.return_records = self.store.load("return_records.json",[])

    # ==================================================
    # SAVE ALL DATA
    # ==================================================

    def save_all(self):

        self.store.save("students.json",self.students)

        self.store.save("books.json",self.books)

        self.store.save("borrow_records.json",self.borrow_records)

        self.store.save("return_records.json",self.return_records)

    # ==================================================
    # STUDENTS
    # ==================================================

    def register_student(self,student_id,student_name):

        student_id = required_text(student_id,"Student ID").upper()

        student_name = required_text(student_name,"Student Name")

        if student_id in self.students:

            raise DuplicateRecordError("Student ID already exists. ""Student is already a member.")

        self.students[student_id] = {"name": student_name,"membership": True}

        self.store.save("students.json",self.students)

        return self.students[student_id]

    # ==================================================
    # BOOKS
    # ==================================================

    def add_book(self,book_id,book_name,author,rack,total_books):

        book_id = required_text(book_id,"Book ID").upper()

        book_name = required_text(book_name,"Book Name")

        author = required_text(author,"Author")

        rack = required_text(rack,"Rack").upper()

        total_books = positive_int(total_books,"Total Books")

        if book_id in self.books:

            raise DuplicateRecordError("Book ID already exists.")

        self.books[book_id] = {"name": book_name,"author": author,"rack": rack,"total_books": total_books,"available_books": total_books}

        self.store.save("books.json",self.books)

        return self.books[book_id]

    # ==================================================
    # SEARCH BOOKS
    # ==================================================

    def search_books(self,name,author=""):

        name = required_text(name,"Book Name").lower()

        author = author.strip().lower()

        results = []

        for book_id, book in self.books.items():

            name_match = (name in book["name"].lower())

            author_match = (not author or author in book["author"].lower())

            if name_match and author_match:
                results.append((book_id, book))

        return results

    # ==================================================
    # STUDENT HELPER
    # ==================================================

    def _student(self, student_id):

        student_id = required_text(student_id,"Student ID").upper()

        if student_id not in self.students:

            raise StudentNotFoundError("Student is not registered.")

        return (student_id,self.students[student_id])

    # ==================================================
    # BOOK HELPER
    # ==================================================

    def _book(self, book_id):

        book_id = required_text(book_id,"Book ID").upper()

        if book_id not in self.books:

            raise BookNotFoundError("Book does not exist in the library.")

        return (book_id,self.books[book_id])

    # ==================================================
    # CURRENTLY BORROWED BOOKS
    # ==================================================

    def current_borrowed(self,student_id):

        student_id, _ = self._student(student_id)

        return [

            record

            for record in self.borrow_records
            if (
                record["student_id"] == student_id
                and record["return_date"] == ""
            )
        ]

    # ==================================================
    # ISSUE BOOK
    # ==================================================

    def issue_book(self,student_id,book_id,issue_date):

        student_id, student = self._student(student_id)

        if not student["membership"]:

            raise ValidationError("Library membership is not active.")

        current_books = self.current_borrowed(student_id)

        if len(current_books) >= self.MAX_BORROWED_BOOKS:

            raise BorrowLimitError("Maximum limit is " + str(self.MAX_BORROWED_BOOKS) + "books.")

        book_id, book = self._book(book_id)

        if book["available_books"] <= 0:

            raise BookUnavailableError("Book is currently NOT AVAILABLE.")

        for record in current_books:

            if record["book_id"] == book_id:

                raise DuplicateRecordError("You have already borrowed this book.")

        issue_date = date_dd_mm_yyyy(issue_date,"Issue Date")

        self.borrow_records.append({

            "student_id": student_id,

            "student_name": student["name"],

            "book_id": book_id,

            "book_name": book["name"],

            "issue_date": issue_date,

            "return_date": ""
        })

        book["available_books"] -= 1

        self.save_all()

        return book

    # ==================================================
    # RETURN BOOK
    # ==================================================

    def return_book(self,student_id,book_id,return_date):

        student_id, student = self._student(student_id)

        book_id, book = self._book(book_id)

        return_date = date_dd_mm_yyyy(return_date,"Return Date")

        for record in self.borrow_records:

            if (
                record["student_id"] == student_id
                and record["book_id"] == book_id
                and record["return_date"] == ""
            ):
                record["return_date"] = return_date
                self.return_records.append({

                    "student_id": student_id,

                    "student_name": student["name"],

                    "book_id": book_id,

                    "book_name": record["book_name"],

                    "return_date": return_date
                })

                book["available_books"] += 1

                self.save_all()
                return record

        raise ValidationError("This student has not borrowed this book.")

    # ==================================================
    # STUDENT REPORT
    # ==================================================

    def student_report(self,search_value):

        search_value = required_text(search_value,"Student ID or Name").lower()

        for student_id, student in self.students.items():

            if (
                search_value == student_id.lower()
                or search_value == student["name"].lower()
            ):

                history = [

                    record

                    for record in self.borrow_records

                    if record["student_id"] == student_id
                ]

                return (student_id,student,history)

        raise StudentNotFoundError("Student not found.")

    # ==================================================
    # BOOK HISTORY
    # ==================================================

    def book_history(self,book_name):

        book_name = required_text(book_name,"Book Name").lower()

        for book_id, book in self.books.items():

            if book["name"].lower() == book_name:

                history = [

                    record

                    for record in self.borrow_records

                    if record["book_id"] == book_id
                ]

                unique_students = {

                    record["student_id"]

                    for record in history
                }

                return (
                    book_id,
                    book,
                    history,
                    unique_students
                )

        raise BookNotFoundError("Book not found.")

class BooksModel:

    all_books = [{"id": 1, "title": "The Da Vinci Code", "author": "Dan Brown", "category": "Mystery", "url": "https..."},
             {"id": 2, "title": "Almost Heaven", "author": "Judith McNaught", "category": "Romance", "url": "https..."},
             {"id": 3, "title": "The Juror", "author": "John Grisham", "category": "Drama", "url": "https..."}]

    def __init__(self):
        pass

    def book_add(self, book):
        """ method to add book dictionaries to the books list"""
        self.all_books.append(book)

    def book_all(self):
        "method returns all books"
        return self.all_books

    def book_specific(self, id):
        """method returns specific book according to book id"""
        for each_book in self.all_books:
            if each_book["id"] == id:
                return each_book

    # FINISH UP THIS CODE THAT REPLACES THE UPDATED BOOK WITH THE OLD BOOK IN THE all_books LIST
    def book_update(self, id, book_update):
        """method returns specific book according to book id"""
        old_book = None
        for each_book in self.all_books:
            if each_book["id"] == id:
                old_book = each_book
        # finding the index of the book with matching title
        for i, j in enumerate(self.all_books):
            if j == old_book:
                # editing the books list
                self.all_books[i] = book_update
        return self.all_books

    def book_delete(self, book_title):
        """method deletes specific book according to book id"""
        old_book = None
        for each_book in self.all_books:
            if each_book["title"] == book_title:
                old_book = each_book
        # finding the index of the book with matching title
        for i, j in enumerate(self.all_books):
            if j == old_book:
                del self.all_books[i]
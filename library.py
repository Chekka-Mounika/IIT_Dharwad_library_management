import psycopg2
from colorama import init, Fore, Back, Style
from tabulate import tabulate

conn = psycopg2.connect(
    database="librarydb",
    host="localhost",
    user="postgres",
    password="Mounika@2004",
    port=5432,
)
mycursor = conn.cursor()

init(autoreset=True)

menu = f"""
{Fore.BLUE}{Style.BRIGHT}┌────────────────────────────────────────────────────────────┐
│{Fore.MAGENTA}{Style.BRIGHT}                     IITDh Library                          {Fore.BLUE}{Style.BRIGHT}│
│{Fore.GREEN}{Style.BRIGHT} Main Menu                                                  {Fore.BLUE}{Style.BRIGHT}│
│{Fore.GREEN}{Style.BRIGHT}                                                            {Fore.BLUE}{Style.BRIGHT}│
│{Fore.CYAN}{Style.BRIGHT} Enter the respective numbers to perform the required task: {Fore.BLUE}{Style.BRIGHT}│
│   {Fore.YELLOW}1. Borrow/Renew a Book                                   {Fore.BLUE}{Style.BRIGHT}│
│   {Fore.YELLOW}2. Return a Book                                         {Fore.BLUE}{Style.BRIGHT}│
│   {Fore.YELLOW}3. Book/Ebook Search                                     {Fore.BLUE}{Style.BRIGHT}│
│   {Fore.YELLOW}4. Book Information                                      {Fore.BLUE}{Style.BRIGHT}│
│   {Fore.YELLOW}5. Add records                                           {Fore.BLUE}{Style.BRIGHT}│
│   {Fore.YELLOW}6. Delete records                                        {Fore.BLUE}{Style.BRIGHT}│
│   {Fore.RED}7. Exit                                                  {Fore.BLUE}{Style.BRIGHT}│
{Fore.BLUE}{Style.BRIGHT}└────────────────────────────────────────────────────────────┘{Fore.WHITE}{Style.BRIGHT}
"""



def add_book(
    book_id,
    title,
    cpys,
    image_url,
    ISBN,
    publication_year,
    description,
    ddc_classification,
    publication_date,
    language,
    price,
    publication_details,
    edition,
    document_type,
    online_access,
):
    try:
        if not image_url:
            image_url = None
        if not ISBN:
            ISBN = None
        if not publication_year:
            publication_year = None
        if not description:
            description = None
        if not ddc_classification:
            ddc_classification = None
        if not publication_details:
            publication_details = None
        if not online_access:
            online_access = None
        if not edition:
            edition = None
        if not document_type:
            document_type = None
        if not publication_date:
            publication_date = None
        if not language:
            language = None
        if not price:
            price = None
        if not title and book_id:
            print("Title and Book ID is a required field for a book.")
            return
        insert_query = """
        INSERT INTO books (book_id, title, image_url, ISBN, publication_year, copies_available_to_draw, total_copies, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        mycursor.execute(
            insert_query,
            (
                book_id,
                title,
                image_url,
                ISBN,
                publication_year,
                cpys,
                cpys,
                description,
                ddc_classification,
                publication_date,
                language,
                price,
                publication_details,
                edition,
                document_type,
                online_access,
            ),
        )
        conn.commit()
        print(f"Book '{title}' with ID {book_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a book:", e)


def add_ebook(
    book_id,
    title,
    image_url,
    ISBN,
    publication_year,
    description,
    ddc_classification,
    publication_date,
    language,
    price,
    publication_details,
    edition,
    document_type,
    online_access,
):
    try:
        if not image_url:
            image_url = None
        if not ISBN:
            ISBN = None
        if not publication_year:
            publication_year = None
        if not description:
            description = None
        if not ddc_classification:
            ddc_classification = None
        if not publication_details:
            publication_details = None
        if not online_access:
            online_access = None
        if not edition:
            edition = None
        if not document_type:
            document_type = None
        if not publication_date:
            publication_date = None
        if not language:
            language = None
        if not price:
            price = None
        if not title and book_id:
            print("Title and Book ID is a required field for a E-book.")
            return
        insert_query = """
        INSERT INTO ebooks (book_id, title, image_url, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        mycursor.execute(
            insert_query,
            (
                book_id,
                title,
                image_url,
                ISBN,
                publication_year,
                description,
                ddc_classification,
                publication_date,
                language,
                price,
                publication_details,
                edition,
                document_type,
                online_access,
            ),
        )
        conn.commit()
        print(f"Book '{title}' with ID {book_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a book:", e)


def faculty_checkout_search(sid):
    try:
        query = """SELECT sc.checkout_id,
                sc.checkout_date,
                sc.due_date,
                sc.renewal_count,
                sc.return_date,
                b.book_id,
                b.title AS book_title
                FROM faculty_checkouts sc
                JOIN books b ON sc.book_id = b.book_id
                WHERE sc.faculty_id = %s;
                """
        mycursor.execute(query, (sid,))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No matching records found.")
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def student_checkout_search(sid):
    try:
        query = """SELECT sc.checkout_id,
                sc.checkout_date,
                sc.due_date,
                sc.renewal_count,
                sc.return_date,
                b.book_id,
                b.title AS book_title
                FROM student_checkouts sc
                JOIN books b ON sc.book_id = b.book_id
                WHERE sc.student_id = %s;
                """
        mycursor.execute(query, (sid,))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No matching records found.")
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def overdue_search():
    try:
        query = """SELECT fc.checkout_id, fc.faculty_id AS borrower_id, fc.book_id, fc.due_date, 'Faculty' AS borrower_type, f.faculty_name AS borrower_name, CASE WHEN fc.due_date < CURRENT_DATE THEN CURRENT_DATE - fc.due_date ELSE 0 END AS days_overdue FROM faculty_checkouts fc LEFT JOIN faculty f ON fc.faculty_id = f.faculty_id WHERE fc.due_date < CURRENT_DATE AND fc.return_date IS NULL UNION ALL SELECT sc.checkout_id, sc.student_id AS borrower_id, sc.book_id, sc.due_date, 'Student' AS borrower_type, s.student_name AS borrower_name, CASE WHEN sc.due_date < CURRENT_DATE THEN CURRENT_DATE - sc.due_date ELSE 0 END AS days_overdue FROM student_checkouts sc LEFT JOIN student s ON sc.student_id = s.student_id WHERE sc.due_date < CURRENT_DATE AND sc.return_date IS NULL;"""
        mycursor.execute(query)
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No overdue books.")
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def document_type_search(inpdocument_type):
    try:
        query = """SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type,  online_access
                FROM books
                WHERE document_type = %s
                UNION
                SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM ebooks
                WHERE document_type = %s;"""
        mycursor.execute(query, (inpdocument_type, inpdocument_type))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print(
                "No records matching the specified document type were found in the database."
            )
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def author_search(author):
    try:
        query = """SELECT books.book_id, books.title
            	FROM books
            	JOIN book_author ON books.book_id = book_author.book_id
            	JOIN author ON book_author.author_id = author.author_id
            	WHERE author.author_name = %s;"""
        mycursor.execute(query, (author,))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No books matching the author were found in the database.")

    except psycopg2.Error as e:
        print(e)


def subject_search(subject):
    try:
        query = """SELECT books.book_id, books.title
							FROM books
							JOIN subject_books ON books.book_id = subject_books.book_id
							JOIN subjects ON subject_books.subject_id = subjects.subject_id
							WHERE subjects.subject_name = %s;"""
        mycursor.execute(query, (subject,))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No books matching the subject were found in the database.")

    except psycopg2.Error as e:
        print(e)


def avgrating_search(avg_rating):
    try:
        query = """SELECT books.book_id, books.title, ROUND(AVG(rating.rating), 2) AS average_rating
							FROM books
							LEFT JOIN rating ON books.book_id = rating.book_id
							GROUP BY books.book_id, books.title
							HAVING AVG(rating.rating) >= %s
							ORDER BY average_rating DESC;"""
        mycursor.execute(query, (avg_rating,))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No books above the rating were found in the database.")

    except psycopg2.Error as e:
        print(e)


def popular_books():
    try:
        query = """SELECT books.book_id, books.title, COUNT(*) AS total_checkouts
							FROM books
							LEFT JOIN faculty_checkouts ON books.book_id = faculty_checkouts.book_id
							LEFT JOIN student_checkouts ON books.book_id = student_checkouts.book_id
							GROUP BY books.book_id, books.title
							ORDER BY total_checkouts DESC;"""
        mycursor.execute(query)
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
    except psycopg2.Error as e:
        print(e)


def copycount(book_id):
    try:
        query = """SELECT copies_available_to_draw
							FROM books
							WHERE book_id = %s;"""
        mycursor.execute(query, (book_id,))
        results = mycursor.fetchall()
        if results[0][0] > 0:
            print("There are %s copies available at the moment.\n" % results[0][0])
        else:
            print(
                "There are no copies of the requested book available at the moment.\n"
            )

    except psycopg2.Error as e:
        print(e)


def name_search(name):
    try:
        query = """SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM books
                WHERE title LIKE %s
                UNION
                SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM ebooks
                WHERE title LIKE %s;"""
        mycursor.execute(query, ("%" + name + "%", "%" + name + "%"))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No records matching the specified name were found in the database.")
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def language_search(inplang):
    try:
        query = """SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM books
                WHERE language = %s
                UNION
                SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM ebooks
                WHERE language = %s;"""
        mycursor.execute(query, (inplang, inplang))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print(
                "No records matching the specified language were found in the database."
            )
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def edition_search(edition):
    try:
        query = """SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM books
                WHERE edition = %s
                UNION
                SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM ebooks
                WHERE edition = %s;"""
        mycursor.execute(query, (edition, edition))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No records with the specified edition were found in the database.")
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def publication_year_search():
    try:
        query = """ SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM books WHERE publication_year = %s
                UNION
                SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM ebooks WHERE publication_year = %s;"""
        mycursor.execute(query, (inpyear, inpyear))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print(
                "No records with the specified publication year were found in the database."
            )
    except psycopg2.Error as e:
        print("An error occurred while searching for records:", e)


def add_student(student_id, student_name, phone, email, enrollment_date, dept_id):
    try:
        if not student_id or not student_name or not enrollment_date or not dept_id:
            print(
                "Student ID, Name, Enrollment Date, and Department are required fields."
            )
            return
        phone = phone or None
        email = email or None
        query = """
        INSERT INTO student (student_id, student_name, phone, email, enrollment_date, dept_id)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        mycursor.execute(
            query, (student_id, student_name, phone, email, enrollment_date, dept_id)
        )
        conn.commit()
        print(f"Student {student_name} with ID {student_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a student:", e)


def borrow_or_renew(bid, sid):
    mycursor.execute("BEGIN;")
    check = "SELECT COUNT(*) FROM student WHERE student_id = %s"
    mycursor.execute(check, (sid,))
    res = mycursor.fetchall()
    if res[0][0] <= 0:
        print("No matching student found with the given ID.")
        return
    check = "SELECT COUNT(*) FROM books WHERE book_id = %s"
    mycursor.execute(check, (bid,))
    res = mycursor.fetchall()
    if res[0][0] <= 0:
        print("No matching books found with the given ID.")
        return
    check = "SELECT COUNT(*) FROM books WHERE book_id = %s AND copies_available_to_draw > 0;"
    mycursor.execute(check, (bid,))
    res = mycursor.fetchall()
    if res[0][0] <= 0:
        print("No copies of requested book available to draw.")
        return
    # do count is 0,1,2 and renewing or count is 0,1 and not renewing check
    check = "SELECT COUNT(*) FROM student_checkouts WHERE student_id = %s AND return_date IS NULL;"
    mycursor.execute(check, (sid,))
    res = mycursor.fetchall()
    if res[0][0] == 2:
        check = "SELECT COUNT(*) FROM student_checkouts WHERE student_id = %s AND book_id = %s AND return_date IS NULL"
        mycursor.execute(check, (sid, bid))
        res = mycursor.fetchall()
        if res[0][0] == 0:
            print("Cannot borrow more than 2 books at a time.")
            return
        else:
            query = """UPDATE student_checkouts SET return_date = NOW() WHERE student_id = %s AND book_id = %s AND return_date IS NULL;
                        INSERT INTO student_checkouts (student_id, book_id, due_date, checkout_date, renewal_count) VALUES (%s, %s, NOW() + INTERVAL '2 weeks', NOW(), (select renewal_count FROM student_checkouts WHERE student_id = %s AND book_id = %s order by renewal_count desc limit 1) + 1);
                        """
            params = (sid, bid, sid, bid, sid, bid)
            try:
                mycursor.execute(query, params)
                conn.commit()
                check = "SELECT count(*) FROM student_checkouts WHERE student_id = %s AND book_id = %s AND return_date IS NULL"
                mycursor.execute(check, (sid, bid))
                res = mycursor.fetchall()
                if res[0][0] >= 1:
                    print("Book renewed successfully.")
                    return
                else:
                    print("Book borrowed successfully.")
                return
            except psycopg2.Error as e:
                print(e)
                return
    elif res[0][0] < 2:
        query = """DO $$ 
        BEGIN 
            IF EXISTS (SELECT 1 FROM books WHERE book_id = %s AND copies_available_to_draw > 0) THEN
                IF (SELECT COUNT(*) FROM student_checkouts WHERE student_id = %s AND return_date IS NULL) < 2 THEN
                    IF EXISTS (SELECT 1 FROM student WHERE student_id = %s) AND EXISTS (SELECT 1 FROM books WHERE book_id = %s) THEN
                        IF EXISTS (SELECT 1 FROM student_checkouts WHERE student_id = %s AND book_id = %s AND return_date IS NULL) THEN
                            UPDATE student_checkouts SET return_date = NOW() WHERE student_id = %s AND book_id = %s AND return_date IS NULL;
                            INSERT INTO student_checkouts (student_id, book_id, due_date, checkout_date, renewal_count) VALUES (%s, %s, NOW() + INTERVAL '2 weeks', NOW(), (select renewal_count FROM student_checkouts WHERE student_id = %s AND book_id = %s order by renewal_count desc limit 1) + 1);
                        ELSE
                            INSERT INTO student_checkouts (student_id, book_id, due_date, checkout_date) VALUES (%s, %s, NOW() + INTERVAL '2 weeks', NOW());
                            UPDATE books SET copies_available_to_draw = copies_available_to_draw - 1 WHERE book_id = %s;
                        END IF;
                    END IF;
                END IF;
            END IF;
        END $$;"""
        params = (
            bid,
            sid,
            sid,
            bid,
            sid,
            bid,
            sid,
            bid,
            sid,
            bid,
            sid,
            bid,
            sid,
            bid,
            bid,
        )
        try:
            mycursor.execute(query, params)
            conn.commit()
            check = "SELECT count(*) FROM student_checkouts WHERE student_id = %s AND book_id = %s AND return_date IS NULL"
            mycursor.execute(check, (sid, bid))
            res = mycursor.fetchall()
            print("Book borrowed successfully.")
            return
        except psycopg2.Error as e:
            print(e)
            return
    else:
        print("Cannot borrow more than 2 books at a time.")
        return


def retbook(bid, sid):
    mycursor.execute("BEGIN;")
    retcheck = "SELECT COUNT(*) FROM student_checkouts WHERE student_id = %s AND book_id = %s AND return_date is null;"
    mycursor.execute(retcheck, (sid, bid))
    ret = mycursor.fetchall()
    if ret[0][0] > 0:
        returns = "UPDATE student_checkouts SET return_date = NOW()::DATE where book_id = %s and student_id = %s and return_date IS NULL;"
        params = (bid, sid)
        try:
            mycursor.execute(returns, params)
            conn.commit()
        except psycopg2.Error as e:
            print(e)
        q1 = "SELECT copies_available_to_draw FROM books WHERE book_id = %s;"
        mycursor.execute(q1, (bid,))
        book_count = mycursor.fetchall()
        avail_copies = book_count[0][0]
        newcopycount = avail_copies + 1
        copyincrease = (
            "UPDATE books SET copies_available_to_draw = %s where book_id = %s ;"
        )
        mycursor.execute(copyincrease, (newcopycount, bid))
        conn.commit()
        print("Book returned successfully.")
    else:
        print(
            f"No records found for student ID {sid} and book ID {bid} in the return list."
        )
    return


def book_exists(book_id):
    query = "SELECT 1 FROM books WHERE book_id = %s"
    mycursor.execute(query, (book_id,))
    return mycursor.fetchone() is not None


def book_exists(book_id):
    query = "SELECT 1 FROM ebooks WHERE book_id = %s"
    mycursor.execute(query, (book_id,))
    return mycursor.fetchone() is not None


def add_rating(rating, book_id):
    try:
        if not book_exists(book_id):
            print(f"Book with ID {book_id} does not exist.")
            return

        query = """
        INSERT INTO rating (rating, book_id)
        VALUES (%s, %s);
        """
        mycursor.execute(query, (rating, book_id))
        conn.commit()
        print(f"Rating {rating} for Book ID {book_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a rating:", e)


def add_ebook_rating(rating, book_id):
    try:
        if not book_exists(book_id):
            print(f"E-Book with ID {book_id} does not exist.")
            return

        query = """
        INSERT INTO e_rating (rating, book_id)
        VALUES (%s, %s);
        """
        mycursor.execute(query, (rating, book_id))
        conn.commit()
        print(f"Rating {rating} for E-Book ID {book_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a rating:", e)


def ISBN_search(inpisbn):
    try:
        query = """SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM books
                WHERE isbn = %s
                UNION
                SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM ebooks
                WHERE isbn = %s LIMIT 1;"""
        mycursor.execute(query, (inpisbn, inpisbn))
        results = mycursor.fetchall()
        if results:
            rows = []
            headers = [
                "Book ID:",
                "Title:",
                "Image URL:",
                "ISBN:",
                "Publication Year:",
                "Description:",
                "DDC Classification:",
                "Publication Date:",
                "Language:",
                "Price:",
                "Publication Details:",
                "Edition:",
                "Document Type:",
                "Online Access:",
            ]
            for row in results:
                for i in range(len(row)):
                    rows.append([headers[i], row[i]])
            print("\n  Book Details: ")
            print(tabulate(rows, tablefmt="grid"))
        else:
            print("ISBN not found in the database.")
    except psycopg2.Error as e:
        print(e)


def price_search(min, max):
    try:
        query = """SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM books
                WHERE price between %s AND %s
                UNION
                SELECT book_id, title, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access
                FROM ebooks
                WHERE price BETWEEN %s AND %s;"""
        mycursor.execute(query, (min, max, min, max))
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print(
                "No books matching the specified price range were found in the database."
            )
    except psycopg2.Error as e:
        print(e)


def subject_book_exists(subject_id, book_id):
    query = "SELECT 1 FROM subject_books WHERE subject_id = %s AND book_id = %s"
    mycursor.execute(query, (subject_id, book_id))
    return mycursor.fetchone() is not None


def add_subject_book(subject_id, book_id):
    try:
        if not subject_book_exists(subject_id, book_id):
            query = """
            INSERT INTO subject_books (subject_id, book_id)
            VALUES (%s, %s);
            """
            mycursor.execute(query, (subject_id, book_id))
            conn.commit()
            print(
                f"Subject with ID {subject_id} and Book with ID {book_id} have been associated."
            )
        else:
            print(
                f"Subject with ID {subject_id} and Book with ID {book_id} are already associated."
            )
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a subject book association:", e)


def view_checked_out_books():
    try:
        query = """
        SELECT fc.checkout_id, fc.faculty_id AS borrower_id, fc.book_id, fc.due_date, 
               'Faculty' AS borrower_type, f.faculty_name AS borrower_name
        FROM faculty_checkouts fc
        LEFT JOIN faculty f ON fc.faculty_id = f.faculty_id
        WHERE fc.return_date IS NULL
        UNION ALL
        SELECT sc.checkout_id, sc.student_id AS borrower_id, sc.book_id, sc.due_date, 
               'Student' AS borrower_type, s.student_name AS borrower_name
        FROM student_checkouts sc
        LEFT JOIN student s ON sc.student_id = s.student_id
        WHERE sc.return_date IS NULL;
        """
        mycursor.execute(query)
        results = mycursor.fetchall()
        if results:
            headers = [desc[0] for desc in mycursor.description]
            formatted_results = [list(row) for row in results]
            print(tabulate(formatted_results, headers, tablefmt="pretty"))
        else:
            print("No books are currently checked out.")
    except psycopg2.Error as e:
        print("An error occurred while retrieving checked-out books:", e)


def author_exists(author_id):
    query = "SELECT 1 FROM author WHERE author_id = %s"
    mycursor.execute(query, (author_id,))
    return mycursor.fetchone() is not None


def get_average_rating(book_id):
    try:
        mycursor.execute("SELECT 1 FROM books WHERE book_id = %s", (book_id,))
        if not mycursor.fetchone():
            print(f"Book with ID {book_id} does not exist.")
            return
        mycursor.execute(
            "SELECT AVG(rating) FROM rating WHERE book_id = %s", (book_id,)
        )
        average_rating = mycursor.fetchone()[0]
        if average_rating is not None:
            print(f"The average rating for Book ID {book_id} is: {average_rating:.2f}")
        else:
            print(f"No ratings found for Book ID {book_id}")
    except psycopg2.Error as e:
        print("An error occurred:", e)


def add_author(author_id, author_name):
    try:
        if not author_name:
            print("Author Name is a required field for an author.")
            return
        if author_exists(author_id):
            print(f"An author with ID {author_id} already exists.")
            return

        query = """
        INSERT INTO author (author_id, author_name)
        VALUES (%s, %s);
        """
        mycursor.execute(query, (author_id, author_name))
        conn.commit()
        print(f"Author '{author_name}' with ID {author_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding an author:", e)


def book_author_exists(book_id, author_id):
    query = "SELECT 1 FROM book_author WHERE book_id = %s AND author_id = %s"
    mycursor.execute(query, (book_id, author_id))
    return mycursor.fetchone() is not None


def subject_exists(subject_id):
    query = "SELECT 1 FROM subjects WHERE subject_id = %s"
    mycursor.execute(query, (subject_id,))
    return mycursor.fetchone() is not None


def add_subject(subject_id, subject_name):
    try:
        if not subject_name:
            print("Subject Name is a required field for a subject.")
            return
        if subject_exists(subject_id):
            print(f"A subject with ID {subject_id} already exists.")
            return

        query = """
        INSERT INTO subjects (subject_id, subject_name)
        VALUES (%s, %s);
        """
        mycursor.execute(query, (subject_id, subject_name))
        conn.commit()
        print(f"Subject '{subject_name}' with ID {subject_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a subject:", e)

         
def create_menu(title, options):
    menu = f"""
{Fore.BLUE}{Style.BRIGHT}┌─────────────────────────────────────────────┐
│{Fore.MAGENTA}{Style.BRIGHT} {title} {Fore.BLUE}{Style.BRIGHT}                           │
│                                             │
{Fore.BLUE}{Style.BRIGHT}│{Fore.CYAN}{Style.BRIGHT} Enter the respective numbers to perform     {Fore.BLUE}{Style.BRIGHT}│
{Fore.BLUE}{Style.BRIGHT}│{Fore.CYAN}{Style.BRIGHT} the required task:                          {Fore.BLUE}{Style.BRIGHT}│
│                                             │
"""

    for index, option in enumerate(options, start=1):
        menu += f"{Fore.YELLOW}{Style.BRIGHT}│   {index}. {option} {Fore.BLUE}{Style.BRIGHT}│\n"

    menu += (
        f"{Fore.BLUE}{Style.BRIGHT}│                                             │\n"
    )
    menu += f"{Fore.BLUE}{Style.BRIGHT}└─────────────────────────────────────────────┘{Style.RESET_ALL}\n {Fore.WHITE}{Style.BRIGHT}"

    return menu


def add_book_author(book_id, author_id):
    try:
        if not book_author_exists(book_id, author_id):
            query = """
            INSERT INTO book_author (book_id, author_id)
            VALUES (%s, %s);
            """
            mycursor.execute(query, (book_id, author_id))
            conn.commit()
            print(
                f"Book with ID {book_id} and Author with ID {author_id} have been associated."
            )
        else:
            print(
                f"Book with ID {book_id} and Author with ID {author_id} are already associated."
            )
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a book author association:", e)


def add_faculty(faculty_id, faculty_name, office_location, dept_id, office_phone):
    try:
        if not faculty_id or not faculty_name or not dept_id:
            print("Faculty ID, Name, and Department are required fields.")
            return
        office_location = office_location or None
        query = """
        INSERT INTO faculty (faculty_id, faculty_name, office_location, dept_id)
        VALUES (%s, %s, %s, %s);
        """
        mycursor.execute(query, (faculty_id, faculty_name, office_location, dept_id))
        conn.commit()
        if office_phone:
            phone_query = """
            INSERT INTO faculty_office_phone (office_phone, faculty_id)
            VALUES (%s, %s);
            """
            mycursor.execute(phone_query, (office_phone, faculty_id))
            conn.commit()
        print(f"Faculty {faculty_name} with ID {faculty_id} has been added.")
    except psycopg2.Error as e:
        conn.rollback()
        print("An error occurred while adding a faculty member:", e)


running = True
while running:
    try:
        option = input(menu)

        if option == "1":
            try:
                sid = int(input("Enter Student ID: "))
                check1 = "SELECT * FROM student WHERE student_id = %s;"
                mycursor.execute(check1, (sid,))
                student = mycursor.fetchall()
                if not student:
                    print("Student not on the database")
                    conn.rollback()
                    exit()
                bid = int(input("Enter Book ID: "))
                check2 = "SELECT * FROM books WHERE book_id = %s;"
                mycursor.execute(check2, (bid,))
                book = mycursor.fetchall()
                if not book:
                    print("Invalid Book")
                    conn.rollback()
                borrow_or_renew(bid, sid)
            except psycopg2.Error as e:
                print(e)
        if option == "2":
            try:
                sid = int(input("Enter Student ID: "))
                check1 = "SELECT * FROM student WHERE student_id = %s;"
                mycursor.execute(check1, (sid,))
                student = mycursor.fetchall()
                if not student:
                    print("Student not on the database")
                    conn.rollback()
                    exit()
                bid = int(input("Enter Book ID: "))
                check2 = "SELECT * FROM books WHERE book_id = %s;"
                mycursor.execute(check2, (bid,))
                book = mycursor.fetchall()
                if not book:
                    print("Invalid Book")
                    conn.rollback()
                    exit()
                retbook(bid, sid)

            except psycopg2.Error as e:
                print(e)
        if option == "3":
            criteria_menu = f"""
{Fore.BLUE}{Style.BRIGHT}┌────────────────────────────────────────┐
│{Style.RESET_ALL}     {Fore.BLUE}{Style.BRIGHT}Retrieve books based on:{Style.RESET_ALL}           {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 1. Name{Style.RESET_ALL}                                {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 2. Publication Year{Style.RESET_ALL}                    {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 3. Language{Style.RESET_ALL}                            {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 4. Price range{Style.RESET_ALL}                         {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 5. Edition{Style.RESET_ALL}                             {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 6. Document Type{Style.RESET_ALL}                       {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 7. ISBN{Style.RESET_ALL}                                {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 8. Author{Style.RESET_ALL}                              {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 9. Subject{Style.RESET_ALL}                             {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 10. Average Rating{Style.RESET_ALL}                     {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 11. Popularity{Style.RESET_ALL}                         {Fore.BLUE}{Style.BRIGHT}│
└────────────────────────────────────────┘{Fore.WHITE}{Style.BRIGHT}
"""
            basedon = input(criteria_menu)
            if basedon == "1":
                name = input("Enter Relevant Name: ")
                name_search(name)
            if basedon == "2":
                inpyear = input("Enter the publication year you want to search for: \n")
                publication_year_search()
            if basedon == "3":
                query = "SELECT DISTINCT(language) FROM books UNION SELECT DISTINCT(language) FROM ebooks;"
                mycursor.execute(query)
                print("Available languages in the database:")
                for row in mycursor.fetchall():
                    language = row[0]
                    print(f"- {language}")
                inplang = input("Enter the language of the books you are looking for: ")
                language_search(inplang)
            if basedon == "4":
                min = int(input("Enter the minimum price: "))
                max = int(input("Enter the maximum price: "))
                price_search(min, max)
            if basedon == "5":
                edition = input(
                    "Enter the edition: For example, 1st Edition, 2nd Edition\n"
                )
                edition_search(edition)
            if basedon == "6":
                query = "SELECT DISTINCT(document_type) FROM books UNION SELECT DISTINCT(document_type) FROM ebooks;"
                mycursor.execute(query)
                print("Available document types in the database:")
                for row in mycursor.fetchall():
                    dt = row[0]
                    print(f"- {dt}")
                inpdocument_type = input("Enter the document type: ")
                document_type_search(inpdocument_type)
            if basedon == "7":
                inpisbn = input("Enter ISBN: \n")
                ISBN_search(inpisbn)
            if basedon == "8":
                query = (
                    "SELECT DISTINCT(author_name) FROM author NATURAL JOIN book_author;"
                )
                mycursor.execute(query)
                print("Authors whose books are available in the library:")
                for row in mycursor.fetchall():
                    dt = row[0]
                    print(f"- {dt}")
                inpauthor = input("Enter the author name: ")
                author_search(inpauthor)
            if basedon == "9":
                query = "SELECT DISTINCT(subject_name) FROM subjects NATURAL JOIN subject_books;"
                mycursor.execute(query)
                print("Enter the subject name: ")
                for row in mycursor.fetchall():
                    dt = row[0]
                    print(f"- {dt}")
                inpsub = input("Enter the subject name: ")
                subject_search(inpsub)
            if basedon == "10":
                inprating = input(
                    "Enter the minimum rating you are interested in for the books you are looking for: "
                )
                avgrating_search(inprating)
            if basedon == "11":
                popular_books()
        if option == "4":
            info = input(
                create_menu(
                    "Book Information",
                    [
                        "List of overdue books                 ",
                        "Student Checkout Details              ",
                        "Faculty Checkout Details              ",
                        "View Checked-out Books                ",
                        "View average rating for a book        ",
                        "View average rating for an E-Book     ",
                        "View available copies for a book      ",
                    ],
                )
            )

            if info == "1":
                overdue_search()
            if info == "2":
                sid = int(input("Enter Student ID: "))
                student_checkout_search(sid)
            if info == "3":
                sid = int(input("Enter Faculty ID: "))
                faculty_checkout_search(sid)
            if info == "4":
                view_checked_out_books()
            if info == "5":
                try:
                    book_id = int(input("Enter Book ID: "))
                    get_average_rating(book_id)
                except ValueError:
                    print("Invalid input. Please enter a valid Book ID as an integer.")
            if info == "6":
                try:
                    book_id = int(input("Enter E-Book ID: "))
                    get_average_rating(book_id)
                except ValueError:
                    print(
                        "Invalid input. Please enter a valid E-Book ID as an integer."
                    )
            if info == "7":
                try:
                    book_id = int(input("Enter Book ID: "))
                    copycount(book_id)
                except ValueError:
                    print("Invalid input. Please enter a valid Book ID as an integer.")
        if option == "5":
            add_records_menu = f"""
{Fore.BLUE}{Style.BRIGHT}┌────────────────────────────────────┐
│{Style.RESET_ALL}        {Fore.BLUE}{Style.BRIGHT}Add Records:{Style.RESET_ALL}                {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 1. Add a student{Style.RESET_ALL}                   {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 2. Add faculty member{Style.RESET_ALL}              {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 3. Add a Book{Style.RESET_ALL}                      {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 4. Add an E-book{Style.RESET_ALL}                   {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 5. Add author{Style.RESET_ALL}                      {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 6. Associate a Book with an Author{Style.RESET_ALL} {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 7. Add a subject{Style.RESET_ALL}                   {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 8. Associate a book with a subject{Style.RESET_ALL} {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 9. Add a rating{Style.RESET_ALL}                    {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 10. Add an E-Book rating{Style.RESET_ALL}           {Fore.BLUE}{Style.BRIGHT}│
└────────────────────────────────────┘{Fore.WHITE}{Style.BRIGHT}
"""
            info = input(add_records_menu)
            if info == "1":
                student_id = input("Enter Student's ID: ")
                student_name = input("Enter Student's Name: ")
                phone = input("Enter Phone: ")
                email = input("Enter Email: ")
                enrollment_date = input("Enter Enrollment Date (YYYY-MM-DD): ")
                dept_id = input("Enter Department ID: ")
                add_student(
                    student_id, student_name, phone, email, enrollment_date, dept_id
                )
            if info == "2":
                faculty_id = input("Enter Faculty's ID: ")
                faculty_name = input("Enter Faculty's Name: ")
                office_location = input("Enter Office Location: ")
                dept_id = input("Enter Department ID: ")
                office_phone = input("Enter Office Phone: ")
                add_faculty(
                    faculty_id, faculty_name, office_location, dept_id, office_phone
                )
            if info == "3":
                book_id = input("Enter Book ID: ")
                check_query = "SELECT 1 FROM books WHERE book_id = %s"
                mycursor.execute(check_query, (book_id,))
                if mycursor.fetchone():
                    print(f"Book with ID {book_id} already exists.")
                else:
                    title = input("Enter Title: ")
                    image_url = input("Enter Image URL: ")
                    ISBN = input("Enter ISBN: ")
                    publication_year = input("Enter Publication Year: ")
                    description = input("Enter Description: ")
                    cpys = input("Enter Number of Copies: ")
                    ddc_classification = input("Enter DDC Classification: ")
                    publication_date = input("Enter Publication Date (YYYY-MM-DD): ")
                    language = input("Enter Language: ")
                    price = input("Enter Price: ")
                    publication_details = input("Enter Publication Details: ")
                    edition = input("Enter Edition: ")
                    document_type = input("Enter Document Type: ")
                    online_access = input("Enter Online Access: ")
                    add_book(
                        book_id,
                        title,
                        cpys,
                        image_url,
                        ISBN,
                        publication_year,
                        description,
                        ddc_classification,
                        publication_date,
                        language,
                        price,
                        publication_details,
                        edition,
                        document_type,
                        online_access,
                    )
            if info == "4":
                book_id = input("Enter E-Book ID: ")
                check_query = "SELECT 1 FROM ebooks WHERE book_id = %s"
                mycursor.execute(check_query, (book_id,))
                if mycursor.fetchone():
                    print(f"Book with ID {book_id} already exists.")
                else:
                    title = input("Enter Title: ")
                    image_url = input("Enter Image URL: ")
                    ISBN = input("Enter ISBN: ")
                    publication_year = input("Enter Publication Year: ")
                    description = input("Enter Description: ")
                    ddc_classification = input("Enter DDC Classification: ")
                    publication_date = input("Enter Publication Date (YYYY-MM-DD): ")
                    language = input("Enter Language: ")
                    price = input("Enter Price: ")
                    publication_details = input("Enter Publication Details: ")
                    edition = input("Enter Edition: ")
                    document_type = input("Enter Document Type: ")
                    online_access = input("Enter Online Access: ")
                    add_ebook(
                        book_id,
                        title,
                        image_url,
                        ISBN,
                        publication_year,
                        description,
                        ddc_classification,
                        publication_date,
                        language,
                        price,
                        publication_details,
                        edition,
                        document_type,
                        online_access,
                    )
            if info == "5":
                author_id = input("Enter Author ID: ")
                author_name = input("Enter Author Name: ")
                add_author(author_id, author_name)
            if info == "6":
                book_id = input("Enter Book ID: ")
                author_id = input("Enter Author ID: ")
                add_book_author(book_id, author_id)
            if info == "7":
                subject_id = input("Enter Subject ID: ")
                subject_name = input("Enter Subject Name: ")
                add_subject(subject_id, subject_name)
            if info == "8":
                subject_id = input("Enter Subject ID: ")
                book_id = input("Enter Book ID: ")
                add_subject_book(subject_id, book_id)
            if info == "9":
                book_id = input("Enter Book ID: ")
                rating = input("Enter Rating (e.g., 4.50): ")
                add_rating(rating, book_id)
            if info == "10":
                book_id = input("Enter E-Book ID: ")
                rating = input("Enter Rating (e.g., 4.50): ")
                add_ebook_rating(rating, book_id)
        if option == "6":
            add_records_menu = f"""
{Fore.BLUE}{Style.BRIGHT}┌──────────────────────────────────────────┐
│{Style.RESET_ALL}        {Fore.BLUE}{Style.BRIGHT}Add Records:{Style.RESET_ALL}                      {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 1. Delete a student{Style.RESET_ALL}                      {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 2. Delete faculty member{Style.RESET_ALL}                 {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 3. Delete a Book{Style.RESET_ALL}                         {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 4. Delete an E-book{Style.RESET_ALL}                      {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 5. Delete author{Style.RESET_ALL}                         {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 6. Delete records for book-author table{Style.RESET_ALL}  {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 7. Delete a subject{Style.RESET_ALL}                      {Fore.BLUE}{Style.BRIGHT}│
│{Fore.YELLOW} 8. Delete records for subject-book table{Style.RESET_ALL} {Fore.BLUE}{Style.BRIGHT}│
└──────────────────────────────────────────┘{Fore.WHITE}{Style.BRIGHT}
"""
            
            info = input(add_records_menu)
            if info == "1":
                id = input("Enter Student ID: ")
                query = """DELETE FROM student WHERE student_id = %s;"""
                mycursor.execute(query, (id,))
                conn.commit()
            elif info == "2":
                id = input("Enter Faculty ID: ")
                query = """DELETE FROM faculty WHERE faculty_id = %s;"""
                mycursor.execute(query, (id,))
                conn.commit()
            elif info == "3":
                id = input("Enter Book ID: ")
                query = """DELETE FROM books WHERE book_id = %s;"""
                mycursor.execute(query, (id,))
                conn.commit()
            elif info == "4":
                id = input("Enter E-Book ID: ")
                query = """DELETE FROM ebooks WHERE book_id = %s;"""
                mycursor.execute(query, (id,))
                conn.commit()
            elif info == "5":
                id = input("Enter Author ID: ")
                query = """DELETE FROM author WHERE author_id = %s;"""
                mycursor.execute(query, (id,))
                conn.commit()
            elif info == "6":
                id1 = input("Enter Author ID: ")
                id2 = input("Enter Book ID: ")
                query = (
                    """DELETE FROM book_author WHERE author_id = %s AND book_id = %s;"""
                )
                mycursor.execute(query, (id1, id2))
                conn.commit()
            elif info == "7":
                id = input("Enter Subject ID: ")
                query = """DELETE FROM subjects WHERE subject_id = %s;"""
                mycursor.execute(query, (id,))
                conn.commit()
            elif info == "8":
                id1 = input("Enter Subject ID: ")
                id2 = input("Enter Book ID: ")
                query = """DELETE FROM subject_books WHERE subject_id = %s AND book_id = %s;"""
                mycursor.execute(query, (id1, id2))
                conn.commit()
            else:
                print("Invalid option. Please select a valid option from the menu.")
        if option == '7':
            running = False
    except psycopg2.Error as e:
        print(e)
conn.close()
mycursor.close()

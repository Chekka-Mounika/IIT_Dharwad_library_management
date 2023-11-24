import psycopg2

database_name = "librarydb"
user = "postgres"
password = "Mounika@2004"
connection = psycopg2.connect(database="postgres", user=user, password=password)
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE {database_name}")
cursor.close()
connection.close()
connection = psycopg2.connect(database=database_name, user=user, password=password)
cursor = connection.cursor()
create_table_query = """
CREATE TABLE department (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(dept_name)) > 0)
);

CREATE TABLE student (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(student_name)) > 0),
    phone VARCHAR(15),
    email VARCHAR(255),
    enrollment_date DATE NOT NULL,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE faculty (
    faculty_id INT PRIMARY KEY,
    faculty_name VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(faculty_name)) > 0),
    office_location VARCHAR(255),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id) 
);

CREATE TABLE faculty_office_phone (
    office_phone VARCHAR(20) PRIMARY KEY,
    faculty_id INT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(title)) > 0),
    image_url VARCHAR(255),
    ISBN VARCHAR(255),
    publication_year INT CHECK (publication_year >= 0),
    copies_available_to_draw INT CHECK (copies_available_to_draw >= 0) DEFAULT 0,
    total_copies INT NOT NULL CHECK (total_copies >= 0) DEFAULT 0,
    description TEXT,
    ddc_classification VARCHAR(255),
    publication_date DATE,
    language VARCHAR(255),
    price DECIMAL(10, 2) CHECK (price >= 0.00),
    publication_details VARCHAR(255),
    edition VARCHAR(255),
    document_type VARCHAR(255) CHECK (document_type IN ('Books', 'Audio Visual Material', 'Book Bank', 'Digital Media', 'E-Books', 'Periodical', 'Standards')),
    online_access VARCHAR(255)
);

CREATE TABLE ebooks (
    book_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(title)) > 0),
    image_url VARCHAR(255),
    ISBN VARCHAR(255),
    publication_year INT CHECK (publication_year >= 0),
    description TEXT,
    ddc_classification VARCHAR(255),
    publication_date DATE,
    language VARCHAR(255),
    price DECIMAL(10, 2) CHECK (price >= 0.00),
    publication_details VARCHAR(255),
    edition VARCHAR(255),
    document_type VARCHAR(255) CHECK (document_type IN ('Books', 'Audio Visual Material', 'Book Bank', 'Digital Media', 'E-Books', 'Periodical', 'Standards')),
    online_access VARCHAR(255)
);

CREATE TABLE author (
    author_id INT PRIMARY KEY,
    author_name VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(author_name)) > 0)
);

CREATE TABLE book_author (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (author_id) REFERENCES author(author_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE rating (
    rating DECIMAL(3, 2) CHECK (rating >= 0.00),
    book_id INT,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE faculty_checkouts (
    checkout_id SERIAL PRIMARY KEY,
    due_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    renewal_count INT DEFAULT 0,
    return_date DATE,
    faculty_id INT,
    book_id INT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE student_checkouts (
    checkout_id SERIAL PRIMARY KEY,
    due_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    renewal_count INT DEFAULT 0,
    return_date DATE,
    student_id INT,
    book_id INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE e_rating (
    book_id INT,
    rating DECIMAL(3, 2) CHECK (rating >= 0.00),
    FOREIGN KEY (book_id) REFERENCES ebooks(book_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE subjects (
    subject_id INT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL CHECK (LENGTH(TRIM(subject_name)) > 0)
);

CREATE TABLE subject_books (
    subject_id INT NOT NULL,
    book_id INT NOT NULL,
    PRIMARY KEY (subject_id, book_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE
); 
"""
cursor.execute(create_table_query)
insert_data_query = """
INSERT INTO department (dept_id, dept_name) VALUES
    (1, 'Computer Science'),
    (2, 'Mathematics'),
    (3, 'Physics'),
    (4, 'Biology'),
    (5, 'History'),
    (6, 'English'),
    (7, 'Chemistry'),
    (8, 'Economics'),
    (9, 'Psychology'),
    (10, 'Art');

INSERT INTO student (student_id, student_name, phone, email, enrollment_date, dept_id) VALUES
    (1, 'John Smith', '123-456-7890', 'john@example.com', '2022-09-01', 1),
    (2, 'Alice Johnson', '987-654-3210', 'alice@example.com', '2022-08-15', 2),
    (3, 'David Brown', '555-123-4567', 'david@example.com', '2022-09-10', 1),
    (4, 'Emily Davis', '111-222-3333', 'emily@example.com', '2022-08-30', 3),
    (5, 'Michael Wilson', '999-888-7777', 'michael@example.com', '2022-09-05', 4),
    (6, 'Sophia Miller', '444-555-6666', 'sophia@example.com', '2022-08-25', 2),
    (7, 'Daniel Lee', '777-888-9999', 'daniel@example.com', '2022-08-20', 3),
    (8, 'Olivia Clark', '222-333-4444', 'olivia@example.com', '2022-09-15', 1),
    (9, 'William Hall', '666-777-8888', 'william@example.com', '2022-09-05', 5),
    (10, 'Ava Scott', '333-222-1111', 'ava@example.com', '2022-08-30', 2);

INSERT INTO faculty (faculty_id, faculty_name, office_location, dept_id) VALUES
    (1, 'Professor Anderson', 'Room 101', 1),
    (2, 'Dr. Johnson', 'Room 201', 2),
    (3, 'Professor Davis', 'Room 102', 1),
    (4, 'Dr. Wilson', 'Room 202', 3),
    (5, 'Professor Smith', 'Room 103', 2),
    (6, 'Dr. Miller', 'Room 203', 4),
    (7, 'Professor Brown', 'Room 104', 3),
    (8, 'Dr. Clark', 'Room 204', 5),
    (9, 'Professor Lee', 'Room 105', 1),
    (10, 'Dr. Hall', 'Room 205', 4);

INSERT INTO faculty_office_phone (office_phone, faculty_id) VALUES
    ('555-111-1111', 1),
    ('555-222-2222', 2),
    ('555-333-3333', 3),
    ('555-444-4444', 4),
    ('555-555-5555', 5),
    ('555-666-6666', 6),
    ('555-777-7777', 7),
    ('555-888-8888', 8),
    ('555-999-9999', 9),
    ('555-000-0000', 10);

INSERT INTO books (book_id, title, image_url, ISBN, publication_year, copies_available_to_draw, total_copies, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access) VALUES
    (1, 'Introduction to Computer Science', 'image1.jpg', '978-1234567890', 2020, 5, 10, 'A comprehensive introduction to computer science.', 'QA76.6', '2020-01-15', 'English', 49.99, 'Publisher A', '1st Edition', 'Books', 'Yes'),
    (2, 'Calculus for Beginners', 'image2.jpg', '978-9876543210', 2019, 3, 7, 'A beginner-friendly calculus textbook.', 'QA303', '2019-05-20', 'English', 29.99, 'Publisher B', '2nd Edition', 'Books', 'No'),
    (3, 'Physics Fundamentals', 'image3.jpg', '978-5555555555', 2018, 7, 10, 'Fundamental principles of physics.', 'QC21', '2018-03-10', 'English', 39.99, 'Publisher C', '1st Edition', 'Books', 'Yes'),
    (4, 'Biology Basics', 'image4.jpg', '978-1111111111', 2021, 4, 8, 'An introduction to the basics of biology.', 'QH308', '2021-07-05', 'English', 34.99, 'Publisher D', '3rd Edition', 'Books', 'No'),
    (5, 'World History', 'image5.jpg', '978-9999999999', 2017, 6, 12, 'A comprehensive history book.', 'D21', '2017-02-01', 'English', 45.99, 'Publisher E', '4th Edition', 'Books', 'Yes'),
    (6, 'English Literature', 'image6.jpg', '978-3333333333', 2019, 4, 9, 'An anthology of English literature.', 'PR1109', '2019-10-10', 'English', 37.99, 'Publisher F', '2nd Edition', 'Books', 'No'),
    (7, 'Chemistry Basics', 'image7.jpg', '978-4444444444', 2020, 5, 11, 'A guide to the basics of chemistry.', 'QD33', '2020-04-20', 'English', 42.99, 'Publisher G', '1st Edition', 'Books', 'Yes'),
    (8, 'Economics 101', 'image8.jpg', '978-2222222222', 2018, 5, 10, 'A beginners guide to economics.', 'HB71', '2018-08-15', 'English', 32.99, 'Publisher H', '3rd Edition', 'Books', 'No'),
    (9, 'Psychology Essentials', 'image9.jpg', '978-8888888888', 2019, 6, 12, 'Essential concepts in psychology.', 'BF121', '2019-09-25', 'English', 36.99, 'Publisher I', '2nd Edition', 'Books', 'Yes'),
    (10, 'Art History', 'image10.jpg', '978-0000000000', 2021, 3, 7, 'An exploration of art through history.', 'N5300', '2021-12-12', 'English', 49.99, 'Publisher J', '1st Edition', 'Books', 'No');

INSERT INTO ebooks (book_id, title, image_url, ISBN, publication_year, description, ddc_classification, publication_date, language, price, publication_details, edition, document_type, online_access) VALUES
    (11, 'Programming with Python (E-Book)', 'ebook1.jpg', '978-9999999998', 2022, 'Learn Python programming from scratch.', 'QA76.73', '2022-03-01', 'English', 19.99, 'Publisher A', '1st Edition', 'E-Books', 'Yes'),
    (12, 'Algebra Made Easy (E-Book)', 'ebook2.jpg', '978-8888888887', 2021, 'A simplified guide to algebra.', 'QA154', '2021-06-15', 'English', 15.99, 'Publisher B', '2nd Edition', 'E-Books', 'Yes'),
    (13, 'Chemical Reactions (E-Book)', 'ebook3.jpg', '978-7777777776', 2022, 'Understanding chemical reactions.', 'QD101', '2022-02-10', 'English', 24.99, 'Publisher C', '1st Edition', 'E-Books', 'Yes'),
    (14, 'History of Ancient Civilizations (E-Book)', 'ebook4.jpg', '978-6666666665', 2021, 'Exploring ancient civilizations.', 'D60', '2021-09-20', 'English', 22.99, 'Publisher D', '3rd Edition', 'E-Books', 'Yes'),
    (15, 'Literary Classics (E-Book)', 'ebook5.jpg', '978-5555555554', 2022, 'A collection of literary classics.', 'PR1109', '2022-11-05', 'English', 21.99, 'Publisher E', '4th Edition', 'E-Books', 'Yes'),
    (16, 'Microeconomics Principles (E-Book)', 'ebook6.jpg', '978-4444444443', 2021, 'Principles of microeconomics.', 'HB171', '2021-08-05', 'English', 18.99, 'Publisher F', '2nd Edition', 'E-Books', 'Yes'),
    (17, 'Psychology of Human Behavior (E-Book)', 'ebook7.jpg', '978-3333333332', 2022, 'Understanding human behavior.', 'BF121', '2022-04-10', 'English', 23.99, 'Publisher G', '1st Edition', 'E-Books', 'Yes'),
    (18, 'Modern Art (E-Book)', 'ebook8.jpg', '978-2222222221', 2021, 'Exploring modern art trends.', 'N7500', '2021-12-25', 'English', 20.99, 'Publisher H', '3rd Edition', 'E-Books', 'Yes'),
    (19, 'Introduction to Astronomy (E-Book)', 'ebook9.jpg', '978-1111111110', 2022, 'Astronomy basics and discoveries.', 'QB44', '2022-07-15', 'English', 17.99, 'Publisher I', '2nd Edition', 'E-Books', 'Yes'),
    (20, 'World Geography (E-Book)', 'ebook10.jpg', '978-0000000009', 2022, 'Exploring the worlds geography.', 'G110', '2022-10-10', 'English', 19.99, 'Publisher J', '1st Edition', 'E-Books', 'Yes');

INSERT INTO author (author_id, author_name) VALUES
    (1, 'John Doe'),
    (2, 'Alice Smith'),
    (3, 'David Johnson'),
    (4, 'Emily Brown'),
    (5, 'Michael Wilson'),
    (6, 'Sophia Miller'),
    (7, 'Daniel Lee'),
    (8, 'Olivia Clark'),
    (9, 'William Hall'),
    (10, 'Ava Scott');

INSERT INTO book_author (book_id, author_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO rating (rating, book_id) VALUES
    (4.5, 1),
    (3.8, 2),
    (4.2, 3),
    (4.0, 4),
    (4.7, 5),
    (4.1, 6),
    (4.4, 7),
    (3.9, 8),
    (4.3, 9),
    (4.6, 10);

INSERT INTO faculty_checkouts (due_date, checkout_date, return_date, faculty_id, book_id) VALUES
    ('2023-01-15', '2023-01-02', '2023-01-10', 1, 1),
    ('2023-01-30', '2023-01-10', '2023-01-25', 2, 2),
    ('2023-02-15', '2023-02-01', '2023-02-10', 3, 3),
    ('2023-02-28', '2023-02-10', NULL, 4, 4),
    ('2023-03-15', '2023-03-01', NULL, 5, 5),
    ('2023-03-30', '2023-03-10', NULL, 6, 6),
    ('2023-04-15', '2023-04-01', NULL, 7, 7),
    ('2023-04-30', '2023-04-10', NULL, 8, 8),
    ('2023-05-15', '2023-05-01', NULL, 9, 9),
    ('2023-05-30', '2023-05-10', NULL, 10, 10);   

INSERT INTO e_rating (book_id, rating) VALUES
    (11, 4.2),
    (12, 3.9),
    (13, 4.0),
    (14, 4.3),
    (15, 4.7),
    (16, 4.1),
    (17, 4.5),
    (18, 3.8),
    (19, 4.4),
    (20, 4.6);

INSERT INTO subjects (subject_id, subject_name) VALUES
    (1, 'Computer Science'),
    (2, 'Mathematics'),
    (3, 'Physics'),
    (4, 'Biology'),
    (5, 'History'),
    (6, 'English'),
    (7, 'Chemistry'),
    (8, 'Economics'),
    (9, 'Psychology'),
    (10, 'Art');

INSERT INTO subject_books (subject_id, book_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO student_checkouts (due_date, checkout_date, return_date, renewal_count, student_id, book_id) VALUES
    ('2023-01-15', '2023-01-02', '2023-01-10', 0, 1, 1),
    ('2023-01-30', '2023-01-10', '2023-01-25', 1, 2, 2),
    ('2023-02-15', '2023-02-01', '2023-02-10', 0, 3, 3),
    ('2023-02-28', '2023-02-10', NULL, 0, 4, 4),
    ('2023-03-15', '2023-03-01', NULL, 0, 5, 5),
    ('2023-03-30', '2023-03-10', NULL, 0, 6, 6),
    ('2023-04-15', '2023-04-01', NULL, 0, 7, 7),
    ('2023-04-30', '2023-04-10', NULL, 0, 8, 8),
    ('2023-05-15', '2023-05-01', NULL, 0, 9, 9),
    ('2023-05-30', '2023-05-10', NULL, 0, 10, 10);
"""
cursor.execute(insert_data_query)
connection.commit()
cursor.close()
connection.close()

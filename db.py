import pymysql

# -------------------------------
# DATABASE CONFIGURATION
# -------------------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "YOUR_MYSQL_PASSWORD"
DB_NAME = "attendance_db"


def get_server_connection():
    """Create a MySQL connection without selecting a database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )


def get_connection():
    """Create and return a MySQL database connection."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


def create_database():
    """Create the database if it does not exist."""
    connection = get_server_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        connection.commit()
    finally:
        connection.close()


def create_tables():
    """Create all tables required by the application."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:

            # CLASSES TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    department VARCHAR(50) NOT NULL,
                    semester VARCHAR(20) NOT NULL,
                    section VARCHAR(20) NOT NULL,
                    UNIQUE KEY unique_class (department, semester, section)
                )
            """)

            # STUDENTS TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    roll_no VARCHAR(20) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(50) NOT NULL,
                    class_id INT NOT NULL,
                    FOREIGN KEY (class_id) REFERENCES classes(id)
                    ON DELETE CASCADE
                )
            """)

            # ATTENDANCE TABLE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    class_id INT NOT NULL,
                    date DATE NOT NULL,
                    status ENUM('Present', 'Absent') NOT NULL,
                    UNIQUE KEY unique_attendance (student_id, date),
                    FOREIGN KEY (student_id) REFERENCES students(id)
                    ON DELETE CASCADE,
                    FOREIGN KEY (class_id) REFERENCES classes(id)
                    ON DELETE CASCADE
                )
            """)

        connection.commit()
    finally:
        connection.close()


def setup_database():
    """Create the database and required tables when the application starts."""
    create_database()
    create_tables()
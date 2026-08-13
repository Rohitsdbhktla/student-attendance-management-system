# Student Attendance & Eligibility Management System

A desktop-based **Student Attendance & Eligibility Management System** developed using **Python, Tkinter, MySQL, and PyMySQL**.

The application is designed to manage student records, organize students by class, record daily attendance, and generate attendance reports based on the **75% attendance eligibility criterion**.

## Features

### Student Management

* Add new students
* View student records
* Update student information
* Delete student records
* Assign students to a specific class
* Manage roll number, name, department, semester, and section

### Attendance Management

* Select a class for attendance
* Select the attendance date
* Display students belonging to the selected class
* Mark students as Present or Absent
* Save attendance records to MySQL
* Prevent duplicate attendance records for the same student and date

### Attendance Reports

* View attendance percentage for all students
* View students with attendance of **75% or above**
* Identify students with attendance **below 75%**
* Calculate attendance percentage automatically

## Technologies Used

* **Python** - Application development
* **Tkinter** - Graphical User Interface
* **MySQL** - Database management
* **PyMySQL** - Python-MySQL database connectivity

## Project Structure

```text
student-attendance-management-system/
│
├── main.py
├── db.py
├── student.py
├── attendance.py
├── reports.py
├── requirements.txt
└── README.md
```

### File Description

| File               | Description                               |
| ------------------ | ----------------------------------------- |
| `main.py`          | Main application window and navigation    |
| `db.py`            | MySQL connection and database/table setup |
| `student.py`       | Student management module                 |
| `attendance.py`    | Attendance management module              |
| `reports.py`       | Attendance reports and eligibility module |
| `requirements.txt` | Python dependencies                       |
| `README.md`        | Project documentation                     |

## Application Workflow

```text
Start Application
       │
       ▼
Database Setup
       │
       ▼
Main Dashboard
   ┌───┼──────────────┐
   ▼   ▼              ▼
Students Attendance  Reports
   │      │             │
   ▼      ▼             ▼
Manage  Mark Daily   Calculate
Students Attendance  Attendance %
                         │
                    ┌────┴────┐
                    ▼         ▼
                Eligible   Defaulters
                 ≥75%        <75%
```

## Database

The application uses **MySQL** for storing class, student, and attendance information.

The main database entities are:

```text
Classes
   │
   ▼
Students
   │
   ▼
Attendance
```

The application creates the required database and tables automatically when it starts.

## Attendance Calculation

Attendance percentage is calculated using:

```text
Attendance % = (Present Days / Total Attendance Days) × 100
```

Students are classified as:

* **Eligible:** Attendance ≥ 75%
* **Defaulter:** Attendance < 75%

## Installation

### Prerequisites

Make sure the following are installed:

* Python 3.x
* MySQL Server

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/student-attendance-management-system.git
```

Navigate to the project directory:

```bash
cd student-attendance-management-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The project requires:

```text
PyMySQL
```

### 3. Configure MySQL

Open `db.py` and configure your local MySQL credentials:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "YOUR_MYSQL_PASSWORD"
DB_NAME = "attendance_db"
```

Replace `YOUR_MYSQL_PASSWORD` with your local MySQL password.

**Never upload your actual MySQL password or other credentials to GitHub.**

### 4. Run the Application

```bash
python main.py
```

The application will initialize the required database and tables when it starts.

## Modules

### Student Module

The student management module provides CRUD operations:

* Create student records
* Read/view student records
* Update student information
* Delete student records

Students can be associated with their respective department and class.

### Attendance Module

The attendance module allows users to select a class and date and record attendance for students.

Each attendance record contains:

* Student
* Class
* Date
* Status

The system prevents duplicate attendance entries for the same student and date.

### Reports Module

The reporting module calculates attendance percentages and provides:

* All Students report
* Eligible Students report
* Defaulters report

## Project Highlights

* Modular Python application structure
* GUI-based desktop application
* MySQL database integration
* CRUD operations
* Class-wise student management
* Date-wise attendance tracking
* Automated attendance percentage calculation
* 75% eligibility checking
* Defaulter identification
* Relational database design using foreign keys

## Project Type

**Academic Project**

## Author

**Rohit**

## Technologies

`Python` `Tkinter` `MySQL` `PyMySQL`

import tkinter as tk
from db import setup_database
from student import StudentWindow
from attendance import AttendanceWindow
from reports import ReportsWindow


class AttendanceApp:
    """
    Main application window.
    Handles navigation between all modules.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Attendance & Eligibility Management System")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        # Setup database and tables
        setup_database()

        self.create_ui()

    def create_ui(self):
        # ---------------- LEFT MENU ----------------
        menu_frame = tk.Frame(self.root, bg="#2c3e50", width=250)
        menu_frame.pack(side="left", fill="y")

        title = tk.Label(
            menu_frame,
            text="Attendance System",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=30)

        btn_style = {
            "font": ("Arial", 12),
            "bg": "#34495e",
            "fg": "white",
            "bd": 0,
            "width": 20,
            "height": 2,
            "activebackground": "#1abc9c"
        }

        tk.Button(
            menu_frame,
            text="Add / View Students",
            command=self.open_student_window,
            **btn_style
        ).pack(pady=10)

        tk.Button(
            menu_frame,
            text="Take Attendance",
            command=self.open_attendance_window,
            **btn_style
        ).pack(pady=10)

        tk.Button(
            menu_frame,
            text="Reports",
            command=self.open_reports_window,
            **btn_style
        ).pack(pady=10)

        tk.Button(
            menu_frame,
            text="Exit",
            command=self.root.quit,
            **btn_style
        ).pack(pady=40)

        # ---------------- RIGHT CONTENT ----------------
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(side="right", fill="both", expand=True)

        welcome = tk.Label(
            content_frame,
            text="Welcome to Attendance & Eligibility\nManagement System",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Arial", 18)
        )
        welcome.place(relx=0.5, rely=0.4, anchor="center")

    # ---------------- WINDOW OPENERS ----------------
    def open_student_window(self):
        StudentWindow(self.root)

    def open_attendance_window(self):
        AttendanceWindow(self.root)

    def open_reports_window(self):
        ReportsWindow(self.root)


# ---------------- APPLICATION START ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

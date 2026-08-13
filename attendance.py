import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import get_connection


class AttendanceWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Take Attendance")
        self.window.geometry("900x550")
        self.window.resizable(False, False)

        self.class_map = {}          # class_display -> class_id
        self.attendance_vars = {}    # student_id -> IntVar

        self.create_ui()
        self.load_classes()

    # ---------------- UI ----------------
    def create_ui(self):
        top = tk.LabelFrame(self.window, text="Attendance Details", padx=15, pady=10)
        top.pack(fill="x", padx=20, pady=10)

        tk.Label(top, text="Class").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(top, text="Date").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.class_combo = ttk.Combobox(top, width=30, state="readonly")
        self.class_combo.grid(row=0, column=1, padx=5, pady=5)
        self.class_combo.bind("<<ComboboxSelected>>", self.load_students)

        self.date_entry = tk.Entry(top, width=15)
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))

        tk.Button(
            top,
            text="Save Attendance",
            width=18,
            command=self.save_attendance
        ).grid(row=0, column=4, padx=15)

        # ---------------- TABLE HEADER ----------------
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(table_frame)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)

        self.list_frame = tk.Frame(canvas)

        self.list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        header = tk.Frame(self.list_frame)
        header.pack(fill="x")

        tk.Label(header, text="S.No", width=6, font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(header, text="Roll No", width=18, font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(header, text="Name", width=30, font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(header, text="Present", width=10, font=("Arial", 10, "bold")).pack(side="left")

    # ---------------- LOAD CLASSES ----------------
    def load_classes(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, department, semester, section FROM classes ORDER BY department")
        rows = cur.fetchall()
        conn.close()

        class_list = []
        self.class_map.clear()

        for r in rows:
            display = f"{r['department']} - {r['semester']} - {r['section']}"
            class_list.append(display)
            self.class_map[display] = r["id"]

        self.class_combo["values"] = class_list

    # ---------------- LOAD STUDENTS (CLASS-WISE) ----------------
    def load_students(self, event=None):
        for widget in self.list_frame.winfo_children()[1:]:
            widget.destroy()

        self.attendance_vars.clear()

        class_display = self.class_combo.get()
        if not class_display:
            return

        class_id = self.class_map[class_display]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, roll_no, name FROM students WHERE class_id=%s ORDER BY roll_no",
            (class_id,)
        )

        students = cur.fetchall()
        conn.close()

        for index, s in enumerate(students, start=1):
            row = tk.Frame(self.list_frame)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=index, width=6).pack(side="left")
            tk.Label(row, text=s["roll_no"], width=18).pack(side="left")
            tk.Label(row, text=s["name"], width=30).pack(side="left")

            var = tk.IntVar()
            tk.Checkbutton(row, variable=var).pack(side="left")

            self.attendance_vars[s["id"]] = var

    # ---------------- SAVE ATTENDANCE ----------------
    def save_attendance(self):
        class_display = self.class_combo.get()
        selected_date = self.date_entry.get().strip()

        if not class_display or not selected_date:
            messagebox.showerror("Error", "Class and Date are required")
            return

        if not self.attendance_vars:
            messagebox.showerror("Error", "No students found for selected class")
            return

        class_id = self.class_map[class_display]

        conn = get_connection()
        cur = conn.cursor()

        try:
            for student_id, var in self.attendance_vars.items():
                status = "Present" if var.get() == 1 else "Absent"

                cur.execute(
                    """
                    INSERT INTO attendance (student_id, class_id, date, status)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE status=VALUES(status)
                    """,
                    (student_id, class_id, selected_date, status)
                )

            conn.commit()
            messagebox.showinfo("Success", "Attendance saved successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            conn.close()

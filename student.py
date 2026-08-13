import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


class StudentWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Student Management")
        self.window.geometry("900x550")
        self.window.resizable(False, False)

        self.selected_student_id = None
        self.class_map = {}  # class_display -> class_id

        self.create_ui()
        self.load_classes()
        self.load_students()

    # ---------------- UI ----------------
    def create_ui(self):
        form = tk.LabelFrame(self.window, text="Student Details", padx=20, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Roll No").grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(form, text="Name").grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(form, text="Department").grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(form, text="Class").grid(row=3, column=0, sticky="w", pady=5)

        self.roll_entry = tk.Entry(form, width=30)
        self.name_entry = tk.Entry(form, width=30)
        self.dept_entry = tk.Entry(form, width=30)
        self.class_combo = ttk.Combobox(form, width=28, state="readonly")

        self.roll_entry.grid(row=0, column=1, pady=5)
        self.name_entry.grid(row=1, column=1, pady=5)
        self.dept_entry.grid(row=2, column=1, pady=5)
        self.class_combo.grid(row=3, column=1, pady=5)

        btn_frame = tk.Frame(form)
        btn_frame.grid(row=4, column=1, pady=15, sticky="e")

        tk.Button(btn_frame, text="Add", width=10, command=self.add_student).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", width=10, command=self.update_student).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", width=10, command=self.delete_student).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", width=10, command=self.clear_form).pack(side="left", padx=5)

        # ---------------- TABLE ----------------
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("sno", "roll", "name", "dept", "class")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("sno", text="S.No")
        self.table.heading("roll", text="Roll No")
        self.table.heading("name", text="Name")
        self.table.heading("dept", text="Department")
        self.table.heading("class", text="Class")

        self.table.column("sno", width=60, anchor="center")
        self.table.column("roll", width=150)
        self.table.column("name", width=220)
        self.table.column("dept", width=120)
        self.table.column("class", width=200)

        self.table.pack(fill="both", expand=True)
        self.table.bind("<ButtonRelease-1>", self.select_student)

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

    # ---------------- STUDENTS ----------------
    def load_students(self):
        self.table.delete(*self.table.get_children())

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.id, s.roll_no, s.name, s.department,
                   CONCAT(c.department, ' - ', c.semester, ' - ', c.section) AS class_name
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            ORDER BY s.roll_no
        """)

        rows = cur.fetchall()
        conn.close()

        for index, r in enumerate(rows, start=1):
            self.table.insert(
                "",
                "end",
                values=(index, r["roll_no"], r["name"], r["department"], r["class_name"]),
                tags=(r["id"],)
            )

    def add_student(self):
        roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        class_display = self.class_combo.get()

        if not roll or not name or not dept or not class_display:
            messagebox.showerror("Error", "All fields are required")
            return

        class_id = self.class_map[class_display]

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO students (roll_no, name, department, class_id) VALUES (%s, %s, %s, %s)",
                (roll, name, dept, class_id)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Student added successfully")
            self.load_students()
            self.clear_form()

        except:
            messagebox.showerror("Error", "Roll number already exists")

    def update_student(self):
        if self.selected_student_id is None:
            messagebox.showerror("Error", "Select a student to update")
            return

        roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        class_display = self.class_combo.get()

        if not roll or not name or not dept or not class_display:
            messagebox.showerror("Error", "All fields are required")
            return

        class_id = self.class_map[class_display]

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE students
                SET roll_no=%s, name=%s, department=%s, class_id=%s
                WHERE id=%s
                """,
                (roll, name, dept, class_id, self.selected_student_id)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Student updated successfully")
            self.load_students()
            self.clear_form()

        except:
            messagebox.showerror("Error", "Roll number already exists")

    def delete_student(self):
        if self.selected_student_id is None:
            messagebox.showerror("Error", "Select a student to delete")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this student?\nAll attendance records will also be deleted."
        )

        if not confirm:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (self.selected_student_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student deleted successfully")
        self.load_students()
        self.clear_form()

    # ---------------- HELPERS ----------------
    def select_student(self, event):
        selected = self.table.focus()
        if not selected:
            return

        values = self.table.item(selected, "values")
        self.selected_student_id = int(self.table.item(selected, "tags")[0])

        self.roll_entry.delete(0, tk.END)
        self.roll_entry.insert(0, values[1])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[2])

        self.dept_entry.delete(0, tk.END)
        self.dept_entry.insert(0, values[3])

        self.class_combo.set(values[4])

    def clear_form(self):
        self.selected_student_id = None
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dept_entry.delete(0, tk.END)
        self.class_combo.set("")

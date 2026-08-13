import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection


class ReportsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Attendance Reports")
        self.window.geometry("900x550")
        self.window.resizable(False, False)

        self.class_map = {}  # display -> class_id

        self.create_ui()
        self.load_classes()

    # ---------------- UI ----------------
    def create_ui(self):
        top = tk.LabelFrame(self.window, text="Report Filters", padx=15, pady=10)
        top.pack(fill="x", padx=20, pady=10)

        tk.Label(top, text="Class").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.class_combo = ttk.Combobox(top, width=35, state="readonly")
        self.class_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(top, text="All Students", width=15, command=self.load_all).grid(row=0, column=2, padx=10)
        tk.Button(top, text="Eligible (≥ 75%)", width=18, command=self.load_eligible).grid(row=0, column=3, padx=5)
        tk.Button(top, text="Defaulters (< 75%)", width=18, command=self.load_defaulters).grid(row=0, column=4, padx=5)

        # ---------------- TABLE ----------------
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("sno", "roll", "name", "percent")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("sno", text="S.No")
        self.table.heading("roll", text="Roll No")
        self.table.heading("name", text="Name")
        self.table.heading("percent", text="Attendance %")

        self.table.column("sno", width=60, anchor="center")
        self.table.column("roll", width=150)
        self.table.column("name", width=300)
        self.table.column("percent", width=150, anchor="center")

        self.table.pack(fill="both", expand=True)

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

    # ---------------- CORE LOGIC ----------------
    def fetch_report_data(self):
        class_display = self.class_combo.get()
        if not class_display:
            messagebox.showerror("Error", "Please select a class")
            return []

        class_id = self.class_map[class_display]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                s.roll_no,
                s.name,
                COUNT(a.date) AS total_days,
                SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) AS present_days
            FROM students s
            LEFT JOIN attendance a
                ON s.id = a.student_id AND a.class_id = %s
            WHERE s.class_id = %s
            GROUP BY s.id
            ORDER BY s.roll_no
        """, (class_id, class_id))

        rows = cur.fetchall()
        conn.close()

        report = []
        for r in rows:
            total = r["total_days"] or 0
            present = r["present_days"] or 0
            percent = round((present / total) * 100, 2) if total > 0 else 0
            report.append((r["roll_no"], r["name"], percent))

        return report

    def clear_table(self):
        self.table.delete(*self.table.get_children())

    # ---------------- REPORT VIEWS ----------------
    def load_all(self):
        self.clear_table()
        data = self.fetch_report_data()

        for i, r in enumerate(data, start=1):
            self.table.insert("", "end", values=(i, r[0], r[1], r[2]))

    def load_eligible(self):
        self.clear_table()
        data = self.fetch_report_data()

        for i, r in enumerate(data, start=1):
            if r[2] >= 75:
                self.table.insert("", "end", values=(i, r[0], r[1], r[2]))

    def load_defaulters(self):
        self.clear_table()
        data = self.fetch_report_data()

        for i, r in enumerate(data, start=1):
            if r[2] < 75:
                self.table.insert("", "end", values=(i, r[0], r[1], r[2]))

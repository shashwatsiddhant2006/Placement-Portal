import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "campus_placement.db")
TABLES = [
    "departments",
    "addresses",
    "companies",
    "skills",
    "staff",
    "students",
    "resumes",
    "recruiters",
    "job_postings",
    "student_skills",
    "job_skills",
    "notifications",
    "applications",
    "interviews",
    "offers",
]


def print_banner(title: str):
    width = 88
    print("\n" + "=" * width)
    print(f" {title.center(width - 2)} ")
    print("=" * width)


def print_section(title: str):
    width = 88
    print("\n" + "-" * width)
    print(f"  [+] {title}")
    print("-" * width)


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database(conn: sqlite3.Connection):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            dept_id TEXT PRIMARY KEY,
            dept_name TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            address_id TEXT PRIMARY KEY,
            city TEXT NOT NULL,
            state TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            co_id TEXT PRIMARY KEY,
            co_name TEXT NOT NULL UNIQUE,
            industry TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            skill_id TEXT PRIMARY KEY,
            skill_name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL CHECK (category IN ('Programming', 'Database', 'Cloud', 'Networking', 'AI/ML', 'Hardware', 'Soft Skills'))
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            staff_id TEXT PRIMARY KEY,
            staff_name TEXT NOT NULL,
            designation TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            dept_id TEXT NOT NULL,
            address_id TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            cgpa REAL NOT NULL CHECK (cgpa >= 0.00 AND cgpa <= 10.00),
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
            FOREIGN KEY (address_id) REFERENCES addresses(address_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            resume_id TEXT PRIMARY KEY,
            roll_no TEXT NOT NULL,
            file_url TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recruiters (
            recruiter_id TEXT PRIMARY KEY,
            co_id TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            FOREIGN KEY (co_id) REFERENCES companies(co_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_postings (
            job_id TEXT PRIMARY KEY,
            co_id TEXT NOT NULL,
            title TEXT NOT NULL,
            package_lpa REAL NOT NULL CHECK (package_lpa > 0.00),
            min_cgpa REAL NOT NULL CHECK (min_cgpa >= 0.00 AND min_cgpa <= 10.00),
            FOREIGN KEY (co_id) REFERENCES companies(co_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_skills (
            roll_no TEXT NOT NULL,
            skill_id TEXT NOT NULL,
            PRIMARY KEY (roll_no, skill_id),
            FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_skills (
            job_id TEXT NOT NULL,
            skill_id TEXT NOT NULL,
            PRIMARY KEY (job_id, skill_id),
            FOREIGN KEY (job_id) REFERENCES job_postings(job_id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            notif_id TEXT PRIMARY KEY,
            staff_id TEXT NOT NULL,
            message TEXT NOT NULL,
            sent_date TEXT NOT NULL,
            FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            app_id TEXT PRIMARY KEY,
            roll_no TEXT NOT NULL,
            job_id TEXT NOT NULL,
            staff_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('Pending', 'Shortlisted', 'Interviewing', 'Rejected', 'Hired')),
            UNIQUE (roll_no, job_id),
            FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
            FOREIGN KEY (job_id) REFERENCES job_postings(job_id) ON DELETE CASCADE,
            FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE RESTRICT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            interview_id TEXT PRIMARY KEY,
            app_id TEXT NOT NULL,
            recruiter_id TEXT NOT NULL,
            mode TEXT NOT NULL CHECK (mode IN ('Online', 'In-Person', 'Hybrid')),
            result TEXT NOT NULL CHECK (result IN ('Pending', 'Cleared', 'Failed')),
            FOREIGN KEY (app_id) REFERENCES applications(app_id) ON DELETE CASCADE,
            FOREIGN KEY (recruiter_id) REFERENCES recruiters(recruiter_id) ON DELETE RESTRICT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            offer_id TEXT PRIMARY KEY,
            app_id TEXT NOT NULL UNIQUE,
            package_offered REAL NOT NULL CHECK (package_offered > 0.00),
            offer_status TEXT NOT NULL CHECK (offer_status IN ('Offered', 'Accepted', 'Declined', 'Revoked')),
            FOREIGN KEY (app_id) REFERENCES applications(app_id) ON DELETE CASCADE
        );
    """)

    conn.commit()


def table_has_rows(conn: sqlite3.Connection, table_name: str) -> bool:
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    return cur.fetchone()[0] > 0


def seed_data(conn: sqlite3.Connection):
    cur = conn.cursor()

    if table_has_rows(conn, "departments"):
        return

    cur.executemany("INSERT INTO departments VALUES (?, ?, ?);", [
        ("DEP001", "Computer Science & Engineering", "+91-44-2250-0101"),
        ("DEP002", "Information Technology", "+91-44-2250-0102"),
        ("DEP003", "Artificial Intelligence & Data Science", "+91-44-2250-0103"),
        ("DEP004", "Electronics & Communication Engineering", "+91-44-2250-0104"),
        ("DEP005", "Mechanical Engineering", "+91-44-2250-0105"),
        ("DEP006", "Electrical & Electronics Engineering", "+91-44-2250-0106"),
    ])

    cur.executemany("INSERT INTO addresses VALUES (?, ?, ?);", [
        ("ADDR001", "Bengaluru", "Karnataka"),
        ("ADDR002", "Chennai", "Tamil Nadu"),
        ("ADDR003", "Hyderabad", "Telangana"),
        ("ADDR004", "Pune", "Maharashtra"),
        ("ADDR005", "Mumbai", "Maharashtra"),
        ("ADDR006", "New Delhi", "Delhi"),
    ])

    cur.executemany("INSERT INTO companies VALUES (?, ?, ?);", [
        ("CO001", "Google India", "Information Technology & Cloud"),
        ("CO002", "Microsoft Corporation", "Software & Enterprise Cloud"),
        ("CO003", "Amazon Web Services", "E-Commerce & Cloud Infrastructure"),
        ("CO004", "Oracle India", "Enterprise Database & Applications"),
        ("CO005", "Cisco Systems", "Networking & Telecommunications"),
        ("CO006", "Qualcomm India", "Semiconductors & Embedded Systems"),
        ("CO007", "Tata Consultancy Services", "IT Services & Consulting"),
        ("CO008", "Infosys Limited", "Digital Services & Consulting"),
    ])

    cur.executemany("INSERT INTO skills VALUES (?, ?, ?);", [
        ("SK001", "Python Programming", "Programming"),
        ("SK002", "Java Enterprise", "Programming"),
        ("SK003", "C++ System Architecture", "Programming"),
        ("SK004", "Relational Database Design & SQL", "Database"),
        ("SK005", "Oracle PL/SQL & Stored Logic", "Database"),
        ("SK006", "Cloud Architecture (AWS/GCP)", "Cloud"),
        ("SK007", "Distributed Systems & Microservices", "Cloud"),
        ("SK008", "Machine Learning & Deep Neural Nets", "AI/ML"),
        ("SK009", "Data Structures & Algorithms", "Programming"),
        ("SK010", "Computer Networks & TCP/IP", "Networking"),
        ("SK011", "Embedded C & RTOS", "Hardware"),
        ("SK012", "System Verilog & VLSI Design", "Hardware"),
        ("SK013", "DevOps & Docker Containers", "Cloud"),
        ("SK014", "Technical Communication", "Soft Skills"),
        ("SK015", "Leadership & Team Management", "Soft Skills"),
    ])

    cur.executemany("INSERT INTO staff VALUES (?, ?, ?);", [
        ("STF001", "Dr. Sundararajan V.", "Director - Training & Placement"),
        ("STF002", "Prof. Kavitha Raman", "Senior Placement Officer - Tier 1 Firms"),
        ("STF003", "Mr. Dinesh Kumar", "Placement Executive - Core Engineering"),
        ("STF004", "Ms. Shalini Murugan", "T&P Compliance & Corporate Liaison"),
    ])

    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?);", [
        ("25BCE5227", "DEP001", "ADDR001", "Shashwat Siddhant", "shashwat.siddhant2025@campus.edu", 9.40),
        ("25BCE5392", "DEP001", "ADDR002", "Srnav Semwal", "srnav.semwal2025@campus.edu", 9.25),
        ("25BAI3003", "DEP003", "ADDR003", "Priya Sharma", "priya.sharma@campus.edu", 9.10),
        ("25BCE1001", "DEP001", "ADDR004", "Ananya Iyer", "ananya.iyer@campus.edu", 8.90),
        ("25BIT2015", "DEP002", "ADDR005", "Neha Kulkarni", "neha.kulkarni@campus.edu", 8.75),
        ("25BIT2002", "DEP002", "ADDR001", "Rohan Gupta", "rohan.gupta@campus.edu", 8.50),
        ("25BEE6006", "DEP006", "ADDR003", "Meera Reddy", "meera.reddy@campus.edu", 8.10),
        ("25BEC4004", "DEP004", "ADDR006", "Vikram Patel", "vikram.patel@campus.edu", 7.80),
        ("25BME5005", "DEP005", "ADDR004", "Aditya Verma", "aditya.verma@campus.edu", 7.20),
        ("25BCE1010", "DEP001", "ADDR002", "Kabir Das", "kabir.das@campus.edu", 6.80),
    ])

    cur.executemany("INSERT INTO resumes VALUES (?, ?, ?, ?);", [
        ("RES001", "25BCE5227", "https://storage.campus.edu/cv/25bce5227_shashwat_v2.pdf", "2026-08-01"),
        ("RES002", "25BCE5392", "https://storage.campus.edu/cv/25bce5392_srnav_v2.pdf", "2026-08-01"),
        ("RES003", "25BAI3003", "https://storage.campus.edu/cv/25bai3003_priya.pdf", "2026-08-02"),
        ("RES004", "25BCE1001", "https://storage.campus.edu/cv/25bce1001_ananya.pdf", "2026-08-02"),
        ("RES005", "25BIT2015", "https://storage.campus.edu/cv/25bit2015_neha.pdf", "2026-08-03"),
        ("RES006", "25BIT2002", "https://storage.campus.edu/cv/25bit2002_rohan.pdf", "2026-08-03"),
        ("RES007", "25BEE6006", "https://storage.campus.edu/cv/25bee6006_meera.pdf", "2026-08-04"),
        ("RES008", "25BEC4004", "https://storage.campus.edu/cv/25bec4004_vikram.pdf", "2026-08-04"),
    ])

    cur.executemany("INSERT INTO recruiters VALUES (?, ?, ?, ?);", [
        ("REC001", "CO001", "Aravind Swaminathan", "+91-80-6721-5001"),
        ("REC002", "CO002", "Deepa Krishnan", "+91-80-4000-6002"),
        ("REC003", "CO003", "Harish Nambiar", "+91-80-3000-7003"),
        ("REC004", "CO004", "Monica Sen", "+91-80-2200-8004"),
        ("REC005", "CO005", "Rajeev Menon", "+91-80-4422-9005"),
        ("REC006", "CO007", "Sunita Rao", "+91-22-6778-1001"),
        ("REC007", "CO008", "Pradeep Shenoy", "+91-80-2852-0261"),
        ("REC008", "CO006", "Karthik Balan", "+91-80-4112-3456"),
    ])

    cur.executemany("INSERT INTO job_postings VALUES (?, ?, ?, ?, ?);", [
        ("JOB001", "CO001", "Software Development Engineer - I", 42.50, 8.50),
        ("JOB002", "CO002", "Cloud Systems & AI Engineer", 38.00, 8.00),
        ("JOB003", "CO003", "Backend SDE (Distributed Systems)", 34.00, 8.00),
        ("JOB004", "CO004", "Database Kernel Engineer", 28.50, 7.50),
        ("JOB005", "CO005", "Network Systems Software Engineer", 22.00, 7.00),
        ("JOB006", "CO006", "Embedded Firmware Engineer", 24.00, 7.00),
        ("JOB007", "CO007", "Digital Solutions Engineer", 9.50, 6.50),
        ("JOB008", "CO008", "Systems Analyst Trainee", 7.20, 6.00),
    ])

    cur.executemany("INSERT INTO student_skills VALUES (?, ?);", [
        ("25BCE5227", "SK001"), ("25BCE5227", "SK004"), ("25BCE5227", "SK005"), ("25BCE5227", "SK007"), ("25BCE5227", "SK009"),
        ("25BCE5392", "SK002"), ("25BCE5392", "SK004"), ("25BCE5392", "SK006"), ("25BCE5392", "SK007"), ("25BCE5392", "SK009"),
        ("25BAI3003", "SK001"), ("25BAI3003", "SK008"), ("25BAI3003", "SK006"), ("25BAI3003", "SK009"),
        ("25BCE1001", "SK001"), ("25BCE1001", "SK002"), ("25BCE1001", "SK004"), ("25BCE1001", "SK009"),
        ("25BIT2015", "SK002"), ("25BIT2015", "SK004"), ("25BIT2015", "SK006"), ("25BIT2015", "SK013"),
        ("25BIT2002", "SK001"), ("25BIT2002", "SK004"), ("25BIT2002", "SK009"),
        ("25BEE6006", "SK001"), ("25BEE6006", "SK010"), ("25BEE6006", "SK014"),
        ("25BEC4004", "SK003"), ("25BEC4004", "SK011"), ("25BEC4004", "SK012"),
    ])

    cur.executemany("INSERT INTO job_skills VALUES (?, ?);", [
        ("JOB001", "SK001"), ("JOB001", "SK007"), ("JOB001", "SK009"),
        ("JOB002", "SK001"), ("JOB002", "SK006"), ("JOB002", "SK008"),
        ("JOB003", "SK002"), ("JOB003", "SK006"), ("JOB003", "SK007"), ("JOB003", "SK009"),
        ("JOB004", "SK003"), ("JOB004", "SK004"), ("JOB004", "SK005"),
        ("JOB005", "SK003"), ("JOB005", "SK010"),
        ("JOB006", "SK003"), ("JOB006", "SK011"), ("JOB006", "SK012"),
        ("JOB007", "SK001"), ("JOB007", "SK004"), ("JOB007", "SK014"),
        ("JOB008", "SK002"), ("JOB008", "SK004"),
    ])

    cur.executemany("INSERT INTO notifications VALUES (?, ?, ?, ?);", [
        ("NOT001", "STF001", "Campus Placement Drive 2026-27 is now LIVE. Upload resumes.", "2026-08-01 09:00:00"),
        ("NOT002", "STF002", "Google India SDE-I registration closes on 15-August-2026.", "2026-08-05 14:30:00"),
        ("NOT003", "STF002", "Microsoft Corporation technical rounds commence tomorrow.", "2026-08-10 11:00:00"),
    ])

    cur.executemany("INSERT INTO applications VALUES (?, ?, ?, ?, ?);", [
        ("APP001", "25BCE5227", "JOB001", "STF002", "Hired"),
        ("APP002", "25BCE5392", "JOB003", "STF002", "Hired"),
        ("APP003", "25BAI3003", "JOB002", "STF002", "Hired"),
        ("APP004", "25BCE1001", "JOB001", "STF002", "Interviewing"),
        ("APP005", "25BIT2002", "JOB003", "STF002", "Interviewing"),
        ("APP006", "25BIT2015", "JOB002", "STF002", "Shortlisted"),
        ("APP007", "25BCE5227", "JOB004", "STF002", "Shortlisted"),
        ("APP008", "25BEC4004", "JOB005", "STF003", "Shortlisted"),
        ("APP009", "25BEE6006", "JOB007", "STF003", "Hired"),
        ("APP010", "25BME5005", "JOB007", "STF003", "Interviewing"),
        ("APP011", "25BCE1010", "JOB007", "STF003", "Pending"),
        ("APP012", "25BEC4004", "JOB006", "STF003", "Pending"),
    ])

    cur.executemany("INSERT INTO interviews VALUES (?, ?, ?, ?, ?);", [
        ("INT001", "APP001", "REC001", "Online", "Cleared"),
        ("INT002", "APP002", "REC003", "Online", "Cleared"),
        ("INT003", "APP003", "REC002", "Online", "Cleared"),
        ("INT004", "APP004", "REC001", "In-Person", "Pending"),
        ("INT005", "APP005", "REC003", "Online", "Pending"),
        ("INT006", "APP009", "REC006", "In-Person", "Cleared"),
    ])

    cur.executemany("INSERT INTO offers VALUES (?, ?, ?, ?);", [
        ("OFR001", "APP001", 42.50, "Accepted"),
        ("OFR002", "APP002", 34.00, "Accepted"),
        ("OFR003", "APP003", 38.00, "Accepted"),
        ("OFR004", "APP009", 9.50, "Accepted"),
    ])

    conn.commit()
    print("  [SUCCESS] Sample placement data loaded.")


def print_query_result(title: str, rows, columns):
    if not rows:
        print(f"\n  {title}: (No rows found)")
        return

    widths = [len(str(c)) for c in columns]
    formatted_rows = [[str(v) for v in row] for row in rows]
    for row in formatted_rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))

    print(f"\n  {title}")
    print("  " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(columns)))
    print("  " + "-+-".join("-" * widths[i] for i in range(len(columns))))
    for row in formatted_rows:
        print("  " + " | ".join(val.ljust(widths[i]) for i, val in enumerate(row)))


def show_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
    tables = [row[0] for row in cur.fetchall()]
    print_section("LIST OF TABLES")
    if not tables:
        print("  No tables found.")
        return
    for name in tables:
        print(f"  - {name}")


def describe_all_tables(conn):
    print_section("SCHEMA DESCRIPTION")
    for table in TABLES:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table});")
        cols = cur.fetchall()
        print(f"\n  TABLE: {table}")
        if not cols:
            print("    (No columns found)")
            continue
        for col in cols:
            cid, name, dtype, notnull, default_value, pk = col
            print(f"    - {name}: {dtype} | NOT NULL={bool(notnull)} | PK={bool(pk)} | DEFAULT={default_value}")


def view_selected_table(conn):
    print("  Available tables:")
    for t in TABLES:
        print(f"    - {t}")
    table_name = input("  Enter table name: ").strip()
    if table_name not in TABLES:
        print("  Invalid table name.")
        return

    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} LIMIT 50;")
    rows = cur.fetchall()
    cur.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cur.fetchall()]
    print_query_result(f"DATA FROM {table_name}", rows, columns)


def display_all_tables(conn):
    for table in TABLES:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} LIMIT 20;")
        rows = cur.fetchall()
        cur.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cur.fetchall()]
        print_query_result(f"{table} ({len(rows)} shown)", rows, columns)


def custom_query(conn):
    print_section("CUSTOM SQL QUERY")
    q = input("  Enter SQL statement: ").strip()
    if not q:
        print("  No SQL entered.")
        return

    try:
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall()
        if cur.description:
            columns = [desc[0] for desc in cur.description]
            print_query_result("CUSTOM QUERY RESULT", rows, columns)
        else:
            conn.commit()
            print("  Query executed successfully.")
    except sqlite3.Error as e:
        print(f"  SQL Error: {e}")


def get_table_columns(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name});")
    return [row[1] for row in cur.fetchall()]


def insert_record(conn):
    print_section("INSERT RECORD")
    print("  Available tables:")
    for t in TABLES:
        print(f"    - {t}")
    table_name = input("  Enter table name: ").strip()
    if table_name not in TABLES:
        print("  Invalid table name.")
        return

    columns = get_table_columns(conn, table_name)
    if not columns:
        print("  Table has no columns.")
        return

    values = []
    print(f"  Enter values for table '{table_name}'")
    for col in columns:
        value = input(f"    {col}: ").strip()
        if value == "":
            values.append(None)
        else:
            try:
                if value.lower() in ["true", "false"]:
                    values.append(value.lower() == "true")
                elif value.lower() in ["null"]:
                    values.append(None)
                else:
                    values.append(value)
            except Exception:
                values.append(value)

    try:
        placeholders = ", ".join(["?"] * len(columns))
        col_list = ", ".join(columns)
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders});", values)
        conn.commit()
        print(f"  [SUCCESS] Record inserted into {table_name}.")
    except sqlite3.Error as e:
        print(f"  Insert failed: {e}")


def update_record(conn):
    print_section("UPDATE RECORD")
    print("  Available tables:")
    for t in TABLES:
        print(f"    - {t}")
    table_name = input("  Enter table name: ").strip()
    if table_name not in TABLES:
        print("  Invalid table name.")
        return

    columns = get_table_columns(conn, table_name)
    if not columns:
        print("  Table has no columns.")
        return

    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} LIMIT 20;")
    rows = cur.fetchall()
    if rows:
        print_query_result(f"Current rows in {table_name}", rows, columns)
    else:
        print("  No rows available to update.")
        return

    print("  Columns available:")
    for c in columns:
        print(f"    - {c}")

    filter_col = input("  Enter column to match: ").strip()
    if filter_col not in columns:
        print("  Invalid filter column.")
        return

    filter_val = input(f"  Enter value for {filter_col}: ").strip()
    update_col = input("  Enter column to update: ").strip()
    if update_col not in columns:
        print("  Invalid update column.")
        return

    new_value = input(f"  Enter new value for {update_col}: ").strip()
    if new_value == "":
        new_value = None

    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE {table_name} SET {update_col} = ? WHERE {filter_col} = ?;", (new_value, filter_val))
        conn.commit()
        print(f"  [SUCCESS] Updated rows in {table_name}.")
    except sqlite3.Error as e:
        print(f"  Update failed: {e}")


def delete_record(conn):
    print_section("DELETE RECORD")
    print("  Available tables:")
    for t in TABLES:
        print(f"    - {t}")
    table_name = input("  Enter table name: ").strip()
    if table_name not in TABLES:
        print("  Invalid table name.")
        return

    columns = get_table_columns(conn, table_name)
    if not columns:
        print("  Table has no columns.")
        return

    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} LIMIT 20;")
    rows = cur.fetchall()
    if rows:
        print_query_result(f"Rows in {table_name}", rows, columns)
    else:
        print("  No rows available to delete.")
        return

    filter_col = input("  Enter column to match: ").strip()
    if filter_col not in columns:
        print("  Invalid column.")
        return

    filter_val = input(f"  Enter value for {filter_col}: ").strip()
    try:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name} WHERE {filter_col} = ?;", (filter_val,))
        conn.commit()
        print(f"  [SUCCESS] Deleted matching record(s) from {table_name}.")
    except sqlite3.Error as e:
        print(f"  Delete failed: {e}")


def search_records(conn):
    print_section("SEARCH RECORDS")
    print("  Available tables:")
    for t in TABLES:
        print(f"    - {t}")
    table_name = input("  Enter table name: ").strip()
    if table_name not in TABLES:
        print("  Invalid table name.")
        return

    columns = get_table_columns(conn, table_name)
    if not columns:
        print("  Table has no columns.")
        return

    print("  Available columns:")
    for c in columns:
        print(f"    - {c}")

    filter_col = input("  Enter search column: ").strip()
    if filter_col not in columns:
        print("  Invalid search column.")
        return

    search_value = input(f"  Enter value to search for in {filter_col}: ").strip()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {filter_col} LIKE ? LIMIT 50;", (f"%{search_value}%",))
        rows = cur.fetchall()
        print_query_result(f"SEARCH RESULTS IN {table_name}", rows, columns)
    except sqlite3.Error as e:
        print(f"  Search failed: {e}")


def reinitialize_database(conn):
    cur = conn.cursor()
    for table in reversed(TABLES):
        cur.execute(f"DROP TABLE IF EXISTS {table};")
    conn.commit()
    initialize_database(conn)
    seed_data(conn)
    print("  [SUCCESS] Database has been reset and reloaded.")


def show_menu():
    print_banner("CAMPUS PLACEMENT DATABASE MENU")
    print("  1. Display all tables")
    print("  2. Describe all tables")
    print("  3. View selected table values")
    print("  4. Display all tables data")
    print("  5. Run custom SQL query")
    print("  6. Insert a record")
    print("  7. Update a record")
    print("  8. Delete a record")
    print("  9. Search records")
    print("  10. Reinitialize database")
    print("  11. Exit")


def main():
    print_banner("THE CAMPUS PLACEMENT PORTAL")
    print(f"  Database location: {DB_FILE}")
    conn = get_connection()
    try:
        initialize_database(conn)
        seed_data(conn)
        while True:
            show_menu()
            choice = input("\n  Enter your choice: ").strip()

            if choice == "1":
                show_tables(conn)
            elif choice == "2":
                describe_all_tables(conn)
            elif choice == "3":
                view_selected_table(conn)
            elif choice == "4":
                display_all_tables(conn)
            elif choice == "5":
                custom_query(conn)
            elif choice == "6":
                insert_record(conn)
            elif choice == "7":
                update_record(conn)
            elif choice == "8":
                delete_record(conn)
            elif choice == "9":
                search_records(conn)
            elif choice == "10":
                reinitialize_database(conn)
            elif choice == "11":
                print("\n  Exiting application. Goodbye!")
                break
            else:
                print("  Invalid option. Please choose a number from 1 to 11.")

            input("\n  Press Enter to continue...")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

import psycopg2
from psycopg2 import sql

# ----------------------------------------------------------------------
# Database connection configuration
# Adjust these values to match your local PostgreSQL installation.
# ----------------------------------------------------------------------
DB_CONFIG = {
    "dbname":   "School",
    "user":     "postgres",
    "password": "kirby",
    "host":     "localhost",
    "port":     5432
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ----------------------------------------------------------------------
# CRUD FUNCTIONS
# ----------------------------------------------------------------------
def getAllStudents():
    """
    Retrieves and prints every row from the students table.
    Uses a read-only cursor and fetches all rows at once.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT student_id, first_name, last_name, email, enrollment_date "
                "FROM students ORDER BY student_id;"
            )
            rows = cur.fetchall()

            print(f"{'ID':<5}{'First':<12}{'Last':<12}{'Email':<30}{'Enrolled':<12}")
            print("-" * 75)
            for sid, first, last, email, edate in rows:
                edate_str = edate.strftime("%Y-%m-%d") if edate else "N/A"
                print(f"{sid:<5}{first:<12}{last:<12}{email:<30}{edate_str:<12}")
    finally:
        conn.close()


def addStudent(first_name, last_name, email, enrollment_date):
    """
    Inserts a new student record.
    enrollment_date may be a 'YYYY-MM-DD' string or None.
    Uses a parameterized query to prevent SQL injection.
    Commits the transaction on success; rolls back on error.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s) RETURNING student_id;",
                (first_name, last_name, email, enrollment_date)
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            print(f"[OK] Added student '{first_name} {last_name}' with ID {new_id}.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to add student: {e}")
    finally:
        conn.close()


def updateStudentEmail(student_id, new_email):
    """
    Updates the email address of the student whose student_id matches.
    Reports whether any row was affected.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id)
            )
            if cur.rowcount == 0:
                print(f"[WARN] No student found with ID {student_id}.")
            else:
                conn.commit()
                print(f"[OK] Updated email for student ID {student_id} to {new_email}.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to update email: {e}")
    finally:
        conn.close()


def deleteStudent(student_id):
    """
    Deletes the student with the given student_id.
    Reports whether any row was affected.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM students WHERE student_id = %s;",
                (student_id,)
            )
            if cur.rowcount == 0:
                print(f"[WARN] No student found with ID {student_id}.")
            else:
                conn.commit()
                print(f"[OK] Deleted student with ID {student_id}.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to delete student: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    import sys

    def usage():
        print(
            "Usage:\n"
            "  python app.py list\n"
            "  python app.py add <first_name> <last_name> <email> <YYYY-MM-DD|none>\n"
            "  python app.py update <student_id> <new_email>\n"
            "  python app.py delete <student_id>"
        )

    args = sys.argv[1:]
    if not args:
        usage()
        sys.exit(1)

    cmd = args[0].lower()

    if cmd == "list" and len(args) == 1:
        getAllStudents()

    elif cmd == "add" and len(args) == 5:
        first, last, email, date = args[1], args[2], args[3], args[4]
        if date.lower() == "none":
            date = None
        addStudent(first, last, email, date)

    elif cmd == "update" and len(args) == 3:
        updateStudentEmail(int(args[1]), args[2])

    elif cmd == "delete" and len(args) == 2:
        deleteStudent(int(args[1]))

    else:
        usage()
        sys.exit(1)
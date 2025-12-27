import mysql.connector

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change if needed
        password="root",      # change if needed
        database="sih"   # your database name
    )


# -----------------------------
# INITIAL DB CHECK
# -----------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.close()
    conn.close()


# -----------------------------
# DOCTORS
# -----------------------------
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT doctor, specialization, available_days, available_time
        FROM doctors
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_doctor_by_specialty(problem):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT doctor, specialization, available_days, available_time
        FROM doctors
        WHERE specialization LIKE %s
        LIMIT 1
    """, (f"%{problem}%",))

    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


# -----------------------------
# APPOINTMENTS
# -----------------------------
def book_appointment(doctor, problem):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT IGNORE INTO appointments (doctor, problem)
        VALUES (%s, %s)
    """, (doctor, problem))

    conn.commit()
    cursor.close()
    conn.close()


# -----------------------------
# HEALTH TIPS
# -----------------------------
def get_tip():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tip_text
        FROM health_tips
        ORDER BY RAND()
        LIMIT 1
    """)

    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data[0] if data else None


# -----------------------------
# MEDICINES
# -----------------------------
# def get_medicine_info(medicine_name):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT medicine_name, use_case, availability
#         FROM medicines
#         WHERE medicine_name LIKE %s
#         LIMIT 1
#     """, (f"%{medicine_name}%",))

#     data = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return data

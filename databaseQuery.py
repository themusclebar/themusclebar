import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()


def create_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS membertable(member_id TEXT, firstName TEXT,lastName TEXT, email TEXT, mobileNo TEXT, address TEXT, pinCode TEXT,nationalIDType TEXT,nationalIDNo TEXT, subscriptedFor TEXT, height TEXT, weight TEXT, status TEXT, dateOfBirth DATE, dateOfRegistration DATE, dateOfPayment DATE, paymentAmount TEXT, neXtPaymentDue DATE)"
    )


def add_data(
    member_id,
    firstName,
    lastName,
    email,
    mobileNo,
    address,
    pinCode,
    nationalIDType,
    nationalIDNo,
    subscriptedFor,
    height,
    weight,
    status,
    dateOfBirth,
    dateOfRegistration,
    dateOfPayment,
    paymentAmount,
    neXtPaymentDue,
):
    c.execute(
        "INSERT INTO membertable(member_id,firstName,lastName, email, mobileNo, address, pinCode, nationalIDType,nationalIDNo, subscriptedFor, height, weight,  status, dateOfBirth,  dateOfRegistration,  dateOfPayment, paymentAmount,neXtPaymentDue) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            member_id,
            firstName,
            lastName,
            email,
            mobileNo,
            address,
            pinCode,
            nationalIDType,
            nationalIDNo,
            subscriptedFor,
            height,
            weight,
            status,
            dateOfBirth,
            dateOfRegistration,
            dateOfPayment,
            paymentAmount,
            neXtPaymentDue,
        ),
    )
    conn.commit()


def view_all_data():
    c.execute("SELECT * FROM membertable")
    data = c.fetchall()
    return data


def delete_member(member_id):
    c.execute('DELETE FROM membertable WHERE member_id="{}"'.format(member_id))
    conn.commit()


def view_all_member_id():
    c.execute("SELECT DISTINCT member_id FROM membertable")
    data = c.fetchall()
    return data


def view_by_member_id(member_id):
    c.execute('SELECT * FROM membertable WHERE member_id="{}"'.format(member_id))
    data = c.fetchall()
    return data


def view_by_first_name(first_name):
    c.execute(
        'SELECT * FROM membertable WHERE first_name LIKE "%{}%"'.format(first_name)
    )
    data = c.fetchall()
    return data


def view_selected_details_by_member_id(member_id, selected_details):
    c.execute(
        "SELECT "
        + ", ".join(selected_details)
        + ' member_id FROM membertable WHERE member_id="{}"'.format(member_id)
    )
    data = c.fetchall()
    return data


def edit_task_data(
    new_firstName,
    new_lastName,
    new_email,
    new_mobileNo,
    new_address,
    new_pinCode,
    new_nationalIDType,
    new_nationalIDNo,
    new_subscriptedFor,
    new_height,
    new_weight,
    new_status,
    new_dateOfBirth,
    new_dateOfRegistration,
    new_dateOfPayment,
    new_paymentAmount,
    new_neXtPaymentDue,
    member_id,
):
    c.execute(
        "UPDATE membertable SET firstName=?,lastName=?,email=?,mobileNo=?,address=?,pinCode=?,nationalIDType=?,nationalIDNo=?,subscriptedFor=?,height=?,weight=?,status=?,dateOfBirth=?,dateOfRegistration=?,dateOfPayment=?,paymentAmount=?,neXtPaymentDue=? WHERE member_id=?",
        (
            new_firstName,
            new_lastName,
            new_email,
            new_mobileNo,
            new_address,
            new_pinCode,
            new_nationalIDType,
            new_nationalIDNo,
            new_subscriptedFor,
            new_height,
            new_weight,
            new_status,
            new_dateOfBirth,
            new_dateOfRegistration,
            new_dateOfPayment,
            new_paymentAmount,
            new_neXtPaymentDue,
            member_id,
        ),
    )
    conn.commit()
    data = c.fetchall()
    return data

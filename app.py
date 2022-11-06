from datetime import date, datetime, timedelta

# import numpy as np
import pandas as pd
# import plotly.express as px
import shortuuid
import streamlit as st

from databaseQuery import *
from widgets import __login__

# from matplotlib.pyplot import flag
# from PIL import Image


# im = Image.open(r".\p_logo.jpeg")
st.set_page_config(page_title="TheMuscleBar")

__login__obj = __login__(
    auth_token="courier_auth_token",
    company_name="Shims",
    width=200,
    height=250,
    logout_button_name="Logout",
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url="https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json",
)

LOGGED_IN = __login__obj.build_login_ui()


feature_list = [
    "member_id",
    "firstName",
    "lastName",
    "email",
    "mobileNo",
    "address",
    "pinCode",
    "nationalIDType",
    "nationalIDNo",
    "subscriptedFor",
    "height",
    "weight",
    "status",
    "dateOfBirth",
    "dateOfRegistration",
    "dateOfPayment",
    "paymentAmount",
    "neXtPaymentDue",
]


def addMember():
    st.write("Add New Member")
    with st.form("Information Form"):
        st.subheader("Add Item")
        col1, col2 = st.columns(2)
        with col1:
            s = shortuuid.ShortUUID(alphabet="0123456789")
            member_id = s.random(length=5)
            st.write("Member ID : ", member_id)
            firstName = st.text_input("First Name : ")
            lastName = st.text_input("Last Name : ")
            email = st.text_input("Email : ")
            mobileNo = st.text_input("Mobile : ", max_chars=10)
            dateOfBirth = st.date_input(
                "Date of Birth : ", min_value=pd.to_datetime("1950/01/01")
            )
            address = st.text_input("Address : ")
            pinCode = st.text_input("PIN Code : ", max_chars=6)
            nationalIDType = st.selectbox(
                "National ID Type : ", ["Adhar", "Voter", "PAN", "Passport", "Other"]
            )
            nationalIDNo = st.text_input("National ID No : ")
        with col2:
            height = st.text_input("Height : ")
            weight = st.text_input("Weight : ")
            dateOfRegistration = st.date_input("Date Of Registration : ")
            dateOfPayment = st.date_input("Date Of Payment : ")
            paymentAmount = st.text_input("Payment Amount: ")
            subscriptedFor = st.slider("Subscripted For (in Months) : ", 1, 12)
            neXtPaymentDue = dateOfPayment + timedelta(subscriptedFor * 30)
            status = st.selectbox("Status : ", ["Active", "Expired", "Hold"])

        submission = st.form_submit_button(label="Submit")
        if (
            submission == True
            and len(mobileNo) == 10
            and "@" in email
            and ".com" in email
            and len(firstName) > 0
            and len(lastName) > 0
        ):
            try:
                int(mobileNo) > 0
                add_data(
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
                )
                st.success("New member is Added")
            except:
                st.write("Give a correct mobile No")
        else:
            st.write("Give a correct email")


def get_age(born):
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def due_days_flag(dates):
    dates_var = datetime.strptime(dates, "%Y-%m-%d").date()
    today = date.today()
    return (today - dates_var).days


def viewMember():
    with st.expander("View All"):
        result = view_all_data()
        # st.write(result)
        clean_df = pd.DataFrame(result)
        clean_df.columns = feature_list
        clean_df["Age"] = clean_df["dateOfBirth"].apply(get_age)
        clean_df["flag"] = clean_df["neXtPaymentDue"].apply(due_days_flag)
        selected_status = st.selectbox(
            "Status : ", ["Active", "Expired", "Payment Due"]
        )
        if selected_status == "Active":
            clean_df_selected = clean_df[clean_df["flag"] < 0]
        elif selected_status == "Payment Due":
            clean_df_selected = clean_df[clean_df["flag"] > 0]
        elif selected_status == "Expired":
            clean_df_selected = clean_df[clean_df["flag"] > 90]
        selected_details = st.multiselect(
            "Select the details you want to get : ",
            feature_list,
            default=["member_id", "firstName", "lastName"],
        )
        st.dataframe(clean_df_selected[selected_details])


def deleteMember():
    st.subheader("Delete Member")
    with st.expander("View Data"):
        result = view_all_data()
        # st.write(result)
        clean_df = pd.DataFrame(
            result,
            columns=feature_list,
        )
        st.dataframe(clean_df)

    unique_list = [i[0] for i in view_all_member_id()]
    delete_by_member_id = st.selectbox("Select Member ID", unique_list)
    if st.button("Delete"):
        delete_member(delete_by_member_id)
        st.warning("Deleted: '{}'".format(delete_by_member_id))

    with st.expander("Updated Data"):
        result = view_all_data()
        # st.write(result)
        clean_df = pd.DataFrame(
            result,
            columns=feature_list,
        )
        st.dataframe(clean_df)


def updateMember():
    st.subheader("Edit Items")
    with st.expander("Current Data"):
        result = view_all_data()
        # st.write(result)
        clean_df = pd.DataFrame(
            result,
            columns=feature_list,
        )
        st.dataframe(clean_df)

    unique_list = [i[0] for i in view_all_member_id()]
    member_id = st.selectbox("Member ID : ", unique_list)
    task_result = view_by_member_id(member_id)
    if task_result:
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
        ) = [task_result[0][i] for i in range(len(task_result[0]))]

        col1, col2 = st.columns(2)
        with col1:
            st.write("member id", member_id)
            new_firstName = st.text_input("First Name : ", value=firstName)
            new_lastName = st.text_input("Last Name : ", value=lastName)
            new_email = st.text_input("Email : ", value=email)
            new_mobileNo = st.text_input("Mobile : ", value=mobileNo)
            new_dateOfBirth = st.date_input(
                "Date of Birth : ", value=pd.to_datetime(dateOfBirth)
            )
            new_address = st.text_input("Address : ", value=address)
            new_pinCode = st.text_input("PIN Code : ", value=pinCode)
            new_nationalIDType = st.selectbox(
                "National ID Type : ",
                ["Adhar", "Voter", "PAN", "Passport", "Other"],
                index=["Adhar", "Voter", "PAN", "Passport", "Other"].index(
                    nationalIDType
                ),
            )
            new_nationalIDNo = st.text_input("National ID No : ", value=nationalIDNo)
        with col2:
            new_height = st.text_input("Height : ", value=height)
            new_weight = st.text_input("Weight : ", value=weight)
            new_dateOfRegistration = st.date_input(
                "Date Of Registration : ", value=pd.to_datetime(dateOfRegistration)
            )
            new_dateOfPayment = st.date_input(
                "Date Of Payment : ", value=pd.to_datetime(dateOfPayment)
            )
            new_paymentAmount = st.text_input("Payment Amount: ", value=paymentAmount)
            new_subscriptedFor = st.selectbox(
                "Subscripted For (in Months) : ",
                ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                index=[
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                ].index(subscriptedFor),
            )
            new_neXtPaymentDue = new_dateOfPayment + timedelta(
                int(new_subscriptedFor) * 30
            )
            new_status = st.selectbox(
                "Status : ",
                ["Active", "Expired", "Hold"],
                index=["Active", "Expired", "Hold"].index(status),
            )

        if st.button("Update Member Details"):
            edit_task_data(
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
            )
            st.success("Updated")


if LOGGED_IN == True:
    st.title("The Muscle Bar Dashboard")
    hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    menu = [
        "Add New Member",
        "View All Member",
        "Update Member Details",
        "Delete Member",
        "Export Member Details",
    ]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    if choice == "Add New Member":
        addMember()
    elif choice == "View All Member":
        viewMember()
    elif choice == "Delete Member":
        deleteMember()
    elif choice == "Update Member Details":
        updateMember()
    elif choice == "Export Member Details":
        result = view_all_data()
        clean_df = pd.DataFrame(result)
        clean_df.columns = feature_list
        download_submission = st.button("Download")
        if download_submission == True:
            # clean_df.to_excel("./abc.xlsx")
            st.write("Not Now")

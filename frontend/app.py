import streamlit as st
import requests
import pandas as pd
from fake_data_transactions import generate_fake_transactions

st.set_page_config(layout="wide")

# st.image("logo.png", width=200)

st.title("Customer Management")


def show_response_message(response):
    if response.status_code == 200:
        st.success("Operation carried out successfully!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Erro: {errors}")
                else:
                    st.error(f"Erro: {data['detail']}")
        except ValueError:
            st.error("Unknown error. Unable to decode the response.")


with st.expander("Add a New Costumer"):
    with st.form("new_Costumer"):
        name = st.text_input("Costumer name")
        email = st.text_input("Costumer e-mail")
        phone = st.text_input("Phone")
        address = st.text_area("Costumer address")
        submit_button = st.form_submit_button("Add Customer")

        if submit_button:
            response = requests.post(
                "http://backend:8000/customers/",
                json={
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "address": address,
                },
            )
            show_response_message(response)

with st.expander("View customers"):
    if st.button("View All customers"):
        response = requests.get("http://backend:8000/customers/")
        if response.status_code == 200:
            customer = response.json()
            df = pd.DataFrame(customer)

            if not df.empty:
                df = df[
                    [
                        "id",
                        "name",
                        "email",
                        "phone",
                        "address",
                        "created_at",
                    ]
                ]

                st.write(df.to_html(index=False), unsafe_allow_html=True)
            else:
                st.info("No customers found.")
        else:
            show_response_message(response)

with st.expander("Get Details of a customer"):
    get_id = st.number_input("customer ID", min_value=1, format="%d", key="get_details_customer_id")
    if st.button("Search customer", key="search_customer"):
        response = requests.get(f"http://backend:8000/customers/{get_id}")
        if response.status_code == 200:
            customer = response.json()
            df = pd.DataFrame([customer])

            df = df[
                [
                    "id",
                    "name",
                    "email",
                    "phone",
                    "address",
                    "created_at",
                ]
            ]

            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

with st.expander("Delete customer"):
    delete_id = st.number_input("customer ID to Delete", min_value=1, format="%d", key="delete_customer_id")
    if st.button("Delete customer"):
        response = requests.delete(f"http://backend:8000/customers/{delete_id}")
        show_response_message(response)

with st.expander("Update customer"):
    with st.form("update_customer"):
        update_id = st.number_input("Customer ID", min_value=1, format="%d", key="update_customer_id")
        new_name = st.text_input("New customer Name")
        new_email = st.text_input("New customer e-mail")
        new_phone = st.text_input("New phone")
        new_address = st.text_area("New customer address")

        update_button = st.form_submit_button("Update customer")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_email:
                update_data["email"] = new_email
            if len(new_phone) > 0:
                update_data["phone"] = new_phone
            if new_address:
                update_data["address"] = new_address

            if update_data:
                response = requests.put(
                    f"http://backend:8000/customers/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("No information provided for update")

with st.expander("Bank statement"):
    get_customer_transactions = st.number_input("Customer ID", min_value=1, format="%d", key="get_transactions_customer_id")
    if st.button("Search customer", key="search_transactions_customer"):
        response = requests.get(f"http://backend:8000/customers/{get_customer_transactions}")
        if response.status_code == 200:
            customer = response.json()
            df = pd.DataFrame([customer])

            df = df[
                [
                    "id",
                    "name",
                    "email",
                    "phone",
                    "address",
                    "created_at",
                ]
            ]

            transactions = generate_fake_transactions()
            transactions = transactions[transactions["customer_id"] == get_customer_transactions]

            df_final = transactions.merge(df, left_on="customer_id", right_on="id")
            df_final = df_final[
                [
                    "customer_id",
                    "transaction_date",
                    "amount",
                    "name",
                ]
            ]

            df_final = df_final[['name', 'transaction_date', 'amount']]
            df_final['month'] = pd.to_datetime(df_final['transaction_date']).dt.to_period('M')

            df_final = df_final.groupby(["name", "transaction_date"]).agg({"amount": "sum"}).reset_index()

            st.write(df_final.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)
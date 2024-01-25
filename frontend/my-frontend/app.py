import streamlit as st
import requests

SERVER_URL = "http://127.0.0.1:9100"

with open("tok.txt", "r", encoding="utf8") as f:
    current_token = f.readline()


def get_user():
    return requests.get(f"{SERVER_URL}/users/me/")


def write_tok(tok):
    with open("tok.txt", "r", encoding="utf8") as f:
        line = f.readline().strip()
        if line != tok:
            new_line = line.replace(line, tok)
            with open("tok.txt", "w", encoding="utf8") as f:
                f.write(new_line)


def write_data(data):
    with open("data.txt", "r", encoding="utf8") as f:
        line = f.readline().strip()
        if line != data[0]:
            new_line = line.replace(line, data[0])
            with open("data.txt", "w", encoding="utf8") as f:
                f.write(new_line)


def main_page():
    st.header("ML приложение для классификации глиомы мозга")


def login_page():
    st.header("Авторизация")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Войти"):
        # Отправка данных на сервер
        login_data = {"username": username, "password": password}
        response = requests.post(f"{SERVER_URL}/token/", data=login_data)
        token = response.json().get("access_token")
        write_tok(token)
        if token:
            st.success("Авторизация прошла успешно!")
            return token
        else:
            st.error("Ошибка авторизации. Пожалуйста, проверьте ваши учетные данные.")


def registration_page():
    st.header("Регистрация нового пользователя")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    name = st.text_input("Name")
    surname = st.text_input("Surname")

    if st.button("Зарегистрировать"):
        # Отправка данных на сервер
        user_data = {
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "surname": surname,
        }
        response = requests.post(f"{SERVER_URL}/new_user/", json=user_data)
        st.write(response.json()["mes"])


def data_input_page():
    headers = {"Authorization": f"Bearer {current_token}"}
    st.header("Выбор модели и ввод данных")
    with open("data.txt", "r", encoding="utf8") as f:
        data_id = f.readline()
    data_id = None if data_id is None else int(data_id)
    years_at_diagnosis = st.number_input("Years at diagnosis", min_value=0)
    days_at_diagnosis = st.number_input("Days at diagnosis", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female"])
    race = st.selectbox(
        "Race",
        [
            "white",
            "black or african american",
            "not reported",
            "asian",
            "american indian or alaska native",
        ],
    )
    IDH1 = st.selectbox("IDH1", ["MUTATED", "NOT_MUTATED"])
    TP53 = st.selectbox("TP53", ["MUTATED", "NOT_MUTATED"])
    ATRX = st.selectbox("ATRX", ["MUTATED", "NOT_MUTATED"])
    PTEN = st.selectbox("PTEN", ["MUTATED", "NOT_MUTATED"])
    EGFR = st.selectbox("EGFR", ["MUTATED", "NOT_MUTATED"])
    CIC = st.selectbox("CIC", ["MUTATED", "NOT_MUTATED"])
    MUC16 = st.selectbox("MUC16", ["MUTATED", "NOT_MUTATED"])
    PIK3CA = st.selectbox("PIK3CA", ["MUTATED", "NOT_MUTATED"])
    NF1 = st.selectbox("NF1", ["MUTATED", "NOT_MUTATED"])
    PIK3R1 = st.selectbox("PIK3R1", ["MUTATED", "NOT_MUTATED"])
    FUBP1 = st.selectbox("FUBP1", ["MUTATED", "NOT_MUTATED"])
    RB1 = st.selectbox("RB1", ["MUTATED", "NOT_MUTATED"])
    NOTCH1 = st.selectbox("NOTCH1", ["MUTATED", "NOT_MUTATED"])
    BCOR = st.selectbox("BCOR", ["MUTATED", "NOT_MUTATED"])
    CSMD3 = st.selectbox("CSMD3", ["MUTATED", "NOT_MUTATED"])
    SMARCA4 = st.selectbox("SMARCA4", ["MUTATED", "NOT_MUTATED"])
    GRIN2A = st.selectbox("GRIN2A", ["MUTATED", "NOT_MUTATED"])
    IDH2 = st.selectbox("IDH2", ["MUTATED", "NOT_MUTATED"])
    FAT4 = st.selectbox("FAT4", ["MUTATED", "NOT_MUTATED"])
    PDGFRA = st.selectbox("PDGFRA", ["MUTATED", "NOT_MUTATED"])

    # Ваши поля для выбора модели
    model_options = ["Linear regression", "Random forest", "LightGBM"]
    selected_model = st.selectbox("Select Model", model_options)

    if st.button("Ввести данные"):
        data = {
            "Years_at_diagnosis": years_at_diagnosis,
            "Days_at_diagnosis": days_at_diagnosis,
            "Gender": gender,
            "Race": race,
            "model_id": model_options.index(selected_model)
            + 1,  # Индексация начинается с 1
            "IDH1": IDH1,
            "TP53": TP53,
            "ATRX": ATRX,
            "PTEN": PTEN,
            "EGFR": EGFR,
            "CIC": CIC,
            "MUC16": MUC16,
            "PIK3CA": PIK3CA,
            "NF1": NF1,
            "PIK3R1": PIK3R1,
            "FUBP1": FUBP1,
            "RB1": RB1,
            "NOTCH1": NOTCH1,
            "BCOR": BCOR,
            "CSMD3": CSMD3,
            "SMARCA4": SMARCA4,
            "GRIN2A": GRIN2A,
            "IDH2": IDH2,
            "FAT4": FAT4,
            "PDGFRA": PDGFRA,
        }

        response = requests.post(f"{SERVER_URL}/get_data/", json=data, headers=headers)
        st.write(response.json()["mes"])
        data_id = [s for s in response.json()["mes"][:-1].split() if s.isdigit()]
        write_data(data_id)

    if st.button("Отказаться от рассчета"):
        response = requests.put(
            f"{SERVER_URL}/reject/{data_id}/",
            headers=headers,
        )
        st.write(response.json()["mes"])
    if st.button("Рассчитать данные"):
        response = requests.post(
            f"{SERVER_URL}/calculate/", json={"id": data_id}, headers=headers
        )
        st.write(response.json()["mes"])


def user_dashboard():
    st.header("Личный кабинет пользователя")
    headers = {"Authorization": f"Bearer {current_token}"}
    if st.button("Посмотреть баланс"):
        response = requests.post(f"{SERVER_URL}/deposit/", headers=headers)

        st.write(f"Текущий баланс: {response.json()['id']} credits")

    if st.button("Пополнить баланс"):
        refill_credits = st.text_input("Введите количество credits для пополнения")
        refill_credits = int(refill_credits) if refill_credits else 0
        response = requests.post(
            f"{SERVER_URL}/refill/",
            json={"id": int(refill_credits)},
            headers=headers,
        )
        st.write(response.json()["mes"])


if __name__ == "__main__":
    st.set_page_config(page_title="Brain Tumor Classification App", page_icon="🧠")
    current_page = st.sidebar.radio(
        "Navigation",
        [
            "Главная",
            "Регистрация",
            "Авторизация",
            "Ввод данных",
            "Личный кабинет",
        ],
    )

    if current_page == "Главная":
        main_page()
    elif current_page == "Регистрация":
        registration_page()
    elif current_page == "Ввод данных":
        data_input_page()
    elif current_page == "Личный кабинет":
        user_dashboard()
    elif current_page == "Авторизация":
        login_page()

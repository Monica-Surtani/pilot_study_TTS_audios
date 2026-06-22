import streamlit as st
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials

# -------------------------------
# Google Sheets helpers
# -------------------------------
def get_gsheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ],
    )
    client = gspread.authorize(creds)
    return client.open_by_key("1MHM4Oo9tGsCSDr6UQNnx43P29qQ3bJ-LL-fAQGCa0Pc")


def save_participant(name, email, gender, mother_tongue, native_place, proficiency):
    try:
        sheet = get_gsheet().worksheet("participants")
        sheet.append_row([
            email, name, gender, mother_tongue, native_place, proficiency
        ])
    except Exception as e:
        st.error(f"SAVE ERROR: {e}")


def load_participants():
    try:
        sheet = get_gsheet().worksheet("participants")
        data_records = sheet.get_all_records()
        return pd.DataFrame(data_records)
    except Exception as e:
        st.error(f"Cannot load participants: {e}")
        return pd.DataFrame(
            columns=["email", "name", "gender", "mother_tongue", "native_place", "proficiency"]
        )


def save_single_audio(audio_idx, email):
    sheet = get_gsheet().worksheet("annotations")
    all_rows = sheet.get_all_values()

    header = ["email", "audio_idx", "labels"]
    filtered_rows = [header]

    for row in all_rows[1:]:
        if len(row) >= 2:
            same_user = row[0] == email
            same_audio = row[1] == str(audio_idx)
            if not (same_user and same_audio):
                filtered_rows.append(row)

    filtered_rows.append([
        email,
        str(audio_idx),
        str(st.session_state.annotations[audio_idx])
    ])

    sheet.clear()
    sheet.append_rows(filtered_rows)


# -------------------------------
# Title
# -------------------------------
st.title("Speech Emphasis Annotation Tool")

# -------------------------------
# Login / Registration
# -------------------------------
participants_df = load_participants()

email = st.text_input("Enter Email ID")

existing_user = False

if email and not participants_df.empty and "email" in participants_df.columns:
    existing_user = (
        email.strip().lower()
        in participants_df["email"].astype(str).str.strip().str.lower().values
    )

if email and not existing_user:
    st.header("Participant Details")

    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    mother_tongue = st.text_input("Mother Tongue")
    native_place = st.text_input("Native Place")
    proficiency = st.selectbox(
        "English Proficiency",
        ["Beginner", "Intermediate", "Advanced", "Professional"]
    )

    if st.button("Register"):
        save_participant(name, email, gender, mother_tongue, native_place, proficiency)
        participants_df = load_participants()
        st.success("Registered successfully!")

# -------------------------------
# MAIN APP
# -------------------------------
if existing_user:

    st.success("Welcome back!")

    st.header("Instructions")
    st.markdown("""
    - Hear the audio carefully  
    - Default = non-emphasized  
    - Click a word → becomes **🔴 emphasized**  
    - Click again → revert  
    """)

    # -------------------------------
    # Data (MUST be defined before any code that references it)
    # -------------------------------
    data = [
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_06_sprt1.wav', 'words': ['I', 'SAID', 'SNOW', 'NOT', 'TOMORROW']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_07_sprt1.wav', 'words': ['I', 'SAID', 'CLOTHES', 'NOT', 'BIOLOGICAL']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_11_sprt1.wav', 'words': ['I', 'SAID', 'PHRASE', 'NOT', 'BAR']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_12_sprt1.wav', 'words': ['I', 'SAID', 'GOT', 'NOT', 'GOAT']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_13_sprt1.wav', 'words': ['I', 'SAID', 'MEET', 'NOT', 'WATER']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_14_sprt1.wav', 'words': ['I', 'SAID', 'CHEAP', 'NOT', 'OTHER']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_15_sprt1.wav', 'words': ['I', 'SAID', 'THROUGH', 'NOT', 'TOUGH']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_17_sprt1.wav', 'words': ['I', 'SAID', 'BOOK', 'NOT', 'DO']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_18_sprt1.wav', 'words': ['I', 'SAID', 'CLIMBING', 'NOT', 'CHEESE']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_21_sprt1.wav', 'words': ['I', 'SAID', 'HATE', 'NOT', 'TIN']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_57_sprt1.wav', 'words': ['I', 'THINK', "IT'S", 'EXTRAORDINARY']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_58_sprt1.wav', 'words': ['THAT', 'ADVERT', 'SHOULD', 'BE', 'BANNED']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_59_sprt1.wav', 'words': ['STAFF', 'MUST', 'RECORD', 'ALL', 'ACCIDENTS', 'IN', 'THE', 'BOOK']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKF_01_sprt1.wav', 'words': ['COULD', 'I', 'HAVE', 'CHICKEN', 'SOUP', 'AS', 'A', 'STARTER', 'AND', 'THEN', 'LAMB', 'CHOPS']},
        {'audio_path': 'audios/ISLE_SESS0183_BLOCKG_07_sprt1.wav', 'words': ['I', 'WOULD', 'LIKE', 'TO', 'GO', 'TO', 'CHINA', 'FOR', 'A', 'COUPLE', 'OF', 'WEEKS']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_01_sprt1.wav', 'words': ['I', 'SAID', 'WHITE', 'NOT', 'BAIT']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_02_sprt1.wav', 'words': ['I', 'SAID', 'NEW', 'NOT', 'NO']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_04_sprt1.wav', 'words': ['I', 'SAID', 'LATE', 'NOT', 'SITE']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_05_sprt1.wav', 'words': ['I', 'SAID', 'FIGHT', 'NOT', 'CENTRE']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_06_sprt1.wav', 'words': ['I', 'SAID', 'SNOW', 'NOT', 'TOMORROW']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_08_sprt1.wav', 'words': ['I', 'SAID', 'PUT', 'NOT', 'BLUE']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_17_sprt1.wav', 'words': ['I', 'SAID', 'BOOK', 'NOT', 'DO']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_18_sprt1.wav', 'words': ['I', 'SAID', 'CLIMBING', 'NOT', 'CHEESE']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_19_sprt1.wav', 'words': ['I', 'SAID', 'PSYCHOLOGY', 'NOT', 'PNEUMATIC']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_20_sprt1.wav', 'words': ['I', 'SAID', 'THIN', 'NOT', 'SHEEP']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_22_sprt1.wav', 'words': ['I', 'SAID', "WON'T", 'NOT', 'UDDER']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_23_sprt1.wav', 'words': ['I', 'SAID', 'SIXTHS', 'NOT', 'BIOLOGY']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_26_sprt1.wav', 'words': ['I', 'SAID', 'CALL', 'NOT', 'SHALL']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_27_sprt1.wav', 'words': ['I', 'SAID', "DON'T", 'NOT', 'SHOULDER']},
        {'audio_path': 'audios/ISLE_SESS0184_BLOCKD01_28_sprt1.wav', 'words': ['I', 'SAID', 'WOULD', 'NOT', 'FILM']},
    ]

    ground_truth = {
        0: [0, 0, 1, 0, 1], 1: [0, 0, 1, 0, 0], 2: [0, 0, 1, 0, 1], 3: [0, 0, 0, 0, 1],
        4: [0, 0, 1, 0, 1], 5: [0, 0, 1, 0, 0], 6: [0, 0, 0, 0, 1], 7: [0, 0, 1, 0, 1],
        8: [0, 0, 1, 0, 1], 9: [0, 0, 1, 0, 0], 10: [0, 0, 0, 1], 11: [1, 0, 0, 0, 0],
        12: [0, 1, 0, 0, 0, 0, 0, 0], 13: [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
        14: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 15: [0, 0, 1, 0, 1], 16: [0, 0, 1, 0, 1],
        17: [0, 0, 0, 0, 1], 18: [0, 0, 1, 0, 1], 19: [0, 0, 1, 0, 0], 20: [0, 0, 1, 0, 0],
        21: [0, 0, 1, 0, 1], 22: [0, 0, 1, 0, 1], 23: [1, 0, 1, 0, 0], 24: [0, 0, 1, 0, 1],
        25: [0, 1, 1, 0, 0], 26: [0, 0, 1, 0, 1], 27: [0, 0, 1, 0, 1], 28: [0, 0, 1, 0, 1],
        29: [0, 0, 1, 1, 1],
    }

    # -------------------------------
    # Optional one-time diagnostic
    # Uncomment ONLY if you need to debug missing audio files.
    # It is safe here because `data` is already defined above.
    # -------------------------------
    # audio_files = set(os.listdir("audios"))
    # missing = [
    #     os.path.basename(item["audio_path"])
    #     for item in data
    #     if os.path.basename(item["audio_path"]) not in audio_files
    # ]
    # st.write("Missing files:", len(missing))
    # st.write(missing)

    def show_ground_truth(audio_idx):
        words = data[audio_idx]["words"]
        gt_labels = ground_truth[audio_idx]
        gt_words = [word for word, label in zip(words, gt_labels) if label == 1]
        st.success("Correct emphasized words: " + ", ".join(gt_words))

    # -------------------------------
    # UI
    # -------------------------------
    WORDS_PER_ROW = 4

    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    if "revealed" not in st.session_state:
        st.session_state.revealed = {}
    if "saved_audios" not in st.session_state:
        st.session_state.saved_audios = {}

    for idx, item in enumerate(data):
        words = item["words"]

        if idx not in st.session_state.annotations:
            st.session_state.annotations[idx] = [0] * len(words)

        total = len(words)
        selected = sum(st.session_state.annotations[idx])

        st.markdown(f"### Audio {idx + 1} ({total} words)")
        st.progress(selected / total)

        audio_path = os.path.join(os.path.dirname(__file__), item["audio_path"])

        if os.path.exists(audio_path):
            st.audio(audio_path)
        else:
            st.error(f"Audio file missing: {audio_path}")

        for row_start in range(0, len(words), WORDS_PER_ROW):
            row_words = words[row_start:row_start + WORDS_PER_ROW]
            cols = st.columns(len(row_words))

            for i, (col, word) in enumerate(zip(cols, row_words)):
                global_idx = row_start + i
                with col:
                    key = f"{idx}_{global_idx}"
                    if key not in st.session_state:
                        st.session_state[key] = bool(st.session_state.annotations[idx][global_idx])
                    checked = st.checkbox(word, key=key)
                    st.session_state.annotations[idx][global_idx] = int(checked)

        save_key = f"save_audio_{idx}"
        if st.button(f"Save Audio {idx + 1}", key=save_key):
            try:
                save_single_audio(idx, email)
                st.session_state.saved_audios[idx] = True
                st.session_state.revealed[idx] = True
                st.success("Annotation saved!")
            except Exception as e:
                st.error(f"Save failed: {e}")

        if st.session_state.revealed.get(idx, False):
            show_ground_truth(idx)

        st.divider()

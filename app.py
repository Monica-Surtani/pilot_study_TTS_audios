import ast
import os
from pathlib import Path

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Speech Emphasis Annotation Tool", layout="wide")

APP_DIR = Path(__file__).resolve().parent
WORDS_PER_ROW = 4
GSheet_KEY = "1UIaeZu9y6RwlpifeZHWVEoVcf_EEjaParYD4dfncluw"
#################14_07_26######################
DATA = [
    {"audio_path": "audio/ISLE_SESS0181_BLOCKE_03_sprt1.wav", "words": ["I", "WASN'T", "PRESENT", "AT", "THE", "LAST", "MEETING"]},
    {"audio_path": "audio/ISLE_SESS0181_BLOCKE_04_sprt1.wav", "words": ["THEY", "WANTED", "TO", "PROTEST", "AGAINST", "STUDENT", "FEES"]},
    {"audio_path": "audio/ISLE_SESS0181_BLOCKE_21_sprt1.wav", "words": ["HE", "HADN'T", "INTENDED", "TO", "INSULT", "THE", "POLICEMAN"]},
    {"audio_path": "audio/ISLE_SESS0181_BLOCKE_31_sprt1.wav", "words": ["THE", "PROJECT", "HAS", "PROVIDED", "VALUABLE", "EXPERIENCE"]},
    {"audio_path": "audio/ISLE_SESS0181_BLOCKE_39_sprt1.wav", "words": ["SHE", "EXPECTS", "TO", "GRADUATE_V", "NEXT", "SUMMER"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_01_sprt1.wav", "words": ["I", "SAID", "WHITE", "NOT", "BAIT"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_02_sprt1.wav", "words": ["I", "SAID", "NEW", "NOT", "NO"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_03_sprt1.wav", "words": ["I", "SAID", "BAD", "NOT", "BED"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_04_sprt1.wav", "words": ["I", "SAID", "LATE", "NOT", "SITE"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_07_sprt1.wav", "words": ["I", "SAID", "CLOTHES", "NOT", "BIOLOGICAL"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_08_sprt1.wav", "words": ["I", "SAID", "PUT", "NOT", "BLUE"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_09_sprt1.wav", "words": ["I", "SAID", "LIVE", "NOT", "BED"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_10_sprt1.wav", "words": ["I", "SAID", "ALONE", "NOT", "GONE"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_18_sprt1.wav", "words": ["I", "SAID", "CLIMBING", "NOT", "CHEESE"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_19_sprt1.wav", "words": ["I", "SAID", "PSYCHOLOGY", "NOT", "PNEUMATIC"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_31_sprt1.wav", "words": ["WHAT", "IS", "SHE", "DRINKING", "A", "CUP", "OF", "COFFEE"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_35_sprt1.wav", "words": ["A", "MUG", "OF", "TEA"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_43_sprt1.wav", "words": ["IN", "A", "PARK", "NEAR", "A", "PATH"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_44_sprt1.wav", "words": ["BESIDE", "A", "TREE", "IN", "A", "PARK"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_78_sprt1.wav", "words": ["WHAT'S", "SHE", "WEARING", "SHE'S", "WEARING", "A", "LEATHER", "JACKET", "AND", "CORDUROY", "TROUSERS"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_79_sprt1.wav", "words": ["WHAT'S", "HE", "WEARING", "HE'S", "WEARING", "A", "BIG", "BEIGE", "JUMPER", "AND", "A", "COWBOY", "HAT"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_80_sprt1.wav", "words": ["SHE'S", "WEARING", "A", "BROWN", "WOOLY", "HAT", "AND", "RED", "SCARF"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKE_01_sprt1.wav", "words": ["THE", "REFEREE", "NEEDED", "A", "POLICE", "ESCORT", "AFTER", "THE", "MATCH"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKE_09_sprt1.wav", "words": ["THE", "PRIME", "SUSPECT", "IS", "THE", "DIRECTOR"]},
    {"audio_path": "audio/ISLE_SESS0182_BLOCKE_14_sprt1.wav", "words": ["OVER", "THE", "NEXT", "TWO", "WEEKS", "EACH", "PAIR", "WILL", "CONTEST", "EIGHT", "GAMES"]},
]

GROUND_TRUTH = {
    0: [0, 0, 1, 0, 0, 0, 0],
    1: [0, 0, 0, 1, 0, 0, 0],
    2: [0, 0, 1, 0, 1, 0, 0],
    3: [0, 1, 0, 0, 0, 0],
    4: [0, 1, 0, 0, 0, 1],
    5: [0, 0, 1, 0, 1],
    6: [0, 0, 1, 0, 1],
    7: [0, 0, 1, 0, 0],
    8: [0, 0, 1, 0, 0],
    9: [0, 0, 1, 0, 1],
    10: [0, 0, 1, 0, 0],
    11: [0, 0, 1, 0, 0],
    12: [0, 0, 1, 0, 0],
    13: [0, 0, 1, 0, 0],
    14: [0, 0, 1, 0, 1],
    15: [0, 0, 0, 1, 0, 0, 0, 1],
    16: [0, 1, 0, 1],
    17: [0, 0, 1, 0, 0, 1],
    18: [1, 0, 0, 0, 0, 1],
    19: [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    20: [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    21: [0, 1, 0, 1, 1, 1, 0, 1, 0],
    22: [0, 1, 0, 0, 0, 1, 0, 0, 0],
    23: [0, 1, 1, 0, 0, 1],
    24: [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
}

############8_07_26##########################
# DATA = [
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_01_sprt1.wav", "words": ["I", "said", "white", "not", "baits"]},
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_02_sprt1.wav", "words": ["I", "said", "new", "not", "no"]},
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_31_sprt1.wav", "words": ["What", "is", "she", "drinking", "a", "cup", "of", "coffee"]},
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_51_sprt1.wav", "words": ["What", "can", "you", "see", "in", "the", "picture", "a", "ginger", "biscuit"]},
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_60_sprt1.wav", "words": ["What's", "in", "the", "picture", "a", "pub"]},
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_72_sprt1.wav", "words": ["a", "mouse"]},
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKE_48_sprt1.wav", "words": ["Children", "often", "rebel", "against", "their", "parents"]},
#     {"audio_path": "audio/ISLE_SESS0003_BLOCKE_57_sprt1.wav", "words": ["I", "think", "he's", "extraordinary"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKD01_38_sprt1.wav", "words": ["at", "home"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKD01_41_sprt1.wav", "words": ["on", "a", "bench", "in", "the", "park"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKD01_76_sprt1.wav", "words": ["a", "blouse"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_06_sprt1.wav", "words": ["EU", "nations", "don't", "need", "work", "permits"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_24_sprt1.wav", "words": ["the", "area", "become", "a", "desert"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_29_sprt1.wav", "words": ["he's", "a", "photographer"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_31_sprt1.wav", "words": ["the", "project", "has", "provided", "a", "valuable", "experience"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_32_sprt1.wav", "words": ["he", "takes", "wonderful", "but", "strange", "photographs"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_33_sprt1.wav", "words": ["they", "predict", "a", "close", "contest", "in", "the", "next", "election"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_34_sprt1.wav", "words": ["Students", "stayed", "a", "protest", "march", "outside", "parliament"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_37_sprt1.wav", "words": ["Food", "and", "clothing", "imports", "are", "rising"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_38_sprt1.wav", "words": ["Export", "orders", "are", "higher", "than", "last", "year"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_39_sprt1.wav", "words": ["She", "expects", "to", "graduate", "next", "summer"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_40_sprt1.wav", "words": ["They", "will", "have", "to", "transport", "the", "components", "over", "land"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_50_sprt1.wav", "words": ["Businesses", "must", "export", "to", "survive"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_51_sprt1.wav", "words": ["The", "police", "suspect", "a", "conspiracy"]},
#     {"audio_path": "audio/ISLE_SESS0040_BLOCKE_52_sprt1.wav", "words": ["they", "sell", "fresh", "farm", "produce"]},
#     {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_39_sprt1.wav", "words": ["by", "a", "river"]},
#     {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_40_sprt1.wav", "words": ["in", "the", "theater"]},
#     {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_53_sprt1.wav", "words": ["a", "man's", "finger"]},
#     {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_55_sprt1.wav", "words": ["what", "is", "this", "buidling", "a", "power", "station"]},
#     {"audio_path": "audio/ISLE_SESS0041_BLOCKE_04_sprt1.wav", "words": ["they", "wanted", "to", "protest", "against", "student", "fees"]},
# ]

# GROUND_TRUTH = {
#     0: [0, 0, 1, 0, 0],
#     1: [0, 0, 1, 0, 1],
#     2: [0, 0, 0, 1, 0, 0, 0, 1],
#     3: [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
#     4: [1, 0, 0, 1, 0, 1],
#     5: [0, 1],
#     6: [1, 0, 1, 0, 0, 1],
#     7: [0, 1, 0, 0],
#     8: [0, 1],
#     9: [0, 0, 1, 0, 0, 1],
#     10: [0, 1],
#     11: [0, 1, 0, 0, 0, 1],
#     12: [0, 1, 0, 0, 1],
#     13: [0, 0, 1],
#     14: [0, 1, 0, 0, 0, 0, 1],
#     15: [0, 0, 1, 0, 1, 0],
#     16: [0, 0, 0, 1, 1, 0, 0, 0, 1],
#     17: [0, 1, 0, 0, 0, 0, 1],
#     18: [1, 0, 1, 1, 0, 0],
#     19: [1, 0, 0, 1, 0, 0, 0],
#     20: [0, 1, 0, 0, 1, 0],
#     21: [0, 0, 0, 0, 0, 0, 1, 0, 0],
#     22: [0, 1, 0, 0, 1],
#     23: [0, 1, 0, 0, 1],
#     24: [0, 1, 1, 0, 1],
#     25: [1, 0, 1],
#     26: [0, 0, 1],
#     27: [0, 1, 0],
#     28: [1, 0, 0, 1, 0, 1, 0],
#     29: [1, 0, 0, 1, 0, 0, 1],
# }


def ensure_session_state() -> None:
    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    if "revealed" not in st.session_state:
        st.session_state.revealed = {}
    if "saved_audio" not in st.session_state:
        st.session_state.saved_audio = {}
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


@st.cache_resource(show_spinner=False)
def get_gsheet():
    try:
        service_account = st.secrets["gcp_service_account"]
    except Exception:
        return None

    try:
        creds = Credentials.from_service_account_info(
            service_account,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        client = gspread.authorize(creds)
        return client.open_by_key(GSheet_KEY)
    except Exception:
        return None


def normalize_email(value: str) -> str:
    return value.strip().lower()


def reset_user_state() -> None:
    st.session_state.annotations = {}
    st.session_state.revealed = {}
    st.session_state.saved_audio = {}


def load_annotations_for_user(email: str, annotations_df: pd.DataFrame) -> None:
    if annotations_df.empty or "email" not in annotations_df.columns:
        return

    user_data = annotations_df[annotations_df["email"] == email]
    for _, row in user_data.iterrows():
        try:
            audio_idx = int(row["audio_idx"])
            st.session_state.annotations[audio_idx] = ast.literal_eval(str(row["labels"]))
        except Exception:
            continue


def save_participant_record(name: str, email: str, gender: str, mother_tongue: str, native_place: str, proficiency: str) -> None:
    email = normalize_email(email)
    sheet = get_gsheet()
    if sheet is None:
        st.error("Google Sheets is not available. Add the Streamlit secrets for gcp_service_account.")
        return

    sheet = sheet.worksheet("participants")
    existing_emails = [str(value).strip().lower() for value in sheet.col_values(1)[1:]]
    if email not in existing_emails:
        sheet.append_row([email, name, gender, mother_tongue, native_place, proficiency])


def save_current_annotations(email: str, audio_idx: int) -> None:
    """Persist only one audio row for the current user."""
    autosave_current_audio(email, audio_idx)


def autosave_current_audio(email: str, audio_idx: int) -> None:
    email = normalize_email(email)
    book = get_gsheet()
    if book is None:
        st.error("Google Sheets is not available. Add the Streamlit secrets for gcp_service_account.")
        return

    sheet = book.worksheet("annotations")
    labels = str(st.session_state.annotations.get(audio_idx, []))
    records = sheet.get_all_records()

    target_row = None
    for row_number, row in enumerate(records, start=2):
        if str(row.get("email", "")).strip().lower() == email and str(row.get("audio_idx", "")) == str(audio_idx):
            target_row = row_number
            break

    if target_row is None:
        sheet.append_row([email, int(audio_idx), labels])
    else:
        sheet.update(
            f"A{target_row}:C{target_row}",
            [[email, int(audio_idx), labels]],
        )


def show_ground_truth(audio_idx: int) -> None:
    words = DATA[audio_idx]["words"]
    labels = GROUND_TRUTH.get(audio_idx, [])
    emphasized = [word for word, label in zip(words, labels) if label == 1]
    if emphasized:
        st.success("Correct emphasized words: " + ", ".join(emphasized))
    else:
        st.info("No ground truth available for this audio.")


def main() -> None:
    st.title("Speech Emphasis Annotation Tool")
    ensure_session_state()

    book = get_gsheet()
    if book is None:
        st.error("Google Sheets secrets are missing. Add gcp_service_account to Streamlit secrets.")
        st.stop()

    st.caption("Storage mode: Google Sheets")
    participants_sheet = book.worksheet("participants")
    annotations_sheet = book.worksheet("annotations")

    participants_rows = participants_sheet.get_all_records()
    annotations_rows = annotations_sheet.get_all_records()

    participants_df = pd.DataFrame(participants_rows)
    annotations_df = pd.DataFrame(annotations_rows)

    if participants_df.empty:
        participants_df = pd.DataFrame(columns=["name", "email", "gender", "mother_tongue", "native_place", "proficiency"])
    if annotations_df.empty:
        annotations_df = pd.DataFrame(columns=["email", "audio_idx", "labels"])

    email = normalize_email(st.text_input("Enter Email ID"))

    participants_df["email"] = participants_df["email"].astype(str).str.strip().str.lower()
    participant_exists = bool(email) and email in participants_df["email"].values
    if bool(email) and not participant_exists:
        st.header("Participant Details")
        name = st.text_input("Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        mother_tongue = st.text_input("Mother Tongue")
        native_place = st.text_input("Native Place")
        proficiency = st.selectbox("English Proficiency", ["Beginner", "Intermediate", "Advanced", "Professional"])

        if st.button("Register"):
            save_participant_record(name, email, gender, mother_tongue, native_place, proficiency)
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success("Registered successfully!")
            st.rerun()
        return

    if participant_exists:
        active_email = st.session_state.get("email")
        if active_email != email:
            reset_user_state()
        st.session_state.logged_in = True
        st.session_state.email = email

    if not st.session_state.logged_in:
        st.info("Enter a registered email or complete registration to continue.")
        return

    current_email = normalize_email(st.session_state.get("email", email))
    load_annotations_for_user(current_email, annotations_df)

    st.success("Welcome back!")
    st.header("Instructions")
    st.markdown(
        """
        - Hear the audio carefully
        - Default = non-emphasized
        - Click a word to mark it as emphasized
        - Click again to revert
        """
    )

    for idx, item in enumerate(DATA):
        words = item["words"]
        if idx not in st.session_state.annotations:
            st.session_state.annotations[idx] = [0] * len(words)

        total = len(words)
        selected = sum(st.session_state.annotations[idx])

        st.markdown(f"### Audio {idx + 1} ({total} words)")
        st.progress(selected / total if total else 0)
        st.audio(item["audio_path"])
        st.write("")

        for row_start in range(0, len(words), WORDS_PER_ROW):
            row_words = words[row_start:row_start + WORDS_PER_ROW]
            cols = st.columns(len(row_words))

            for i, (col, word) in enumerate(zip(cols, row_words)):
                global_idx = row_start + i
                checkbox_key = f"{idx}_{global_idx}"
                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = bool(st.session_state.annotations[idx][global_idx])

                with col:
                    checked = st.checkbox(word, key=checkbox_key)
                    st.session_state.annotations[idx][global_idx] = int(checked)

        if st.button(f"Save Audio {idx + 1}", key=f"save_audio_{idx}"):
            save_current_annotations(current_email, idx)
            st.session_state.saved_audio[idx] = True
            st.session_state.revealed[idx] = True
            st.success("Annotation saved successfully!")

        if st.session_state.revealed.get(idx, False):
            show_ground_truth(idx)

        st.divider()


if __name__ == "__main__":
    main()

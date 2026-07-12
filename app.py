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
GSheet_KEY = "1MHM4Oo9tGsCSDr6UQNnx43P29qQ3bJ-LL-fAQGCa0Pc"

DATA = [
    {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_01_sprt1.wav", "words": ["I", "said", "white", "not", "baits"]},
    {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_02_sprt1.wav", "words": ["I", "said", "new", "not", "no"]},
    {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_31_sprt1.wav", "words": ["What", "is", "she", "drinking", "a", "cup", "of", "coffee"]},
    {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_51_sprt1.wav", "words": ["What", "can", "you", "see", "in", "the", "picture", "a", "ginger", "biscuit"]},
    {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_60_sprt1.wav", "words": ["What's", "in", "the", "picture", "a", "pub"]},
    {"audio_path": "audio/ISLE_SESS0003_BLOCKD01_72_sprt1.wav", "words": ["a", "mouse"]},
    {"audio_path": "audio/ISLE_SESS0003_BLOCKE_48_sprt1.wav", "words": ["Children", "often", "rebel", "against", "their", "parents"]},
    {"audio_path": "audio/ISLE_SESS0003_BLOCKE_57_sprt1.wav", "words": ["I", "think", "he's", "extraordinary"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKD01_38_sprt1.wav", "words": ["at", "home"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKD01_41_sprt1.wav", "words": ["on", "a", "bench", "in", "the", "park"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKD01_76_sprt1.wav", "words": ["a", "blouse"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_06_sprt1.wav", "words": ["EU", "nations", "don't", "need", "work", "permits"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_24_sprt1.wav", "words": ["the", "area", "become", "a", "desert"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_29_sprt1.wav", "words": ["he's", "a", "photographer"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_31_sprt1.wav", "words": ["the", "project", "has", "provided", "a", "valuable", "experience"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_32_sprt1.wav", "words": ["he", "takes", "wonderful", "but", "strange", "photographs"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_33_sprt1.wav", "words": ["they", "predict", "a", "close", "contest", "in", "the", "next", "election"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_34_sprt1.wav", "words": ["Students", "stayed", "a", "protest", "march", "outside", "parliament"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_37_sprt1.wav", "words": ["Food", "and", "clothing", "imports", "are", "rising"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_38_sprt1.wav", "words": ["Export", "orders", "are", "higher", "than", "last", "year"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_39_sprt1.wav", "words": ["She", "expects", "to", "graduate", "next", "summer"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_40_sprt1.wav", "words": ["They", "will", "have", "to", "transport", "the", "components", "over", "land"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_50_sprt1.wav", "words": ["Businesses", "must", "export", "to", "survive"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_51_sprt1.wav", "words": ["The", "police", "suspect", "a", "conspiracy"]},
    {"audio_path": "audio/ISLE_SESS0040_BLOCKE_52_sprt1.wav", "words": ["they", "sell", "fresh", "farm", "produce"]},
    {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_39_sprt1.wav", "words": ["by", "a", "river"]},
    {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_40_sprt1.wav", "words": ["in", "the", "theater"]},
    {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_53_sprt1.wav", "words": ["a", "man's", "finger"]},
    {"audio_path": "audio/ISLE_SESS0041_BLOCKD01_55_sprt1.wav", "words": ["what", "is", "this", "buidling", "a", "power", "station"]},
    {"audio_path": "audio/ISLE_SESS0041_BLOCKE_04_sprt1.wav", "words": ["they", "wanted", "to", "protest", "against", "student", "fees"]},
]

GROUND_TRUTH = {
    0: [0, 0, 1, 0, 0],
    1: [0, 0, 1, 0, 1],
    2: [0, 0, 0, 1, 0, 0, 0, 1],
    3: [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    4: [1, 0, 0, 1, 0, 1],
    5: [0, 1],
    6: [1, 0, 1, 0, 0, 1],
    7: [0, 1, 0, 0],
    8: [0, 1],
    9: [0, 0, 1, 0, 0, 1],
    10: [0, 1],
    11: [0, 1, 0, 0, 0, 1],
    12: [0, 1, 0, 0, 1],
    13: [0, 0, 1],
    14: [0, 1, 0, 0, 0, 0, 1],
    15: [0, 0, 1, 0, 1, 0],
    16: [0, 0, 0, 1, 1, 0, 0, 0, 1],
    17: [0, 1, 0, 0, 0, 0, 1],
    18: [1, 0, 1, 1, 0, 0],
    19: [1, 0, 0, 1, 0, 0, 0],
    20: [0, 1, 0, 0, 1, 0],
    21: [0, 0, 0, 0, 0, 0, 1, 0, 0],
    22: [0, 1, 0, 0, 1],
    23: [0, 1, 0, 0, 1],
    24: [0, 1, 1, 0, 1],
    25: [1, 0, 1],
    26: [0, 0, 1],
    27: [0, 1, 0],
    28: [1, 0, 0, 1, 0, 1, 0],
    29: [1, 0, 0, 1, 0, 0, 1],
}


def load_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    if path.exists():
        frame = pd.read_csv(path)
        missing = set(columns) - set(frame.columns)
        if not missing:
            return frame
    return pd.DataFrame(columns=columns)


def save_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False)


def ensure_session_state() -> None:
    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    if "revealed" not in st.session_state:
        st.session_state.revealed = {}
    if "saved_audio" not in st.session_state:
        st.session_state.saved_audio = {}
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


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
        participants_df = load_csv(
            PARTICIPANT_FILE,
            ["name", "email", "gender", "mother_tongue", "native_place", "proficiency"],
        )
        participants_df["email"] = participants_df["email"].astype(str).str.strip().str.lower()
        participants_df = participants_df[participants_df["email"] != email]
        participants_df = pd.concat(
            [
                participants_df,
                pd.DataFrame([
                    {
                        "name": name,
                        "email": email,
                        "gender": gender,
                        "mother_tongue": mother_tongue,
                        "native_place": native_place,
                        "proficiency": proficiency,
                    }
                ]),
            ],
            ignore_index=True,
        )
        save_csv(participants_df, PARTICIPANT_FILE)
        return

    sheet = sheet.worksheet("participants")
    existing_emails = [str(value).strip().lower() for value in sheet.col_values(2)[1:]]
    if email not in existing_emails:
        sheet.append_row([email, name, gender, mother_tongue, native_place, proficiency])


def save_current_annotations(email: str) -> None:
    email = normalize_email(email)
    book = get_gsheet()
    if book is None:
        rows = []
        for audio_idx, labels in st.session_state.annotations.items():
            rows.append({"email": email, "audio_idx": int(audio_idx), "labels": str(labels)})

        annotations_df = load_csv(ANNOTATION_FILE, ["email", "audio_idx", "labels"])
        annotations_df = annotations_df[annotations_df["email"].astype(str).str.strip().str.lower() != email]
        annotations_df = pd.concat([annotations_df, pd.DataFrame(rows)], ignore_index=True)
        save_csv(annotations_df, ANNOTATION_FILE)
        return

    sheet = book.worksheet("annotations")
    data_all = sheet.get_all_values()
    new_data = [data_all[0] if data_all else ["email", "audio_idx", "labels"]]

    for row in data_all[1:]:
        if str(row[0]).strip().lower() != email:
            new_data.append(row)

    for audio_idx, labels in st.session_state.annotations.items():
        new_data.append([email, int(audio_idx), str(labels)])

    sheet.clear()
    sheet.append_rows(new_data)


def autosave_current_audio(email: str, audio_idx: int) -> None:
    email = normalize_email(email)
    book = get_gsheet()
    if book is None:
        annotations_df = load_csv(ANNOTATION_FILE, ["email", "audio_idx", "labels"])
        annotations_df["email"] = annotations_df["email"].astype(str).str.strip().str.lower()
        annotations_df = annotations_df[
            ~(
                (annotations_df["email"] == email)
                & (annotations_df["audio_idx"].astype(str) == str(audio_idx))
            )
        ]

        updated_row = pd.DataFrame([
            {
                "email": email,
                "audio_idx": int(audio_idx),
                "labels": str(st.session_state.annotations.get(audio_idx, [])),
            }
        ])
        annotations_df = pd.concat([annotations_df, updated_row], ignore_index=True)
        save_csv(annotations_df, ANNOTATION_FILE)
        return

    sheet = book.worksheet("annotations")
    data_all = sheet.get_all_values()
    new_data = [data_all[0] if data_all else ["email", "audio_idx", "labels"]]

    for row in data_all[1:]:
        if not (
            str(row[0]).strip().lower() == email
            and str(row[1]) == str(audio_idx)
        ):
            new_data.append(row)

    new_data.append([
        email,
        int(audio_idx),
        str(st.session_state.annotations.get(audio_idx, [])),
    ])

    sheet.clear()
    sheet.append_rows(new_data)


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
        st.warning("Google Sheets secrets are missing. Using local CSV files for this session.")
        participants_df = load_csv(
            PARTICIPANT_FILE,
            ["name", "email", "gender", "mother_tongue", "native_place", "proficiency"],
        )
        annotations_df = load_csv(ANNOTATION_FILE, ["email", "audio_idx", "labels"])
        st.caption("Storage mode: local CSV")
    else:
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

        autosave_current_audio(current_email, idx)

        if st.button(f"Save Audio {idx + 1}", key=f"save_audio_{idx}"):
            save_current_annotations(current_email)
            st.session_state.saved_audio[idx] = True
            st.session_state.revealed[idx] = True
            st.success("Annotation saved successfully!")

        if st.session_state.revealed.get(idx, False):
            show_ground_truth(idx)

        st.divider()


if __name__ == "__main__":
    main()

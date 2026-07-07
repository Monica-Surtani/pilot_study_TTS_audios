import streamlit as st
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials


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
    sheet = get_gsheet().worksheet("participants")
    sheet.append_row([email, name, gender, mother_tongue, native_place, proficiency])

def save_annotations():
    sheet = get_gsheet().worksheet("annotations")

    # Get existing data
    data_all = sheet.get_all_values()

    # Header
    header = ["email", "audio_idx", "labels"]

    # Keep rows from other users only
    new_data = [header]

    for row in data_all[1:]:
        if row[0] != email:
            new_data.append(row)

    # Clear and rewrite
    sheet.clear()
    sheet.append_rows(new_data)

    # Add fresh data (ONLY per audio)
    rows = []

    for audio_idx, labels in st.session_state.annotations.items():
        rows.append([
            email,
            audio_idx,
            str(labels)   # store full list
        ])

    sheet.append_rows(rows)



# -------------------------------
# Files
# -------------------------------

ANNOTATION_FILE = "annotations.csv"
PARTICIPANT_FILE = "participants.csv"
# try:
#     sh = get_gsheet()
#     st.write([ws.title for ws in sh.worksheets()])
# except Exception as e:
#     st.error(e)
# -------------------------------
# Helpers
# -------------------------------
def load_csv(file, cols):
    if os.path.exists(file):
        df = pd.read_csv(file)
        if set(cols).issubset(df.columns):
            return df
    return pd.DataFrame(columns=cols)

def save_csv(df, file):
    df.to_csv(file, index=False)

# -------------------------------
# Title
# -------------------------------
st.title("Speech Emphasis Annotation Tool")

# -------------------------------
# Login
# -------------------------------
email = st.text_input("Enter Email ID")

participants_df = load_csv(
    PARTICIPANT_FILE,
    ["name","email","gender","mother_tongue","native_place","proficiency"]
)

# -------------------------------
# Registration
# -------------------------------
if email and email not in participants_df["email"].values:

    st.header("Participant Details")

    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male","Female","Other","Prefer not to say"])
    mother_tongue = st.text_input("Mother Tongue")
    native_place = st.text_input("Native Place")
    proficiency = st.selectbox(
        "English Proficiency",
        ["Beginner","Intermediate","Advanced","Professional"]
    )

    if st.button("Register"):
    
        save_participant(name, email, gender, mother_tongue, native_place, proficiency)
    
        st.session_state["logged_in"] = True
        st.session_state["email"] = email
    
        st.success("Registered successfully!")
        st.rerun()
        # participants_df = pd.concat([participants_df, new], ignore_index=True)
        # save_participant(name, email, gender, mother_tongue, native_place, proficiency)
        save_participant(name, email, gender, mother_tongue, native_place, proficiency)

        st.success("Registered! Reloading...")
        st.rerun()

# -------------------------------
# MAIN APP
# -------------------------------
if ("logged_in" in st.session_state and st.session_state["logged_in"]) or \
   (email and email in participants_df["email"].values):

    st.success("Welcome back!")

    # -------------------------------
    # Instructions
    # -------------------------------
    st.header("Instructions")
    st.markdown("""
    - Hear the audio carefully  
    - Default = non-emphasized  
    - Click a word → becomes **🔴 emphasized**  
    - Click again → revert  
    """)

    # -------------------------------
    # Data
    # -------------------------------
    data = [{'audio_path': 'audio/ISLE_SESS0137_BLOCKD02_01_2_sprt1.wav', 'words': ['I', 'SAID', 'WHITE', 'NOT', 'BAIT']}, {'audio_path': 'audio/ISLE_SESS0137_BLOCKD02_01_sprt1.wav', 'words': ['I', 'SAID', 'WHITE', 'NOT', 'BAIT']}, {'audio_path': 'audio/ISLE_SESS0137_BLOCKD02_02_2_sprt1.wav', 'words': ['I', 'SAID', 'NEW', 'NOT', 'NO']}, {'audio_path': 'audio/ISLE_SESS0137_BLOCKD02_02_sprt1.wav', 'words': ['I', 'SAID', 'NEW', 'NOT', 'NO']}, {'audio_path': 'audio/ISLE_SESS0137_BLOCKD02_03_2_sprt1.wav', 'words': ['I', 'SAID', 'BAD', 'NOT', 'BED']}, {'audio_path': 'audio/ISLE_SESS0162_BLOCKD01_43_sprt1.wav', 'words': ['IN', 'A', 'PARK', 'NEAR', 'A', 'PATH']}, {'audio_path': 'audio/ISLE_SESS0162_BLOCKD01_65_sprt1.wav', 'words': ['THREE', 'TREES']}, {'audio_path': 'audio/ISLE_SESS0162_BLOCKE_39_sprt1.wav', 'words': ['SHE', 'EXPECTS', 'TO', 'GRADUATE', 'NEXT', 'SUMMER']}, {'audio_path': 'audio/ISLE_SESS0162_BLOCKE_58_sprt1.wav', 'words': ['THAT', 'ADVERT', 'SHOULD', 'BE', 'BANNED']}, {'audio_path': 'audio/ISLE_SESS0162_BLOCKE_59_sprt1.wav', 'words': ['STAFF', 'MUST', 'RECORD', 'ALL', 'ACCIDENTS', 'IN', 'THE', 'BOOK']}, {'audio_path': 'audio/ISLE_SESS0162_BLOCKE_62_sprt1.wav', 'words': ['THEY', 'IGNORED', 'HIS', 'WARNINGS', 'ABOUT', 'THEIR', 'CONDUCT_N']}, {'audio_path': 'audio/ISLE_SESS0163_BLOCKD01_41_sprt1.wav', 'words': ['ON', 'A', 'BENCH', 'IN', 'THE', 'PARK']}, {'audio_path': 'audio/ISLE_SESS0163_BLOCKD01_42_sprt1.wav', 'words': ['OUTSIDE', 'A', 'PUP', 'BY', 'THE', 'RIVER']}, {'audio_path': 'audio/ISLE_SESS0163_BLOCKD01_45_sprt1.wav', 'words': ['BESIDE', 'THE', 'FIRE', 'IN', 'A', 'PUB']}, {'audio_path': 'audio/ISLE_SESS0163_BLOCKD01_47_sprt1.wav', 'words': ['WHERE', 'THE', 'CUP', 'ON', 'THE', 'EDGE', 'OF', 'THE', 'TABLE']}, {'audio_path': 'audio/ISLE_SESS0163_BLOCKD01_54_sprt1.wav', 'words': ['A', 'BELL', 'RINGER']}, {'audio_path': 'audio/ISLE_SESS0164_BLOCKD01_22_sprt1.wav', 'words': ['I', 'SAID', "WON'T", 'NOT', 'UDDER']}, {'audio_path': 'audio/ISLE_SESS0164_BLOCKD01_24_sprt1.wav', 'words': ['I', 'SAID', 'HAT', 'NOT', 'SURE']}, {'audio_path': 'audio/ISLE_SESS0164_BLOCKD01_25_sprt1.wav', 'words': ['I', 'SAID', 'SLEEP', 'NOT', 'HOPE']}, {'audio_path': 'audio/ISLE_SESS0164_BLOCKD01_33_sprt1.wav', 'words': ['A', 'GLASS', 'OF', 'WINE']}, {'audio_path': 'audio/ISLE_SESS0164_BLOCKE_29_sprt1.wav', 'words': ["HE'S", 'A', 'PHOTOGRAPHER']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKD01_05_sprt1.wav', 'words': ['I', 'SAID', 'FIGHT', 'NOT', 'CENTRE']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKD01_09_sprt1.wav', 'words': ['I', 'SAID', 'LIVE', 'NOT', 'BED']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKD01_25_sprt1.wav', 'words': ['I', 'SAID', 'SLEEP', 'NOT', 'HOPE']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKD01_43_sprt1.wav', 'words': ['IN', 'A', 'PARK', 'NEAR', 'A', 'PATH']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKD01_45_sprt1.wav', 'words': ['BESIDE', 'THE', 'FIRE', 'IN', 'A', 'PUB']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKD01_51_sprt1.wav', 'words': ['WHAT', 'CAN', 'YOU', 'SEE', 'IN', 'THE', 'PICTURE', 'A', 'GINGER', 'BISCUIT']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_29_sprt1.wav', 'words': ["HE'S", 'A', 'PHOTOGRAPHER']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_49_sprt1.wav', 'words': ['THE', 'VILLAGE', 'LOOKS', 'QUITE', 'DESERTED']}, {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_57_sprt1.wav', 'words': ['I', 'THINK', "IT'S", 'EXTRAORDINARY']}]

       # 29_06_26 [{'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_16_sprt1.wav', 'words': ['I', 'SAID', 'LET', 'NOT', 'LEAVE']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_17_sprt1.wav', 'words': ['I', 'SAID', 'BOOK', 'NOT', 'DO']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_18_sprt1.wav', 'words': ['I', 'SAID', 'CLIMBING', 'NOT', 'CHEESE']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_20_sprt1.wav', 'words': ['I', 'SAID', 'THIN', 'NOT', 'SHEEP']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_22_sprt1.wav', 'words': ['I', 'SAID', "WON'T", 'NOT', 'UDDER']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_33_sprt1.wav', 'words': ['A', 'GLASS', 'OF', 'WINE']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_34_sprt1.wav', 'words': ['A', 'BOTTLE', 'OF', 'WATER']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_35_sprt1.wav', 'words': ['A', 'MUG', 'OF', 'TEA']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_36_sprt1.wav', 'words': ['WHERE', 'ARE', 'THEY', 'SITTING', 'IN', 'A', 'PARK']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_37_sprt1.wav', 'words': ['IN', 'A', 'PUB']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_38_sprt1.wav', 'words': ['AT', 'HOME']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_40_sprt1.wav', 'words': ['IN', 'THE', 'THEATRE']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_41_sprt1.wav', 'words': ['ON', 'A', 'BENCH', 'IN', 'THE', 'PARK']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_43_sprt1.wav', 'words': ['IN', 'A', 'PARK', 'NEAR', 'A', 'PATH']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_45_sprt1.wav', 'words': ['BESIDE', 'THE', 'FIRE', 'IN', 'A', 'PUB']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_46_sprt1.wav', 'words': ['IN', 'A', 'BOAT', 'ON', 'THE', 'RIVER']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_49_sprt1.wav', 'words': ['NEXT', 'TO', 'THE', 'JUG', 'ON', 'THE', 'TABLE']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_50_sprt1.wav', 'words': ['IN', 'THE', 'CUPBOARD']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_52_sprt1.wav', 'words': ['A', 'SINGER', 'SINGING']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_53_sprt1.wav', 'words': ['A', "MAN'S", 'FINGER']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_54_sprt1.wav', 'words': ['A', 'BELL', 'RINGER']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_59_sprt1.wav', 'words': ['AN', 'ART', 'GALLERY']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_60_sprt1.wav', 'words': ["WHAT'S", 'IN', 'THE', 'PICTURE', 'A', 'PUB']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_64_sprt1.wav', 'words': ['A', 'PEN']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKD01_78_sprt1.wav', 'words': ["WHAT'S", 'SHE', 'WEARING', "SHE'S", 'WEARING', 'A', 'LEATHER', 'JACKET', 'AND', 'CORDUROY', 'TROUSERS']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_29_sprt1.wav', 'words': ["HE'S", 'A', 'PHOTOGRAPHER']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_30_sprt1.wav', 'words': ['THE', 'REBEL_N', 'LEADER', 'HAS', 'BEEN', 'ARRESTED']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_43_sprt1.wav', 'words': ['HAVE', 'YOU', 'MADE', 'ANY', 'PROGRESS_N', 'ON', 'YOUR', 'REPORT']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_49_sprt1.wav', 'words': ['THE', 'VILLAGE', 'LOOKS', 'QUITE', 'DESERTED']}, {'audio_path': 'audios/ISLE_SESS0183_BLOCKE_51_sprt1.wav', 'words': ['THE', 'POLICE', 'SUSPECT_V', 'A', 'CONSPIRACY']}]  
       # 25_6_26 [{'audio_path': 'audio/ISLE_SESS0192_BLOCKD01_78_sprt1.wav', 'words': ["WHAT'S", 'SHE', 'WEARING', "SHE'S", 'WEARING', 'A', 'LEATHER', 'JACKET', 'AND', 'CORDUROY', 'TROUSERS']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_01_sprt1.wav', 'words': ['THE', 'REFEREE', 'NEEDED', 'A', 'POLICE', 'ESCORT', 'AFTER', 'THE', 'MATCH']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_03_sprt1.wav', 'words': ['I', "WASN'T", 'PRESENT', 'AT', 'THE', 'LAST', 'MEETING']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_04_sprt1.wav', 'words': ['THEY', 'WANTED', 'TO', 'PROTEST', 'AGAINST', 'STUDENT', 'FEES']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_06_sprt1.wav', 'words': ['EU', 'NATIONALS', "DON'T", 'NEED', 'WORK', 'PERMITS']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_08_sprt1.wav', 'words': ['SINGERS', 'LEARN', 'HOW', 'TO', 'PROJECT', 'THEIR', 'VOICES']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_09_sprt1.wav', 'words': ['THE', 'PRIME', 'SUSPECT', 'IS', 'THE', 'DIRECTOR']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_10_sprt1.wav', 'words': ['I', 'AM', 'UNABLE', 'TO', 'ESTIMATE', 'THE', 'COST']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_11_sprt1.wav', 'words': ['THE', 'COMPANY', 'EXPECTS', 'TO', 'INCREASE', 'ITS', 'WORKFORCE', 'NEXT', 'YEAR']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_13_sprt1.wav', 'words': ['THE', 'COMMITTEE', 'WILL', 'CONDUCT', 'A', 'FULL', 'INVESTIGATION', 'INTO', 'HIS', 'BEHAVIOUR']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_14_sprt1.wav', 'words': ['OVER', 'THE', 'NEXT', 'TWO', 'WEEKS', 'EACH', 'PAIR', 'WILL', 'CONTEST_V', 'EIGHT', 'GAMES']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_15_sprt1.wav', 'words': ['THEY', 'SHOULD', 'SURVEY', 'ALL', 'STAFF', 'ON', 'THIS', 'QUESTION']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_16_sprt1.wav', 'words': ['WHAT', 'DO', 'YOU', 'THINK', 'OF', 'THIS', 'ADVERTISEMENT']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_18_sprt1.wav', 'words': ['WE', 'NEED', 'TO', 'PROGRESS', 'TO', 'A', 'HIGHER', 'LEVEL']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_20_sprt1.wav', 'words': ['THE', 'UK', 'IMPORTS', 'MOST', 'OF', 'ITS', 'FOOD']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_21_sprt1.wav', 'words': ['HE', "HADN'T", 'INTENDED', 'TO', 'INSULT', 'THE', 'POLICEMAN']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_24_sprt1.wav', 'words': ['THE', "AREA'S", 'BECOME', 'A', 'DESERT']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_29_sprt1.wav', 'words': ["HE'S", 'A', 'PHOTOGRAPHER']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_30_sprt1.wav', 'words': ['THE', 'REBEL', 'LEADER', 'HAS', 'BEEN', 'ARRESTED']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_31_sprt1.wav', 'words': ['THE', 'PROJECT', 'HAS', 'PROVIDED', 'VALUABLE', 'EXPERIENCE']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_33_sprt1.wav', 'words': ['THEY', 'PREDICT', 'A', 'CLOSE', 'CONTEST', 'AT', 'THE', 'NEXT', 'ELECTION']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_38_sprt1.wav', 'words': ['EXPORT', 'ORDERS', 'ARE', 'HIGHER', 'THAN', 'LAST', 'YEAR']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_41_sprt1.wav', 'words': ['THERE', 'HAS', 'BEEN', 'AN', 'INCREASE', 'IN', 'GLOBAL', 'TEMPERATURES']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_42_sprt1.wav', 'words': ['THEY', 'HAD', 'TO', 'REJECT', 'HIS', 'PLAN']}, {'audio_path': 'audio/ISLE_SESS0192_BLOCKE_43_sprt1.wav', 'words': ['HAVE', 'YOU', 'MADE', 'ANY', 'PROGRESS', 'ON', 'YOUR', 'REPORT']}, {'audio_path': 'audio/ISLE_SESS0193_BLOCKD01_44_sprt1.wav', 'words': ['BESIDE', 'A', 'TREE', 'IN', 'A', 'PARK']}, {'audio_path': 'audio/ISLE_SESS0193_BLOCKD01_47_sprt1.wav', 'words': ['WHERE', 'IS', 'THE', 'CUP', 'ON', 'THE', 'EDGE', 'OF', 'THE', 'TABLE']}, {'audio_path': 'audio/ISLE_SESS0193_BLOCKD01_48_sprt1.wav', 'words': ['IN', 'THE', 'MIDDLE', 'OF', 'THE', 'TABLE']}, {'audio_path': 'audio/ISLE_SESS0193_BLOCKD01_49_sprt1.wav', 'words': ['NEXT', 'TO', 'THE', 'JUG', 'ON', 'THE', 'TABLE']}, {'audio_path': 'audio/ISLE_SESS0193_BLOCKD01_51_sprt1.wav', 'words': ['WHAT', 'CAN', 'YOU', 'SEE', 'IN', 'THE', 'PICTURE', 'A', 'GINGER', 'BISCUIT']}]
       #24_6_26[{'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_43_sprt1.wav', 'words': ['IN', 'A', 'PARK', 'NEAR', 'A', 'PATH']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_44_sprt1.wav', 'words': ['BESIDE', 'THE', 'TREE', 'IN', 'THE', 'PARK']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_45_sprt1.wav', 'words': ['BESIDE', 'THE', 'FIRE', 'IN', 'A', 'PUB']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_46_sprt1.wav', 'words': ['IN', 'A', 'BOAT', 'ON', 'THE', 'RIVER']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_47_sprt1.wav', 'words': ['WHERE', 'IS', 'THE', 'CUP', 'IN', 'THE', 'MIDDLE', 'OF', 'THE', 'TABLE']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_48_sprt1.wav', 'words': ['ON', 'THE', 'EDGE', 'OF', 'THE', 'TABLE']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_49_sprt1.wav', 'words': ['NEXT', 'TO', 'THE', 'JUG', 'ON', 'THE', 'TABLE']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_50_sprt1.wav', 'words': ['IN', 'THE', 'CUPBOARD']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_51_sprt1.wav', 'words': ['WHAT', 'CAN', 'YOU', 'SEE', 'IN', 'THE', 'PICTURE', 'A', 'SINGER', 'SINGING']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_52_sprt1.wav', 'words': ['A', 'GINGER', 'BISCUIT']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_53_sprt1.wav', 'words': ['A', "MAN'S", 'FINGER']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_54_sprt1.wav', 'words': ['A', 'BELL', 'RINGER']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_55_sprt1.wav', 'words': ['WHAT', 'IS', 'THIS', 'BUILDING', 'A', 'RAILWAY', 'STATION']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_56_sprt1.wav', 'words': ['A', 'POWER', 'STATION']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKD02_57_sprt1.wav', 'words': ['A', 'BUS', 'TERMINAL']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKE_03_sprt1.wav', 'words': ['I', "WASN'T", 'PRESENT', 'AT', 'THE', 'LAST', 'MEETING']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKE_04_sprt1.wav', 'words': ['THEY', 'WANTED', 'TO', 'PROTEST', 'AGAINST', 'STUDENT', 'FEES']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKE_09_sprt1.wav', 'words': ['THE', 'PRIME', 'SUSPECT', 'IS', 'DIRECTOR']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKE_13_sprt1.wav', 'words': ['THE', 'COMMITTEE', 'WILL', 'CONDUCT', 'A', 'FULL', 'INVESTIGATION', 'INTO', 'HIS', 'BEHAVIOUR']}, {'audio_path': 'audio/ISLE_SESS0131_BLOCKE_17_sprt1.wav', 'words': ['I', 'NEED', 'TO', 'TRANSFER', 'MONEY', 'FROM', 'MY', 'ACCOUNT']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_01_sprt1.wav', 'words': ['I', 'SAID', 'WHITE', 'NOT', 'BAIT']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_02_sprt1.wav', 'words': ['I', 'SAID', 'NEW', 'NOT', 'NO']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_03_sprt1.wav', 'words': ['I', 'SAID', 'BAD', 'NOT', 'BED']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_04_sprt1.wav', 'words': ['I', 'SAID', 'LATE', 'NOT', 'SITE']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_05_sprt1.wav', 'words': ['I', 'SAID', 'FIGHT', 'NOT', 'CENTRE']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_06_sprt1.wav', 'words': ['I', 'SAID', 'SNOW', 'NOT', 'TOMORROW']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_07_sprt1.wav', 'words': ['I', 'SAID', 'CLOTHES', 'NOT', 'BIOLOGICAL']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_08_sprt1.wav', 'words': ['I', 'SAID', 'PATH', 'NOT', 'BLUE']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_09_sprt1.wav', 'words': ['I', 'SAID', 'LIVE', 'NOT', 'BED']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_10_sprt1.wav', 'words': ['I', 'SAID', 'ALONE', 'NOT', 'GONE']}, {'audio_path': 'audio/ISLE_SESS0132_BLOCKD02_13_sprt1.wav', 'words': ['I', 'SAID', 'MEET', 'NOT', 'WATER']}]
       
     
       #22_6_26 [{'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_06_sprt1.wav', 'words': ['I', 'SAID', 'SNOW', 'NOT', 'TOMORROW']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_07_sprt1.wav', 'words': ['I', 'SAID', 'CLOTHES', 'NOT', 'BIOLOGICAL']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_11_sprt1.wav', 'words': ['I', 'SAID', 'PHRASE', 'NOT', 'BAR']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_12_sprt1.wav', 'words': ['I', 'SAID', 'GOT', 'NOT', 'GOAT']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_13_sprt1.wav', 'words': ['I', 'SAID', 'MEET', 'NOT', 'WATER']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_14_sprt1.wav', 'words': ['I', 'SAID', 'CHEAP', 'NOT', 'OTHER']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_15_sprt1.wav', 'words': ['I', 'SAID', 'THROUGH', 'NOT', 'TOUGH']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_17_sprt1.wav', 'words': ['I', 'SAID', 'BOOK', 'NOT', 'DO']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_18_sprt1.wav', 'words': ['I', 'SAID', 'CLIMBING', 'NOT', 'CHEESE']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKD01_21_sprt1.wav', 'words': ['I', 'SAID', 'HATE', 'NOT', 'TIN']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKE_57_sprt1.wav', 'words': ['I', 'THINK', "IT'S", 'EXTRAORDINARY']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKE_58_sprt1.wav', 'words': ['THAT', 'ADVERT', 'SHOULD', 'BE', 'BANNED']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKE_59_sprt1.wav', 'words': ['STAFF', 'MUST', 'RECORD', 'ALL', 'ACCIDENTS', 'IN', 'THE', 'BOOK']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKF_01_sprt1.wav', 'words': ['COULD', 'I', 'HAVE', 'CHICKEN', 'SOUP', 'AS', 'A', 'STARTER', 'AND', 'THEN', 'LAMB', 'CHOPS']}, {'audio_path': 'audio/ISLE_SESS0183_BLOCKG_07_sprt1.wav', 'words': ['I', 'WOULD', 'LIKE', 'TO', 'GO', 'TO', 'CHINA', 'FOR', 'A', 'COUPLE', 'OF', 'WEEKS']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_01_sprt1.wav', 'words': ['I', 'SAID', 'WHITE', 'NOT', 'BAIT']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_02_sprt1.wav', 'words': ['I', 'SAID', 'NEW', 'NOT', 'NO']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_04_sprt1.wav', 'words': ['I', 'SAID', 'LATE', 'NOT', 'SITE']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_05_sprt1.wav', 'words': ['I', 'SAID', 'FIGHT', 'NOT', 'CENTRE']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_06_sprt1.wav', 'words': ['I', 'SAID', 'SNOW', 'NOT', 'TOMORROW']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_08_sprt1.wav', 'words': ['I', 'SAID', 'PUT', 'NOT', 'BLUE']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_17_sprt1.wav', 'words': ['I', 'SAID', 'BOOK', 'NOT', 'DO']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_18_sprt1.wav', 'words': ['I', 'SAID', 'CLIMBING', 'NOT', 'CHEESE']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_19_sprt1.wav', 'words': ['I', 'SAID', 'PSYCHOLOGY', 'NOT', 'PNEUMATIC']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_20_sprt1.wav', 'words': ['I', 'SAID', 'THIN', 'NOT', 'SHEEP']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_22_sprt1.wav', 'words': ['I', 'SAID', "WON'T", 'NOT', 'UDDER']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_23_sprt1.wav', 'words': ['I', 'SAID', 'SIXTHS', 'NOT', 'BIOLOGY']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_26_sprt1.wav', 'words': ['I', 'SAID', 'CALL', 'NOT', 'SHALL']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_27_sprt1.wav', 'words': ['I', 'SAID', "DON'T", 'NOT', 'SHOULDER']}, {'audio_path': 'audio/ISLE_SESS0184_BLOCKD01_28_sprt1.wav', 'words': ['I', 'SAID', 'WOULD', 'NOT', 'FILM']}]

#         "audio_path": "audios/you can also select left or right tank for the fuel supply.wav",
#         "words": "you can also select left or right tank for the fuel supply".split()
#     },
#     {
#         "audio_path": "audios/either they have specified.wav",
#         "words": "either they have specified".split()
#     },
#     {
#         "audio_path": "audios/then you will really get the juice of this fundamental understanding.wav",
#         "words": "then you will really get the juice of this fundamental understanding".split()
#     },
#     {
#         "audio_path": "audios/so a single propeller if something happens what will happen.wav",
#         "words": "so a single propeller if something happens what will happen".split()
#     },
#     {
#         "audio_path": "audios/i am just showing it for a short while.wav",
#         "words": "i am just showing it for a short while".split()
#     },
#     {
#         "audio_path": "audios/and sometimes when we take care of there is a reduction in the voltage or increase in the voltage.wav",
#         "words": "and sometimes when we take care of there is a reduction in the voltage or increase in the voltage".split()
#     },
#     {
#         "audio_path": "audios/now the inverter what it gets out will also be of the order of fifty volts or something.wav",
#         "words": "now the inverter what it gets out will also be of the order of fifty volts or something".split()
#     },
#     {
#         "audio_path": "audios/it is unloading itself on the load.wav",
#         "words": "it is unloading itself on the load".split()
#     },
#     {
#         "audio_path": "audios/there are few challenges.wav",
#         "words": "there are few challenges".split()
#     },
#     {
#         "audio_path": "audios/so they are planted for the bio refinery or energy purposes.wav",
#         "words": "so they are planted for the bio refinery or energy purposes".split()
#     },
#     {
#         "audio_path": "audios/it is not about the energy demand or energy requirement.wav",
#         "words": "it is not about the energy demand or energy requirement".split()
#     },
#     {
#         "audio_path": "audios/because they can tell what is the best way to use this product.wav",
#         "words": "because they can tell what is the best way to use this product".split()
#     },
#     {
#         "audio_path": "audios/then i am selling products of male utilities.wav",
#         "words": "then i am selling products of male utilities".split()
#     },
#     {
#         "audio_path": "audios/so like if i am specialized in developing the overhead tanks.wav",
#         "words": "so like if i am specialized in developing the overhead tanks".split()
#     },
#     {
#         "audio_path": "audios/so i will be developing the overhead tanks.wav",
#         "words": "so i will be developing the overhead tanks".split()
#     },
#     {
#         "audio_path": "audios/so i will make highways.wav",
#         "words": "so i will make highways".split()
#     },
#     {
#         "audio_path": "audios/because that decision you can take whether you want a fluorescent attachment or not.wav",
#         "words": "because that decision you can take whether you want a fluorescent attachment or not".split()
#     },
#     {
#         "audio_path": "audios/we consider that life will cannot be positively oriented for somebody.wav",
#         "words": "we consider that life will cannot be positively oriented for somebody".split()
#     },
#     {
#         "audio_path": "audios/this comes when you have a proper skeletal system which supports you.wav",
#         "words": "this comes when you have a proper skeletal system which supports you".split()
#     },
#     {
#         "audio_path": "audios/so either i react this way or i will do the way i love.wav",
#         "words": "so either i react this way or i will do the way i love".split()
#     }
    
# ]
    ground_truth = {0: [0, 1, 1, 0, 1], 1: [0, 0, 1, 0, 1], 2: [0, 1, 1, 0, 0], 3: [0, 0, 1, 0, 0], 4: [0, 1, 1, 0, 0], 5: [0, 0, 1, 0, 0, 1], 6: [0, 1], 7: [0, 1, 0, 0, 0, 1], 8: [0, 1, 0, 0, 0], 9: [1, 0, 0, 0, 1, 0, 0, 0], 10: [0, 1, 0, 1, 0, 0, 0], 11: [0, 0, 1, 0, 0, 1], 12: [0, 0, 1, 0, 0, 0], 13: [1, 0, 0, 0, 0, 1], 14: [0, 0, 1, 0, 0, 0, 0, 0, 1], 15: [0, 1, 0], 16: [0, 0, 1, 0, 1], 17: [0, 0, 1, 0, 0], 18: [0, 0, 1, 0, 0], 19: [0, 0, 0, 1], 20: [1, 0, 0], 21: [0, 0, 1, 0, 0], 22: [0, 0, 1, 0, 0], 23: [0, 0, 0, 0, 1], 24: [0, 0, 1, 0, 0, 1], 25: [0, 0, 0, 0, 0, 1], 26: [0, 0, 0, 0, 0, 1, 0, 0, 1], 27: [0, 0, 1], 28: [0, 1, 0, 0, 0], 29: [0, 1, 0, 1]}

       #29_06_26 {0: [0, 0, 1, 0, 1], 1: [0, 0, 1, 0, 1], 2: [0, 0, 1, 0, 1], 3: [0, 1, 0, 0, 1], 4: [0, 0, 1, 0, 1], 5: [0, 0, 0, 1], 6: [0, 0, 0, 1], 7: [0, 1, 0, 1], 8: [0, 0, 0, 1, 0, 0, 1], 9: [0, 0, 1], 10: [0, 1], 11: [0, 0, 1], 12: [0, 0, 1, 0, 0, 1], 13: [0, 0, 1, 0, 0, 1], 14: [0, 1, 1, 0, 0, 1], 15: [0, 0, 1, 0, 0, 1], 16: [1, 0, 0, 1, 0, 0, 1], 17: [0, 0, 1], 18: [0, 1, 1], 19: [0, 1, 0], 20: [0, 1, 0], 21: [0, 1, 0], 22: [0, 0, 0, 1, 0, 1], 23: [0, 1], 24: [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1], 25: [1, 0, 0], 26: [0, 1, 0, 0, 0], 27: [0, 0, 0, 1, 1, 0, 0, 0], 28: [0, 0, 0, 0, 1], 29: [0, 0, 0, 0, 1]}

       # 25_6_26 {0: [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1], 1: [0, 1, 0, 0, 1, 1, 0, 0, 0], 2: [1, 1, 1, 0, 0, 1, 0], 3: [0, 1, 0, 1, 1, 0, 0], 4: [1, 1, 0, 0, 1, 1], 5: [1, 0, 0, 0, 1, 0, 1], 6: [0, 1, 1, 0, 0, 1], 7: [0, 0, 1, 0, 1, 0, 1], 8: [0, 0, 1, 0, 1, 0, 1, 0, 0], 9: [1, 1, 0, 0, 0, 1, 1, 0, 0, 1], 10: [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1], 11: [1, 0, 0, 1, 1, 0, 0, 0], 12: [0, 0, 1, 0, 0, 0, 1], 13: [0, 0, 0, 1, 0, 0, 1, 1], 14: [0, 1, 1, 0, 0, 0, 1], 15: [1, 0, 1, 0, 0, 0, 1], 16: [1, 1, 0, 0, 1], 17: [1, 0, 1], 18: [0, 1, 0, 0, 0, 1], 19: [0, 1, 0, 1, 0, 1], 20: [0, 1, 0, 0, 0, 0, 0, 1, 1], 21: [1, 1, 0, 1, 0, 1, 0], 22: [0, 0, 0, 0, 1, 0, 0, 0], 23: [0, 0, 0, 1, 0, 0], 24: [0, 0, 0, 0, 1, 0, 0, 0], 25: [0, 0, 1, 0, 0, 1], 26: [0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 27: [0, 0, 0, 0, 0, 1], 28: [0, 0, 0, 0, 0, 0, 1], 29: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]}

       #24_6_26{0: [0, 0, 1, 0, 0, 1], 1: [0, 0, 1, 0, 0, 1], 2: [1, 0, 0, 0, 0, 1], 3: [0, 0, 1, 0, 0, 1], 4: [0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 5: [0, 0, 1, 0, 0, 1], 6: [0, 0, 0, 1, 0, 0, 1], 7: [0, 0, 1], 8: [0, 0, 0, 0, 0, 0, 1, 0, 0, 1], 9: [0, 0, 1], 10: [0, 1, 1], 11: [0, 1, 1], 12: [0, 0, 0, 1, 0, 1, 1], 13: [0, 1, 1], 14: [0, 1, 1], 15: [0, 0, 1, 0, 0, 0, 1], 16: [0, 0, 0, 1, 1, 0, 1], 17: [0, 1, 0, 0, 0, 1], 18: [0, 1, 0, 0, 0, 0, 1, 0, 0, 1], 19: [0, 0, 0, 1, 0, 0, 0, 1], 20: [0, 0, 1, 0, 1], 21: [0, 0, 1, 0, 0], 22: [0, 1, 1, 0, 0], 23: [0, 1, 1, 0, 1], 24: [0, 0, 1, 0, 1], 25: [0, 0, 1, 0, 1], 26: [0, 1, 1, 0, 0], 27: [0, 0, 1, 0, 0], 28: [0, 0, 1, 0, 1], 29: [0, 0, 1, 0, 1], 30: [0, 1, 1, 0, 0]}

       # 
       #22_6_26 {0: [0, 0, 1, 0, 1], 1: [0, 0, 1, 0, 0], 2: [0, 0, 1, 0, 1], 3: [0, 0, 0, 0, 1], 4: [0, 0, 1, 0, 1], 5: [0, 0, 1, 0, 0], 6: [0, 0, 0, 0, 1], 7: [0, 0, 1, 0, 1], 8: [0, 0, 1, 0, 1], 9: [0, 0, 1, 0, 0], 10: [0, 0, 0, 1], 11: [1, 0, 0, 0, 0], 12: [0, 1, 0, 0, 0, 0, 0, 0], 13: [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1], 14: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 15: [0, 0, 1, 0, 1], 16: [0, 0, 1, 0, 1], 17: [0, 0, 0, 0, 1], 18: [0, 0, 1, 0, 1], 19: [0, 0, 1, 0, 0], 20: [0, 0, 1, 0, 0], 21: [0, 0, 1, 0, 1], 22: [0, 0, 1, 0, 1], 23: [1, 0, 1, 0, 0], 24: [0, 0, 1, 0, 1], 25: [0, 1, 1, 0, 0], 26: [0, 0, 1, 0, 1], 27: [0, 0, 1, 0, 1], 28: [0, 0, 1, 0, 1], 29: [0, 0, 1, 1, 1]} # ground_truth = {
#     0: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
#     1: [0, 0, 0, 1],
#     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     4: [0, 0, 0, 1, 0, 0, 0, 0, 0],
#     5: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     6: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     7: [0, 0, 0, 0, 0, 0, 1],
#     8: [0, 0, 0, 1],
#     9: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     11: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     12: [0, 0, 0, 0, 0, 0, 1, 0],
#     13: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     14: [0, 0, 0, 0, 0, 0, 0, 1],
#     15: [0, 0, 0, 0, 1],
#     16: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     17: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     18: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     19: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
# }
    # def save_single_audio(audio_idx):
    def save_single_audio(audio_idx):
        try:
        
            sheet = get_gsheet().worksheet("annotations")
        
            data_all = sheet.get_all_values()
        
            header = ["email", "audio_idx", "labels"]
        
            new_data = [header]
        
            for row in data_all[1:]:
                if not (
                    row[0] == email and
                    str(row[1]) == str(audio_idx)
                ):
                    new_data.append(row)
        
            sheet.clear()
            sheet.append_rows(new_data)
        
            sheet.append_row([
                email,
                audio_idx,
                str(st.session_state.annotations[audio_idx])
            ])
        except Exception as e:
            st.error(f"save_single_audio failed: {e}")            
    def show_ground_truth(audio_idx):
    
        words = data[audio_idx]["words"]
        gt_labels = ground_truth[audio_idx]
    
        gt_words = [
            word
            for word, label in zip(words, gt_labels)
            if label == 1
        ]
    
        st.success(
            "Correct emphasized words: "
            + ", ".join(gt_words)
        )

    annotations_df = load_csv(
        ANNOTATION_FILE,
        ["email","audio_idx","labels"]
    )

    # -------------------------------
    # Load previous annotations
    # -------------------------------
    if "annotations" not in st.session_state:
        st.session_state.annotations = {}

        user_data = annotations_df[annotations_df["email"] == email]

        for _, row in user_data.iterrows():
            st.session_state.annotations[row["audio_idx"]] = eval(row["labels"])
    # -------------------------------
    # UI
    # -------------------------------

    WORDS_PER_ROW = 4

    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    if "revealed" not in st.session_state:
        st.session_state.revealed = {}

    if "saved_audio" not in st.session_state:
        st.session_state.saved_audio = {}
    
    for idx, item in enumerate(data):
    
        words = item["words"]
    
        # Initialize
        if idx not in st.session_state.annotations:
            st.session_state.annotations[idx] = [0]*len(words)
    
        total = len(words)
        selected = sum(st.session_state.annotations[idx])
    
        # Header
        st.markdown(f"### Audio {idx+1} ({total} words)")
        st.progress(selected / total)
    
        # ✅ AUDIO MUST BE HERE
        st.audio(item["audio_path"])
    
        st.write("")
    
        # WORD GRID
        for row_start in range(0, len(words), WORDS_PER_ROW):
    
            row_words = words[row_start:row_start+WORDS_PER_ROW]
            cols = st.columns(len(row_words))
    
            for i, (col, word) in enumerate(zip(cols, row_words)):
                global_idx = row_start + i
    
                with col:
                    key = f"{idx}_{global_idx}"
    
                    # Initialize checkbox state
                    if key not in st.session_state:
                        st.session_state[key] = bool(st.session_state.annotations[idx][global_idx])
    
                    # Checkbox
                    checked = st.checkbox(word, key=key)
    
                    # Update annotation
                    st.session_state.annotations[idx][global_idx] = int(checked)
    
        # st.divider()
        save_key = f"save_audio_{idx}"

        if st.button(
                f"Save Audio {idx+1}",
                key=save_key
        ):
        
            save_single_audio(idx)
        
            st.session_state.saved_audio[idx] = True
            st.session_state.revealed[idx] = True
        
            st.success("Annotation saved successfully!")
        
        if st.session_state.revealed.get(idx, False):
        
            show_ground_truth(idx)
        
        st.divider()

    # # -------------------------------
    # # Submit
    # # -------------------------------
    # if st.button("Submit"):
    #     save_annotations()
    #     st.success("All annotations saved!")

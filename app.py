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
# def save_annotations():
#     sheet = get_gsheet().worksheet("annotations")

#     # Get all existing data
#     data_all = sheet.get_all_values()

#     # Keep header
#     header = data_all[0]

#     # Filter out current user's old data
#     new_data = [header]

#     for row in data_all[1:]:
#         if row[0] != email:   # column 0 = email
#             new_data.append(row)

#     # Clear sheet and rewrite filtered data
#     sheet.clear()
#     sheet.append_rows(new_data)

#     # Now add fresh annotations
#     rows = []

#     for audio_idx, labels in st.session_state.annotations.items():
#         words = data[audio_idx]["words"]

#         for word_idx, label in enumerate(labels):
#             rows.append([
#                 email,
#                 audio_idx,
#                 word_idx,
#                 words[word_idx],
#                 label
#             ])

#     sheet.append_rows(rows)
# def save_annotations():
#     sheet = get_gsheet().worksheet("annotations")

#     for audio_idx, labels in st.session_state.annotations.items():
#         words = data[audio_idx]["words"]

#         rows = []
        
#         for audio_idx, labels in st.session_state.annotations.items():
#             words = data[audio_idx]["words"]
        
#             for word_idx, label in enumerate(labels):
#                 rows.append([
#                     email,
#                     audio_idx,
#                     word_idx,
#                     words[word_idx],
#                     label
#                 ])
        
#         sheet.append_rows(rows)


# -------------------------------
# Files
# -------------------------------
# BASE_DIR = "/home/monica/Documents/interspeech25/FastSpeech2/streamlit"

# ANNOTATION_FILE = os.path.join(BASE_DIR, "annotations.csv")
# PARTICIPANT_FILE = os.path.join(BASE_DIR, "participants.csv")
ANNOTATION_FILE = "annotations.csv"
PARTICIPANT_FILE = "participants.csv"

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
    # if st.button("Register"):
    
    #     save_participant(name, email, gender, mother_tongue, native_place, proficiency)
    
    #     st.session_state["logged_in"] = True
    #     st.session_state["email"] = email
    
    #     st.success("Registered successfully!")
    #     st.rerun()

    # if st.button("Register"):
    #     new = pd.DataFrame([{
    #         "name": name,
    #         "email": email,
    #         "gender": gender,
    #         "mother_tongue": mother_tongue,
    #         "native_place": native_place,
    #         "proficiency": proficiency
    #     }])
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
    data = [
    {
        "audio_path": "audios/you can also select left or right tank for the fuel supply.wav",
        "words": "you can also select left or right tank for the fuel supply".split()
    },
    {
        "audio_path": "audios/either they have specified.wav",
        "words": "either they have specified".split()
    },
    {
        "audio_path": "audios/then you will really get the juice of this fundamental understanding.wav",
        "words": "then you will really get the juice of this fundamental understanding".split()
    },
    {
        "audio_path": "audios/so a single propeller if something happens what will happen.wav",
        "words": "so a single propeller if something happens what will happen".split()
    },
    {
        "audio_path": "audios/i am just showing it for a short while.wav",
        "words": "i am just showing it for a short while".split()
    },
    {
        "audio_path": "audios/and sometimes when we take care of there is a reduction in the voltage or increase in the voltage.wav",
        "words": "and sometimes when we take care of there is a reduction in the voltage or increase in the voltage".split()
    },
    {
        "audio_path": "audios/now the inverter what it gets out will also be of the order of fifty volts or something.wav",
        "words": "now the inverter what it gets out will also be of the order of fifty volts or something".split()
    },
    {
        "audio_path": "audios/it is unloading itself on the load.wav",
        "words": "it is unloading itself on the load".split()
    },
    {
        "audio_path": "audios/there are few challenges.wav",
        "words": "there are few challenges".split()
    },
    {
        "audio_path": "audios/so they are planted for the bio refinery or energy purposes.wav",
        "words": "so they are planted for the bio refinery or energy purposes".split()
    },
    {
        "audio_path": "audios/it is not about the energy demand or energy requirement.wav",
        "words": "it is not about the energy demand or energy requirement".split()
    },
    {
        "audio_path": "audios/because they can tell what is the best way to use this product.wav",
        "words": "because they can tell what is the best way to use this product".split()
    },
    {
        "audio_path": "audios/then i am selling products of male utilities.wav",
        "words": "then i am selling products of male utilities".split()
    },
    {
        "audio_path": "audios/so like if i am specialized in developing the overhead tanks.wav",
        "words": "so like if i am specialized in developing the overhead tanks".split()
    },
    {
        "audio_path": "audios/so i will be developing the overhead tanks.wav",
        "words": "so i will be developing the overhead tanks".split()
    },
    {
        "audio_path": "audios/so i will make highways.wav",
        "words": "so i will make highways".split()
    },
    {
        "audio_path": "audios/because that decision you can take whether you want a fluorescent attachment or not.wav",
        "words": "because that decision you can take whether you want a fluorescent attachment or not".split()
    },
    {
        "audio_path": "audios/we consider that life will cannot be positively oriented for somebody.wav",
        "words": "we consider that life will cannot be positively oriented for somebody".split()
    },
    {
        "audio_path": "audios/this comes when you have a proper skeletal system which supports you.wav",
        "words": "this comes when you have a proper skeletal system which supports you".split()
    },
    {
        "audio_path": "audios/so either i react this way or i will do the way i love.wav",
        "words": "so either i react this way or i will do the way i love".split()
    }
]
#     data = [
#     {
#         "audio_path": "audios/it will be done by one person.wav",
#         "words": "it will be done by one person".split()
#     },
#     {
#         "audio_path": "audios/it is then statically stable in lateral mode but how does it generate.wav",
#         "words": "it is then statically stable in lateral mode but how does it generate".split()
#     },
#     {
#         "audio_path": "audios/so do steady side slip maneuver you get.wav",
#         "words": "so do steady side slip maneuver you get".split()
#     },
#     {
#         "audio_path": "audios/meeting half of the existing u.wav",
#         "words": "meeting half of the existing u".split()
#     },
#     {
#         "audio_path": "audios/two point five percent of existing cropping area would.wav",
#         "words": "two point five percent of existing cropping area would".split()
#     },
#     {
#         "audio_path": "audios/if you talk about micro algae to biodiesel.wav",
#         "words": "if you talk about micro algae to biodiesel".split()
#     },
#     {
#         "audio_path": "audios/then this value is zero.wav",
#         "words": "then this value is zero".split()
#     },
#     {
#         "audio_path": "audios/i am discussing the i s code recommendations because now i.wav",
#         "words": "i am discussing the i s code recommendations because now i".split()
#     },
#     {
#         "audio_path": "audios/i will check the maximum settlement.wav",
#         "words": "i will check the maximum settlement".split()
#     },
#     {
#         "audio_path": "audios/where as i want to interrupt fundamentally the current.wav",
#         "words": "where as i want to interrupt fundamentally the current".split()
#     },
#     {
#         "audio_path": "audios/anything ultimately yields sinusoid.wav",
#         "words": "anything ultimately yields sinusoid".split()
#     },
#     {
#         "audio_path": "audios/i will require less amount of current assuming that the.wav",
#         "words": "i will require less amount of current assuming that the".split()
#     },
#     {
#         "audio_path": "audios/now we will be concentrating on the indicator electrode of course.wav",
#         "words": "now we will be concentrating on the indicator electrode of course".split()
#     },
#     {
#         "audio_path": "audios/so now we are talking about the indicator electrode metal.wav",
#         "words": "so now we are talking about the indicator electrode metal".split()
#     },
#     {
#         "audio_path": "audios/we are talking about the change in the potential.wav",
#         "words": "we are talking about the change in the potential".split()
#     },
#     {
#         "audio_path": "audios/then you can produce sugar.wav",
#         "words": "then you can produce sugar".split()
#     },
#     {
#         "audio_path": "audios/you have some kind of seasonal input input is available in a particular season.wav",
#         "words": "you have some kind of seasonal input input is available in a particular season".split()
#     },
#     {
#         "audio_path": "audios/if i talk within a factory.wav",
#         "words": "if i talk within a factory".split()
#     },
#     {
#         "audio_path": "audios/a stimulation is sustained then it is negative emotion.wav",
#         "words": "a stimulation is sustained then it is negative emotion".split()
#     },
#     {
#         "audio_path": "audios/these are the three criterias.wav",
#         "words": "these are the three criterias".split()
#     }
# ]

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
    # Save function
    # -------------------------------
    # def save_annotations():
    #     rows = []
    #     for idx, labels in st.session_state.annotations.items():
    #         rows.append({
    #             "email": email,
    #             "audio_idx": idx,
    #             "labels": str(labels)
    #         })

    #     new_df = pd.DataFrame(rows)

    #     global annotations_df
    #     annotations_df = annotations_df[annotations_df["email"] != email]
    #     annotations_df = pd.concat([annotations_df, new_df], ignore_index=True)

    #     save_annotations()
    # def get_gsheet():
    # creds = Credentials.from_service_account_info(
    #     st.secrets["gcp_service_account"],
    #     scopes=[
    #         "https://www.googleapis.com/auth/spreadsheets",
    #         "https://www.googleapis.com/auth/drive"
    #     ],
    # )
    # client = gspread.authorize(creds)
    # return client.open("1MHM4Oo9tGsCSDr6UQNnx43P29qQ3bJ-LL-fAQGCa0Pc")
    # def get_gsheet():
    #     creds = Credentials.from_service_account_info(
    #         st.secrets["gcp_service_account"],
    #         scopes=[
    #             "https://www.googleapis.com/auth/spreadsheets",
    #             "https://www.googleapis.com/auth/drive"
    #         ],
    #     )
    
    #     client = gspread.authorize(creds)
    #     return client.open("1MHM4Oo9tGsCSDr6UQNnx43P29qQ3bJ-LL-fAQGCa0Pc")
    
    #     # client = gspread.authorize(creds)
    #     # return client.open("1MHM4Oo9tGsCSDr6UQNnx43P29qQ3bJ-LL-fAQGCa0Pc")

    # def save_participant(name, email, gender, mother_tongue, native_place, proficiency):
    #     sheet = get_gsheet().worksheet("participants")
    #     sheet.append_row([email, name, gender, mother_tongue, native_place, proficiency])
    
    # def save_annotations():
    #     sheet = get_gsheet().worksheet("annotations")
    
    #     for audio_idx, labels in st.session_state.annotations.items():
    #         words = data[audio_idx]["words"]
    
    #         for word_idx, label in enumerate(labels):
    #             sheet.append_row([
    #                 email,
    #                 audio_idx,
    #                 word_idx,
    #                 words[word_idx],
    #                 label
    #             ])

    # -------------------------------
    # UI
    # -------------------------------
    WORDS_PER_ROW = 4

    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    
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
    
        st.divider()
    # WORDS_PER_ROW = 4
    
    # if "annotations" not in st.session_state:
    #     st.session_state.annotations = {}
    
    # for idx, item in enumerate(data):

    #     words = item["words"]
    
    #     if idx not in st.session_state.annotations:
    #         st.session_state.annotations[idx] = [0]*len(words)
    
    #     for row_start in range(0, len(words), WORDS_PER_ROW):
    
    #         row_words = words[row_start:row_start+WORDS_PER_ROW]
    #         cols = st.columns(len(row_words))
    
    #         for i, (col, word) in enumerate(zip(cols, row_words)):
    #             global_idx = row_start + i
    
    #             with col:
    #                 key = f"{idx}_{global_idx}"
    
    #                 if key not in st.session_state:
    #                     st.session_state[key] = bool(st.session_state.annotations[idx][global_idx])
    
    #                 checked = st.checkbox(word, key=key)
    
    #                 st.session_state.annotations[idx][global_idx] = int(checked)

    # WORDS_PER_ROW = 4

    # for idx, item in enumerate(data):

    #     words = item["words"]

    #     # Ensure correct length
    #     if idx not in st.session_state.annotations:
    #     #     st.session_state.annotations[idx] = [0]*len(words)
    #     # elif len(st.session_state.annotations[idx]) != len(words):
    #     #     st.session_state.annotations[idx] = [0]*len(words)

    #     total = len(words)
    #     selected = sum(st.session_state.annotations[idx])

    #     st.markdown(f"### Audio {idx+1} ({total} words)")
    #     st.progress(selected / total)

    #     st.audio(item["audio_path"])
    #     st.write("")
    #     for row_start in range(0, len(words), WORDS_PER_ROW):
        
    #         row_words = words[row_start:row_start+WORDS_PER_ROW]
    #         cols = st.columns(len(row_words))
        
    #         for i, (col, word) in enumerate(zip(cols, row_words)):
    #             global_idx = row_start + i
        
    #             with col:
    #                 # st.session_state.annotations[idx][global_idx] = 1 - value
    #                 value = st.session_state.annotations[idx][global_idx]
        
    #                 label = f"🔴 {word}" if value == 1 else word
        
    #                 if st.button(label, key=f"{idx}_{global_idx}", use_container_width=True):
    #                    st.session_state.annotations[idx][global_idx] = 1 - st.session_state.annotations[idx][global_idx]
    #     # WORD GRID (stable)
    #     for row_start in range(0, len(words), WORDS_PER_ROW):

    #         row_words = words[row_start:row_start+WORDS_PER_ROW]
    #         cols = st.columns(len(row_words))

    #         for i, (col, word) in enumerate(zip(cols, row_words)):
    #             global_idx = row_start + i

    #             with col:

    #                 value = st.session_state.annotations[idx][global_idx]

    #                 label = f"🔴 {word}" if value == 1 else word
    #                 if st.button(word, key=f"{idx}_{global_idx}", use_container_width=True):
                    
    #                     current = st.session_state.annotations[idx][global_idx]
    #                     st.session_state.annotations[idx][global_idx] = 1 - current
                    
    #                 value = st.session_state.annotations[idx][global_idx]
                    
    #                 label = f"🔴 {word}" if value == 1 else word
                    
    #                 st.write(label)
    #                     # save_annotations()
    #                     # st.rerun()

        # st.divider()

    # -------------------------------
    # Submit
    # -------------------------------
    if st.button("Submit"):
        save_annotations()
        st.success("All annotations saved!")

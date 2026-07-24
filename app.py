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
#######################24_07_26#############################################
DATA = [
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_46_sprt1.wav', 'words': ['IT', 'IS', 'A', 'MEASURE', 'THAT', 'CONFLICTS_V', 'WITH', 'A', 'LONG', 'TERM', 'POLICY']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_47_sprt1.wav', 'words': ['WHEN', 'ARE', 'THEY', 'GOING', 'TO', 'IMPLEMENT', 'THE', 'SCHEME']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_49_sprt1.wav', 'words': ['THE', 'VILLAGE', 'LOOKS', 'QUITE', 'DESERTED']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_50_sprt1.wav', 'words': ['BUSINESSES', 'MUST', 'EXPORT_V', 'TO', 'SURVIVE']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_51_sprt1.wav', 'words': ['THE', 'POLICE', 'SUSPECT_V', 'A', 'CONSPIRACY']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_52_sprt1.wav', 'words': ['THEY', 'SELL', 'FRESH', 'FARM', 'PRODUCE_N']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_56_sprt1.wav', 'words': ['MANY', 'PEOPLE', 'DISLIKE', 'TRAVELLING', 'BY', 'PUBLIC', 'TRANSPORT_N']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_59_sprt1.wav', 'words': ['STAFF', 'MUST', 'RECORD_V', 'ALL', 'ACCIDENTS', 'IN', 'THE', 'BOOK']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_60_sprt1.wav', 'words': ['THEY', 'HAVE', 'MADE', 'RECORD_ADJ', 'PROFITS', 'FROM', 'THE', 'SALE', 'OF', 'COMPUTERS']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_61_sprt1.wav', 'words': ['HE', 'WAS', 'ATTACKED', 'WITH', 'A', 'SHARP', 'IMPLEMENT']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_62_sprt1.wav', 'words': ['THEY', 'IGNORED', 'HIS', 'WARNINGS', 'ABOUT', 'THEIR', 'CONDUCT_N']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKE_63_sprt1.wav', 'words': ['IT', 'IS', 'EASY', 'TO', 'IMAGINE', 'CONFLICTS_N', 'OF', 'INTEREST']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKF_03_sprt1.wav', 'words': ["I'D", 'LIKE', 'PRAWN', 'COCKTAIL', 'AS', 'A', 'STARTER', 'AND', 'THEN', 'ROAST', 'CHICKEN']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKF_06_sprt1.wav', 'words': ['I', 'WOULD', 'LIKE', 'PORK', 'CHOPS', 'WITH', 'FRIED', 'POTATOES', 'GREEN', 'BEANS', 'AND', 'A', 'BOTTLE', 'OF', 'WINE']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKF_08_sprt1.wav', 'words': ['COULD', 'I', 'HAVE', 'LAMB', 'WITH', 'BOILED', 'POTATOES', 'PEAS', 'AND', 'A', 'GLASS', 'OF', 'WATER', 'AND', 'FOR', 'DESSERT', 'CAN', 'I', 'HAVE', 'FRUIT', 'SALAD']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKF_09_sprt1.wav', 'words': ['I', 'WANT', 'A', 'SALAD', 'THEN', 'BEEF', 'WITH', 'BOILED', 'POTATOES', 'BROAD', 'BEANS', 'AND', 'A', 'BOTTLE', 'OF', 'WATER']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_01_sprt1.wav', 'words': ['THIS', 'SUMMER', "I'D", 'LIKE', 'TO', 'VISIT', 'ROME', 'FOR', 'A', 'FEW', 'DAYS']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_02_sprt1.wav', 'words': ["I'D", 'LIKE', 'TO', 'GO', 'TO', 'SPAIN', 'JUST', 'FOR', 'A', 'FORTNIGHT']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_03_sprt1.wav', 'words': ["WE'RE", 'PLANNING', 'TO', 'TRAVEL', 'TO', 'EGYPT', 'FOR', 'A', 'WEEK', 'OR', 'SO']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_04_sprt1.wav', 'words': ['THIS', 'YEAR', "I'D", 'LOVE', 'TO', 'GO', 'TO', 'JAPAN']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_05_sprt1.wav', 'words': ["I'D", 'LIKE', 'TO', 'VISIT', 'RUSSIA', 'JUST', 'FOR', 'A', 'WEEKEND', 'OR', 'SO']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_06_sprt1.wav', 'words': ['I', 'PLAN', 'TO', 'GO', 'TO', 'THE', 'UNITED', 'STATES']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_07_sprt1.wav', 'words': ['I', 'WOULD', 'LIKE', 'TO', 'GO', 'TO', 'CHINA', 'FOR', 'A', 'COUPLE', 'OF', 'WEEKS']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_08_sprt1.wav', 'words': ['THIS', 'YEAR', 'WE', 'PLAN', 'TO', 'GO', 'TO', 'NEW', 'YORK', 'FOR', 'TEN', 'DAYS']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_09_sprt1.wav', 'words': ['THIS', 'YEAR', "HE'S", 'HOPING', 'TO', 'STAY', 'IN', 'PARIS', 'JUST', 'FOR', 'A', 'COUPLE', 'OF', 'WEEKS']},
    {'audio_path': 'audio/ISLE_SESS0161_BLOCKG_11_sprt1.wav', 'words': ['THIS', 'SUMMER', "I'M", 'GOING', 'TO', 'GERMANY', 'JUST', 'FOR', 'TEN', 'DAYS']},
    {'audio_path': 'audio/ISLE_SESS0162_BLOCKD01_01_sprt1.wav', 'words': ['I', 'SAID', 'WHITE', 'NOT', 'BAIT']},
    {'audio_path': 'audio/ISLE_SESS0162_BLOCKD01_02_sprt1.wav', 'words': ['I', 'SAID', 'NEW', 'NOT', 'NO']},
    {'audio_path': 'audio/ISLE_SESS0162_BLOCKD01_03_sprt1.wav', 'words': ['I', 'SAID', 'BAD', 'NOT', 'BED']},
    {'audio_path': 'audio/ISLE_SESS0162_BLOCKD01_04_sprt1.wav', 'words': ['I', 'SAID', 'LATE', 'NOT', 'SITE']},
    {'audio_path': 'audio/ISLE_SESS0162_BLOCKD01_05_sprt1.wav', 'words': ['I', 'SAID', 'FIGHT', 'NOT', 'CENTRE']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKD01_78_sprt1.wav', 'words': ["WHAT'S", 'SHE', 'WEARING', "SHE'S", 'WEARING', 'A', 'LEATHER', 'JACKET', 'AND', 'CORDUROY', 'TROUSERS']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKD01_80_sprt1.wav', 'words': ["SHE'S", 'WEARING', 'A', 'BROWN', 'WOOLY', 'HAT', 'AND', 'A', 'RED', 'SCARF']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKD01_81_sprt1.wav', 'words': ["HE'S", 'WEARING', 'A', 'YELLOW', 'SCARF', 'AND', 'A', 'FLOWERY', 'SHIRT']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_01_sprt1.wav', 'words': ['THE', 'REFEREE', 'NEEDED', 'A', 'POLICE', 'ESCORT_N', 'AFTER', 'THE', 'MATCH']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_03_sprt1.wav', 'words': ['I', "WASN'T", 'PRESENT_ADJ', 'AT', 'THE', 'LAST', 'MEETING']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_04_sprt1.wav', 'words': ['THEY', 'WANTED', 'TO', 'PROTEST_V', 'AGAINST', 'STUDENT', 'FEES']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_05_sprt1.wav', 'words': ['HE', 'HAS', 'HIS', 'OWN', 'PHOTOGRAPHIC', 'STUDIO']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_06_sprt1.wav', 'words': ['EU', 'NATIONALS', "DON'T", 'NEED', 'WORK', 'PERMITS_N']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_08_sprt1.wav', 'words': ['SINGERS', 'LEARN', 'HOW', 'TO', 'PROJECT_V', 'THEIR', 'VOICES']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_10_sprt1.wav', 'words': ['I', 'AM', 'UNABLE', 'TO', 'ESTIMATE_V', 'THE', 'COST']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_11_sprt1.wav', 'words': ['THE', 'COMPANY', 'EXPECTS', 'TO', 'INCREASE_V', 'ITS', 'WORKFORCE', 'NEXT', 'YEAR']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_12_sprt1.wav', 'words': ['THE', 'GOVERNMENT', 'PUBLISHED', 'AN', 'ESTIMATE_N', 'OF', 'FUTURE', 'TAX', 'INCOME']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_13_sprt1.wav', 'words': ['THE', 'COMMITTEE', 'WILL', 'CONDUCT_V', 'A', 'FULL', 'INVESTIGATION', 'INTO', 'HIS', 'BEHAVIOUR']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_14_sprt1.wav', 'words': ['OVER', 'THE', 'NEXT', 'TWO', 'WEEKS', 'EACH', 'PAIR', 'WILL', 'CONTEST_V', 'EIGHT', 'GAMES']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_15_sprt1.wav', 'words': ['THEY', 'SHOULD', 'SURVEY_V', 'ALL', 'STAFF', 'ON', 'THIS', 'QUESTION']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_18_sprt1.wav', 'words': ['WE', 'NEED', 'TO', 'PROGRESS_V', 'TO', 'A', 'HIGHER', 'LEVEL']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_21_sprt1.wav', 'words': ['HE', "HADN'T", 'INTENDED', 'TO', 'INSULT_V', 'THE', 'POLICEMAN']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_22_sprt1.wav', 'words': ['THEIR', 'MUSICAL', 'STYLES', 'CONTRAST_V', 'STRONGLY']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_23_sprt1.wav', 'words': ["SHE'S", 'A', 'GRADUATE_N', 'OF', 'CAMBRIDGE', 'UNIVERSITY']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_26_sprt1.wav', 'words': ['THE', 'TEAM', 'WILL', 'PRESENT_V', 'THEIR', 'RESULTS', 'AT', 'THE', 'CONFERENCE']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_27_sprt1.wav', 'words': ['YOUR', 'TICKET', 'DOES', 'NOT', 'INCLUDE', 'TRANSFER_N', 'FROM', 'THE', 'AIRPORT', 'TO', 'YOUR', 'HOTEL']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_28_sprt1.wav', 'words': ['THE', 'COMPANY', 'CANNOT', 'SELL', 'ITS', 'REJECT_ADJ', 'FURNITURE']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_29_sprt1.wav', 'words': ["HE'S", 'A', 'PHOTOGRAPHER']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_30_sprt1.wav', 'words': ['THE', 'REBEL_N', 'LEADER', 'HAS', 'BEEN', 'ARRESTED']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_32_sprt1.wav', 'words': ['HE', 'TAKES', 'WONDERFUL', 'BUT', 'STRANGE', 'PHOTOGRAPHS']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_33_sprt1.wav', 'words': ['THEY', 'PREDICT', 'A', 'CLOSE', 'CONTEST_N', 'AT', 'THE', 'NEXT', 'ELECTION']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_34_sprt1.wav', 'words': ['STUDENTS', 'STAGED', 'A', 'PROTEST_N', 'MARCH', 'OUTSIDE', 'PARLIAMENT']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_37_sprt1.wav', 'words': ['FOOD', 'AND', 'CLOTHING', 'IMPORTS_N', 'ARE', 'RISING']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_38_sprt1.wav', 'words': ['EXPORT_N', 'ORDERS', 'ARE', 'HIGHER', 'THAN', 'LAST', 'YEAR']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_39_sprt1.wav', 'words': ['SHE', 'EXPECTS', 'TO', 'GRADUATE_V', 'NEXT', 'SUMMER']},
    {'audio_path': 'audio/ISLE_SESS0015_BLOCKE_42_sprt1.wav', 'words': ['THEY', 'HAD', 'TO', 'REJECT_V', 'HIS', 'PLAN']},
    {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_03_sprt1.wav', 'words': ['I', "WASN'T", 'PRESENT', 'AT', 'THE', 'LAST', 'MEETING']},
    {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_04_sprt1.wav', 'words': ['THEY', 'WANTED', 'TO', 'PROTEST', 'AGAINST', 'STUDENT', 'FEES']},
    {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_21_sprt1.wav', 'words': ['HE', "HADN'T", 'INTENDED', 'TO', 'INSULT', 'THE', 'POLICEMAN']},
    {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_31_sprt1.wav', 'words': ['THE', 'PROJECT', 'HAS', 'PROVIDED', 'VALUABLE', 'EXPERIENCE']},
    {'audio_path': 'audio/ISLE_SESS0181_BLOCKE_39_sprt1.wav', 'words': ['SHE', 'EXPECTS', 'TO', 'GRADUATE_V', 'NEXT', 'SUMMER']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_01_sprt1.wav', 'words': ['I', 'SAID', 'WHITE', 'NOT', 'BAIT']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_02_sprt1.wav', 'words': ['I', 'SAID', 'NEW', 'NOT', 'NO']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_03_sprt1.wav', 'words': ['I', 'SAID', 'BAD', 'NOT', 'BED']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_04_sprt1.wav', 'words': ['I', 'SAID', 'LATE', 'NOT', 'SITE']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_07_sprt1.wav', 'words': ['I', 'SAID', 'CLOTHES', 'NOT', 'BIOLOGICAL']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_08_sprt1.wav', 'words': ['I', 'SAID', 'PUT', 'NOT', 'BLUE']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_09_sprt1.wav', 'words': ['I', 'SAID', 'LIVE', 'NOT', 'BED']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_10_sprt1.wav', 'words': ['I', 'SAID', 'ALONE', 'NOT', 'GONE']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_18_sprt1.wav', 'words': ['I', 'SAID', 'CLIMBING', 'NOT', 'CHEESE']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_19_sprt1.wav', 'words': ['I', 'SAID', 'PSYCHOLOGY', 'NOT', 'PNEUMATIC']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_31_sprt1.wav', 'words': ['WHAT', 'IS', 'SHE', 'DRINKING', 'A', 'CUP', 'OF', 'COFFEE']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_35_sprt1.wav', 'words': ['A', 'MUG', 'OF', 'TEA']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_43_sprt1.wav', 'words': ['IN', 'A', 'PARK', 'NEAR', 'A', 'PATH']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_44_sprt1.wav', 'words': ['BESIDE', 'A', 'TREE', 'IN', 'A', 'PARK']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_78_sprt1.wav', 'words': ["WHAT'S", 'SHE', 'WEARING', "SHE'S", 'WEARING', 'A', 'LEATHER', 'JACKET', 'AND', 'CORDUROY', 'TROUSERS']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_79_sprt1.wav', 'words': ["WHAT'S", 'HE', 'WEARING', "HE'S", 'WEARING', 'A', 'BIG', 'BEIGE', 'JUMPER', 'AND', 'A', 'COWBOY', 'HAT']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKD01_80_sprt1.wav', 'words': ["SHE'S", 'WEARING', 'A', 'BROWN', 'WOOLY', 'HAT', 'AND', 'RED', 'SCARF']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKE_01_sprt1.wav', 'words': ['THE', 'REFEREE', 'NEEDED', 'A', 'POLICE', 'ESCORT', 'AFTER', 'THE', 'MATCH']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKE_09_sprt1.wav', 'words': ['THE', 'PRIME', 'SUSPECT', 'IS', 'THE', 'DIRECTOR']},
    {'audio_path': 'audio/ISLE_SESS0182_BLOCKE_14_sprt1.wav', 'words': ['OVER', 'THE', 'NEXT', 'TWO', 'WEEKS', 'EACH', 'PAIR', 'WILL', 'CONTEST', 'EIGHT', 'GAMES']},
]

GROUND_TRUTH = {
    0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    1: [0, 0, 0, 0, 0, 0, 0, 0],
    2: [0, 0, 0, 0, 0],
    3: [0, 0, 0, 0, 0],
    4: [0, 0, 0, 0, 0],
    5: [0, 0, 0, 0, 0],
    6: [0, 0, 0, 0, 0, 0, 0],
    7: [0, 0, 0, 0, 0, 0, 0, 0],
    8: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    9: [0, 0, 0, 0, 0, 0, 0],
    10: [0, 0, 0, 0, 0, 0, 0],
    11: [0, 0, 0, 0, 0, 0, 0, 0],
    12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    14: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    15: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    16: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    17: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    18: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    19: [0, 0, 0, 0, 0, 0, 0, 0],
    20: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    21: [0, 0, 0, 0, 0, 0, 0, 0],
    22: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    23: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    24: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    25: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    26: [0, 0, 0, 0, 0],
    27: [0, 0, 0, 0, 0],
    28: [0, 0, 0, 0, 0],
    29: [0, 0, 0, 0, 0],
    30: [0, 0, 0, 0, 0],
    31: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    32: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    33: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    34: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    35: [0, 0, 0, 0, 0, 0, 0],
    36: [0, 0, 0, 0, 0, 0, 0],
    37: [0, 0, 0, 0, 0, 0],
    38: [0, 0, 0, 0, 0, 0],
    39: [0, 0, 0, 0, 0, 0, 0],
    40: [0, 0, 0, 0, 0, 0, 0],
    41: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    42: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    43: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    44: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    45: [0, 0, 0, 0, 0, 0, 0, 0],
    46: [0, 0, 0, 0, 0, 0, 0, 0],
    47: [0, 0, 0, 0, 0, 0, 0],
    48: [0, 0, 0, 0, 0],
    49: [0, 0, 0, 0, 0, 0],
    50: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    51: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    52: [0, 0, 0, 0, 0, 0, 0],
    53: [0, 0, 0],
    54: [0, 0, 0, 0, 0, 0],
    55: [0, 0, 0, 0, 0, 0],
    56: [0, 0, 0, 0, 0, 0, 0, 0, 0],
    57: [0, 0, 0, 0, 0, 0, 0],
    58: [0, 0, 0, 0, 0, 0],
    59: [0, 0, 0, 0, 0, 0, 0],
    60: [0, 0, 0, 0, 0, 0],
    61: [0, 0, 0, 0, 0, 0],
    62: [0, 0, 1, 0, 0, 0, 0],
    63: [0, 0, 0, 1, 0, 0, 0],
    64: [0, 0, 1, 0, 1, 0, 0],
    65: [0, 1, 0, 0, 0, 0],
    66: [0, 1, 0, 0, 0, 1],
    67: [0, 0, 1, 0, 1],
    68: [0, 0, 1, 0, 1],
    69: [0, 0, 1, 0, 0],
    70: [0, 0, 1, 0, 0],
    71: [0, 0, 1, 0, 1],
    72: [0, 0, 1, 0, 0],
    73: [0, 0, 1, 0, 0],
    74: [0, 0, 1, 0, 0],
    75: [0, 0, 1, 0, 0],
    76: [0, 0, 1, 0, 1],
    77: [0, 0, 0, 1, 0, 0, 0, 1],
    78: [0, 1, 0, 1],
    79: [0, 0, 1, 0, 0, 1],
    80: [1, 0, 0, 0, 0, 1],
    81: [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    82: [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    83: [0, 1, 0, 1, 1, 1, 0, 1, 0],
    84: [0, 1, 0, 0, 0, 1, 0, 0, 0],
    85: [0, 1, 1, 0, 0, 1],
    86: [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
}

###################22_07_26_fastspeech_audios_set_2##############################
# DATA = [
#     {"audio_path": "audios/you can also select left or right tank for the fuel supply.wav", "words": ["you", "can", "also", "select", "left", "or", "right", "tank", "for", "the", "fuel", "supply"]},
#     {"audio_path": "audios/either they have specified.wav", "words": ["either", "they", "have", "specified"]},
#     {"audio_path": "audios/then you will really get the juice of this fundamental understanding.wav", "words": ["then", "you", "will", "really", "get", "the", "juice", "of", "this", "fundamental", "understanding"]},
#     {"audio_path": "audios/so a single propeller if something happens what will happen.wav", "words": ["so", "a", "single", "propeller", "if", "something", "happens", "what", "will", "happen"]},
#     {"audio_path": "audios/i am just showing it for a short while.wav", "words": ["i", "am", "just", "showing", "it", "for", "a", "short", "while"]},
#     {"audio_path": "audios/and sometimes when we take care of there is a reduction in the voltage or increase in the voltage.wav", "words": ["and", "sometimes", "when", "we", "take", "care", "of", "there", "is", "a", "reduction", "in", "the", "voltage", "or", "increase", "in", "the", "voltage"]},
#     {"audio_path": "audios/now the inverter what it gets out will also be of the order of fifty volts or something.wav", "words": ["now", "the", "inverter", "what", "it", "gets", "out", "will", "also", "be", "of", "the", "order", "of", "fifty", "volts", "or", "something"]},
#     {"audio_path": "audios/it is unloading itself on the load.wav", "words": ["it", "is", "unloading", "itself", "on", "the", "load"]},
#     {"audio_path": "audios/there are few challenges.wav", "words": ["there", "are", "few", "challenges"]},
#     {"audio_path": "audios/so they are planted for the bio refinery or energy purposes.wav", "words": ["so", "they", "are", "planted", "for", "the", "bio", "refinery", "or", "energy", "purposes"]},
#     {"audio_path": "audios/it is not about the energy demand or energy requirement.wav", "words": ["it", "is", "not", "about", "the", "energy", "demand", "or", "energy", "requirement"]},
#     {"audio_path": "audios/because they can tell what is the best way to use this product.wav", "words": ["because", "they", "can", "tell", "what", "is", "the", "best", "way", "to", "use", "this", "product"]},
#     {"audio_path": "audios/then i am selling products of male utilities.wav", "words": ["then", "i", "am", "selling", "products", "of", "male", "utilities"]},
#     {"audio_path": "audios/so like if i am specialized in developing the overhead tanks.wav", "words": ["so", "like", "if", "i", "am", "specialized", "in", "developing", "the", "overhead", "tanks"]},
#     {"audio_path": "audios/so i will be developing the overhead tanks.wav", "words": ["so", "i", "will", "be", "developing", "the", "overhead", "tanks"]},
#     {"audio_path": "audios/so i will make highways.wav", "words": ["so", "i", "will", "make", "highways"]},
#     {"audio_path": "audios/because that decision you can take whether you want a fluorescent attachment or not.wav", "words": ["because", "that", "decision", "you", "can", "take", "whether", "you", "want", "a", "fluorescent", "attachment", "or", "not"]},
#     {"audio_path": "audios/we consider that life will cannot be positively oriented for somebody.wav", "words": ["we", "consider", "that", "life", "will", "cannot", "be", "positively", "oriented", "for", "somebody"]},
#     {"audio_path": "audios/this comes when you have a proper skeletal system which supports you.wav", "words": ["this", "comes", "when", "you", "have", "a", "proper", "skeletal", "system", "which", "supports", "you"]},
#     {"audio_path": "audios/so either i react this way or i will do the way i love.wav", "words": ["so", "either", "i", "react", "this", "way", "or", "i", "will", "do", "the", "way", "i", "love"]},
# ]

# GROUND_TRUTH = {
#     0:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     1:  [0, 0, 0, 0],
#     2:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     3:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     4:  [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     5:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     6:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     7:  [0, 0, 0, 0, 0, 0, 0],
#     8:  [0, 0, 0, 0],
#     9:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     11: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     12: [0, 0, 0, 0, 0, 0, 0, 0],
#     13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     14: [0, 0, 0, 0, 0, 0, 0, 0],
#     15: [0, 0, 0, 0, 0],
#     16: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     17: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     18: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     19: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# }
###################22_07_26_fastspeech_audios_set_1##############################
# DATA = [
#     {"audio_path": "audios/it will be done by one person.wav", "words": ["it", "will", "be", "done", "by", "one", "person"]},
#     {"audio_path": "audios/it is then statically stable in lateral mode but how does it generate.wav", "words": ["it", "is", "then", "statically", "stable", "in", "lateral", "mode", "but", "how", "does", "it", "generate"]},
#     {"audio_path": "audios/so do steady side slip maneuver you get.wav", "words": ["so", "do", "steady", "side", "slip", "maneuver", "you", "get"]},
#     {"audio_path": "audios/meeting half of the existing u.wav", "words": ["meeting", "half", "of", "the", "existing", "u"]},
#     {"audio_path": "audios/two point five percent of existing cropping area would.wav", "words": ["two", "point", "five", "percent", "of", "existing", "cropping", "area", "would"]},
#     {"audio_path": "audios/if you talk about micro algae to biodiesel.wav", "words": ["if", "you", "talk", "about", "micro", "algae", "to", "biodiesel"]},
#     {"audio_path": "audios/then this value is zero.wav", "words": ["then", "this", "value", "is", "zero"]},
#     {"audio_path": "audios/i am discussing the i s code recommendations because now i.wav", "words": ["i", "am", "discussing", "the", "i", "s", "code", "recommendations", "because", "now", "i"]},
#     {"audio_path": "audios/i will check the maximum settlement.wav", "words": ["i", "will", "check", "the", "maximum", "settlement"]},
#     {"audio_path": "audios/where as i want to interrupt fundamentally the current.wav", "words": ["where", "as", "i", "want", "to", "interrupt", "fundamentally", "the", "current"]},
#     {"audio_path": "audios/anything ultimately yields sinusoid.wav", "words": ["anything", "ultimately", "yields", "sinusoid"]},
#     {"audio_path": "audios/i will require less amount of current assuming that the.wav", "words": ["i", "will", "require", "less", "amount", "of", "current", "assuming", "that", "the"]},
#     {"audio_path": "audios/now we will be concentrating on the indicator electrode of course.wav", "words": ["now", "we", "will", "be", "concentrating", "on", "the", "indicator", "electrode", "of", "course"]},
#     {"audio_path": "audios/so now we are talking about the indicator electrode metal.wav", "words": ["so", "now", "we", "are", "talking", "about", "the", "indicator", "electrode", "metal"]},
#     {"audio_path": "audios/we are talking about the change in the potential.wav", "words": ["we", "are", "talking", "about", "the", "change", "in", "the", "potential"]},
#     {"audio_path": "audios/then you can produce sugar.wav", "words": ["then", "you", "can", "produce", "sugar"]},
#     {"audio_path": "audios/you have some kind of seasonal input input is available in a particular season.wav", "words": ["you", "have", "some", "kind", "of", "seasonal", "input", "input", "is", "available", "in", "a", "particular", "season"]},
#     {"audio_path": "audios/if i talk within a factory.wav", "words": ["if", "i", "talk", "within", "a", "factory"]},
#     {"audio_path": "audios/a stimulation is sustained then it is negative emotion.wav", "words": ["a", "stimulation", "is", "sustained", "then", "it", "is", "negative", "emotion"]},
#     {"audio_path": "audios/these are the three criterias.wav", "words": ["these", "are", "the", "three", "criterias"]},
# ]

# GROUND_TRUTH = {
#     0:  [0, 0, 0, 0, 0, 0, 0],
#     1:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     2:  [0, 0, 0, 0, 0, 0, 0, 0],
#     3:  [0, 0, 0, 0, 0, 0],
#     4:  [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     5:  [0, 0, 0, 0, 0, 0, 0, 0],
#     6:  [0, 0, 0, 0, 0],
#     7:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     8:  [0, 0, 0, 0, 0, 0],
#     9:  [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     10: [0, 0, 0, 0],
#     11: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     14: [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     15: [0, 0, 0, 0, 0],
#     16: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     17: [0, 0, 0, 0, 0, 0],
#     18: [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     19: [0, 0, 0, 0, 0],
# }
################################22_06_26##########20_07_26###############################################
# DATA = [
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_06_sprt1.wav", "words": ["I", "SAID", "SNOW", "NOT", "TOMORROW"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_07_sprt1.wav", "words": ["I", "SAID", "CLOTHES", "NOT", "BIOLOGICAL"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_11_sprt1.wav", "words": ["I", "SAID", "PHRASE", "NOT", "BAR"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_12_sprt1.wav", "words": ["I", "SAID", "GOT", "NOT", "GOAT"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_13_sprt1.wav", "words": ["I", "SAID", "MEET", "NOT", "WATER"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_14_sprt1.wav", "words": ["I", "SAID", "CHEAP", "NOT", "OTHER"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_15_sprt1.wav", "words": ["I", "SAID", "THROUGH", "NOT", "TOUGH"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_17_sprt1.wav", "words": ["I", "SAID", "BOOK", "NOT", "DO"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_18_sprt1.wav", "words": ["I", "SAID", "CLIMBING", "NOT", "CHEESE"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKD01_21_sprt1.wav", "words": ["I", "SAID", "HATE", "NOT", "TIN"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKE_57_sprt1.wav", "words": ["I", "THINK", "IT'S", "EXTRAORDINARY"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKE_58_sprt1.wav", "words": ["THAT", "ADVERT", "SHOULD", "BE", "BANNED"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKE_59_sprt1.wav", "words": ["STAFF", "MUST", "RECORD", "ALL", "ACCIDENTS", "IN", "THE", "BOOK"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKF_01_sprt1.wav", "words": ["COULD", "I", "HAVE", "CHICKEN", "SOUP", "AS", "A", "STARTER", "AND", "THEN", "LAMB", "CHOPS"]},
#     {"audio_path": "audio/ISLE_SESS0183_BLOCKG_07_sprt1.wav", "words": ["I", "WOULD", "LIKE", "TO", "GO", "TO", "CHINA", "FOR", "A", "COUPLE", "OF", "WEEKS"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_01_sprt1.wav", "words": ["I", "SAID", "WHITE", "NOT", "BAIT"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_02_sprt1.wav", "words": ["I", "SAID", "NEW", "NOT", "NO"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_04_sprt1.wav", "words": ["I", "SAID", "LATE", "NOT", "SITE"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_05_sprt1.wav", "words": ["I", "SAID", "FIGHT", "NOT", "CENTRE"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_06_sprt1.wav", "words": ["I", "SAID", "SNOW", "NOT", "TOMORROW"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_08_sprt1.wav", "words": ["I", "SAID", "PUT", "NOT", "BLUE"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_17_sprt1.wav", "words": ["I", "SAID", "BOOK", "NOT", "DO"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_18_sprt1.wav", "words": ["I", "SAID", "CLIMBING", "NOT", "CHEESE"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_19_sprt1.wav", "words": ["I", "SAID", "PSYCHOLOGY", "NOT", "PNEUMATIC"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_20_sprt1.wav", "words": ["I", "SAID", "THIN", "NOT", "SHEEP"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_22_sprt1.wav", "words": ["I", "SAID", "WON'T", "NOT", "UDDER"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_23_sprt1.wav", "words": ["I", "SAID", "SIXTHS", "NOT", "BIOLOGY"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_26_sprt1.wav", "words": ["I", "SAID", "CALL", "NOT", "SHALL"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_27_sprt1.wav", "words": ["I", "SAID", "DON'T", "NOT", "SHOULDER"]},
#     {"audio_path": "audio/ISLE_SESS0184_BLOCKD01_28_sprt1.wav", "words": ["I", "SAID", "WOULD", "NOT", "FILM"]},
# ]

# GROUND_TRUTH = {
#     0:  [0, 0, 1, 0, 1],
#     1:  [0, 0, 1, 0, 0],
#     2:  [0, 0, 1, 0, 1],
#     3:  [0, 0, 0, 0, 1],
#     4:  [0, 0, 1, 0, 1],
#     5:  [0, 0, 1, 0, 0],
#     6:  [0, 0, 0, 0, 1],
#     7:  [0, 0, 1, 0, 1],
#     8:  [0, 0, 1, 0, 1],
#     9:  [0, 0, 1, 0, 0],
#     10: [0, 0, 0, 1],
#     11: [1, 0, 0, 0, 0],
#     12: [0, 1, 0, 0, 0, 0, 0, 0],
#     13: [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
#     14: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     15: [0, 0, 1, 0, 1],
#     16: [0, 0, 1, 0, 1],
#     17: [0, 0, 0, 0, 1],
#     18: [0, 0, 1, 0, 1],
#     19: [0, 0, 1, 0, 0],
#     20: [0, 0, 1, 0, 0],
#     21: [0, 0, 1, 0, 1],
#     22: [0, 0, 1, 0, 1],
#     23: [1, 0, 1, 0, 0],
#     24: [0, 0, 1, 0, 1],
#     25: [0, 1, 1, 0, 0],
#     26: [0, 0, 1, 0, 1],
#     27: [0, 0, 1, 0, 1],
#     28: [0, 0, 1, 0, 1],
#     29: [0, 0, 1, 1, 1],
# }





####################16_07_26##############################
# DATA = [
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_46_sprt1.wav", "words": ["IT", "IS", "A", "MEASURE", "THAT", "CONFLICTS_V", "WITH", "A", "LONG", "TERM", "POLICY"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_47_sprt1.wav", "words": ["WHEN", "ARE", "THEY", "GOING", "TO", "IMPLEMENT", "THE", "SCHEME"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_49_sprt1.wav", "words": ["THE", "VILLAGE", "LOOKS", "QUITE", "DESERTED"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_50_sprt1.wav", "words": ["BUSINESSES", "MUST", "EXPORT_V", "TO", "SURVIVE"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_51_sprt1.wav", "words": ["THE", "POLICE", "SUSPECT_V", "A", "CONSPIRACY"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_52_sprt1.wav", "words": ["THEY", "SELL", "FRESH", "FARM", "PRODUCE_N"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_56_sprt1.wav", "words": ["MANY", "PEOPLE", "DISLIKE", "TRAVELLING", "BY", "PUBLIC", "TRANSPORT_N"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_59_sprt1.wav", "words": ["STAFF", "MUST", "RECORD_V", "ALL", "ACCIDENTS", "IN", "THE", "BOOK"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_60_sprt1.wav", "words": ["THEY", "HAVE", "MADE", "RECORD_ADJ", "PROFITS", "FROM", "THE", "SALE", "OF", "COMPUTERS"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_61_sprt1.wav", "words": ["HE", "WAS", "ATTACKED", "WITH", "A", "SHARP", "IMPLEMENT"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_62_sprt1.wav", "words": ["THEY", "IGNORED", "HIS", "WARNINGS", "ABOUT", "THEIR", "CONDUCT_N"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKE_63_sprt1.wav", "words": ["IT", "IS", "EASY", "TO", "IMAGINE", "CONFLICTS_N", "OF", "INTEREST"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKF_03_sprt1.wav", "words": ["I'D", "LIKE", "PRAWN", "COCKTAIL", "AS", "A", "STARTER", "AND", "THEN", "ROAST", "CHICKEN"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKF_06_sprt1.wav", "words": ["I", "WOULD", "LIKE", "PORK", "CHOPS", "WITH", "FRIED", "POTATOES", "GREEN", "BEANS", "AND", "A", "BOTTLE", "OF", "WINE"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKF_08_sprt1.wav", "words": ["COULD", "I", "HAVE", "LAMB", "WITH", "BOILED", "POTATOES", "PEAS", "AND", "A", "GLASS", "OF", "WATER", "AND", "FOR", "DESSERT", "CAN", "I", "HAVE", "FRUIT", "SALAD"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKF_09_sprt1.wav", "words": ["I", "WANT", "A", "SALAD", "THEN", "BEEF", "WITH", "BOILED", "POTATOES", "BROAD", "BEANS", "AND", "A", "BOTTLE", "OF", "WATER"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_01_sprt1.wav", "words": ["THIS", "SUMMER", "I'D", "LIKE", "TO", "VISIT", "ROME", "FOR", "A", "FEW", "DAYS"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_02_sprt1.wav", "words": ["I'D", "LIKE", "TO", "GO", "TO", "SPAIN", "JUST", "FOR", "A", "FORTNIGHT"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_03_sprt1.wav", "words": ["WE'RE", "PLANNING", "TO", "TRAVEL", "TO", "EGYPT", "FOR", "A", "WEEK", "OR", "SO"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_04_sprt1.wav", "words": ["THIS", "YEAR", "I'D", "LOVE", "TO", "GO", "TO", "JAPAN"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_05_sprt1.wav", "words": ["I'D", "LIKE", "TO", "VISIT", "RUSSIA", "JUST", "FOR", "A", "WEEKEND", "OR", "SO"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_06_sprt1.wav", "words": ["I", "PLAN", "TO", "GO", "TO", "THE", "UNITED", "STATES"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_07_sprt1.wav", "words": ["I", "WOULD", "LIKE", "TO", "GO", "TO", "CHINA", "FOR", "A", "COUPLE", "OF", "WEEKS"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_08_sprt1.wav", "words": ["THIS", "YEAR", "WE", "PLAN", "TO", "GO", "TO", "NEW", "YORK", "FOR", "TEN", "DAYS"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_09_sprt1.wav", "words": ["THIS", "YEAR", "HE'S", "HOPING", "TO", "STAY", "IN", "PARIS", "JUST", "FOR", "A", "COUPLE", "OF", "WEEKS"]},
#     {"audio_path": "audio/ISLE_SESS0161_BLOCKG_11_sprt1.wav", "words": ["THIS", "SUMMER", "I'M", "GOING", "TO", "GERMANY", "JUST", "FOR", "TEN", "DAYS"]},
#     {"audio_path": "audio/ISLE_SESS0162_BLOCKD01_01_sprt1.wav", "words": ["I", "SAID", "WHITE", "NOT", "BAIT"]},
#     {"audio_path": "audio/ISLE_SESS0162_BLOCKD01_02_sprt1.wav", "words": ["I", "SAID", "NEW", "NOT", "NO"]},
#     {"audio_path": "audio/ISLE_SESS0162_BLOCKD01_03_sprt1.wav", "words": ["I", "SAID", "BAD", "NOT", "BED"]},
#     {"audio_path": "audio/ISLE_SESS0162_BLOCKD01_04_sprt1.wav", "words": ["I", "SAID", "LATE", "NOT", "SITE"]},
#     {"audio_path": "audio/ISLE_SESS0162_BLOCKD01_05_sprt1.wav", "words": ["I", "SAID", "FIGHT", "NOT", "CENTRE"]},
# ]

# GROUND_TRUTH = {
#     0:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     1:  [0, 0, 0, 0, 0, 0, 0, 0],
#     2:  [0, 0, 0, 0, 0],
#     3:  [0, 0, 0, 0, 0],
#     4:  [0, 0, 0, 0, 0],
#     5:  [0, 0, 0, 0, 0],
#     6:  [0, 0, 0, 0, 0, 0, 0],
#     7:  [0, 0, 0, 0, 0, 0, 0, 0],
#     8:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     9:  [0, 0, 0, 0, 0, 0, 0],
#     10: [0, 0, 0, 0, 0, 0, 0],
#     11: [0, 0, 0, 0, 0, 0, 0, 0],
#     12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     14: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     15: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     16: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     17: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     18: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     19: [0, 0, 0, 0, 0, 0, 0, 0],
#     20: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     21: [0, 0, 0, 0, 0, 0, 0, 0],
#     22: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     23: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     24: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     25: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     26: [0, 0, 0, 0, 0],
#     27: [0, 0, 0, 0, 0],
#     28: [0, 0, 0, 0, 0],
#     29: [0, 0, 0, 0, 0],
#     30: [0, 0, 0, 0, 0],
# }
##############15_07_26######################
# DATA = [
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKD01_78_sprt1.wav", "words": ["WHAT'S", "SHE", "WEARING", "SHE'S", "WEARING", "A", "LEATHER", "JACKET", "AND", "CORDUROY", "TROUSERS"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKD01_80_sprt1.wav", "words": ["SHE'S", "WEARING", "A", "BROWN", "WOOLY", "HAT", "AND", "A", "RED", "SCARF"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKD01_81_sprt1.wav", "words": ["HE'S", "WEARING", "A", "YELLOW", "SCARF", "AND", "A", "FLOWERY", "SHIRT"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_01_sprt1.wav", "words": ["THE", "REFEREE", "NEEDED", "A", "POLICE", "ESCORT_N", "AFTER", "THE", "MATCH"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_03_sprt1.wav", "words": ["I", "WASN'T", "PRESENT_ADJ", "AT", "THE", "LAST", "MEETING"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_04_sprt1.wav", "words": ["THEY", "WANTED", "TO", "PROTEST_V", "AGAINST", "STUDENT", "FEES"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_05_sprt1.wav", "words": ["HE", "HAS", "HIS", "OWN", "PHOTOGRAPHIC", "STUDIO"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_06_sprt1.wav", "words": ["EU", "NATIONALS", "DON'T", "NEED", "WORK", "PERMITS_N"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_08_sprt1.wav", "words": ["SINGERS", "LEARN", "HOW", "TO", "PROJECT_V", "THEIR", "VOICES"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_10_sprt1.wav", "words": ["I", "AM", "UNABLE", "TO", "ESTIMATE_V", "THE", "COST"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_11_sprt1.wav", "words": ["THE", "COMPANY", "EXPECTS", "TO", "INCREASE_V", "ITS", "WORKFORCE", "NEXT", "YEAR"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_12_sprt1.wav", "words": ["THE", "GOVERNMENT", "PUBLISHED", "AN", "ESTIMATE_N", "OF", "FUTURE", "TAX", "INCOME"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_13_sprt1.wav", "words": ["THE", "COMMITTEE", "WILL", "CONDUCT_V", "A", "FULL", "INVESTIGATION", "INTO", "HIS", "BEHAVIOUR"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_14_sprt1.wav", "words": ["OVER", "THE", "NEXT", "TWO", "WEEKS", "EACH", "PAIR", "WILL", "CONTEST_V", "EIGHT", "GAMES"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_15_sprt1.wav", "words": ["THEY", "SHOULD", "SURVEY_V", "ALL", "STAFF", "ON", "THIS", "QUESTION"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_18_sprt1.wav", "words": ["WE", "NEED", "TO", "PROGRESS_V", "TO", "A", "HIGHER", "LEVEL"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_21_sprt1.wav", "words": ["HE", "HADN'T", "INTENDED", "TO", "INSULT_V", "THE", "POLICEMAN"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_22_sprt1.wav", "words": ["THEIR", "MUSICAL", "STYLES", "CONTRAST_V", "STRONGLY"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_23_sprt1.wav", "words": ["SHE'S", "A", "GRADUATE_N", "OF", "CAMBRIDGE", "UNIVERSITY"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_26_sprt1.wav", "words": ["THE", "TEAM", "WILL", "PRESENT_V", "THEIR", "RESULTS", "AT", "THE", "CONFERENCE"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_27_sprt1.wav", "words": ["YOUR", "TICKET", "DOES", "NOT", "INCLUDE", "TRANSFER_N", "FROM", "THE", "AIRPORT", "TO", "YOUR", "HOTEL"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_28_sprt1.wav", "words": ["THE", "COMPANY", "CANNOT", "SELL", "ITS", "REJECT_ADJ", "FURNITURE"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_29_sprt1.wav", "words": ["HE'S", "A", "PHOTOGRAPHER"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_30_sprt1.wav", "words": ["THE", "REBEL_N", "LEADER", "HAS", "BEEN", "ARRESTED"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_32_sprt1.wav", "words": ["HE", "TAKES", "WONDERFUL", "BUT", "STRANGE", "PHOTOGRAPHS"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_33_sprt1.wav", "words": ["THEY", "PREDICT", "A", "CLOSE", "CONTEST_N", "AT", "THE", "NEXT", "ELECTION"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_34_sprt1.wav", "words": ["STUDENTS", "STAGED", "A", "PROTEST_N", "MARCH", "OUTSIDE", "PARLIAMENT"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_37_sprt1.wav", "words": ["FOOD", "AND", "CLOTHING", "IMPORTS_N", "ARE", "RISING"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_38_sprt1.wav", "words": ["EXPORT_N", "ORDERS", "ARE", "HIGHER", "THAN", "LAST", "YEAR"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_39_sprt1.wav", "words": ["SHE", "EXPECTS", "TO", "GRADUATE_V", "NEXT", "SUMMER"]},
#     {"audio_path": "audio/ISLE_SESS0015_BLOCKE_42_sprt1.wav", "words": ["THEY", "HAD", "TO", "REJECT_V", "HIS", "PLAN"]},
# ]
# GROUND_TRUTH = {
#     0:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     1:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     2:  [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     3:  [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     4:  [0, 0, 0, 0, 0, 0, 0],
#     5:  [0, 0, 0, 0, 0, 0, 0],
#     6:  [0, 0, 0, 0, 0, 0],
#     7:  [0, 0, 0, 0, 0, 0],
#     8:  [0, 0, 0, 0, 0, 0, 0],
#     9:  [0, 0, 0, 0, 0, 0, 0],
#     10: [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     11: [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     14: [0, 0, 0, 0, 0, 0, 0, 0],
#     15: [0, 0, 0, 0, 0, 0, 0, 0],
#     16: [0, 0, 0, 0, 0, 0, 0],
#     17: [0, 0, 0, 0, 0],
#     18: [0, 0, 0, 0, 0, 0],
#     19: [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     20: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     21: [0, 0, 0, 0, 0, 0, 0],
#     22: [0, 0, 0],
#     23: [0, 0, 0, 0, 0, 0],
#     24: [0, 0, 0, 0, 0, 0],
#     25: [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     26: [0, 0, 0, 0, 0, 0, 0],
#     27: [0, 0, 0, 0, 0, 0],
#     28: [0, 0, 0, 0, 0, 0, 0],
#     29: [0, 0, 0, 0, 0, 0],
#     30: [0, 0, 0, 0, 0, 0]
# }
#################14_07_26######################
# DATA = [
#     {"audio_path": "audio/ISLE_SESS0181_BLOCKE_03_sprt1.wav", "words": ["I", "WASN'T", "PRESENT", "AT", "THE", "LAST", "MEETING"]},
#     {"audio_path": "audio/ISLE_SESS0181_BLOCKE_04_sprt1.wav", "words": ["THEY", "WANTED", "TO", "PROTEST", "AGAINST", "STUDENT", "FEES"]},
#     {"audio_path": "audio/ISLE_SESS0181_BLOCKE_21_sprt1.wav", "words": ["HE", "HADN'T", "INTENDED", "TO", "INSULT", "THE", "POLICEMAN"]},
#     {"audio_path": "audio/ISLE_SESS0181_BLOCKE_31_sprt1.wav", "words": ["THE", "PROJECT", "HAS", "PROVIDED", "VALUABLE", "EXPERIENCE"]},
#     {"audio_path": "audio/ISLE_SESS0181_BLOCKE_39_sprt1.wav", "words": ["SHE", "EXPECTS", "TO", "GRADUATE_V", "NEXT", "SUMMER"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_01_sprt1.wav", "words": ["I", "SAID", "WHITE", "NOT", "BAIT"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_02_sprt1.wav", "words": ["I", "SAID", "NEW", "NOT", "NO"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_03_sprt1.wav", "words": ["I", "SAID", "BAD", "NOT", "BED"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_04_sprt1.wav", "words": ["I", "SAID", "LATE", "NOT", "SITE"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_07_sprt1.wav", "words": ["I", "SAID", "CLOTHES", "NOT", "BIOLOGICAL"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_08_sprt1.wav", "words": ["I", "SAID", "PUT", "NOT", "BLUE"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_09_sprt1.wav", "words": ["I", "SAID", "LIVE", "NOT", "BED"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_10_sprt1.wav", "words": ["I", "SAID", "ALONE", "NOT", "GONE"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_18_sprt1.wav", "words": ["I", "SAID", "CLIMBING", "NOT", "CHEESE"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_19_sprt1.wav", "words": ["I", "SAID", "PSYCHOLOGY", "NOT", "PNEUMATIC"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_31_sprt1.wav", "words": ["WHAT", "IS", "SHE", "DRINKING", "A", "CUP", "OF", "COFFEE"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_35_sprt1.wav", "words": ["A", "MUG", "OF", "TEA"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_43_sprt1.wav", "words": ["IN", "A", "PARK", "NEAR", "A", "PATH"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_44_sprt1.wav", "words": ["BESIDE", "A", "TREE", "IN", "A", "PARK"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_78_sprt1.wav", "words": ["WHAT'S", "SHE", "WEARING", "SHE'S", "WEARING", "A", "LEATHER", "JACKET", "AND", "CORDUROY", "TROUSERS"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_79_sprt1.wav", "words": ["WHAT'S", "HE", "WEARING", "HE'S", "WEARING", "A", "BIG", "BEIGE", "JUMPER", "AND", "A", "COWBOY", "HAT"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKD01_80_sprt1.wav", "words": ["SHE'S", "WEARING", "A", "BROWN", "WOOLY", "HAT", "AND", "RED", "SCARF"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKE_01_sprt1.wav", "words": ["THE", "REFEREE", "NEEDED", "A", "POLICE", "ESCORT", "AFTER", "THE", "MATCH"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKE_09_sprt1.wav", "words": ["THE", "PRIME", "SUSPECT", "IS", "THE", "DIRECTOR"]},
#     {"audio_path": "audio/ISLE_SESS0182_BLOCKE_14_sprt1.wav", "words": ["OVER", "THE", "NEXT", "TWO", "WEEKS", "EACH", "PAIR", "WILL", "CONTEST", "EIGHT", "GAMES"]},
# ]

# GROUND_TRUTH = {
#     0: [0, 0, 1, 0, 0, 0, 0],
#     1: [0, 0, 0, 1, 0, 0, 0],
#     2: [0, 0, 1, 0, 1, 0, 0],
#     3: [0, 1, 0, 0, 0, 0],
#     4: [0, 1, 0, 0, 0, 1],
#     5: [0, 0, 1, 0, 1],
#     6: [0, 0, 1, 0, 1],
#     7: [0, 0, 1, 0, 0],
#     8: [0, 0, 1, 0, 0],
#     9: [0, 0, 1, 0, 1],
#     10: [0, 0, 1, 0, 0],
#     11: [0, 0, 1, 0, 0],
#     12: [0, 0, 1, 0, 0],
#     13: [0, 0, 1, 0, 0],
#     14: [0, 0, 1, 0, 1],
#     15: [0, 0, 0, 1, 0, 0, 0, 1],
#     16: [0, 1, 0, 1],
#     17: [0, 0, 1, 0, 0, 1],
#     18: [1, 0, 0, 0, 0, 1],
#     19: [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
#     20: [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
#     21: [0, 1, 0, 1, 1, 1, 0, 1, 0],
#     22: [0, 1, 0, 0, 0, 1, 0, 0, 0],
#     23: [0, 1, 1, 0, 0, 1],
#     24: [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
# }

# ############8_07_26##########################
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

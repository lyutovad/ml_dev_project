import pandas as pd

DAYS_MEDIAN = 18769.5
DIAG_MEAN, DIAG_STD = 18595.10780885781, 5744.5973380867545
MAP_GEN = {"Male": 0, "Female": 1}
MAP_RACE = {
    "white": 0,
    "black or african american": 1,
    "not reported": 2,
    "asian": 3,
    "american indian or alaska native": 4,
}
MAP_FEAT = {"MUTATED": 0, "NOT_MUTATED": 1}
FEATURES = [
    "IDH1",
    "TP53",
    "ATRX",
    "PTEN",
    "EGFR",
    "CIC",
    "MUC16",
    "PIK3CA",
    "NF1",
    "PIK3R1",
    "FUBP1",
    "RB1",
    "NOTCH1",
    "BCOR",
    "CSMD3",
    "SMARCA4",
    "GRIN2A",
    "IDH2",
    "FAT4",
    "PDGFRA",
]


# class DataDf:
#     def __init__(self, df):
#         self.df = df

#     def preprocess(self):
#         self.df["Days_at_diagnosis"] = (
#             self.df.Years_at_diagnosis * 365
#             + self.df.Years_at_diagnosis // 4
#             + self.df.Days_at_diagnosis
#         )
#         self.df.drop("Years_at_diagnosis", axis=1, inplace=True)
#         self.df.Gender = self.df.Gender.map(MAP_GEN)
#         self.df.Race = self.df.Race.map(MAP_RACE)
#         for f in FEATURES:
#             self.df[f"{f}"] = self.df[f"{f}"].map(MAP_FEAT)
#         return self.df

#     def scaling(self, diag_mean=DIAG_MEAN, diag_std=DIAG_STD):
#         X_scaled = self.df.copy()
#         X_scaled["Days_at_diagnosis"] = (
#             X_scaled.Days_at_diagnosis - diag_mean
#         ) / diag_std
#         return X_scaled


def preprocess(df):
    df["Days_at_diagnosis"] = (
        df.Years_at_diagnosis * 365 + df.Years_at_diagnosis // 4 + df.Days_at_diagnosis
    )
    df.drop("Years_at_diagnosis", axis=1, inplace=True)
    df.Gender = df.Gender.map(MAP_GEN)
    df.Race = df.Race.map(MAP_RACE)
    for f in FEATURES:
        df[f"{f}"] = df[f"{f}"].map(MAP_FEAT)
    return df


def scaling(df, diag_mean=DIAG_MEAN, diag_std=DIAG_STD):
    X_scaled = df.copy()
    X_scaled["Days_at_diagnosis"] = (X_scaled.Days_at_diagnosis - diag_mean) / diag_std
    return X_scaled

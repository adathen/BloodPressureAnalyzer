import pandas as pd
import matplotlib.pyplot as plt

class BloodPressureAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
        self._prepare_data()

    def _prepare_data(self):
        self.df["時間"] = pd.to_datetime(self.df["時間"])
        self.df.dropna(subset=["收縮壓", "舒張壓"], inplace=True)
        self.df["日期"] = self.df["時間"].dt.date
        self.df["小時"] = self.df["時間"].dt.hour

        def classify_bp(row):
            if row["收縮壓"] < 120 and row["舒張壓"] < 80:
                return "正常"
            elif (120 <= row["收縮壓"] <= 140) or (80 <= row["舒張壓"] <= 90):
                return "偏高"
            elif row["收縮壓"] > 140 or row["舒張壓"] > 90:
                return "高血壓"
            return "未分類"

        def period_class(hour):
            if 5 <= hour < 12:
                return "早上"
            elif 12 <= hour < 17:
                return "下午"
            elif 17 <= hour < 22:
                return "晚上"
            else:
                return "夜間"

        self.df["血壓等級"] = self.df.apply(classify_bp, axis=1)
        self.df["時段"] = self.df["小時"].apply(period_class)
        self.df["每日首次"] = self.df.groupby("日期")["時間"].transform("min") == self.df["時間"]

    def get_daily_distribution(self):
        daily = self.df.groupby(["日期", "血壓等級"]).size().unstack(fill_value=0)
        return daily.div(daily.sum(axis=1), axis=0) * 100

    def get_period_distribution(self):
        period = self.df.groupby(["時段", "血壓等級"]).size().unstack(fill_value=0)
        return period.div(period.sum(axis=1), axis=0) * 100

    def get_first_bp_distribution(self):
        return self.df[self.df["每日首次"]].groupby("血壓等級").size()

    def plot_trends(self):
        plt.figure(figsize=(14, 6))
        plt.plot(self.df["時間"], self.df["收縮壓"], label="收縮壓", marker='o')
        plt.plot(self.df["時間"], self.df["舒張壓"], label="舒張壓", marker='s')

        for y in [120, 130, 140]:
            plt.axhline(y=y, color="red", linestyle="--", label=f"收縮壓 {y}")
        for y in [80, 85, 90]:
            plt.axhline(y=y, color="blue", linestyle="--", label=f"舒張壓 {y}")

        plt.xlabel("時間", fontsize=14)
        plt.ylabel("血壓 (mmHg)", fontsize=14)
        plt.title("血壓趨勢圖", fontsize=16)
        plt.legend(loc="upper right")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

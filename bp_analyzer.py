import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

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

    def plot_trends_plotly(self, save_path="bp_trend.png"):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.df["時間"], y=self.df["收縮壓"],
            mode='lines+markers', name='收縮壓',
            line=dict(color='red')
        ))

        fig.add_trace(go.Scatter(
            x=self.df["時間"], y=self.df["舒張壓"],
            mode='lines+markers', name='舒張壓',
            line=dict(color='blue')
        ))

        # 收縮壓水平線
        for y in [120, 130, 140]:
            fig.add_hline(y=y, line=dict(color='red', dash='dash'),
                          annotation_text=f"收縮壓 {y}", annotation_position="top left")

        # 舒張壓水平線
        for y in [80, 85, 90]:
            fig.add_hline(y=y, line=dict(color='blue', dash='dash'),
                          annotation_text=f"舒張壓 {y}", annotation_position="top left")

        fig.update_layout(
            title="血壓趨勢圖",
            xaxis_title="時間",
            yaxis_title="血壓 (mmHg)",
            font=dict(family="Microsoft JhengHei", size=14),
            height=600
        )

        # 儲存為圖片
        write_image(fig, save_path)
        return save_path

    def generate_pdf_report(self, pdf_path="血壓分析報表.pdf"):
        chart_path = self.plot_trends_plotly()

        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        # 標題
        c.setFont("Helvetica-Bold", 18)
        c.drawString(72, height - 72, "血壓分析報表")

        # 畫圖
        c.drawImage(chart_path, 72, height - 500, width=450, preserveAspectRatio=True)

        # 基本統計
        self.df["血壓等級"] = self.df.apply(lambda row: "正常" if row["收縮壓"] < 120 and row["舒張壓"] < 80 else
                                             "偏高" if (120 <= row["收縮壓"] <= 140 or 80 <= row["舒張壓"] <= 90) else
                                             "高血壓", axis=1)
        stats = self.df["血壓等級"].value_counts(normalize=True) * 100
        y = height - 540
        c.setFont("Helvetica", 12)
        for level in ["正常", "偏高", "高血壓"]:
            percent = stats.get(level, 0)
            c.drawString(72, y, f"{level}：{percent:.2f}%")
            y -= 20

        c.setFont("Helvetica", 10)
        c.drawString(72, 40, f"產生時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        c.save()
        print(f"✅ PDF 報表已儲存至：{pdf_path}")

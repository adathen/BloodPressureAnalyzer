import pandas as pd
from bp_analyzer import BloodPressureAnalyzer

# 匯入血壓數據 Excel
df = pd.read_excel("血壓.xlsx")

# 初始化分析模組
analyzer = BloodPressureAnalyzer(df)

# 顯示每日血壓分類百分比
print("📊 每日血壓分類百分比：")
print(analyzer.get_daily_distribution().round(2))
print()

# 顯示各時段血壓分類百分比
print("🕑 各時段血壓分類百分比：")
print(analyzer.get_period_distribution().round(2))
print()

# 顯示每日首次血壓分類統計
print("📌 每日首次血壓分類統計：")
print(analyzer.get_first_bp_distribution())
print()

# 繪製血壓趨勢圖
analyzer.plot_trends()

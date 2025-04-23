from blood_pressure_analyzer import BloodPressureAnalyzer
import pandas as pd

df = pd.read_excel("your_blood_pressure_data.xlsx")
analyzer = BloodPressureAnalyzer(df)

# 查看各類分析結果
print(analyzer.get_daily_distribution())
print(analyzer.get_period_distribution())
print(analyzer.get_first_bp_distribution())

# 顯示血壓趨勢圖
analyzer.plot_trends()

# 匯出 PDF 報告
analyzer.generate_pdf_report("bp_report.pdf")

# BloodPressureAnalyzer 📈

This Python module provides comprehensive tools for analyzing blood pressure measurement data, 
categorizing the levels, and visualizing trends with respect to medication timing and daily patterns.

## Features

- Classify blood pressure into Normal / Elevated / Hypertension
- Identify and mark the first reading of each day
- Group data into time periods (Morning, Afternoon, Evening, Night)
- Generate daily and time-of-day distribution reports
- Visualize trends with reference lines and medication points

## Usage

```python
from bp_analyzer import BloodPressureAnalyzer
import pandas as pd

df = pd.read_excel("血壓.xlsx")
analyzer = BloodPressureAnalyzer(df)

analyzer.plot_trends()

daily = analyzer.get_daily_distribution()
print(daily)

period = analyzer.get_period_distribution()
print(period)

first_bp = analyzer.get_first_bp_distribution()
print(first_bp)

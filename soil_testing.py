import pandas as pd
import xlsxwriter

# Optimized and compact Gantt chart task data
tasks = [
    ("Soil Sampling", "Testing", 0, 1),
    ("Sample Labeling", "Testing", 0.5, 0.5),
    ("Sample Drying", "Testing", 1, 1),
    ("Sample Sieving", "Testing", 1.5, 1),
    ("Sample Packing", "Testing", 2, 0.5),
    ("PH Extraction Prep", "PH-Level", 2, 0.5),
    ("PH Measurement", "PH-Level", 2.5, 0.5),
    ("NPK Extraction Preps", "NPK", 3, 1),
    ("NPK Measurements", "NPK", 4, 1),
    ("Carbon Reagent Prep", "Organic Carbon", 5, 0.5),
    ("Organic Carbon Titration", "Organic Carbon", 5.5, 0.5),
    ("Result Compilation", "Reporting", 6, 0.5),
    ("Result Verification", "Reporting", 6.5, 0.5),
    ("Reporting to Farmer", "Reporting", 7, 0.5)
]

df = pd.DataFrame(tasks, columns=["Task", "Category", "Start", "Duration"])
df["Delay"] = 0
df["Adj Start"] = df["Start"]

# Output file path
output_path = r"C:\Users\Mahima\Downloads\Soil_Analysis_Compact_Gantt.xlsx"

# Create Excel writer
with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Gantt", startrow=1)
    workbook = writer.book
    worksheet = writer.sheets["Gantt"]

    # Time scale: Day 0 to 8 in 0.5 increments = 16 steps
    time_steps = 16
    for i in range(time_steps):
        worksheet.write(0, 6 + i, f"Day {i * 0.5:.1f}")

    # Column headers
    headers = list(df.columns) + [f"Day {i * 0.5:.1f}" for i in range(time_steps)]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Category color coding
    category_colors = {
        "Testing": "#ADD8E6",
        "PH-Level": "#90EE90",
        "NPK": "#FFD700",
        "Organic Carbon": "#FFB6C1",
        "Reporting": "#D3D3D3"
    }

    # Draw Gantt bars
    for i, row in df.iterrows():
        excel_row = i + 2
        duration = int(row["Duration"] * 2)
        start = int(row["Start"] * 2)
        task_name = row["Task"]
        color = category_colors.get(row["Category"], "#CCCCCC")
        fmt = workbook.add_format({
            'bg_color': color,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        # Formula for adjusted start
        worksheet.write_formula(excel_row - 1, 5, f"=C{excel_row}+E{excel_row}")

        for d in range(duration):
            col = 6 + start + d
            worksheet.write(excel_row - 1, col, task_name if d == 0 else "", fmt)

    # Formatting
    worksheet.set_column("A:A", 35)
    worksheet.set_column("B:E", 15)
    for col in range(6, 6 + time_steps):
        worksheet.set_column(col, col, 9)

print(f"✅ File saved to: {output_path}")

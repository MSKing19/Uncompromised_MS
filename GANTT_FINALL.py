import pandas as pd
import xlsxwriter

# Output file path
output_file = "Interactive_Gantt_PerTaskDropdown.xlsx"

# Task data
tasks = [
    ("Understand Crop Requirement", "Planning", 0, 1),
    ("Determine Sowing Window", "Planning", 0, 1),
    ("Identify Suitable Varieties", "Planning", 0, 1),
    ("Evaluate Crop Variety Suitability", "Planning", 1, 1),
    ("Search for Certified Vendors", "Vendor", 2, 1),
    ("Vendor Verification", "Vendor", 3, 1),
    ("Vendor Approval", "Vendor", 4, 1),
    ("Check Seed Cost", "Costing", 5, 1),
    ("Assess Availability", "Costing", 5, 1),
    ("Finalize Procurement Decision", "Costing", 6, 1),
    ("Seed Procurement", "Procurement", 7, 1),
    ("Seed Conditioning", "Procurement", 8, 1),
    ("Storage Planning", "Procurement", 9, 1),
]

# Create DataFrame
df = pd.DataFrame(tasks, columns=["Task", "Category", "Start", "Duration"])
df["Delay Scenario"] = "None"
df["Delay"] = 0
df["Adj Start"] = df["Start"] + df["Delay"]

# Write to Excel
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Gantt", startrow=1)
    workbook = writer.book
    worksheet = writer.sheets["Gantt"]

    # Timeline headers (15 days)
    for i in range(15):
        worksheet.write(0, 7 + i, f"Day {i}")

    # Column headers
    headers = list(df.columns) + [f"Day {i}" for i in range(15)]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Category colors
    category_colors = {
        "Planning": "#B0E0E6",
        "Vendor": "#90EE90",
        "Costing": "#DDA0DD",
        "Procurement": "#FFA500",
    }

    # Dropdown options
    options = ['None', 'Vendor Delay', 'Rain Delay', 'Cost Issue']

    for i, row in df.iterrows():
        excel_row = i + 1  # considering header
        category = row["Category"]
        start = int(row["Start"])
        duration = int(row["Duration"])
        task_name = row["Task"]
        color = category_colors.get(category, "#CCCCCC")

        # Add dropdown
        worksheet.data_validation(excel_row, 4, excel_row, 4, {
            'validate': 'list',
            'source': options,
            'input_message': 'Choose a delay scenario',
        })

        # Gantt bar (static, based on Start)
        format_cell = workbook.add_format({
            'bg_color': color,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        for d in range(duration):
            col = 7 + start + d
            worksheet.write(excel_row, col, task_name if d == 0 else "", format_cell)

    # Set column widths
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:G", 15)
    for col in range(7, 22):
        worksheet.set_column(col, col, 14)

print(f"✅ Excel file saved to: {output_file}")

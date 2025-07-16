import pandas as pd

# Full master workflow across 4 modules with logical ordering, overlaps, minimal durations
tasks = [
    # --- Preceding Crop Details ---
    ("Identify Preceding Crop", "Crop History", 0, 0.5, "None"),
    ("Confirm Crop Type from Records", "Crop History", 0.5, 0.5, "Farmer log delay"),
    ("Retrieve Harvest Date", "Crop History", 1, 0.5, "Record not updated"),
    ("Verify Harvest Records", "Crop History", 1.5, 0.5, "Manual entry mistake"),
    ("Inspect Field for Residues", "Field Check", 2, 1, "Field inaccessible"),
    ("Lab Testing for Residual Nutrients", "Lab Analysis", 2, 1, "Lab backlog"),
    ("Pest Scouting", "Field Check", 3, 1, "Heavy rain"),
    ("Compile Residue & Pest Report", "Reporting", 4, 0.5, "Staff unavailability"),

    # --- Soil Testing ---
    ("Soil Sampling", "Testing", 4.5, 1, "Sample collection delay"),
    ("Sample Labeling", "Testing", 4.5, 0.5, "Tag mismatch"),
    ("Sample Drying", "Testing", 5, 1, "Dryer malfunction"),
    ("Sample Sieving", "Testing", 5.5, 1, "Sieve unavailable"),
    ("Sample Packing", "Testing", 6, 0.5, "Bag shortage"),
    ("PH Extraction Prep", "PH-Level", 6, 0.5, "Reagent unavailability"),
    ("PH Measurement", "PH-Level", 6.5, 0.5, "pH meter calibration"),
    ("NPK Extraction Preps", "NPK", 7, 1, "Glassware shortage"),
    ("NPK Measurements", "NPK", 8, 1, "Instrument drift"),
    ("Carbon Reagent Prep", "Organic Carbon", 9, 0.5, "Reagent delay"),
    ("Organic Carbon Titration", "Organic Carbon", 9.5, 0.5, "Burette unavailable"),
    ("Result Compilation", "Reporting", 10, 0.5, "Format error"),
    ("Result Verification", "Reporting", 10.5, 0.5, "Supervisor unavailable"),
    ("Reporting to Farmer", "Reporting", 11, 0.5, "Farmer unavailable"),

    # --- Compost Planning (simplified) ---
    ("Compost Material Collection", "Compost", 11.5, 1, "Transport delay"),
    ("Compost Pit Setup", "Compost", 12.5, 1, "Labor shortage"),
    ("Initial Moisture Adjustment", "Compost", 13.5, 0.5, "Water scarcity"),
    ("Microbial Inoculation", "Compost", 14, 0.5, "Culture expired"),
    ("Initial Covering", "Compost", 14.5, 0.5, "Cover material delay"),
    ("1st Turning", "Compost", 16.5, 0.5, "Tool unavailability"),
    ("2nd Turning", "Compost", 20.5, 0.5, "Rain interruption"),
    ("3rd Turning", "Compost", 25, 0.5, "Low labor"),
    ("Final Compost Testing", "Lab Analysis", 28, 1, "Lab overload"),
    ("Compost Ready to Use", "Reporting", 29, 0.5, "Final approval delay"),

    # --- Seed Procurement ---
    ("Select Crop Variety", "Seed Planning", 11.5, 1, "Farmer indecision"),
    ("Check Vendor List", "Seed Planning", 12.5, 1, "List outdated"),
    ("Request Quotation", "Vendor", 13.5, 1, "Late response"),
    ("Price Comparison", "Vendor", 14.5, 0.5, "Data error"),
    ("Place Order", "Procurement", 15, 0.5, "Payment delay"),
    ("Vendor Confirmation", "Vendor", 15.5, 0.5, "No response"),
    ("Receive Seeds", "Procurement", 16, 1, "Courier delay"),
    ("Verify Seed Quality", "Procurement", 17, 1, "Sample rejected"),
    ("Store Seeds Properly", "Storage", 18, 0.5, "Store not ready")
]

df = pd.DataFrame(tasks, columns=["Task", "Category", "Start", "Duration", "Possible Delay Cause"])
df["Delay"] = 0
df["Adj Start"] = df["Start"]

# Output file
output_path = r"C:\Users\Mahima\Downloads\All_4_Workflows_Master_Gantt.xlsx"

# Write Excel with Gantt bars
with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="MasterGantt", startrow=1)
    workbook = writer.book
    worksheet = writer.sheets["MasterGantt"]

    # Time axis setup (0 to 35 in 0.5 increments = 70 cols)
    time_steps = 70
    for i in range(time_steps):
        worksheet.write(0, 7 + i, f"Day {i * 0.5:.1f}")

    headers = list(df.columns) + [f"Day {i * 0.5:.1f}" for i in range(time_steps)]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Color codes
    category_colors = {
        "Crop History": "#DDEBF7",
        "Field Check": "#FCE4D6",
        "Lab Analysis": "#E2EFDA",
        "Reporting": "#FFF2CC",
        "Testing": "#ADD8E6",
        "PH-Level": "#90EE90",
        "NPK": "#FFD700",
        "Organic Carbon": "#FFB6C1",
        "Compost": "#C4D79B",
        "Seed Planning": "#B7DEE8",
        "Vendor": "#E6B8B7",
        "Procurement": "#B4C6E7",
        "Storage": "#F4B084"
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
        worksheet.write_formula(excel_row - 1, 6, f'=IF(AND(ISNUMBER(C{excel_row}), ISNUMBER(E{excel_row})), C{excel_row}+E{excel_row}, "")')
        for d in range(duration):
            col = 7 + start + d
            worksheet.write(excel_row - 1, col, task_name if d == 0 else "", fmt)

    worksheet.set_column("A:A", 40)
    worksheet.set_column("B:F", 18)
    for col in range(7, 7 + time_steps):
        worksheet.set_column(col, col, 10)

output_path

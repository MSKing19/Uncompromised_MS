import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Combined task buckets from all systems
combined_task_buckets = {
    "Seed Planning": [
        ("Seed Procurement", 0, 2),
        ("Certified Vendor", "Seed Procurement", 2),
        ("Crop Variety Suitability", "Certified Vendor", 3),
        ("Cost & Availability", "Crop Variety Suitability", 2),
        ("Vendor Approval", "Certified Vendor", 1),
        ("Logistics Planning", "Seed Procurement", 2)
    ],
    "Compost Planning": [
        ("Crop & Soil Analysis", 0, 5),
        ("Compost Requirement", "Crop & Soil Analysis", 2),
        ("Decision Tree Finalization", "Compost Requirement", 3),
        ("Gobar Procurement", "Decision Tree Finalization", 4),
        ("Green Manure Collection", "Decision Tree Finalization", 4),
        ("Pit Readiness", "Decision Tree Finalization", 3),
        ("Compost Mixing", "Gobar Procurement", 2),
        ("Pit Monitoring", "Compost Mixing", 36),
        ("Tractor Preparation", "Pit Monitoring", 1),
        ("Rotavator Check", "Tractor Preparation", 1),
        ("Field Prep & Compost Application", "Rotavator Check", 4),
        ("Sowing Preparation", "Field Prep & Compost Application", 3)
    ],
    "Soil Testing": [
        ("Soil Testing", 0, 2),
        ("PH-Level", "Soil Testing", 2),
        ("NPK Balance", "Soil Testing", 2),
        ("Organic Carbon", "Soil Testing", 2)
    ]
}

combined_category_colors = {
    "Seed Planning": "cornflowerblue",
    "Compost Planning": "lightgreen",
    "Soil Testing": "lightpink"
}

def resolve_combined_schedule():
    flat = []
    task_end = {}
    for category, items in combined_task_buckets.items():
        for task in items:
            name = task[0]
            if isinstance(task[1], str):
                depends_on = task[1]
                duration = task[2]
                start = task_end[depends_on]
                end = start + duration
            else:
                start = task[1]
                end = task[2]
            flat.append((name, category, start, end))
            task_end[name] = end
    return flat

def apply_delay_logic(decision_map, task_list, category):
    delay_map = decision_map
    task_end = {}
    updated = []

    for t in task_list:
        name, cat, start, end = t
        if cat == category:
            delay = delay_map.get(name, 0)
            start += delay
            end += delay
        updated.append((name, cat, start, end))
        task_end[name] = end

    return updated

class UnifiedGanttApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unified Gantt Chart with Soil Testing")
        self.geometry("1400x1000")
        self.base_tasks = resolve_combined_schedule()
        self.build_ui()

    def build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.tabs = {}
        for category in combined_task_buckets:
            tab = tk.Frame(notebook)
            notebook.add(tab, text=category)
            self.tabs[category] = tab

        self.control_vars = {}
        for cat in self.tabs:
            self.create_controls(cat, self.tabs[cat])

    def create_controls(self, category, tab):
        frame = tk.Frame(tab)
        frame.pack(pady=10)

        tk.Label(frame, text=f"{category} Delay Trigger:").grid(row=0, column=0, padx=10)
        var = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=var)

        if category == "Seed Planning":
            combo['values'] = ["None", "Vendor Delay", "Cost Issue", "Rain Delay"]
        elif category == "Compost Planning":
            combo['values'] = ["None", "Compost Immature", "Power Failure", "Gobar Vendor Delay", "Labour Shortage"]
        elif category == "Soil Testing":
            combo['values'] = ["None", "Lab Delay", "Sensor Malfunction"]

        combo.set("None")
        combo.grid(row=0, column=1, padx=10)
        ttk.Button(frame, text="Apply", command=lambda c=category, v=var: self.update_gantt(c, v)).grid(row=0, column=2, padx=10)

        canvas = tk.Frame(tab)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_gantt_chart(self.base_tasks, canvas, category)
        self.control_vars[category] = (var, canvas)

    def draw_gantt_chart(self, tasks, container, category):
        filtered = [t for t in tasks if t[1] == category]
        fig, ax = plt.subplots(figsize=(16, 8))
        for i, (label, cat, start, end) in enumerate(filtered):
            duration = end - start
            color = combined_category_colors.get(cat, 'gray')
            ax.barh(i, duration, left=start, color=color, edgecolor='black')
            ax.text(start + duration / 2, i, label, ha='center', va='center', fontsize=9)

        ax.set_yticks(range(len(filtered)))
        ax.set_yticklabels([t[0] for t in filtered])
        ax.set_xlabel("Day Number")
        ax.set_title(f"Gantt Chart: {category}")
        ax.invert_yaxis()
        ax.grid(True)

        for widget in container.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_gantt(self, category, var):
        decision = var.get()
        delay_map = {}

        if category == "Seed Planning":
            if decision == "Vendor Delay":
                delay_map = {"Certified Vendor": 2}
            elif decision == "Cost Issue":
                delay_map = {"Cost & Availability": 1}
            elif decision == "Rain Delay":
                delay_map = {"Logistics Planning": 3}

        elif category == "Compost Planning":
            if decision == "Compost Immature":
                delay_map = {"Field Prep & Compost Application": 7, "Sowing Preparation": 7}
            elif decision == "Power Failure":
                delay_map = {"Decision Tree Finalization": 2}
            elif decision == "Gobar Vendor Delay":
                delay_map = {"Gobar Procurement": 3}
            elif decision == "Labour Shortage":
                delay_map = {"Compost Mixing": 2, "Pit Readiness": 2}

        elif category == "Soil Testing":
            if decision == "Lab Delay":
                delay_map = {"PH-Level": 2, "NPK Balance": 2, "Organic Carbon": 2}
            elif decision == "Sensor Malfunction":
                delay_map = {"Soil Testing": 3}

        updated = apply_delay_logic(delay_map, resolve_combined_schedule(), category)
        self.draw_gantt_chart(updated, self.control_vars[category][1], category)

if __name__ == "__main__":
    app = UnifiedGanttApp()
    app.mainloop()

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Optimized task breakdown with reduced durations
task_buckets = {
    "Planning": [
        ("Understand Crop Requirement", 0, 1),
        ("Determine Sowing Window", 0, 1),
        ("Identify Suitable Varieties", 0, 1),
        ("Evaluate Crop Variety Suitability", "Identify Suitable Varieties", 1)
    ],
    "Vendor": [
        ("Search for Certified Vendors", "Evaluate Crop Variety Suitability", 1),
        ("Vendor Verification", "Search for Certified Vendors", 0.5),
        ("Vendor Approval", "Vendor Verification", 0.5)
    ],
    "Costing": [
        ("Check Seed Cost", "Vendor Approval", 0.5),
        ("Assess Availability", "Vendor Approval", 0.5),
        ("Finalize Procurement Decision", ["Check Seed Cost", "Assess Availability"], 0.5)
    ],
    "Procurement": [
        ("Seed Procurement", "Finalize Procurement Decision", 1),
        ("Seed Conditioning", "Seed Procurement", 0.5),
        ("Storage Planning", "Seed Conditioning", 0.5)
    ]
}

# Color coding for each category
category_colors = {
    "Planning": "skyblue",
    "Vendor": "lightgreen",
    "Costing": "violet",
    "Procurement": "orange"
}

# Delay simulation based on selected decision
def apply_decision_logic(decision, task_list):
    delay_map = {}
    if decision == "Vendor Delay":
        delay_map["Vendor Verification"] = 2
    elif decision == "Rain Delay":
        delay_map["Seed Procurement"] = 2
    elif decision == "Cost Issue":
        delay_map["Check Seed Cost"] = 1

    updated = []
    for task in task_list:
        name, category, start, end = task
        delay = delay_map.get(name, 0)
        updated.append((name, category, start + delay, end + delay))
    return updated

# Resolve tasks with support for multiple dependencies
def resolve_task_schedule():
    flat = []
    task_end = {}

    for category, tasks in task_buckets.items():
        for task in tasks:
            name = task[0]
            dependency = task[1]
            duration = task[2]

            if isinstance(dependency, str):
                start = task_end[dependency]
            elif isinstance(dependency, (list, tuple)):
                start = max(task_end[dep] for dep in dependency)
            else:
                start = dependency

            end = start + duration
            flat.append((name, category, start, end))
            task_end[name] = end

    return flat

# GUI Class
class GanttGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Seed Procurement Gantt Tracker")
        self.geometry("1200x850")
        self.task_list = resolve_task_schedule()
        self.build_ui()

    def build_ui(self):
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Simulate Delay Scenario:").grid(row=0, column=0, padx=10)
        self.decision_var = tk.StringVar()
        self.decision_combo = ttk.Combobox(control_frame, textvariable=self.decision_var)
        self.decision_combo['values'] = ["None", "Vendor Delay", "Rain Delay", "Cost Issue"]
        self.decision_combo.set("None")
        self.decision_combo.grid(row=0, column=1, padx=10)

        ttk.Button(control_frame, text="Update Gantt", command=self.update_gantt).grid(row=0, column=2, padx=10)

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.draw_gantt_chart(self.task_list)

    def draw_gantt_chart(self, tasks):
        fig, ax = plt.subplots(figsize=(14, 8))
        for i, (label, category, start, end) in enumerate(tasks):
            duration = end - start
            color = category_colors.get(category, 'gray')
            ax.barh(i, duration, left=start, color=color, edgecolor='black')
            ax.text(start + duration / 2, i, label, ha='center', va='center', fontsize=8)

        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels([t[0] for t in tasks])
        ax.set_xlabel("Day")
        ax.set_title("Seed Procurement Gantt Timeline")
        ax.invert_yaxis()
        ax.grid(True)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_gantt(self):
        decision = self.decision_var.get()
        scheduled = resolve_task_schedule()
        modified = apply_decision_logic(decision, scheduled) if decision != "None" else scheduled
        self.draw_gantt_chart(modified)

# Run the application
if __name__ == "__main__":
    app = GanttGUI()
    app.mainloop()

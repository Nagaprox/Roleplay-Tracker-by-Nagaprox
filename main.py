import ttkbootstrap as ttk
from tkinter import messagebox  # still valid for message dialogs
import tkinter as tk  # only if you're still using tk.Text or tk.Listbox


# Universal save/load system registry
tab_savers = {}
tab_loaders = {}

def register_tab(tab_name, save_func, load_func):
    tab_savers[tab_name] = save_func
    tab_loaders[tab_name] = load_func

from tkinter import filedialog
import json
# Initialize main window
style = ttk.Style("superhero")  # Default is dark mode
root = style.master  # Use the internal Tk root from style

my_text = tk.Text(root, font=("Segoe UI", 15))
# Define default and selected styles for injury buttons
style.configure("Injury.Default.TButton")
style.configure("Injury.Selected.TButton")
style.map("Injury.Selected.TButton",
          background=[("!disabled", "#c0392b")],  # red
          foreground=[("!disabled", "white")])

root.title("Roleplay Tracker")
root.geometry("550x700")

# Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

def setup_injury_styles():
    style.configure("Injury.Default.TButton")
    style.configure("Injury.Selected.TButton")
    style.map("Injury.Selected.TButton",
              background=[("!disabled", "#c0392b")],
              foreground=[("!disabled", "white")])


def switch_theme(theme_name):
    style.theme_use(theme_name)
    setup_injury_styles()  # Re-apply injury styles after theme change

def toggle_theme():
    current = style.theme.name
    if current == "superhero":
        switch_theme("flatly")
    else:
        switch_theme("superhero")


theme_frame = ttk.Frame(root)
theme_frame.pack(pady=5)

ttk.Label(theme_frame, text="Theme:").pack(side="left", padx=(10, 5))

theme_btn = ttk.Button(theme_frame, text="Toggle Light/Dark", command=toggle_theme)
theme_btn.pack(side="left")

setup_injury_styles()  # 👈 Initial style setup

# =========================
# Tab 1: Advanced Injury System
# =========================
injury_tab = ttk.Frame(notebook)
notebook.add(injury_tab, text="Injuries")

# Injury mapping and effects
injury_parts = {
    "Head": "Unconscious or disoriented.",
    "Left Arm": "Can't aim or shoot properly.",
    "Right Arm": "Can't aim or shoot properly.",
    "Lower Left Arm": "Losing control on left hand",
    "Lower Right Arm": "Losing control on right hand",
    "Upper Torso": "Heavy bleeding, risk of collapse.",
    "Lower Torso": "Internal injury, slow bleeding.",
    "Left Hand": "Can't grip properly.",
    "Right Hand": "Can't grip properly.",
    "Left Leg": "Limping, slower movement.",
    "Right Leg": "Limping, slower movement.",
    "Left Foot": "Balance disrupted.",
    "Right Foot": "Balance disrupted."
}
injured = {}

injury_output = tk.Text(injury_tab, height=5)
injury_output.pack(side="bottom", fill="x", padx=10, pady=10)

def toggle_injury(part, button):
    if injured.get(part):
        injured.pop(part)
        button.config(style="Injury.Default.TButton")
    else:
        injured[part] = injury_parts[part]
        button.config(style="Injury.Selected.TButton")
    update_injury_output()

def update_injury_output():
    injury_output.delete(1.0, tk.END)
    for part, effect in injured.items():
        injury_output.insert(tk.END, f"{part}: {effect}\n")

# Layout grid for injury buttons
injury_frame = tk.Frame(injury_tab)
injury_frame.pack(pady=20)

# Map of button positions in grid (row, col)
body_layout = {
    "Head": (0, 2),
    "Left Arm": (1, 1),
    "Upper Torso": (1, 2),
    "Right Arm": (1, 3),
    "Lower Torso": (2, 2),
    "Lower Left Arm": (2, 1),
    "Lower Right Arm": (2, 3),
    "Left Hand": (3, 0),
    "Right Hand": (3, 4),
    "Left Leg": (3, 1),
    "Right Leg": (3, 3),
    "Left Foot": (4, 1),
    "Right Foot": (4, 3)
}

# Create body part buttons
buttons = {}
for part, (row, col) in body_layout.items():
    btn = ttk.Button(injury_frame, text=part, width=12,
                     style="Injury.Default.TButton",
                     command=lambda p=part: toggle_injury(p, buttons[p]))
    buttons[part] = btn
    btn.grid(row=row, column=col, padx=5, pady=5)

def save_injuries():
    return list(injured.keys())

def load_injuries(data):
    for part in buttons:
        if part in data:
            injured[part] = injury_parts[part]
            buttons[part].config(style="Injury.Selected.TButton")
        else:
            injured.pop(part, None)
            buttons[part].config(style="Injury.Default.TButton")
    update_injury_output()


register_tab("injuries", save_injuries, load_injuries)

# ====================
# Tab 2: Inventory
# ====================
inventory_tab = ttk.Frame(notebook)
notebook.add(inventory_tab, text="Inventory")

inventory = []

def update_inventory_display():
    inventory_listbox.delete(0, tk.END)
    for item in inventory:
        inventory_listbox.insert(tk.END, item)

def add_inventory_item():
    item = inventory_item_entry.get().strip()
    if not item:
        return
    inventory.append(item)
    update_inventory_display()
    inventory_item_entry.delete(0, tk.END)

def remove_selected_inventory_item():
    selected = inventory_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    del inventory[index]
    update_inventory_display()

# Entry
input_frame = tk.Frame(inventory_tab)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Item:").pack(side="left", padx=5)
inventory_item_entry = tk.Entry(input_frame, width=30)
inventory_item_entry.pack(side="left", padx=5)

tk.Button(input_frame, text="Add Item", command=add_inventory_item).pack(side="left", padx=5)
tk.Button(inventory_tab, text="Remove Selected Item", command=remove_selected_inventory_item).pack(pady=5)

# Display
inventory_listbox = tk.Listbox(inventory_tab, height=10)
inventory_listbox.pack(fill="both", padx=10, pady=10, expand=True)

# Save/load functions (already registered if you're using the universal system)
def save_inventory_tab():
    return inventory

def load_inventory_tab(data):
    global inventory
    inventory = data
    update_inventory_display()

register_tab("inventory", save_inventory_tab, load_inventory_tab)

# ====================
# Tab 3: Wallet
# ====================
wallet_tab = ttk.Frame(notebook)
notebook.add(wallet_tab, text="Wallet")

wallet_balance = tk.DoubleVar(value=0.00)
wallet_logs = []

def update_wallet_display():
    wallet_label.config(text=f"Current Balance: ${wallet_balance.get():.2f}")

def log_wallet_message(message):
    wallet_logs.append(message)
    wallet_logbox.config(state="normal")
    wallet_logbox.delete("1.0", tk.END)
    for line in wallet_logs:
        wallet_logbox.insert(tk.END, line + "\n")
    wallet_logbox.config(state="disabled")

def add_money():
    try:
        amt = float(wallet_entry.get())
        if amt <= 0:
            raise ValueError
        wallet_balance.set(wallet_balance.get() + amt)
        unit = "Dollar" if amt >= 1 else "cent"
        log_wallet_message(f"You have gained {amt:.2f} Dollars")
        update_wallet_display()
        wallet_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

def subtract_money():
    try:
        amt = float(wallet_entry.get())
        if amt <= 0:
            raise ValueError
        wallet_balance.set(wallet_balance.get() - amt)
        unit = "Dollar" if amt >= 1 else "cent"
        log_wallet_message(f"You have spend {amt:.2f} Dollars")
        update_wallet_display()
        wallet_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
def save_wallet():
    path = filedialog.asksaveasfilename(defaultextension=".json", title="Save Wallet", filetypes=[("JSON files", "*.json")])
    if path:
        data = {
            "balance": wallet_balance.get(),
            "logs": wallet_logs
        }
        with open(path, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", "Wallet data saved successfully.")

def load_wallet():
    global wallet_logs
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], title="Load Wallet")
    if path:
        with open(path, "r") as f:
            data = json.load(f)
        wallet_balance.set(data.get("balance", 0))
        wallet_logs = data.get("logs", [])
        update_wallet_display()
        log_wallet_message("Wallet loaded.")
        update_wallet_display()

wallet_top = tk.Frame(wallet_tab)
wallet_top.pack(pady=10)

tk.Label(wallet_top, text="Amount:").pack(side="left", padx=5)
wallet_entry = tk.Entry(wallet_top, width=10)
wallet_entry.pack(side="left")

tk.Button(wallet_top, text="Add", command=add_money).pack(side="left", padx=5)
tk.Button(wallet_top, text="Spend", command=subtract_money).pack(side="left", padx=5)

wallet_label = tk.Label(wallet_tab, text="Current Balance: $0.00", font=("Arial", 14))
wallet_label.pack(pady=5)

tk.Label(wallet_tab, text="Transaction Log:").pack()
wallet_logbox = tk.Text(wallet_tab, height=10, state="disabled")
wallet_logbox.pack(fill="both", padx=10, pady=5, expand=True)

wallet_button_frame = tk.Frame(wallet_tab)
wallet_button_frame.pack(pady=5)

tk.Button(wallet_button_frame, text="Save Wallet", command=save_wallet).pack(side="left", padx=5)
tk.Button(wallet_button_frame, text="Load Wallet", command=load_wallet).pack(side="left", padx=5)
def save_wallet_tab():
    return {
        "balance": wallet_balance.get(),
        "logs": wallet_logs
    }

def load_wallet_tab(data):
    global wallet_logs
    wallet_balance.set(data.get("balance", 0.0))
    wallet_logs = data.get("logs", [])
    update_wallet_display()
    log_wallet_message("Wallet loaded.")

register_tab("wallet", save_wallet_tab, load_wallet_tab)

# ====================
# Tab 4: Journal
# ====================

from tkinter import colorchooser
from datetime import datetime
import tkinter as tk

# Use plain tkinter Frame instead of themed ttkbootstrap
journal_tab = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(journal_tab, text="Journal")

journal_color = "#ffffff"
journal_logs = []

# --- Input Form ---
journal_form = tk.Frame(journal_tab, bg="#f0f0f0")
journal_form.pack(pady=5, padx=10, fill="x")

tk.Label(journal_form, text="Title:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
journal_title = tk.Entry(journal_form, width=30, bg="white")
journal_title.grid(row=0, column=1, padx=5)

tk.Label(journal_form, text="Subtitle:", bg="#f0f0f0").grid(row=0, column=2, sticky="w")
journal_subtitle = tk.Entry(journal_form, width=30, bg="white")
journal_subtitle.grid(row=0, column=3, padx=5)

tk.Label(journal_form, text="Date:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
journal_date = tk.Entry(journal_form, width=30, bg="white")
journal_date.insert(0, datetime.now().strftime("2165-%m-%d"))
journal_date.grid(row=1, column=1, padx=5)

color_display = tk.Label(journal_form, text="      ", bg=journal_color, relief="groove", width=5)
color_display.grid(row=1, column=2, padx=5)


def pick_color():
    global journal_color
    color = colorchooser.askcolor()[1]
    if color:
        journal_color = color
        color_display.config(bg=color)




# --- Entry Content ---
tk.Label(journal_tab, text="Entry Content:", bg="#f0f0f0").pack(anchor="w", padx=10)
journal_entry = tk.Text(journal_tab, height=5, wrap="word", bg="white")
journal_entry.pack(fill="x", padx=10)

# --- Scrollable Journal Display ---
journal_display_frame = tk.Frame(journal_tab, bg="#f0f0f0")
journal_display_frame.pack(fill="both", expand=True, padx=10, pady=10)

canvas = tk.Canvas(journal_display_frame, bg="#f0f0f0", highlightthickness=0)
scrollbar = tk.Scrollbar(journal_display_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def add_journal_entry():
    global journal_logs
    title = journal_title.get().strip()
    subtitle = journal_subtitle.get().strip()
    date = journal_date.get().strip()
    content = journal_entry.get("1.0", tk.END).strip()

    if not title or not content:
        return

    color = journal_color
    container = tk.Frame(scrollable_frame, bg=color, bd=2, relief="ridge", padx=10, pady=5)
    container.pack(fill="x", pady=5)

    tk.Label(container, text=title, font=("Arial", 14, "bold"), bg=color).pack(anchor="w")
    tk.Label(container, text=subtitle, font=("Arial", 10, "italic"), bg=color).pack(anchor="w")
    tk.Label(container, text=date, font=("Arial", 9), bg=color).pack(anchor="w")
    tk.Label(container, text=content, font=("Arial", 11), wraplength=600, justify="left", bg=color).pack(anchor="w")

    journal_logs.append([title, subtitle, date, content, color])

    journal_title.delete(0, tk.END)
    journal_subtitle.delete(0, tk.END)
    journal_entry.delete("1.0", tk.END)


tk.Button(journal_tab, text="Add Entry", command=add_journal_entry).pack(pady=5)


def load_journal_tab(data):
    global journal_logs
    journal_logs = data
    for entry in data:
        title, subtitle, date, content, color = entry
        container = tk.Frame(scrollable_frame, bg=color, bd=2, relief="ridge", padx=10, pady=5)
        container.pack(fill="x", pady=5)

        tk.Label(container, text=title, font=("Arial", 14, "bold"), bg=color).pack(anchor="w")
        tk.Label(container, text=subtitle, font=("Arial", 10, "italic"), bg=color).pack(anchor="w")
        tk.Label(container, text=date, font=("Arial", 9), bg=color).pack(anchor="w")
        tk.Label(container, text=content, font=("Arial", 11), wraplength=600, justify="left", bg=color).pack(anchor="w")


def save_journal_tab():
    return journal_logs


register_tab("journal", save_journal_tab, load_journal_tab)


# ====================
# Tab 5: Profile
# ====================
profile_tab = ttk.Frame(notebook)
notebook.add(profile_tab, text="Profile")

profile_data = {
    "name": "",
    "name_color": "#000000",
    "age": "",
    "aka": "",
    "description": "",
    "finalized": False
}

def toggle_profile_fields(state):
    entries = [name_entry, age_entry, aka_entry, desc_text, name_color_button]
    for widget in entries:
        widget.config(state=state)
    edit_btn.config(state="normal" if state == "disabled" else "disabled")
    finalize_btn.config(state=state)

def pick_name_color():
    color = colorchooser.askcolor(title="Pick Name Color")[1]
    if color:
        profile_data["name_color"] = color
        name_entry.config(fg=color)



def finalize_profile():
    profile_data["name"] = name_entry.get().strip()
    profile_data["age"] = age_entry.get().strip()
    profile_data["aka"] = aka_entry.get().strip()
    profile_data["description"] = desc_text.get("1.0", tk.END).strip()
    profile_data["finalized"] = True
    toggle_profile_fields("disabled")

def edit_profile():
    toggle_profile_fields("normal")

# === UI ===

form_frame = tk.Frame(profile_tab)
form_frame.pack(pady=5)

tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e")
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, padx=5)

name_color_button = tk.Button(form_frame, text="Pick Color", command=pick_name_color)
name_color_button.grid(row=0, column=2, padx=5)

tk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="e")
age_entry = tk.Entry(form_frame, width=30)
age_entry.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Also Known As:").grid(row=2, column=0, sticky="e")
aka_entry = tk.Entry(form_frame, width=30)
aka_entry.grid(row=2, column=1, padx=5)

tk.Label(profile_tab, text="Description & Backstory:").pack(anchor="w", padx=10)
desc_frame = tk.Frame(profile_tab)
desc_frame.pack(fill="both", expand=True, padx=10, pady=5)

desc_scrollbar = tk.Scrollbar(desc_frame)
desc_scrollbar.pack(side="right", fill="y")

desc_text = tk.Text(desc_frame, wrap="word", yscrollcommand=desc_scrollbar.set)
desc_text.pack(fill="both", expand=True)

desc_scrollbar.config(command=desc_text.yview)


btn_frame = tk.Frame(profile_tab)
btn_frame.pack(pady=5)

finalize_btn = tk.Button(btn_frame, text="Finalize", command=finalize_profile)
finalize_btn.pack(side="left", padx=5)

edit_btn = tk.Button(btn_frame, text="Edit", command=edit_profile, state="disabled")
edit_btn.pack(side="left", padx=5)

def save_profile_tab():
    return {
        "name": profile_data["name"],
        "name_color": profile_data["name_color"],
        "age": profile_data["age"],
        "aka": profile_data["aka"],
        "description": profile_data["description"],
        "finalized": profile_data["finalized"]
    }

def load_profile_tab(data):
    profile_data.update(data)

    name_entry.delete(0, tk.END)
    name_entry.insert(0, data["name"])
    name_entry.config(fg=data["name_color"])

    age_entry.delete(0, tk.END)
    age_entry.insert(0, data["age"])

    aka_entry.delete(0, tk.END)
    aka_entry.insert(0, data["aka"])

    desc_text.delete("1.0", tk.END)
    desc_text.insert("1.0", data["description"])


    toggle_profile_fields("disabled" if data.get("finalized") else "normal")

register_tab("profile", save_profile_tab, load_profile_tab)

# ====================
# Tab 6: Notepad
# ====================
notepad_tab = ttk.Frame(notebook)
notebook.add(notepad_tab, text="Notepad")

# Default font config
notepad_font_family = "Arial"
notepad_font_size = tk.IntVar(value=12)
notepad_text = tk.Text(notepad_tab, wrap="word", font=(notepad_font_family, notepad_font_size.get()))
notepad_text.pack(fill="both", expand=True, padx=10, pady=(0, 5))

# Font size dropdown
size_frame = tk.Frame(notepad_tab)
size_frame.pack(pady=5)
tk.Label(size_frame, text="Font Size:").pack(side="left", padx=5)

font_size_option = ttk.Combobox(size_frame, width=5, textvariable=notepad_font_size, values=list(range(8, 15)))
font_size_option.pack(side="left")

def update_font_size(*args):
    current_tags = notepad_text.tag_names("sel.first")
    new_font = (notepad_font_family, notepad_font_size.get())
    notepad_text.configure(font=new_font)
    for tag in current_tags:
        notepad_text.tag_config(tag, font=new_font)

notepad_font_size.trace_add("write", update_font_size)

# Style tag toggling
def toggle_style(tag_name, font_weight=None, font_slant=None):
    try:
        start, end = notepad_text.index("sel.first"), notepad_text.index("sel.last")
    except tk.TclError:
        return

    # Tag config
    font_conf = {
        "font": (notepad_font_family, notepad_font_size.get(), f"{font_weight or ''} {font_slant or ''}".strip())
    }
    notepad_text.tag_config(tag_name, **font_conf)

    if tag_name in notepad_text.tag_names("sel.first"):
        notepad_text.tag_remove(tag_name, start, end)
    else:
        notepad_text.tag_add(tag_name, start, end)

# Buttons
format_btns = tk.Frame(notepad_tab)
format_btns.pack(pady=5)

tk.Button(format_btns, text="Bold", command=lambda: toggle_style("bold", font_weight="bold")).pack(side="left", padx=5)
tk.Button(format_btns, text="Italic", command=lambda: toggle_style("italic", font_slant="italic")).pack(side="left", padx=5)

# Save/load support
def save_notepad_tab():
    return {
        "content": notepad_text.get("1.0", tk.END),
        "tags": [(tag, notepad_text.index(start), notepad_text.index(end))
                 for tag in notepad_text.tag_names()
                 for start, end in zip(notepad_text.tag_ranges(tag)[::2], notepad_text.tag_ranges(tag)[1::2])],
        "font_size": notepad_font_size.get()
    }

def load_notepad_tab(data):
    notepad_text.delete("1.0", tk.END)
    notepad_text.insert("1.0", data.get("content", ""))
    notepad_font_size.set(data.get("font_size", 12))

    for tag, start, end in data.get("tags", []):
        notepad_text.tag_add(tag, start, end)

register_tab("notepad", save_notepad_tab, load_notepad_tab)

# ====================
# Tab 6: Quests & Objectives
# ====================
from tkinter import simpledialog

quests_tab = ttk.Frame(notebook)
notebook.add(quests_tab, text="Quests")

quest_data = []

# Scrollable frame setup
quest_display_frame = tk.Frame(quests_tab)
quest_display_frame.pack(fill="both", expand=True, padx=10, pady=(10, 40))  # space for progress bar

quest_canvas = tk.Canvas(quest_display_frame)
quest_scrollbar = ttk.Scrollbar(quest_display_frame, orient="vertical", command=quest_canvas.yview)
quest_scrollable = tk.Frame(quest_canvas)

quest_scrollable.bind("<Configure>", lambda e: quest_canvas.configure(scrollregion=quest_canvas.bbox("all")))
quest_canvas.create_window((0, 0), window=quest_scrollable, anchor="nw")
quest_canvas.configure(yscrollcommand=quest_scrollbar.set)

quest_canvas.pack(side="left", fill="both", expand=True)
quest_scrollbar.pack(side="right", fill="y")

# Quest Status Options
STATUS_OPTIONS = ["Active", "Completed", "Failed"]

def update_progress_bar():
    total = len(quest_data)
    if total == 0:
        quest_progress["value"] = 0
        return
    completed = sum(1 for q in quest_data if q["status"] == "Completed")
    percent = (completed / total) * 100
    quest_progress["value"] = percent
    quest_progress_label.config(text=f"{int(percent)}% Complete")

def add_quest_frame(title, desc, status, category):
    frame = tk.Frame(quest_scrollable, bg="white", bd=2, relief="ridge", padx=10, pady=5)
    frame.pack(fill="x", pady=5)

    title_label = tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg="white")
    title_label.pack(anchor="w")

    tk.Label(frame, text=f"Category: {category}", font=("Arial", 10, "italic"), bg="white").pack(anchor="w")
    desc_label = tk.Label(frame, text=desc, font=("Arial", 11), wraplength=500, justify="left", bg="white")
    desc_label.pack(anchor="w")

    status_var = tk.StringVar(value=status)
    status_menu = ttk.OptionMenu(frame, status_var, status, *STATUS_OPTIONS,
                                 command=lambda _: update_status(title, status_var.get()))
    status_menu.pack(anchor="e", pady=5)

    # Edit/Delete buttons
    btn_frame = tk.Frame(frame, bg="white")
    btn_frame.pack(anchor="e")

    tk.Button(btn_frame, text="✏️ Edit", command=lambda: edit_quest(title)).pack(side="left", padx=5)
    tk.Button(btn_frame, text="❌ Delete", command=lambda: delete_quest(title)).pack(side="left")

def update_status(title, new_status):
    for quest in quest_data:
        if quest["title"] == title:
            quest["status"] = new_status
            break
    update_progress_bar()

def delete_quest(title):
    global quest_data
    quest_data = [q for q in quest_data if q["title"] != title]
    refresh_quests()

def edit_quest(title):
    for quest in quest_data:
        if quest["title"] == title:
            new_title = simpledialog.askstring("Edit Title", "New Title:", initialvalue=quest["title"])
            new_desc = simpledialog.askstring("Edit Description", "New Description:", initialvalue=quest["description"])
            new_cat = simpledialog.askstring("Edit Category", "New Category:", initialvalue=quest["category"])
            if new_title and new_desc:
                quest.update({"title": new_title, "description": new_desc, "category": new_cat})
                refresh_quests()
            break

def refresh_quests():
    for widget in quest_scrollable.winfo_children():
        widget.destroy()
    for quest in quest_data:
        add_quest_frame(quest["title"], quest["description"], quest["status"], quest["category"])
    update_progress_bar()

def add_quest():
    title = simpledialog.askstring("Quest Title", "Enter quest title:")
    if not title:
        return
    desc = simpledialog.askstring("Description", "Enter quest description:")
    category = simpledialog.askstring("Category", "Optional category:", initialvalue="General")
    if not desc:
        return
    quest_data.append({
        "title": title,
        "description": desc,
        "status": "Active",
        "category": category
    })
    refresh_quests()

tk.Button(quests_tab, text="➕ Add Quest", command=add_quest).pack(pady=5)

# Progress bar at the bottom
bottom_frame = tk.Frame(quests_tab)
bottom_frame.pack(side="bottom", fill="x", pady=5)

quest_progress_label = tk.Label(bottom_frame, text="0% Complete")
quest_progress_label.pack(side="left", padx=10)

quest_progress = ttk.Progressbar(bottom_frame, orient="horizontal", length=400, mode="determinate")
quest_progress.pack(side="left", expand=True, padx=10)

# Save/load integration
def save_quests_tab():
    return quest_data

def load_quests_tab(data):
    global quest_data
    quest_data = data
    refresh_quests()

register_tab("quests", save_quests_tab, load_quests_tab)

# ====================
# Tab X: Trade Deals / Merchant Log
# ====================
trade_tab = ttk.Frame(notebook)
notebook.add(trade_tab, text="Trade Deals")

trade_logs = []

# Input Form
trade_form = ttk.Frame(trade_tab)
trade_form.pack(padx=10, pady=5, fill="x")

ttk.Label(trade_form, text="Merchant:").grid(row=0, column=0, sticky="e")
trade_merchant = ttk.Entry(trade_form, width=25)
trade_merchant.grid(row=0, column=1, padx=5)

ttk.Label(trade_form, text="Items Given:").grid(row=0, column=2, sticky="e")
trade_given = ttk.Entry(trade_form, width=25)
trade_given.grid(row=0, column=3, padx=5)

ttk.Label(trade_form, text="Items Received:").grid(row=1, column=0, sticky="e")
trade_received = ttk.Entry(trade_form, width=25)
trade_received.grid(row=1, column=1, padx=5)

ttk.Label(trade_form, text="Location:").grid(row=1, column=2, sticky="e")
trade_location = ttk.Entry(trade_form, width=25)
trade_location.grid(row=1, column=3, padx=5)

ttk.Label(trade_form, text="Profit/Loss:").grid(row=2, column=0, sticky="e")
trade_profit = ttk.Entry(trade_form, width=10)
trade_profit.grid(row=2, column=1, padx=5, sticky="w")

def clear_trade_inputs():
    trade_merchant.delete(0, tk.END)
    trade_given.delete(0, tk.END)
    trade_received.delete(0, tk.END)
    trade_location.delete(0, tk.END)
    trade_profit.delete(0, tk.END)

# Scrollable log display
trade_display_frame = ttk.Frame(trade_tab)
trade_display_frame.pack(fill="both", expand=True, padx=10, pady=10)

trade_canvas = tk.Canvas(trade_display_frame)
trade_scrollbar = ttk.Scrollbar(trade_display_frame, orient="vertical", command=trade_canvas.yview)
trade_log_frame = ttk.Frame(trade_canvas)

trade_log_frame.bind(
    "<Configure>",
    lambda e: trade_canvas.configure(scrollregion=trade_canvas.bbox("all"))
)

trade_canvas.create_window((0, 0), window=trade_log_frame, anchor="nw")
trade_canvas.configure(yscrollcommand=trade_scrollbar.set)

trade_canvas.pack(side="left", fill="both", expand=True)
trade_scrollbar.pack(side="right", fill="y")

def add_trade_log():
    merchant = trade_merchant.get().strip()
    given = trade_given.get().strip()
    received = trade_received.get().strip()
    location = trade_location.get().strip()
    profit = trade_profit.get().strip()

    if not merchant or not given or not received:
        return

    entry = {
        "merchant": merchant,
        "given": given,
        "received": received,
        "location": location,
        "profit": profit
    }
    trade_logs.append(entry)
    display_trade_entry(entry)
    clear_trade_inputs()

def display_trade_entry(entry):
    frame = ttk.Frame(trade_log_frame, padding=10, relief="ridge", style="Card.TFrame")
    frame.pack(fill="x", pady=5)

    ttk.Label(frame, text=f"Merchant: {entry['merchant']}", font=("Arial", 12, "bold")).pack(anchor="w")
    ttk.Label(frame, text=f"Items Given: {entry['given']}").pack(anchor="w")
    ttk.Label(frame, text=f"Items Received: {entry['received']}").pack(anchor="w")
    ttk.Label(frame, text=f"Location: {entry['location']}").pack(anchor="w")
    if entry["profit"]:
        ttk.Label(frame, text=f"Profit/Loss: {entry['profit']}").pack(anchor="w")

ttk.Button(trade_tab, text="Add Trade Log", command=add_trade_log).pack(pady=5)

def save_trade_tab():
    return trade_logs

def load_trade_tab(data):
    global trade_logs
    trade_logs = data
    for entry in data:
        display_trade_entry(entry)

register_tab("trade", save_trade_tab, load_trade_tab)


def save_all():
    data = {}
    for name, func in tab_savers.items():
        data[name] = func()
    default_name = tab_savers.get("profile", lambda: {})().get("name", "save")
    path = filedialog.asksaveasfilename(
        defaultextension=".json",
        initialfile=f"{default_name}.json",
        title="Save All",
        filetypes=[("JSON files", "*.json")]
    )
    if path:
        with open(path, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", "All data saved.")

def load_all():
    path = filedialog.askopenfilename(title="Load Save", filetypes=[("JSON files", "*.json")])
    if path:
        with open(path, "r") as f:
            data = json.load(f)
        for name, loader in tab_loaders.items():
            if name in data:
                loader(data[name])
        messagebox.showinfo("Loaded", "All data loaded.")


save_button_frame = tk.Frame(root)
save_button_frame.pack(pady=10)
tk.Button(save_button_frame, text="💾 Save All", command=save_all).pack(side="left", padx=10)
tk.Button(save_button_frame, text="📂 Load All", command=load_all).pack(side="left", padx=10)


root.mainloop()


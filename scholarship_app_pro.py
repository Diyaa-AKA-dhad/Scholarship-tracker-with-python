import json
import os
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

FILE_NAME = "scholarships.json"
editing_index = None

# ---------- DATA HANDLING ----------

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_data():
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- UI ACTIONS ----------

def refresh_list():
    for widget in list_frame.winfo_children():
        widget.destroy()

    data = load_data()

    for index, item in enumerate(data):
        row = ctk.CTkFrame(list_frame)
        row.pack(fill="x", padx=10, pady=5)

        title_label = ctk.CTkLabel(row, text=item["title"], width=250, anchor="w")
        title_label.grid(row=0, column=0, padx=10)

        status_label = ctk.CTkLabel(row, text=item["status"], width=120)
        status_label.grid(row=0, column=1)

        open_btn = ctk.CTkButton(row, text="Open", width=60,
                                 command=lambda i=index: open_link(i))
        open_btn.grid(row=0, column=2, padx=5)

        edit_btn = ctk.CTkButton(row, text="Edit", width=60,
                                 command=lambda i=index: edit_item(i))
        edit_btn.grid(row=0, column=3, padx=5)

        del_btn = ctk.CTkButton(row, text="✖", width=40, fg_color="red",
                                command=lambda i=index: delete_item(i))
        del_btn.grid(row=0, column=4, padx=5)

        # Hover tooltip for link
        create_tooltip(title_label, item["link"])

def add_or_update():
    global editing_index

    title = title_entry.get().strip()
    link = link_entry.get().strip()
    status = status_entry.get().strip()

    if not title or not link or not status:
        messagebox.showerror("Error", "All fields are required.")
        return

    data = load_data()
    new_item = {"title": title, "link": link, "status": status}

    if editing_index is None:
        data.append(new_item)
    else:
        data[editing_index] = new_item
        editing_index = None
        add_button.configure(text="➕ Add Scholarship")

    save_data(data)
    clear_inputs()
    refresh_list()

def delete_item(index):
    data = load_data()
    if messagebox.askyesno("Confirm", "Delete this scholarship?"):
        data.pop(index)
        save_data(data)
        refresh_list()

def open_link(index):
    data = load_data()
    webbrowser.open(data[index]["link"])

def edit_item(index):
    global editing_index
    data = load_data()
    item = data[index]

    title_entry.delete(0, "end")
    link_entry.delete(0, "end")
    status_entry.delete(0, "end")

    title_entry.insert(0, item["title"])
    link_entry.insert(0, item["link"])
    status_entry.insert(0, item["status"])

    editing_index = index
    add_button.configure(text="✅ Save Changes")

def clear_inputs():
    title_entry.delete(0, "end")
    link_entry.delete(0, "end")
    status_entry.delete(0, "end")

# ---------- TOOLTIP SYSTEM ----------

def create_tooltip(widget, text):
    tooltip = ctk.CTkLabel(app, text=text, fg_color="black")
    tooltip.place_forget()

    def show(event):
        tooltip.place(x=event.x_root - app.winfo_rootx() + 10,
                      y=event.y_root - app.winfo_rooty() + 10)

    def hide(event):
        tooltip.place_forget()

    widget.bind("<Enter>", show)
    widget.bind("<Leave>", hide)

# ---------- UI SETUP ----------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Scholarship Tracker Pro")
app.geometry("900x600")

title_label = ctk.CTkLabel(app, text="🎓 Scholarship Tracker", font=("Arial", 24))
title_label.pack(pady=15)

list_container = ctk.CTkScrollableFrame(app, height=300)
list_container.pack(fill="both", expand=True, padx=20, pady=10)

list_frame = list_container

form_frame = ctk.CTkFrame(app)
form_frame.pack(pady=10)

title_entry = ctk.CTkEntry(form_frame, width=600, placeholder_text="Scholarship Title")
title_entry.pack(pady=5)

link_entry = ctk.CTkEntry(form_frame, width=600, placeholder_text="Scholarship Link")
link_entry.pack(pady=5)

status_entry = ctk.CTkEntry(form_frame, width=600, placeholder_text="Status (applied, accepted...)")
status_entry.pack(pady=5)

add_button = ctk.CTkButton(app, text="➕ Add Scholarship", command=add_or_update)
add_button.pack(pady=15)

refresh_list()
app.mainloop()

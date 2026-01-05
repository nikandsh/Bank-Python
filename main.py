import customtkinter as ctk
import sqlite3
from tkinter import messagebox

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("500x600")
app.title("Bank Simulator")

def db():
    return sqlite3.connect("database.db")

# =======================================================================
# 1. بخش ورود که شامل تنظیمات صفحه، دکمه ها ، تابع ها است

vorod = ctk.CTkFrame(app, width=480, height=480)
vorod.place(x=10, y=10)

ctk.CTkLabel(vorod, text="Vorood", font=("Arial", 30)).place(x=190, y=40)

entry_card = ctk.CTkEntry(vorod, placeholder_text="Shomare Kart", font=("Arial", 16), width=220, height=30)
entry_card.place(x=130, y=100)

entry_cvv = ctk.CTkEntry(vorod, placeholder_text="CVV2", font=("Arial", 16), width=220, height=30)
entry_cvv.place(x=130, y=140)

def user_login():
    card = entry_card.get()
    cvv = entry_cvv.get()
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT name, card_number, cvv2, expire_date, balance FROM accounts WHERE card_number=? AND cvv2=?",(card, cvv))
    user = cur.fetchone()
    conn.close()
    if user:
        vorod.place_forget()
        user_panel(user)
    else:
        messagebox.showerror("Error", "Etelaate kart eshtebah ast")

ctk.CTkButton(vorod, text="Vorood", font=("Arial", 16), command=user_login, width=120, height=30).place(x=180, y=200)

def go_to_admin_login():
    vorod.place_forget()
    admin_vorod.place(x=10, y=10)

ctk.CTkButton(vorod, text="Admin", font=("Arial", 16), command=go_to_admin_login, width=120, height=30, fg_color="gray").place(x=180, y=250)


# =======================================================================
# 2. پنل کاربری

user_frame = ctk.CTkFrame(app, width=480, height=580)

# لیبل‌های نمایش اطلاعات کاربر
lbl_name = ctk.CTkLabel(user_frame, text="")
lbl_name.place(x=30, y=20)
lbl_card = ctk.CTkLabel(user_frame, text="")
lbl_card.place(x=30, y=50)
lbl_cvv = ctk.CTkLabel(user_frame, text="")
lbl_cvv.place(x=30, y=80)
lbl_exp = ctk.CTkLabel(user_frame, text="")
lbl_exp.place(x=30, y=110)
lbl_balance = ctk.CTkLabel(user_frame, text="")
lbl_balance.place(x=30, y=140)

# فیلدهای عملیاتی پنل کاربر
entry_to = ctk.CTkEntry(user_frame, placeholder_text="Kart Maghsad", font=("Arial", 16), width=220, height=30)
entry_to.place(x=30, y=190)
entry_amount = ctk.CTkEntry(user_frame, placeholder_text="Mablagh", font=("Arial", 16), width=220, height=30)
entry_amount.place(x=30, y=220)
entry_deposit = ctk.CTkEntry(user_frame, placeholder_text="Mablagh Variz", font=("Arial", 16), width=220, height=30)
entry_deposit.place(x=30, y=260)

text_box = ctk.CTkTextbox(user_frame, width=400, height=150)
text_box.place(x=30, y=345)

# توابع پنل کاربری
def user_panel(user):
    user_frame.place(x=10, y=10)
    lbl_name.configure(text=f"Nam: {user[0]}", font=("Arial", 20))
    lbl_card.configure(text=f"Shomare Kart: {user[1]}", font=("Arial", 20))
    lbl_cvv.configure(text=f"CVV2: {user[2]}", font=("Arial", 20))
    lbl_exp.configure(text=f"Tarikh Engheza: {user[3]}", font=("Arial", 20))
    lbl_balance.configure(text=f"Mojoodi: {user[4]}", font=("Arial", 20))

def logout_user():
    user_frame.place_forget()
    entry_card.delete(0, 'end')
    entry_cvv.delete(0, 'end')
    entry_to.delete(0, 'end')
    entry_amount.delete(0, 'end')
    text_box.delete("1.0", "end")
    vorod.place(x=10, y=10)

def transfer():
    to_card = entry_to.get()
    amount_str = entry_amount.get()
    from_card = lbl_card.cget("text").split(": ")[1]
    if to_card == from_card:
        messagebox.showerror("Error", "Shomare kart mabda va maghsad yeki ast!")
        return
    try:
        amount = int(amount_str)
        conn = db()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM accounts WHERE card_number=?", (from_card,))
        bal = cur.fetchone()[0]
        if bal < amount:
            messagebox.showerror("Error", "Mojoodi kafi nist")
        else:
            cur.execute("UPDATE accounts SET balance=balance-? WHERE card_number=?", (amount, from_card))
            cur.execute("UPDATE accounts SET balance=balance+? WHERE card_number=?", (amount, to_card))
            cur.execute("INSERT INTO enteghal VALUES (?, ?, ?)", (from_card, to_card, amount))
            conn.commit()
            messagebox.showinfo("Succesful", "Enteghal anjam shod")
            cur.execute("SELECT balance FROM accounts WHERE card_number=?", (from_card,))
            new_bal = cur.fetchone()[0]
            lbl_balance.configure(text=f"Mojoodi: {new_bal}")
        conn.close()
    except:
        messagebox.showerror("Error", "Etelaat ghalat ast")

def deposit():
    amount_str = entry_deposit.get()
    from_card = lbl_card.cget("text").split(": ")[1]
    try:
        amount = int(amount_str)
        conn = db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET balance=balance+? WHERE card_number=?", (amount, from_card))
        conn.commit()
        cur.execute("SELECT balance FROM accounts WHERE card_number=?", (from_card,))
        new_bal = cur.fetchone()[0]
        lbl_balance.configure(text=f"Mojoodi: {new_bal}")
        conn.close()
        messagebox.showinfo("Succesful", "Variz anjam shod")
        entry_deposit.delete(0, 'end')
    except:
        messagebox.showerror("Error", "Lotfan adad vared konid")

def tarakonesh():
    from_card = lbl_card.cget("text").split(": ")[1]
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM enteghal WHERE from_card=? OR to_card=?", (from_card, from_card))
    rows = cur.fetchall()
    conn.close()
    text_box.delete("1.0", "end")
    for r in rows:
        text_box.insert("end", f"{r[0]} -> {r[1]} | amount: {r[2]}\n")

# دکمه‌های پنل کاربر
ctk.CTkButton(user_frame, text="Enteghal Vajh", font=("Arial", 16), command=transfer, width=170, height=30, fg_color="green").place(x=260, y=208)
ctk.CTkButton(user_frame, text="Variz be Hesab", font=("Arial", 16), command=deposit, width=170, height=30, fg_color="green").place(x=260, y=260)
ctk.CTkButton(user_frame, text="Gozaresh Tarakonesh", font=("Arial", 16), command=tarakonesh, width=150, height=30).place(x=260, y=310)
ctk.CTkButton(user_frame, text="Khorooj", font=("Arial", 16), command=logout_user, width=150, height=30, fg_color="#e74c3c").place(x=160, y=530)


# =======================================================================
# 3. بخش ادمین

admin_vorod = ctk.CTkFrame(app, width=480, height=200)
entry_admin_pass = ctk.CTkEntry(admin_vorod, placeholder_text="Password Admin", show="*", font=("Arial", 16), width=220, height=30)
entry_admin_pass.place(x=130, y=70)

admin_panel = ctk.CTkFrame(app, width=480, height=520)

def admin_login():
    if entry_admin_pass.get() == "1234":
        admin_vorod.place_forget()
        admin_panel.place(x=10, y=10)
    else:
        messagebox.showerror("Error", "Password eshtebah ast")

ctk.CTkButton(admin_vorod, text="Vorood", font=("Arial", 16), command=admin_login, width=150, height=30).place(x=165, y=120)

# ویجت‌های پنل ادمین
ctk.CTkLabel(admin_panel, text="Sakhte Hesabe Jadid", font=("Arial", 30)).place(x=95, y=10)
new_name = ctk.CTkEntry(admin_panel, placeholder_text="Nam", font=("Arial", 16), width=300, height=30)
new_name.place(x=90, y=60)
new_card = ctk.CTkEntry(admin_panel, placeholder_text="Shomare Kart", font=("Arial", 16), width=300, height=30)
new_card.place(x=90, y=100)
new_cvv = ctk.CTkEntry(admin_panel, placeholder_text="CVV2", font=("Arial", 16), width=300, height=30)
new_cvv.place(x=90, y=140)
new_exp = ctk.CTkEntry(admin_panel, placeholder_text="Tarikh Engheza", font=("Arial", 16), width=300, height=30)
new_exp.place(x=90, y=180)
new_balance = ctk.CTkEntry(admin_panel, placeholder_text="Mojoodie Avalie", font=("Arial", 16), width=300, height=30)
new_balance.place(x=90, y=220)
del_card_entry = ctk.CTkEntry(admin_panel, placeholder_text="Shomare Kart baraye hazf", font=("Arial", 16), width=300, height=30)
del_card_entry.place(x=90, y=320)

# توابع پنل ادمین
def create_account():
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)",
                    (new_name.get(), new_card.get(), new_cvv.get(), new_exp.get(), int(new_balance.get())))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succesful", "Hesab sakhte shod")
    except:
        messagebox.showerror("Error", "Moshkeli dar sakhte hesab pish amade")

def delete_account():
    card_to_delete = del_card_entry.get()
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("DELETE FROM accounts WHERE card_number=?", (card_to_delete,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Successful", "Hesab hazf shod")
        del_card_entry.delete(0, 'end')
    except:
        messagebox.showerror("Error", "Moshkeli dar hazf pish amade")

# دکمه‌های پنل ادمین
ctk.CTkButton(admin_panel, text="Sabt Hesab", font=("Arial", 16), command=create_account, width=150, height=30, fg_color="green").place(x=165, y=270)
ctk.CTkButton(admin_panel, text="Hazfe Hesab", font=("Arial", 16), command=delete_account, width=150, height=30, fg_color="red").place(x=165, y=360)
ctk.CTkButton(admin_panel, text="Khorooj", font=("Arial", 16), command=lambda: admin_panel.place_forget() or vorod.place(x=10, y=10), width=150, height=30, fg_color="red").place(x=165, y=410)

app.mainloop()
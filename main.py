from datetime import datetime
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
#available requests:
available_requests = pd.Series(index=["logo", "poster", "business card", "photo editing", "website front-end", "advertisements", "social media kit", "powerpoint presentation"], data=[135, 170, 100, 115, 180, 160, 200, 140])

#Reading the dataframe:
df = pd.read_csv("purchase_data.csv").dropna(how='all')

#interface:
#inputs: [customer name, email address, purchased requests]
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Invoice Generator")
root.iconbitmap("icon.ico")
#Name entry:
tk.Label(root, text="Enter your name:").grid(row=0, column=0)
name_entry = tk.Entry(root, width= 24)
name_entry.grid(row=0, column=1)

#Email entry:
tk.Label(root, text="Enter your Email:").grid(row=1, column=0)
email_entry = tk.Entry(root, width= 24)
email_entry.grid(row=1, column=1)

#request choices:
tk.Label(root, text="Choose your request:").grid(row=2, column=0)
request = []
prices = []
total_price = 0

def requester(x, y):
    global total_price
    request.append(x)
    prices.append(available_requests[x])
    total_price += y

#Submit button
#What it does: [gets the entries, puts the entries in a dictionary, adds that dictionary into the dataframe, resets the entries]
def submit():
    global name_entry, email_entry, prices ,request ,total_price ,df ,request_in, html
    name = name_entry.get()
    email = email_entry.get()
    date = datetime.today().strftime('%Y-%m-%d')
    if not name or not email or not request:
        messagebox.showerror("Error", "All fields and at least one request are required.")
        return
    #Saved Dictionary in the csv sheet
    df_list = {
        "name" : name,
        "email": email,
        "requests": ", ".join(request),
        "total_price": total_price,
        "date": date
    }
    df = pd.concat([df, pd.DataFrame([df_list])], ignore_index=True) #combine the data
    df.to_csv("purchase_data.csv", index=False) #save the data
    
    #used in the invoice
    request_in = {
        "name": name,
        "requests": pd.Series(data= prices, index= request),
        "total_price": total_price
    }
    #invoice template:
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("invoice_template.html")
    html = template.render(request_in)
    pdfkit.from_string(html, path = fr"invoices\invoice_{name.replace(' ', '_')}_{date}.pdf"
                       ,configuration=config)
    #reset the entries
    request = []
    total_price = 0
    prices = []
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Invoice generated successfully!")

#Request clearer:
def clearer():
    global request, total_price, prices
    request = []
    total_price = 0
    prices = []
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
w = 30
tk.Button(root, text="logo for 135 LE", command= lambda: requester("logo", 135), width= w).grid(row=3, column=0)
tk.Button(root, text="poster for 170 LE", command= lambda: requester("poster", 170), width=w).grid(row=3, column=1)
tk.Button(root, text="business card for 100 LE", command= lambda: requester("business card", 100), width=w).grid(row=4, column=0)
tk.Button(root, text="photo editing for 115 LE", command= lambda: requester("photo editing", 115), width=w).grid(row=4, column=1)
tk.Button(root, text="website front-end for 180 LE", command= lambda: requester("website front-end", 180), width=w).grid(row=5, column=0)
tk.Button(root, text="advertisements for 160 LE", command= lambda: requester("advertisements", 160), width=w).grid(row=5, column=1)
tk.Button(root, text="social media kit for 200 LE", command= lambda: requester("social media kit", 200), width=w).grid(row=6, column=0)
tk.Button(root, text="powerpoint presentation for 140 LE", command= lambda: requester("powerpoint presentation", 140), width=w).grid(row=6, column=1)

#Request clearer:
tk.Button(root, text="clear", command=clearer, width=w).grid(row=7, column=0)

#Request submitter:
tk.Button(root, text="submit", command= submit, width=w).grid(row=7, column=1)

root.mainloop()
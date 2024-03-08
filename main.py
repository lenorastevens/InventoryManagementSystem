import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import OptionMenu
from tkinter import Toplevel
from tkinter.font import Font

# Create the main window
root = Tk()
root.title("Inventory Management System")

# Function to center the window on the screen
def center_window(window, width, height):
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate coordinates to center window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    # Set window geometry
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

# Set main window size and background color
center_window(root, 1030, 800)
root.geometry('1030x800')
root.configure(bg="#80ECFF")

# Initialize Treeview widget
my_tree = ttk.Treeview(root)

# Set store name and font
storeName = "Mastery Protein"
my_font = Font(
    family = 'Helvetica',
    size = 15,
    weight = 'bold',
    slant = 'roman',
)

# Try connecting to the database and creating a table if it doesn't exist
try:
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()
    cursor.execute("""CREATE TABLE IF NOT EXISTS 
                       inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemPack Text, itemQuantity TEXT, itemUtah Text, itemTexas TEXT, itemFlorida TEXT)""")
except sqlite3.Error as e:
    print("SQLite error:", e)

# Function to reverse tuples 
def reverse(tuples):
    return tuples[::-1]

# Function to insert data into the database
def insert(id, name, price, pack, quantity, utah, texas, florida):
    cursor.execute("INSERT INTO inventory (itemId, itemName, itemPrice, itemPack, itemQuantity, itemUtah, itemTexas, itemFlorida) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, name, price, pack, quantity, utah, texas, florida))
    connection.commit()

# Function to delete data from the database
def delete(data):
    cursor.execute("DELETE FROM inventory WHERE itemId =?", (data,))
    connection.commit()

# Function to update data in the database
def update(idName, quantity=None, utah=None, texas=None, florida=None):
    cursor.execute("SELECT * FROM inventory WHERE itemId = ?", (idName,))
    existing_data = cursor.fetchone()

    if existing_data:
        if quantity:
            existing_data = existing_data[:4] + (quantity,) + existing_data[5:]
        if utah:
            existing_data = existing_data[:5] + (utah,) + existing_data[6:]
        if texas:
            existing_data = existing_data[:6] + (texas,) + existing_data[7:]
        if florida:
            existing_data = existing_data[:7] + (florida,) + existing_data[8:]
        
        cursor.execute("UPDATE inventory SET itemQuantity = ?, itemUtah = ?, itemTexas = ?, itemFlorida = ? WHERE itemId = ?", (existing_data[4], existing_data[5], existing_data[6], existing_data[7], idName))
        connection.commit()
        print("Item updated successfully.")
    else:
        print("Item not found in the inventory.")

# Function to read data from the database
def read():
    cursor.execute("SELECT * FROM inventory")
    results = cursor.fetchall()
    connection.commit()
    return results

#Function to set name by selected ID 
def update_selected_id(*args):
    id_index = id_options.index(selected_id.get())
    selected_name.set(name_options[id_index // 2])

# Function to insert data into the database
def insert_data():
    itemId = selected_id.get().strip()
    itemName = selected_name.get().strip()

    if not all((itemId, itemName)):
        print("ERROR: Id and Product Name are required.")
        return
    
    # Set pack size and price based on ID
    if itemId.endswith("12"):
        itemPack = "12"
        itemPrice = "$39.99"
    elif itemId.endswith("24"):
        itemPack = "24"
        itemPrice = "$54.99"
    else:
        print("Invalid ID format.")
        return
    
    # Data for total quantity math
    itemUtah = entryUtah.get().strip()
    itemTexas = entryTexas.get().strip()
    itemFlorida = entryFlorida.get().strip()

    if not all((itemUtah, itemTexas, itemFlorida)):
        print("ERROR: All fields are required.")
        return

    total_quantity = int(itemUtah) + int(itemTexas) + int(itemFlorida)

    insert(itemId, itemName, itemPrice, itemPack, str(total_quantity), itemUtah, itemTexas, itemFlorida)
    update_tree()

# Function to delete data from the database
def delete_data():
    selected_items = my_tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        deleteData = my_tree.item(selected_item)['values'][0]
        delete(deleteData)
        update_tree()       
    else:
        print("No item selected for deletion.")

# Function to update data in the database
def update_data():
    selected_items = my_tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        update_id = my_tree.item(selected_item)['values'][0]

        # Gets quantities
        new_utah = entryUtah.get()
        new_texas = entryTexas.get()
        new_florida = entryFlorida.get()

        cursor.execute("SELECT itemUtah, itemTexas, itemFlorida FROM inventory WHERE itemId =?", (update_id,))
        current_vales = cursor.fetchone()
        current_utah, current_texas, current_florida = current_vales

        # Checks quanties
        if not new_utah:
            new_utah = current_utah
        if not new_texas:
            new_texas = current_texas
        if not new_florida:
            new_florida = current_florida

        total_quantity = int(new_utah) + int(new_texas) + int(new_florida)

        update(update_id, str(total_quantity), new_utah, new_texas, new_florida)
        update_tree()
    else:
        print("No item selected for update.")

# Funtion to update the Treeview widget with database data
def update_tree():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for idx, result in enumerate(reversed(read()), start=1):
        total_quantity = int(result[5]) + int(result[6])+ int (result[7])
        values = (result[0], result[1], result[2], result[3], total_quantity, result[5], result[6], result[7])
      
        my_tree.insert(parent='', index='end', iid=idx, text="", values=values, tags=("orow",))

        # Tags a row if quantities drop below 200
        my_tree.item(idx, tags=("orow",))
        for col, cell_value in enumerate(result[5:], start=5):
            try:
                cell_value_int = int(cell_value)
                if cell_value_int < 200:
                    my_tree.item(idx, tags=(my_tree.item(idx, "tags") or ()) + (f"{['utah', 'texas', 'florida'][col-5]}_red",))
                else:
                    my_tree.item(idx, tags=(my_tree.item(idx, "tags") or ()) + (f"{['utah', 'texas', 'florida'][col-5]}",))
            except ValueError:
                pass
    clear_fields()

# Function to clear entry fields
def clear_fields():
    entryUtah.delete(0, 'end')
    entryTexas.delete(0, 'end')
    entryFlorida.delete(0, 'end')    

# Function to sort Treeview by a specific column
def sort_treeview(column_name):
    cursor.execute(f"SELECT * FROM inventory ORDER BY {column_name}")
    sorted_data = cursor.fetchall()

    for item in my_tree.get_children(''):
        my_tree.delete(item)

    for idx, row in enumerate(sorted_data, start=1):
        my_tree.insert("", "end", values=row)

# Function to create a window for sorting options
def sort_by():
    sort_window = Toplevel(root)
    sort_window.title("Sort By")
    center_window(sort_window, 300, 200)

    sort_window.geometry("300x200")
    sort_window.config(bg="#ffc6f2")

    btn_name = Button(sort_window, text="Sort Product Name", font=my_font, bg="#9945FF", fg="#FBFFF1", command=lambda: sort_selected_column("itemName"))
    btn_name.pack(side="top", anchor="n", pady=10)
    btn_id = Button(sort_window, text="Sort by Product ID", font=my_font, bg="#281CA5", fg="#FBFFF1", command=lambda: sort_selected_column("itemId"))
    btn_id.pack(side="top", anchor="n", pady=10)
    btn_quantity = Button(sort_window, text="Sort by Total Quantity", font=my_font, bg="#FFE448", fg="#FBFFF1", command=lambda: sort_selected_column("itemQuantity"))
    btn_quantity.pack(side="top", anchor="n", pady=10)

    def sort_selected_column(colunm_name):
        sort_treeview(colunm_name)
        sort_window.destroy()

# Labels for input and table data fields
idLabel = Label(root, text="ID", font=my_font, bg="#80ECFF")
nameLabel = Label(root, text="Flavor", font=my_font, bg="#80ECFF")
utahLabel = Label(root, text="Utah Qty", font=my_font, bg="#80ECFF")
texasLabel = Label(root, text="Texas Qty", font=my_font, bg="#80ECFF")
floridaLabel = Label(root, text="Florida Qty", font=my_font, bg="#80ECFF")

# Position labels
idLabel.grid(row=1, column=0, padx=10, pady=10)
nameLabel.grid(row=2, column=0, padx=10, pady=10)
utahLabel.grid(row=1, column=4, padx=10, pady=10)
texasLabel.grid(row=2, column=4, padx=10, pady=10)
floridaLabel.grid(row=3, column=4, padx=10, pady=10)

# ID and Flavor Tuple
id_name_tuples = [
    ("TS112", "TS124", "Tropical Sunrise"),
    ("IB212", "IB224", "Icy Berry"),
    ("PL312", "PL324", "Pink Lemonade"),
    ("AB412", "AB424", "Aurora Berryalis"),
    ("SS512", "SS524", "Strawberry Slam"),
    ("PP612", "PP624", "Passionfruit Peach"),
    ("WW712", "WW724", "Watermelon Wisdom"),
    ("KC812", "KC824", "Kiwi Clarity"),
    ("PG912", "PG924", "Pineapple Guava"),
    ("BB1012", "BB1024", "Blackberry Blast")
]

# Logic to create dropdown menus for ID and Product Name
id_options = [item for pair in id_name_tuples for item in pair[:2]]
name_options = [pair[2] for pair in id_name_tuples]
selected_id = StringVar()
selected_id.set(id_options[0])
selected_id.trace_add("write", update_selected_id)
selected_name = StringVar()
selected_name.set(name_options[0])

# Dropdown menus and entry fields
id_option_menu = OptionMenu(root, selected_id, *id_options)
name_option_menu = OptionMenu(root, selected_name, *name_options)
entryUtah = Entry(root, width=15, bd=5, font=my_font)
entryTexas = Entry(root, width=15, bd=5, font=my_font)
entryFlorida = Entry(root, width=15, bd=5, font=my_font)

# Position dropdown menus and entry fields
id_option_menu.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
name_option_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
entryUtah.grid(row=1, column=5, columnspan=2, padx=5, pady=5)
entryTexas.grid(row=2, column=5, columnspan=2, padx=5, pady=5)
entryFlorida.grid(row=3, column=5, columnspan=2, padx=5, pady=5)

# Buttons for data manipulation
buttonEnter = Button(root, text="Enter", padx=15, pady=5, width=5, bd=3, font=my_font, bg="#3658E1", fg="#FBFFF1", command=insert_data)
buttonEnter.grid(row=4, column=1, columnspan=1)

buttonUpdate = Button(root, text="Update", padx=15, pady=5, width=5, bd=3, font=my_font, bg="#EE521A", fg="#FBFFF1", command=update_data)
buttonUpdate.grid(row=4, column=4, columnspan=1)

buttonDelete = Button(root, text="Delete", padx=15, pady=5, width=5, bd=3, font=my_font, bg="#E173C7", fg="#FBFFF1", command=delete_data)
buttonDelete.grid(row=4, column=2, columnspan=1)

buttonSortBy = Button(root, text="Sort By", padx=15, pady=5, width=5, bd=3, font=my_font, bg="#14F195", fg="#FBFFF1", command=sort_by)
buttonSortBy.grid(row=4,column=3, columnspan=1)

# Configure Treeview widget
style = ttk.Style()
style.configure("Treeview", font=my_font, rowheight=30 , padding=15, fg="#0A2AAE")

my_tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Pack", "Quantity", "Utah", "Texas", "Florida"), show="headings", height=15)
my_tree.column("ID", anchor=W, width=100)
my_tree.column("Name", anchor=W, width=220)
my_tree.column("Price", anchor=W, width=150)
my_tree.column("Pack", anchor=W, width=100)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Utah", anchor=W, width=100)
my_tree.column("Texas", anchor=W, width=100)
my_tree.column("Florida", anchor=W, width=100)

my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Name", text="Product Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Pack", text="Pack Size", anchor=W)
my_tree.heading("Quantity", text="Total Quantity", anchor=W)
my_tree.heading("Utah", text="Utah Qty", anchor=W)
my_tree.heading("Texas", text="Texas Qty", anchor=W)
my_tree.heading("Florida", text="Florida Qty", anchor=W)

my_tree.tag_configure('orow', font=my_font, foreground="#0A2AAE")
my_tree.tag_configure("utah_red", background="red")
my_tree.tag_configure("texas_red", background="red")
my_tree.tag_configure("florida_red", background="red")
my_tree.grid(row=6, column=0, columnspan=8, padx=15, pady=(15,45))

titleLabel = Label(root, text=storeName, font=('Helvetica', 30, 'bold'), bd=2, bg="#80ECFF")
titleLabel.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

update_tree()

# Run the program
root.mainloop()
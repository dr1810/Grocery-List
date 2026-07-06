from tkinter import *
from item import *
from tkinter import messagebox
import os
#----UI---------------
FONT = ("Arial",16,"italic")
FOREGROUND_COLOR = "#90C422"
BACKGROUND_COLOR = "#FFBF00"
canvas_height, canvas_width = 256,256
items = []
words = ["Let\'s Lock in 😤","Time to create a grocery list"]
value = 0
item_number = 0
#---FUNCTIONALITY-----
def animation(value):
    canvas.itemconfig(text,text=words[value%2])
    window.after(1000,animation,value+1)

def add_to_cart():
    global items
    item_name = item_entry.get()
    quantity = quantity_spin_box.get()
    i_price = item_price.get()
    if len(item_name) == 0 or len(i_price) == 0 or i_price.isnumeric() == False:
        messagebox.askretrycancel(title="Incorrect Information",message="Check how the information is formatted")
    elif quantity == "0":
        messagebox.showerror(title="Incorrect Information",message="Quantity cannot be 0")

    else:
        item_name = item_entry.get()
        quantity = int(quantity_spin_box.get())
        i_price = float(item_price.get())
        new_item = Item(name=item_name,number=quantity,price=i_price)
        items.append(new_item)
        messagebox.showinfo(title="Cart",message="Item has been added to the cart")
        cart_item.config(
            text=f"{item_name}\n"
                f"{quantity}\n"
                f"{i_price}"
        )
        item_entry.delete(0,END)
        quantity_spin_box.delete(0,END)
        item_price.delete(0,END)
        

def edit_cart_item():
    if len(items) == 0:
        messagebox.askokcancel(title="Empty Cart",message="No items to edit")
    else:
        messagebox.showwarning(title="Edit Item",message=f"You are about to edit item {item_number+1}")
        curr_item = items[item_number]
        edit_name.insert(0,curr_item.item_name)
        edit_quantity.insert(0,curr_item.item_number)
        edit_price_entry.insert(0,curr_item.item_price)


def edit_insert():
    curr_item = items[item_number]
    name = edit_name.get()
    q = edit_quantity.get()
    price = edit_price_entry.get()
    if len(name) == 0 or q == 0 or price == 0:
        messagebox.askretrycancel(title="Incorrect Details",message="Enter correct details")
    else:
        messagebox.askyesno(title="Item",message=f"Is this okay?\n{name}\n{int(q)}\n{float(price)}")
        curr_item.item_name = name
        curr_item.item_number = q
        curr_item.item_price = price
        edit_name.delete(0,END)
        edit_quantity.delete(0,END)
        edit_price_entry.delete(0,END)
        messagebox.showinfo(title="Notification",message=f"Item {item_number+1} has been edited")
        cart_item.config(
        text=f"{curr_item.item_name}\n"
             f"{curr_item.item_number}\n"
             f"{curr_item.item_price}"
        )

def delete_item():
    curr_item = items[item_number]
    check = messagebox.askyesno(title="Delete Item",message=f"Are you sure you want to delete item {item_number+1}")
    if check:
        items.remove(curr_item)
        edit_name.delete(0,END)
        edit_quantity.delete(0,END)
        edit_price_entry.delete(0,END)
        messagebox.showinfo(title="Deleted Item",message=f"Item {item_number+1} has been successfully deleted")
        cart_item.config(text=f"Item {item_number+1} has been removed")
    else:
        messagebox.showinfo(title="Continue",message="Continue Editing")


def backward():
    global item_number

    if len(items) == 0:
        messagebox.showinfo(title="Empty Cart", message="Your Cart is Empty")
        return

    item_number -= 1

    if item_number < 0:
        item_number = len(items) - 1

    current_item = items[item_number]

    cart_item.config(
        text=f"{current_item.item_name}\n"
             f"{current_item.item_number}\n"
             f"{current_item.item_price}"
    )

def complete_shopping():
    if len(items) == 0:
        messagebox.showerror(title="Empty Cart",message="Unable to generate the bill")
    try:
        with open("bill.txt","a") as bill:
            final = items
            for i in final:
                name = i.item_name
                i.item_price = float(i.item_price)
                i.item_number = int(i.item_number)
                i.calculate_total_price()
                price = i.item_price
                q = i.item_number
                string = f"{name}|{price}|{q}"
                bill.write(string+'\n')
            bill.close()
        item_entry.delete(0,END)
        quantity_spin_box.delete(0,END)
        item_price.delete(0,END)
        edit_name.delete(0,END)
        edit_quantity.delete(0,END)
        edit_price_entry.delete(0,END)

    except FileExistsError:
        messagebox.showerror(title="Old Bill",message="Old Bill still exists")
    
    messagebox.showinfo(title="Shopping Completion",message="Thank You for shopping")

def delete_bill():
    try:
        check = messagebox.askquestion(title="Old Bill",message="Are you sure you want to delete the old bill?")
        if check:
            os.remove('bill.txt')
            messagebox.showinfo(title="Old Bill",message="Old Bill has been deleted")
        else:
            messagebox.showinfo(title="Old Bill",message="Old Bill has been left undeleted")

    except FileNotFoundError:
        messagebox.showerror(title="Old Bill",message="Old Bill does not exist")

def forward():
    global item_number

    if len(items) == 0:
        messagebox.showinfo(title="Empty Cart", message="Your Cart is Empty")
        return

    item_number += 1

    if item_number >= len(items):
        item_number = 0

    current_item = items[item_number]

    cart_item.config(
        text=f"{current_item.item_name}\n"
             f"{current_item.item_number}\n"
             f"{current_item.item_price}"
    )


#-----MAIN------------
window = Tk()
window.title("Shopping Application")
window.minsize(width=500,height=300)
window.config(padx=100,pady=50)
window.config(background=BACKGROUND_COLOR)

canvas = Canvas(width=canvas_width,height=canvas_height)
grocery = PhotoImage(file='grocery_cart.png')
canvas.create_image(canvas_width//2,canvas_height//2,image = grocery)
text = canvas.create_text(canvas_width//2,(canvas_height//2)-90,text="Placeholder")
canvas.grid(column=1,row=0)
animation(value)

#ITEM NAME ENTRY
item_name = Label(text="Item Name: ",fg=FOREGROUND_COLOR,font=FONT)
item_name.grid(column=0,row=1)
item_entry = Entry(width=20)
item_entry.grid(column=1,row=1)

#ITEM QUANTITY
item_quantity = Label(text="Item Quantity",fg=FOREGROUND_COLOR,font=FONT)
quantity_spin_box = Spinbox(from_=0,to=10)
item_quantity.grid(column=0,row=2)
quantity_spin_box.grid(column=1,row=2)

#ITEM PRICE
price_label = Label(text="Item Price",fg=FOREGROUND_COLOR,font=FONT)
item_price = Entry(width=20)
price_label.grid(column=0,row=3)
item_price.grid(column=1,row=3)

#ADD TO CART BUTTON
add_button = Button(text="Add to Cart",fg=FOREGROUND_COLOR,font=FONT,command=add_to_cart)
add_button.grid(column=1,row=4)

#ITEM LABEL
view_cart = Label(text="View Cart",fg=FOREGROUND_COLOR,font=FONT)
view_cart.grid(column=0,row=5)
cart_item = Label(text="No Items in the cart yet",fg=FOREGROUND_COLOR,font=FONT)
cart_item.grid(column=1,row=6)
decrease_button = Button(text="Back",font=FONT,command=backward)
decrease_button.grid(column=0,row=7)
edit_button = Button(text="Edit/Delete",font=FONT,command=edit_cart_item)
edit_button.grid(column=1,row=7)
increase_button = Button(text="Next",font=FONT,command=forward)
increase_button.grid(column=2,row=7)

#EDIT ITEM
edit_cart = Label(text="Edit Cart Item",fg=FOREGROUND_COLOR,font=FONT)
edit_cart.grid(column=0,row=8)
edit_cart_name = Label(text="Edit Cart Item Name",fg=FOREGROUND_COLOR,font=FONT)
edit_cart.grid(column=0,row=9)
edit_name = Entry(width=20)
edit_name.grid(column=1,row=9)
edit_q_label = Label(text="Edit Cart Quantity",fg=FOREGROUND_COLOR,font=FONT)
edit_q_label.grid(column=0,row=10)
edit_quantity = Spinbox(from_=0,to=10)
edit_quantity.grid(column=1,row=10)
edit_price_label = Label(text="Edit Item Price",fg=FOREGROUND_COLOR,font=FONT)
edit_price_label.grid(column=0,row=11)
edit_price_entry = Entry(width=20)
edit_price_entry.grid(column=1,row=11)
final_insert_button = Button(text="Finish",font=FONT,fg=FOREGROUND_COLOR,command=edit_insert)
final_insert_button.grid(column=1,row=12)
delete_button = Button(text="Delete",font=FONT,fg=FOREGROUND_COLOR,command=delete_item)
delete_button.grid(column=2,row=12)

#BILL GENERATION AND DELETION
bill_creation = Button(text="Complete Shopping",font=FONT,fg=FOREGROUND_COLOR,command=complete_shopping)
bill_creation.grid(column=1,row=13)
bill_deletion = Button(text="Delete Old Bill",font=FONT,fg=FOREGROUND_COLOR,command=delete_bill)
bill_deletion.grid(column=1,row=14)
window.mainloop()
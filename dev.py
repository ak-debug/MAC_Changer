from tkinter import *
from threading import Thread
import subprocess
import re
import random

root=Tk()
root.title("MAC Changer")

original_mac=""
interface=""

# Labels
inf_label = Label(root, text="Interface")
mac_add_label = Label(root, text="MAC Address")
inf_label.grid(row=0, column=0, padx=10, pady=10)
mac_add_label.grid(row=1, column=0, padx=10, pady=10)

# Entries
inf = Entry(root,width=20,borderwidth=5)
mac_add=Entry(root,width=20,borderwidth=5)
inf.grid(row=0,column=1,padx=10,pady=10)
mac_add.grid(row=1,column=1,padx=10,pady=10)

# Adding textbox to display results
result_label = Label(root, text="Result")
result_label.grid(row=5, column=0, padx=10, pady=10)
result_box = Text(root, height=10, width=30)
result_box.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Adding scrollbar
scrollbar = Scrollbar(root)
scrollbar.grid(row=6, column=2, sticky="ns")
result_box.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=result_box.yview)

# Adding status bar
status = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
status.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Functions used
def get_current_mac(interface):
    try:
        output = subprocess.check_output(["ifconfig",interface])
        return re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(output)).group(0)
    except Exception as e:
        status.config(text="Error: " + str(e), fg="red")
        return None

def change_mac(interface,mac):
    if mac is None:
        mac = mac_add.get()
    
    if not re.match("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac):
        status.config(text="Error: Invalid MAC address", fg="red")
        return

    status.config(text="Changing MAC of "+interface+ " to "+mac)
    root.update()
    
    try:
        subprocess.run(["sudo", "ifconfig", interface,"down"])
        subprocess.run(["sudo", "ifconfig", interface,"hw", "ether", mac])
        subprocess.run(["sudo", "ifconfig", interface,"up"])
        status.config(text="MAC address changed successfully", fg="green")
        result_box.insert(END, "MAC address changed successfully for " + interface + " to " + mac + "\n")
        current_mac = get_current_mac(interface)
        result_box.insert(END, "Current MAC: " + str(current_mac) + "\n")
    except Exception as e:
        status.config(text="Error: " + str(e), fg="red")
        result_box.insert(END, "Error: " + str(e) + "\n")
        
def random_mac():
    random_mac = ":".join(["{:02x}".format(random.randint(0, 255)) for i in range(6)])
    return random_mac

def change():
    global original_mac
    global interface
    interface=inf.get()
    original_mac=get_current_mac(interface)
    if original_mac is None:
        status.config(text="Error: Could not fetch original MAC", fg="red")
        return
    result_box.insert(END, "Original MAC: " + str(original_mac) + "\n")
    new_mac=mac_add.get()
    if new_mac == "":
        new_mac=random_mac()
        result_box.insert(END, "Generated MAC: " + new_mac + "\n")
    t = Thread(target=change_mac, args=(interface,new_mac,))
    t.start()

def restore():
    global original_mac
    global interface
    if original_mac is None:
        status.config(text="Error: Could not fetch original MAC", fg="red")
        return
    status.config(text="Restoring original MAC of "+interface)
    root.update()
    try:
        subprocess.run(["sudo", "ifconfig", interface,"down"])
        subprocess.run(["sudo", "ifconfig", interface,"hw", "ether", original_mac])
        subprocess.run(["sudo", "ifconfig", interface,"up"])
        status.config(text="Original MAC restored successfully", fg="green")
        result_box.insert(END, "Original MAC restored successfully for " + interface + "\n")
        current_mac = get_current_mac(interface)
        result_box.insert(END, "Current MAC: " + str(current_mac) + "\n")
    except Exception as e:
        status.config(text="Error: " + str(e), fg="red")
        result_box.insert(END, "Error: " + str(e) + "\n")

# Buttons
change_button = Button(root, text="Change", command=change)
change_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
restore_button = Button(root, text="Restore", command=restore)
restore_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

root.mainloop()

from tkinter import *
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

# Functions used
def get_current_mac(interface):
    output = subprocess.check_output(["ifconfig",interface])
    return re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(output)).group(0)

def change_mac(interface,mac):
    if mac==NONE:
        mac=mac_add.get()
    print("[+] Changing MAC of "+interface+ " to "+mac)
    subprocess.run(["sudo", "ifconfig", interface,"down"])
    subprocess.run(["sudo", "ifconfig", interface,"hw", "ether", mac])
    subprocess.run(["sudo", "ifconfig", interface,"up"])

def get_random_mac_address():
    characters = "0123456789abcdef"
    random_mac_address = "00"
    for i in range(5):
        random_mac_address += ":" + \
                        random.choice(characters) \
                        + random.choice(characters)
    return random_mac_address

def click_random(interface):
    mac=get_random_mac_address()
    change_mac(interface,mac)

def click_save():
    global original_mac
    global interface
    original_mac=get_current_mac(inf.get())
    interface=inf.get()

#Defining buttons
button_save=Button(root,text="Save",command=click_save)
button_save.grid(row=2,column=0)

button_mac=Button(root,text="Change Mac",command=lambda: change_mac(interface,NONE))
button_mac.grid(row=2,column=1)

button_reset=Button(root,text="Reset MAC",command=lambda: change_mac(interface,original_mac))
button_reset.grid(row=3,column=0)

button_random=Button(root,text="Random MAC",command=lambda: click_random(interface))
button_random.grid(row=3,column=1)

# Adding textbox to display results
result_label = Label(root, text="Result")

root.mainloop()

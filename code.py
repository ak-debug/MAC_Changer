from tkinter import *
from threading import Thread
import subprocess
import re
import random
import netifaces
import time

# Constants
PADX = 10
PADY = 10
ENTRY_WIDTH = 20
ENTRY_BORDERWIDTH = 5
MAC_PATTERN = "\w\w:\w\w:\w\w:\w\w:\w\w:\w\w"

class MacChanger:
    def __init__(self):
        self.root = Tk()
        self.root.title("MAC Changer")
        self.original_mac = ""
        self.interface = ""
        self.auto_change = False
        self.interval = 0
        self.app_running = True 
        self.initialize_gui()

    def initialize_gui(self):
        self.inf_label, self.mac_add_label, self.current_mac_label = self.initialize_labels()
        self.inf, self.mac_add, self.current_mac_entry = self.initialize_entries()
        self.result_label, self.result_box, self.scrollbar = self.initialize_result_box()
        self.status = self.initialize_status_bar()
        self.interface_var.trace("w", self.update_interface)
        self.change_button, self.restore_button, self.random_button = self.initialize_buttons()
        self.menubar = self.initialize_menu_bar()
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def initialize_labels(self):
        inf_label = Label(self.root, text="Interface")
        mac_add_label = Label(self.root, text="MAC Address")
        current_mac_label = Label(self.root, text="Current MAC Address")
        inf_label.grid(row=0, column=0, padx=PADX, pady=PADY)
        mac_add_label.grid(row=1, column=0, padx=PADX, pady=PADY)
        current_mac_label.grid(row=2, column=0, padx=PADX, pady=PADY)
        return inf_label, mac_add_label, current_mac_label

    def initialize_entries(self):
        interfaces = netifaces.interfaces()
        self.interface_var = StringVar(self.root)
        self.interface_var.set(interfaces[0])
        inf = OptionMenu(self.root, self.interface_var, *interfaces)
        mac_add=Entry(self.root, width=ENTRY_WIDTH, borderwidth=ENTRY_BORDERWIDTH)
        self.current_mac_text = StringVar(self.root, value="")
        current_mac_entry = Entry(self.root, textvariable=self.current_mac_text, state='readonly')
        inf.grid(row=0,column=1,padx=PADX,pady=PADY)
        mac_add.grid(row=1,column=1,padx=PADX,pady=PADY)
        current_mac_entry.grid(row=2,column=1,padx=PADX,pady=PADY)
        return inf, mac_add, current_mac_entry

    def initialize_result_box(self):
        result_label = Label(self.root, text="Result")
        result_label.grid(row=4, column=0, padx=PADX, pady=PADY)
        result_box = Text(self.root, height=10, width=30)
        result_box.grid(row=5, column=0, columnspan=2, padx=PADX, pady=PADY)
        scrollbar = Scrollbar(self.root)
        scrollbar.grid(row=5, column=2, sticky="ns")
        result_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=result_box.yview)
        return result_label, result_box, scrollbar

    def initialize_status_bar(self):
        status = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W)
        status.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        return status

    def initialize_buttons(self):
        change_button = Button(self.root, text="Change", command=self.change, state=NORMAL)
        change_button.grid(row=3, column=0, padx=PADX, pady=PADY)  # placed at column 0
        restore_button = Button(self.root, text="Restore", command=self.restore)
        restore_button.grid(row=3, column=1, padx=PADX, pady=PADY)  # placed at column 1
        random_button = Button(self.root, text="Random MAC", command=self.random_change, state=DISABLED)
        random_button.grid(row=4, column=0, padx=PADX, pady=PADY, columnspan=2)  # moved to row 4
        return change_button, restore_button, random_button



    def initialize_menu_bar(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Settings", command=self.show_settings)
        menubar.add_cascade(label="File", menu=filemenu)
        return menubar

    # Move to here from the previous location
    def update_interface(self, *args):
        self.interface = self.interface_var.get()

    # Group the functions that are dealing with settings
    def show_settings(self):
        settings_window = Toplevel(self.root)
        settings_window.title("Settings")
        self.auto_change_var = BooleanVar()
        auto_change_check = Checkbutton(settings_window, text="Enable automatic MAC changes", variable=self.auto_change_var)
        auto_change_check.grid(row=0, column=0, padx=PADX, pady=PADY)
        interval_label = Label(settings_window, text="Change Interval (s)")
        interval_label.grid(row=1, column=0, padx=PADX, pady=PADY)
        self.interval_entry = Entry(settings_window,width=ENTRY_WIDTH, borderwidth=ENTRY_BORDERWIDTH)
        self.interval_entry.grid(row=1, column=1, padx=PADX, pady=PADY)
        save_button = Button(settings_window, text="Save", command=self.save_settings)
        save_button.grid(row=2, column=0, padx=PADX, pady=PADY, columnspan=2)

    def save_settings(self):
        old_auto_change = self.auto_change
        self.auto_change = self.auto_change_var.get()
        self.interval = self.interval_entry.get()
        if self.interval.isdigit():
            self.interval = int(self.interval)
        else:
            self.interval = 0
        if old_auto_change and not self.auto_change:
            self.auto_change = False
        self.change_button.config(state=DISABLED if self.auto_change else NORMAL)
        self.random_button.config(state=NORMAL if self.auto_change else DISABLED)
        self.status.config(text="Settings saved. Automatic change: "+str(self.auto_change)+". Interval: "+str(self.interval), fg="green")

    def get_current_mac(self, interface):
        try:
            output = subprocess.check_output(["ifconfig", interface])
            current_mac = re.search(MAC_PATTERN, str(output)).group(0)
            self.current_mac_text.set(current_mac)
            return current_mac
        except Exception as e:
            self.status.config(text="Error: " + str(e), fg="red")
            return None

    # Group the functions that are dealing with MAC address change
    def change_mac(self, interface, mac):
        if mac is None:
            mac = self.mac_add.get()
        if not re.match(MAC_PATTERN, mac):
            self.status.config(text="Error: Invalid MAC address", fg="red")
            return
        self.status.config(text="Changing MAC of "+interface+ " to "+mac)
        self.root.update()
        try:
            subprocess.run(["sudo", "ifconfig", interface,"down"])
            subprocess.run(["sudo", "ifconfig", interface,"hw", "ether", mac])
            subprocess.run(["sudo", "ifconfig", interface,"up"])
            self.status.config(text="MAC address changed successfully", fg="green")
            self.result_box.insert(END, "MAC address changed successfully for " + interface + " to " + mac + "\n")
            current_mac = self.get_current_mac(interface)
            self.result_box.insert(END, "Current MAC: " + str(current_mac) + "\n")
        except Exception as e:
            self.status.config(text="Error: " + str(e), fg="red")
            self.result_box.insert(END, "Error: " + str(e) + "\n")

    def random_mac(self):
        return ":".join(["{:02x}".format(random.randint(0, 255)) for i in range(6)])

    def random_change(self):
        random_mac = self.random_mac()
        self.root.after(1, self.change_mac, self.interface, random_mac)

    def auto_change_mac(self):
        while self.auto_change and self.app_running:
            if self.interval > 0:
                self.root.after(self.interval * 1000, self.random_change)
            time.sleep(1)

    # Group the functions that are triggered by the buttons
    def change(self):
        self.original_mac = self.get_current_mac(self.interface)
        if self.original_mac is None:
            self.status.config(text="Error: Could not fetch original MAC", fg="red")
            return
        self.result_box.insert(END, "Original MAC: " + str(self.original_mac) + "\n")
        new_mac = self.mac_add.get()
        if new_mac == "":
            new_mac = self.random_mac()
            self.result_box.insert(END, "Generated MAC: " + new_mac + "\n")
        self.root.after(1, self.change_mac, self.interface, new_mac)
        self.interval = self.interval_entry.get()
        if self.interval.isdigit() and int(self.interval) > 0:
            self.interval = int(self.interval)
            self.auto_change = True
            self.root.after(self.interval * 1000, self.auto_change_mac)

    def restore(self):
        self.auto_change = False
        if self.original_mac is None:
            self.status.config(text="Error: Could not fetch original MAC", fg="red")
            return
        self.status.config(text="Restoring original MAC of "+self.interface)
        self.root.update()
        try:
            subprocess.run(["sudo", "ifconfig", self.interface,"down"])
            subprocess.run(["sudo", "ifconfig", self.interface,"hw", "ether", self.original_mac])
            subprocess.run(["sudo", "ifconfig", self.interface,"up"])
            self.status.config(text="Original MAC restored successfully", fg="green")
            self.result_box.insert(END, "Original MAC restored successfully for " + self.interface + "\n")
            current_mac = self.get_current_mac(self.interface)
            self.result_box.insert(END, "Current MAC: " + str(current_mac) + "\n")
        except Exception as e:
            self.status.config(text="Error: " + str(e), fg="red")
            self.result_box.insert(END, "Error: " + str(e) + "\n")

    # Cleaning up when the application is closed
    def on_closing(self):
        self.app_running = False
        self.root.destroy()

# Create an instance of the MacChanger class to run the application
mac_changer = MacChanger()
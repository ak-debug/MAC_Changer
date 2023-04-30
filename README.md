# MAC_Changer

## **User Guide**

The MAC changer is a GUI application built using Python and Tkinter library. It allows you to change the MAC address of a network interface on your computer.

### **Running the Application**

To run the MAC changer, you need to have Python installed on your computer.

1. Open a terminal window or command prompt.
2. Navigate to the directory where the code is saved.
3. Run the following command:

```
sudo python3 code.py

```

where **`<filename>`** is the name of the file you saved the code in.

### **Using the Application**

The MAC changer has a simple and intuitive interface.

1. In the **`Interface`** field, enter the name of the network interface you want to change the MAC address for.
2. In the **`MAC Address`** field, enter the new MAC address you want to set for the network interface. If you leave this field blank, the application will generate a random MAC address for you.
3. Click the **`Change`** button to change the MAC address. The result of the operation will be displayed in the text box below.
4. If you want to restore the original MAC address, click the **`Restore`** button.

### **Requirements**

To run the MAC changer, you need to have the following installed:

- Python 3
- Tkinter library

### **Limitations**

This application is designed to work on Unix-based systems. It may not work on other operating systems. Additionally, changing the MAC address of a network interface may have legal implications and may not be allowed in some countries.
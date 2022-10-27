import subprocess
import argparse
import random
import re
from time import sleep

#function used to change mac address
def change_mac(interface,mac):
    print("[+] Changing MAC of "+interface+ " to "+mac)
    subprocess.run(["sudo", "ifconfig", interface,"down"])
    subprocess.run(["sudo", "ifconfig", interface,"hw", "ether", mac])
    subprocess.run(["sudo", "ifconfig", interface,"up"])


# used for command line arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",help="Specify the interface",required=True)
    parser.add_argument("-m","--mac",dest="mac_addr",help="Specify the interface")
    args = parser.parse_args() #args variable stores the passed interface value 
    # if not args.interface:
    #     parser.error("Please Specify interface")
    return args

#used to store original mac in case reset needed
def get_current_mac(interface):
    output = subprocess.check_output(["ifconfig",interface])
    return re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(output)).group(0)

def get_random_mac_address():
    characters = "0123456789abcdef"
    random_mac_address = "00"
    for i in range(5):
        random_mac_address += ":" + \
                        random.choice(characters) \
                        + random.choice(characters)
    return random_mac_address

if __name__ == "__main__":
    
    args= get_arguments()
    interface=args.interface
    
    #saving original mac
    original_mac=get_current_mac(interface)
    # if mac was passed during runtime we use it else i have  provided 4 options for the user
    if args.mac_addr:
        mac=args.mac_addr
    else:
        print("Select one of the options\n[1] Generate a Random MAC Address")
        print("[2] Specify a unicast MAC Address")
        print("[3] Export Current MAC Address")
        print("[4] Random MAC after a fixed time interval")
        x= input()
        if x=="1":
            mac =get_random_mac_address()
        elif x=="2":
            mac=input("Enter MAC Address : ")
        elif x=="3": #this is for exporting current mac
            mac=get_current_mac(interface)
            with open('exported_mac.txt','w') as f:
                f.write(mac)
                f.write('\n')
            print("MAC Address Exported Now Exiting ...")
            exit(0)
        else:
            
            for i in range(1,5):
                mac = get_random_mac_address()
                print("Changing MAC iteration number - "+ str(i))
                change_mac(interface,mac)
                # subprocess.run("ifconfig")
                sleep(5)
            print("All iterations done resetting now")
            change_mac(interface,original_mac)
            exit(0)
                
   #Follwing Code is to test options 1 and 2
    change_mac(interface,mac)

    print("After Random")
    subprocess.run("ifconfig")
    print("Resetting------------------")
    change_mac(interface,original_mac)

    subprocess.run("ifconfig")

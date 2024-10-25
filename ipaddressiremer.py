# Import the tkinter library
from tkinter import *
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Create an instance of tkinter frame
root = Tk()

# Size of the window
root.geometry("1024x600")
root.title("iREMER Remote Control")

# hostname of the socket
hostname = socket.gethostname()

# IP address of the hostname
ip_address = get_ip()

label1 = Label(root, text="iREMER Host Name is:", font = "Calibri, 20")
label1.pack(pady=30)

label2 = Label(root, text=hostname, font = "Calibri, 50")
label2.pack(pady=30)

label3 = Label(root, text="iREMER IP Address is:", font = "Calibri, 20")
label3.pack(pady=30)

label4 = Label(root, text=ip_address, font = "Calibri, 50")
label4.pack(pady=30)

root.mainloop()
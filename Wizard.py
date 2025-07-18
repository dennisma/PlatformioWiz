from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog
import requests
import zipfile
import os

# This script is a simple GUI application that allows the user to download a ZIP file from a given URL,
# extract its contents, and open the extracted folder in Visual Studio Code.
# It uses the tkinter library for the GUI, requests for HTTP requests, and zipfile for handling ZIP files.
# The script also includes a placeholder for generating and saving QR codes, but this functionality is not implemented.
# The script is designed to be run as a standalone application.
# The script starts by importing the necessary libraries and defining a function to fetch the ZIP file.
# It then creates a tkinter window with an image, a label, an entry field for the URL, and a button to run the wizard.

# The fetch_zip_file function is called when the button is clicked, and it handles the downloading and extraction of the ZIP file.
# The script also includes a placeholder for generating and saving QR codes, but this functionality is not implemented.
def fetch_zip_file():
    # Try to get the ZIP file
    global url
    
    global window
    #window.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Select a Folder", initialdir=".", parent=window)

    if folder_path:
        os.chdir(folder_path)
        print("Selected folder:", folder_path)
    else:
        print("No folder selected.")
    
    try:
        response = requests.get(url)
    except OSError:
        print('No connection to the server!')
        return None

    # check if the request is succesful
    if response.status_code == 200:
        # Save dataset to file
        filename =  "srbots_client.zip"
        print('Status 200, OK')
        
        try:
            open(filename, 'wb').write(response.content)
            
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall()
            
            last_directory = os.path.basename(folder_path)
            os.rename("srbots_client-main", last_directory)

            os.remove(filename)    
            os.chdir(last_directory)
            os.system("code .")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    else:
        print('ZIP file request not successful!.')
        return None


def genQR(url,asset):
    pass
    
def genNewQR():
    pass
def saveQR():
    pass

window = tk.Tk()

try:
    image = Image.open("assets/platwiz.jpg") # Replace with the actual path to your image file
    tk_image = ImageTk.PhotoImage(image)
except FileNotFoundError:
    pass
    #print("Error: Image file not found.")
    #exit()

url  = 'https://github.com/dennisma/srbots_client/archive/refs/heads/main.zip'
asset = "assets/platwiz.jpg"
window.title("Project Wizard")
window.geometry("700x700")

image_label = tk.Label(window, image=tk_image)
image_label.pack()

# Keep a reference to the image to prevent garbage collection
image_label.image = tk_image

top_frame = tk.Frame( master=window,    relief=tk.RAISED,    borderwidth=3    )   
label_url = tk.Label(master=top_frame, text="Enter Project URL")
entry_url = tk.Entry(master=top_frame,width=100)
entry_url.insert(0,url)

#label_asset = tk.Label(master=top_frame, text="Folder Directory")
#entry_asset = tk.Entry(master=top_frame,width=100)
#entry_asset.insert(0,asset)

button_url = tk.Button(master=top_frame, text="Run Wizard", command=fetch_zip_file )

label_url.pack()
entry_url.pack()

#label_asset.pack()
#entry_asset.pack()
button_url.pack()

top_frame.pack()

window.mainloop()
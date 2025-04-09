# main code

from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
import cv2
import pytesseract
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

root = Tk()
root.title('Text Extraction & Translation')
root.geometry("1200x1000")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=NW)


translator = Translator()
newline = Label(frame)
uploaded_img = Label(frame)
extracted_text = StringVar()
translated_text = StringVar()

# main function to extract text
def extract(path):
    Actual_image = cv2.imread(path)
    gray = cv2.cvtColor(Actual_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    texts = pytesseract.image_to_string(thresh)
    extracted_text.set(texts)

import asyncio 

# to translate text from google trans
def translate_text():
    lang = language_var.get()
    if extracted_text.get():
        translated = translator.translate(extracted_text.get(), dest=lang)
        translated_text.set(asyncio.run(translated).text)  


#   show and build extract button
def show_extract_button(path):
    extractBtn = Button(frame, text="Extract text", command=lambda: extract(path), bg="#4CAF50", fg="white", pady=10, padx=10, font=('Times', 12, 'bold'))
    extractBtn.pack()

# Function to upload image
def upload():
    try:
        path = filedialog.askopenfilename()
        image = Image.open(path)
        # image = image.resize((400, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        uploaded_img.configure(image=img)
        uploaded_img.image = img
        show_extract_button(path)
    except:
        pass  


#main gui
# upload button
uploadbtn = Button(frame, text="Upload an image", command=upload, bg="#2f2f77", fg="white", height=2, width=20, font=('Times', 12, 'bold'))
uploadbtn.pack()
newline.pack()
uploaded_img.pack()

Label(frame, text="Extracted Text:").pack()
text_display = Label(frame, textvariable=extracted_text, wraplength=700, bg="lightgray", font=('Arial', 12))
text_display.pack()


# which lang to choose drop down
Label(frame, text="Translate To:").pack()
language_var = StringVar(value='en')
language_menu = ttk.Combobox(frame, textvariable=language_var, values=["en", "es", "fr", "de", "hi", "zh-cn"])
language_menu.pack()


# translate button
translateBtn = Button(frame, text="Translate", command=translate_text, bg="#4CAF50", fg="white", pady=10, padx=10, font=('Times', 12, 'bold'))
translateBtn.pack()

Label(frame, text="Translated Text:").pack()
translated_display = Label(frame, textvariable=translated_text, wraplength=700, bg="lightgray", font=('Arial', 12))
translated_display.pack()

root.mainloop()
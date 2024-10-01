from openai import OpenAI
import pdfplumber
from tkinter.filedialog import *
from tkinter import *
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ.get("SECRET_KEY")

window = Tk()
window.withdraw()

file_path = askopenfile(title="Select PDF file", filetypes=[("PDF files", ".pdf")], mode="rb").name
text = ""

pdf = pdfplumber.open(file_path)

for page in pdf.pages:
    text += page.extract_text()

client = OpenAI(api_key=key)

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input=text,
) as response:
    response.stream_to_file("speech.mp3")

file_name = asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 File", '.mp3')])
with open("output.mp3", "rb") as src:
    data = src.read()
with open(file_name, "wb") as file:
    file.write(data)


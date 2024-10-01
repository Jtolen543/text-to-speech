from openai import OpenAI, RateLimitError
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
try:
    for page in pdf.pages:
        text += page.extract_text()

    client = OpenAI(api_key=key)

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file("output.mp3")

    file_name = asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 File", '.mp3')])
    with open("output.mp3", "rb") as src:
        data = src.read()
    with open(file_name, "wb") as file:
        pass
        file.write(data)
    print("You PDF file has been successfully converted into a text-to-speech prompt")
except AttributeError:
    print("Please select a file to use the TTS converter")
except RateLimitError:
    print("Please add credits to your account to use the converter")
except FileNotFoundError:
    print("Please enter a name to save the MP3 file")

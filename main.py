# Import required modules
from tkinter import Tk, Label, StringVar, OptionMenu, Button, filedialog, messagebox
from gtts import gTTS
import pdfplumber
from PyPDF2 import PdfReader


class PDFToAudioConverter():
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to MP3 Converter")
        self.root.config(bg="light yellow")
        self.root.resizable(True, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        window_width = 250
        window_height = 100

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

        self.manual_lbl = Label(root, bg="light yellow",
                                text="This app converts text to speech by getting text from a PDF file and converts it into an MP3 file.",
                                anchor="w", justify="left")
        self.manual_lbl.grid(column=0, row=0)

        self.prompt_lbl = Label(root, bg="light yellow",text="Please select a PDF file:")
        self.prompt_lbl.grid(column=0, row=1, sticky="w")

        self.language_lbl = Label(root, bg="light yellow", text="Select Language:")
        self.language_lbl.grid(column=0, row=3, sticky="w")

        self.selected_language = StringVar()
        language_options = ["en", "es", "fr"]
        self.language_menu = OptionMenu(root, self.selected_language, *language_options)
        self.language_menu.grid(column=1, row=3)
        self.selected_language.set("en")

        self.select_btn = Button(root, text="Select File", command=self.select_pdf_file)
        self.select_btn.grid(column=0, row=2, sticky="w")

        self.convert_btn = Button(root, text="Convert to MP3", command=self.convert_to_mp3, state="disabled")
        self.convert_btn.grid(column=1, row=2)

        self.pdf_file_path = ""

    def select_pdf_file(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file_path:
            self.convert_btn.config(state="normal", bg="light green")

    def get_text_from_pdf(self):
        if not self.pdf_file_path:
            return

        text = ""

        with open(self.pdf_file_path, "rb") as pdf:
            pdf_reader = PdfReader(pdf)
        
            for page in pdf_reader.pages:
                content = page.extract_text()
                text += content
        
        return text


    def get_audio_from_text(self, text, language):
        text_to_speech = gTTS(text=text, lang=language, slow=False)

        mp3_file_path = filedialog.asksaveasfilename(defaultextension="mp3", filetypes=[("MP3 Files", "*.mp3")])
        if mp3_file_path:
            text_to_speech.save(mp3_file_path)
            messagebox.showinfo("Info", "Text file converted to audio successfully!")
        else:
            messagebox.showerror("Error", "Could not convert text to MP3 file!")

    def convert_to_mp3(self):
        text = self.get_text_from_pdf()
        selected_language = self.selected_language.get()
        self.get_audio_from_text(text, selected_language)


if __name__ == "__main__":
    root = Tk()
    app = PDFToAudioConverter(root)
    root.mainloop()
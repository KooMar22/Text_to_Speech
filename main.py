# Import required modules
from tkinter import Tk, Label, Entry, StringVar, OptionMenu, Button, filedialog, END
from gtts import gTTS
from pypdf import PdfReader


class PDFToAudioConverter():
    def __init__(self, root):
        """Initiate the GUI"""
        self.root = root
        self.root.title("Markanov Text to Audio Converter")
        self.root.config(bg="light yellow")
        self.root.resizable(True, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Make it appear on the center of the screen
        window_width = 370
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

        # Add some labels
        self.manual_lbl = Label(root, bg="light yellow",
                                text="This app converts text to speech by getting text from a PDF file\nand converts it into an MP3 file.\nIt can only read text from proper PDF files,\ntext within images (OCR-ing) is not yet supported.",
                                anchor="w", justify="left")
        self.manual_lbl.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.prompt_lbl = Label(root, bg="light yellow",text="Please select a PDF file:")
        self.prompt_lbl.grid(column=0, row=1, sticky="w")

        self.language_lbl = Label(root, bg="light yellow", text="Select Language:")
        self.language_lbl.grid(column=0, row=4, sticky="w")

        self.status_lbl = Label(root, bg="light yellow", text="", anchor="w", justify="left")
        self.status_lbl.grid(column=0, row=5, columnspan=2, pady=5)

        # Entry that displays the selected file
        self.selected_file = Entry(root, state="readonly", width=300)
        self.selected_file.grid(column=0, row=3, pady=5)
        self.selected_file.insert(0, "No file selected")

        # Option to choose between available languages
        self.selected_language = StringVar()
        language_options = ["en", "es", "fr", "bs", "de", "hr", "iw"]
        self.language_menu = OptionMenu(root, self.selected_language, *language_options)
        self.language_menu.grid(column=1, row=4)
        self.selected_language.set("en")

        # Add some buttons
        self.select_btn = Button(root, text="Select File", command=self.select_pdf_file)
        self.select_btn.grid(column=0, row=2, sticky="w")

        self.convert_btn = Button(root, text="Convert to MP3",
                                  command=self.convert_to_mp3, state="disabled")
        self.convert_btn.grid(column=1, row=2)

        self.pdf_file_path = ""


    def select_pdf_file(self):
        """Selects the PDF file."""
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file_path:
            self.selected_file.config(state="normal")
            self.selected_file.delete(0, END)
            self.selected_file.insert(0, self.pdf_file_path)
            self.selected_file.config(state="readonly")
            self.convert_btn.config(state="normal", bg="light green")
        else:
            self.selected_file.config(state="readonly")
            self.selected_file.delete(0, END)
            self.selected_file.insert(0, "No file selected")
            self.convert_btn.config(state="disabled")

    def get_text_from_pdf(self):
        """Get the text from chosen PDF file. Only proper PDF files are supported,
        no OCR-ing from images."""
        if not self.pdf_file_path:
            return

        text = ""

        with open(self.pdf_file_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                content = page.extract_text()
                text += content
        
        return text

    def get_audio_from_text(self, text, language):
        """Get the audio from text using Google Text to Speech technology."""
        text_to_speech = gTTS(text=text, lang=language, slow=False)

        mp3_file_path = filedialog.asksaveasfilename(defaultextension="mp3",
                                                     filetypes=[("MP3 Files", "*.mp3")])
        if mp3_file_path:
            text_to_speech.save(mp3_file_path)

    def convert_to_mp3(self):
        """Convert the text to mp3 audio file."""
        text = self.get_text_from_pdf()
        if text is not None:
            selected_language = self.selected_language.get()
            self.status_lbl.config(text="Converting PDF to MP3 file...", bg="light yellow")
            self.root.update()

            try:
                self.get_audio_from_text(text, selected_language)
                self.status_lbl.config(text="Text converted to audio file successfully!",
                                       bg="light green")
            except Exception as e:
                self.status_lbl.config(text=f"Error: {e}", bg="red")
        
        else:
            self.status_lbl.config(text="Error: Could not read text from PDF file.",
                                   bg="red")


if __name__ == "__main__":
    root = Tk()
    app = PDFToAudioConverter(root)
    root.mainloop()
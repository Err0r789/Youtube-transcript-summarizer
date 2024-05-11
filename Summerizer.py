from transformers import BartTokenizer, pipeline
import tkinter as tk
from tkinter import scrolledtext, messagebox,font
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator, LANGUAGES
import re  

print("Starting model download...")
tokenizer = BartTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6')
summarizer_pipeline = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6', tokenizer=tokenizer, framework='pt')
print("Model downloaded successfully.")

def get_video_id(url):
    """ Extracts video ID from YouTube URL using regex to handle various formats. """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def split_text_into_chunks(text, max_length):
    words = text.split()
    safe_words = []
    for word in words:
        while len(word) > max_length:
            part = word[:max_length]
            safe_words.append(part)
            word = word[max_length:]
        safe_words.append(word)
    safe_text = ' '.join(safe_words)
    tokens = tokenizer.encode(safe_text, add_special_tokens=True)
    chunks = []
    current_chunk = []
    current_length = 0
    for token in tokens:
        if current_length + len(tokenizer.decode([token], skip_special_tokens=True)) <= max_length:
            current_chunk.append(token)
            current_length += len(tokenizer.decode([token], skip_special_tokens=True))
        else:
            chunks.append(current_chunk)
            current_chunk = [token]
            current_length = len(tokenizer.decode([token], skip_special_tokens=True))
    if current_chunk:
        chunks.append(current_chunk)
    return [tokenizer.decode(chunk, skip_special_tokens=True, clean_up_tokenization_spaces=True) for chunk in chunks]

def summarize_text(text):
    chunks = split_text_into_chunks(text, 1024 - 2)
    summaries = []
    for chunk in chunks:
        if len(tokenizer.encode(chunk)) <= 1024:
            output = summarizer_pipeline(chunk)
            if output:
                summaries.append(output[0]['summary_text'])
        else:
            print("Chunk too large; skipping summarization for this chunk.")
    return " ".join(summaries)

def get_and_summarize():
    youtube_video = video_entry.get()
    video_id = get_video_id(youtube_video)
    if not video_id:
        messagebox.showerror("Error", "Invalid YouTube URL or Video ID not found.")
        return
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        result = " ".join([item['text'] for item in transcript])
        summarized_text = summarize_text(result)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, summarized_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def translate_text():
    text = text_box.get(1.0, tk.END)
    if validate_language_code(language_entry.get()):
        translator = Translator()
        try:
            translated_text = translator.translate(text, dest=language_entry.get()).text
            translated_text_box.delete(1.0, tk.END)
            translated_text_box.insert(tk.END, translated_text)
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {str(e)}")
    else:
        messagebox.showerror("Error", "Invalid language code")

def validate_language_code(code):
    return code.lower() in LANGUAGES

root = tk.Tk()
root.title("YouTube Summarizer and Translator")
root.geometry("800x600")  

app_font = font.Font(size=12, family="Helvetica") 

main_frame = tk.Frame(root, bd=2, padx=5, pady=5)
main_frame.pack(fill=tk.BOTH, expand=True)

padx, pady = 10, 5

video_label = tk.Label(main_frame, text="YouTube Video Link:", font=app_font)
video_label.grid(row=0, column=0, sticky='w', padx=padx, pady=pady)

video_entry = tk.Entry(main_frame, width=50, font=app_font)
video_entry.grid(row=0, column=1, sticky='ew', padx=padx, pady=pady)

summarize_button = tk.Button(main_frame, text="Summarize", command=get_and_summarize, font=app_font)
summarize_button.grid(row=1, column=1, sticky='ew', padx=padx, pady=pady)

text_box = scrolledtext.ScrolledText(main_frame, height=10, font=app_font)
text_box.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=padx, pady=pady)

language_label = tk.Label(main_frame, text="Translate to (ISO code, e.g., hi for Hindi):", font=app_font)
language_label.grid(row=3, column=0, sticky='w', padx=padx, pady=pady)

language_entry = tk.Entry(main_frame, width=10, font=app_font)
language_entry.grid(row=3, column=1, sticky='ew', padx=padx, pady=pady)

translate_button = tk.Button(main_frame, text="Translate", command=translate_text, font=app_font)
translate_button.grid(row=4, column=1, sticky='ew', padx=padx, pady=pady)


translated_text_box = scrolledtext.ScrolledText(main_frame, height=10, font=app_font)
translated_text_box.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=padx, pady=pady)

main_frame.grid_columnconfigure(1, weight=1)  
main_frame.grid_rowconfigure(2, weight=1)     
main_frame.grid_rowconfigure(5, weight=1)     

root.mainloop()
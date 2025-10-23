import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pdfplumber
from transformers import pipeline
import threading

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def chunk_text(text, max_tokens=1000):
    """Split text into smaller chunks for summarization."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i + max_tokens])
        chunks.append(chunk)
    return chunks

def summarize_text(text, detail_level, progress_label):
    """Summarize text with adjustable length based on detail level."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = chunk_text(text, max_tokens=900)
    summaries = []

    # Adjust summary length based on user selection
    if detail_level == "short":
        min_len, max_len = 40, 100
    elif detail_level == "medium":
        min_len, max_len = 100, 200
    else:  # detailed
        min_len, max_len = 200, 300

    for i, chunk in enumerate(chunks):
        progress_label.config(text=f"Summarizing chunk {i+1}/{len(chunks)}...")
        progress_label.update_idletasks()
        summary = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )[0]['summary_text']
        summaries.append(summary)

    progress_label.config(text="✅ Summary generation completed!")
    final_summary = " ".join(summaries)
    return final_summary

def browse_file():
    """Open file dialog to select a PDF."""
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF Files", "*.pdf")]
    )
    entry_path.delete(0, tk.END)
    entry_path.insert(0, file_path)

def generate_summary():
    """Extract text and summarize the PDF."""
    pdf_path = entry_path.get()

    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return

    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        messagebox.showerror("Error", "No text could be extracted from this PDF.")
        return

    detail_level = summary_option.get()

    def run_summary():
        summary = summarize_text(text, detail_level, progress_label)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, summary)
        save_button.config(state=tk.NORMAL)

    threading.Thread(target=run_summary).start()

def save_summary():
    """Save the summary to a text file."""
    summary_text = text_box.get(1.0, tk.END).strip()
    if not summary_text:
        messagebox.showwarning("Warning", "No summary to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Summary As"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(summary_text)
        messagebox.showinfo("Success", f"Summary saved to:\n{file_path}")

# ---------------- UI Setup ---------------- #
root = tk.Tk()
root.title("PDF Summarizer")
root.geometry("750x650")
root.resizable(False, False)

tk.Label(root, text="📘 PDF Summarizer", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(root, text="Select a PDF and choose how detailed you want the summary to be", font=("Arial", 10)).pack()

frame = tk.Frame(root)
frame.pack(pady=10)

entry_path = tk.Entry(frame, width=60, font=("Arial", 10))
entry_path.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(frame, text="📂 Browse", command=browse_file)
browse_button.pack(side=tk.LEFT)

# Summary detail options
summary_option = tk.StringVar(value="medium")
tk.Label(root, text="Summary Detail:", font=("Arial", 11, "bold")).pack(pady=5)

option_frame = tk.Frame(root)
option_frame.pack()

tk.Radiobutton(option_frame, text="Short", variable=summary_option, value="short").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(option_frame, text="Medium", variable=summary_option, value="medium").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(option_frame, text="Detailed", variable=summary_option, value="detailed").pack(side=tk.LEFT, padx=10)

summarize_button = tk.Button(root, text="🧠 Summarize", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=generate_summary)
summarize_button.pack(pady=10)

progress_label = tk.Label(root, text="", font=("Arial", 10, "italic"))
progress_label.pack()

text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Consolas", 10))
text_box.pack(padx=10, pady=10)

save_button = tk.Button(root, text="💾 Save Summary", font=("Arial", 11), command=save_summary, state=tk.DISABLED)
save_button.pack(pady=5)

root.mainloop()

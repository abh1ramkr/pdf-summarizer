# PDF Summarizer

A simple desktop application that summarizes PDF documents using Natural Language Processing (NLP). The application extracts text from PDF files, generates concise summaries using a pretrained transformer model, and allows users to save the generated summary as a text file.

## Features

- Upload PDF documents through a simple GUI
- Extract text from multi-page PDF files
- Generate AI-powered summaries using the BART Large CNN model
- Choose between:
  - Short Summary
  - Medium Summary
  - Detailed Summary
- Background processing for a responsive interface
- Save generated summaries as `.txt` files

---

## Tech Stack

- Python
- Tkinter
- pdfplumber
- Hugging Face Transformers
- Facebook BART Large CNN
- Threading

---

## Project Structure

```
PDF-Summarizer/
│── pdf_summarizer_gui.py
│── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/PDF-Summarizer.git
```

### 2. Navigate to the project folder

```bash
cd PDF-Summarizer
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

---

## Required Libraries

```text
pdfplumber
transformers
torch
tk
```

---

## Usage

Run the application using:

```bash
python pdf_summarizer_gui.py
```

Then:

1. Click **Browse** to select a PDF.
2. Choose the summary detail level.
3. Click **Summarize**.
4. Wait for the summary to be generated.
5. Save the summary as a text file if needed.

---

## How It Works

1. Extracts text from every page of the selected PDF.
2. Splits the extracted text into manageable chunks.
3. Uses the **facebook/bart-large-cnn** transformer model to summarize each chunk.
4. Combines all chunk summaries into a final summary.
5. Displays the result in the application window.

---

## Future Improvements

- Support for scanned PDFs using OCR
- Export summaries as PDF or Word documents
- Support for multiple summarization models
- Adjustable summary length slider
- Keyword extraction
- Multi-language support
- Dark mode interface

---

## Screenshot

_Add a screenshot of the application here._

---

## Author

**Abhiram K R**

- GitHub: https://github.com/abh1ramkr
- LinkedIn: https://www.linkedin.com/in/abhiram-k-r-3336392b4/

---

## License

This project is open-source and available under the MIT License.

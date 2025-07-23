
import os
import pytesseract
from PIL import Image
import PyPDF2
import docx
import csv

def read_text_file(file_path):
    """Lee un archivo de texto plano."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Intentar con otra codificación si utf-8 falla
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

def read_csv_file(file_path):
    """Lee un archivo CSV y extrae el texto de la columna de mensajes."""
    messages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # Leer encabezado

        # Intentar identificar la columna que contiene mensajes
        message_col = 0
        if header:
            for i, col in enumerate(header):
                if any(term in col.lower() for term in ['mensaje', 'message', 'texto', 'text', 'contenido', 'content']):
                    message_col = i
                    break

        # Leer mensajes
        for row in reader:
            if row and len(row) > message_col:
                messages.append(row[message_col])

    return '\n'.join(messages)

def read_pdf_file(file_path):
    """Extrae texto de un archivo PDF."""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    return text

def read_docx_file(file_path):
    """Extrae texto de un archivo DOCX."""
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_image_file(file_path):
    """Extrae texto de una imagen usando OCR."""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='spa+eng')
        return text
    except Exception as e:
        return f"Error al procesar la imagen: {str(e)}"

def read_file(file_path):
    """Lee un archivo y extrae su contenido según el tipo de archivo."""
    _, ext = os.path.splitext(file_path.lower())

    if ext == '.txt':
        return read_text_file(file_path)
    elif ext == '.csv':
        return read_csv_file(file_path)
    elif ext == '.pdf':
        return read_pdf_file(file_path)
    elif ext == '.docx':
        return read_docx_file(file_path)
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']:
        return read_image_file(file_path)
    else:
        return f"Formato de archivo no soportado: {ext}"

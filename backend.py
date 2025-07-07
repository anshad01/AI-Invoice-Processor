from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import torch
import tempfile
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load model and processor
processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base")

def ocr_with_tesseract(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    words, boxes = [], []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60 and data['text'][i].strip():
            words.append(data['text'][i])
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            boxes.append([x, y, x + w, y + h])
    return words, boxes

def normalize_box(box, width, height):
    return [int(1000 * (box[0] / width)), int(1000 * (box[1] / height)),
            int(1000 * (box[2] / width)), int(1000 * (box[3] / height))]

def process_invoice(image):
    words, boxes = ocr_with_tesseract(image)
    width, height = image.size
    norm_boxes = [normalize_box(b, width, height) for b in boxes]
    encoding = processor(image, words, boxes=norm_boxes, return_tensors="pt", truncation=True, padding="max_length")
    with torch.no_grad():
        outputs = model(**encoding)
    predicted_ids = torch.argmax(outputs.logits, dim=-1).squeeze().tolist()
    labels = [model.config.id2label[i] for i in predicted_ids]
    extracted_data = [(w, l) for w, l in zip(words, labels) if l != 'O']
    return extracted_data

def convert_pdf_to_images(uploaded_pdf):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_pdf.read())
        images = convert_from_bytes(open(tmp_file.name, 'rb').read())
    return images

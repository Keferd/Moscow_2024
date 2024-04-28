import easyocr
import PyPDF2
import fitz
import os
import re

# Функция для получения текста с изображения
def get_text_from_image(img):
    text_result = ""
    reader = easyocr.Reader(['ru', 'en'])
    result = reader.readtext(img)
    for detection in result:
        text = detection[1]
        text_result += " " + text
    return text_result


def get_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            extracted_text = page.extract_text()
            extracted_text = re.sub(r'\s+', ' ', extracted_text)
            text += extracted_text.strip() + " "
    return text.strip()


def get_images_from_pdf(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"{output_folder}/page_{page_number + 1}_image_{image_index}.{image_ext}"
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
    pdf_document.close()


def get_text_from_combination_of_image(folder_path):
    combined_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, filename)
            image_text = get_text_from_image(image_path)
            combined_text += image_text + " "
            os.remove(image_path)
    return combined_text.strip()



def get_text_from_giga_pdf(pdf, image_folder):
    text_from_pdf = get_text_from_pdf(pdf)
    if not text_from_pdf.strip():
        get_images_from_pdf(pdf, image_folder)
        text_from_pdf_prokl = get_text_from_combination_of_image(image_folder)
        return text_from_pdf_prokl
    else:
        return text_from_pdf


# res1 = get_text_from_image("LamodaGroup.png")
# res2 = get_text_from_giga_pdf("LamodaGroup.pdf")
# res3 = get_text_from_giga_pdf("LamodaGroup2.pdf")
# print(res1)
# print(res2)
# print(res3)

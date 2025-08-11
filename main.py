import io
import os
from PIL import Image
import pytesseract
import PyPDF2
import fitz  # PyMuPDF

# Aumentar com segurança o limite de pixels do Pillow para evitar DecompressionBombError
# Alternativa: defina para um valor alto em vez de None, por segurança adicional
Image.MAX_IMAGE_PIXELS = 300_000_000

PDF_PATH = "teste.pdf"
OUTPUT_FOLDER = "extracted_images"


def configure_tesseract_cmd() -> bool:
    """Configura automaticamente o caminho do executável do Tesseract no Windows.
    Retorna True se configurado/encontrado, False caso contrário.
    """
    # 1) Variável de ambiente explícita
    env_path = os.environ.get('TESSERACT_PATH')
    if env_path and os.path.isfile(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
        return True

    # 2) Caminhos comuns
    common_paths = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
    ]
    for candidate in common_paths:
        if os.path.isfile(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            return True

    # 3) Registro do Windows
    try:
        import winreg
        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\tesseract.exe"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Tesseract-OCR"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\Tesseract-OCR"),
        ]
        for hive, subkey in reg_paths:
            try:
                with winreg.OpenKey(hive, subkey) as key:
                    try:
                        # App Paths: valor padrão aponta direto para o exe
                        exe_path, _ = winreg.QueryValueEx(key, None)
                        if exe_path and os.path.isfile(exe_path):
                            pytesseract.pytesseract.tesseract_cmd = exe_path
                            return True
                    except FileNotFoundError:
                        pass
                    for value_name in ("Path", "InstallDir", "TesseractPath"):
                        try:
                            base_dir, _ = winreg.QueryValueEx(key, value_name)
                            candidate = os.path.join(base_dir, "tesseract.exe")
                            if os.path.isfile(candidate):
                                pytesseract.pytesseract.tesseract_cmd = candidate
                                return True
                        except FileNotFoundError:
                            continue
            except FileNotFoundError:
                continue
    except Exception:
        # Sem winreg ou erro de acesso ao Registro
        pass

    return False


def extract_images_from_pdf(pdf_path, output_folder):
    """Extrai imagens incorporadas no PDF e salva na pasta especificada."""
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    extracted_images = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            for image_file_object in getattr(page, 'images', []):
                try:
                    image = Image.open(io.BytesIO(image_file_object.data))

                    image_name = f"image_page_{page_num + 1}_{image_file_object.name}.png"
                    image_path = os.path.join(output_folder, image_name)

                    image.save(image_path)
                    extracted_images.append({
                        'path': image_path,
                        'page': page_num + 1,
                        'name': image_file_object.name
                    })
                    print(f"Imagem salva: {image_path}")
                except Exception as e:
                    print(f"Erro ao processar imagem: {e}")

    return extracted_images


def extract_text_from_saved_images(images_list, language='por'):
    """Extrai texto das imagens já salvas no disco usando Tesseract OCR."""
    print("\nExtraindo texto das imagens salvas...")

    for image_info in images_list:
        try:
            image = Image.open(image_info['path'])
            try:
                text = pytesseract.image_to_string(image, lang=language)
            except pytesseract.TesseractError:
                print(f"Idioma '{language}' indisponível. Tentando 'eng'.")
                text = pytesseract.image_to_string(image, lang='eng')

            if text.strip():
                print(f"\nTexto extraído da imagem {image_info['name']} (página {image_info['page']}):")
                print(text.strip())
            else:
                print(f"Nenhum texto encontrado na imagem {image_info['name']} (página {image_info['page']})")

        except Exception as e:
            print(f"Erro ao processar imagem {image_info['name']}: {e}")


def _compute_zoom_for_page(page, requested_dpi, max_total_pixels):
    """Calcula um fator de zoom para não ultrapassar max_total_pixels por imagem."""
    page_w_in = page.rect.width / 72.0
    page_h_in = page.rect.height / 72.0
    page_area_in2 = max(page_w_in * page_h_in, 1e-6)

    # DPI máximo permitido para respeitar o limite de pixels
    max_dpi_allowed = (max_total_pixels / page_area_in2) ** 0.5
    target_dpi = min(requested_dpi, max_dpi_allowed)
    # Evitar DPI muito baixo que prejudique o OCR
    target_dpi = max(target_dpi, 120)
    return target_dpi / 72.0


def ocr_pdf_by_render(pdf_path, dpi=300, language='por', save_page_images=False, pages_folder=None, max_pixels=25_000_000):
    """Renderiza cada página do PDF em imagem e aplica OCR com controle de resolução.

    - dpi: 300 recomendado para melhor acurácia
    - language: idioma do OCR (ex.: 'por', 'eng')
    - save_page_images: se True, salva as imagens das páginas renderizadas
    - pages_folder: pasta onde salvar as imagens das páginas
    - max_pixels: limite máximo de pixels por imagem renderizada (para evitar estouro de memória)
    """
    if save_page_images:
        pages_folder = pages_folder or os.path.join(OUTPUT_FOLDER, 'pages')
        os.makedirs(pages_folder, exist_ok=True)

    print("\nOCR por renderização das páginas (recomendado)...")
    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            zoom = _compute_zoom_for_page(page, dpi, max_pixels)
            mat = fitz.Matrix(zoom, zoom)
            # Render em tons de cinza para reduzir memória e melhorar OCR
            pix = page.get_pixmap(matrix=mat, alpha=False, colorspace=fitz.csGRAY)
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))

            if save_page_images:
                page_img_path = os.path.join(pages_folder, f"page_{page_index + 1}.png")
                image.save(page_img_path)

            try:
                text = pytesseract.image_to_string(image, lang=language)
            except pytesseract.TesseractError:
                print(f"Idioma '{language}' indisponível. Tentando 'eng'.")
                text = pytesseract.image_to_string(image, lang='eng')

            print(f"\n--- Página {page_index + 1} ---")
            print(text.strip())


def main():
    print("=== Extrator de Texto de Imagens em PDF ===\n")

    if not os.path.exists(PDF_PATH):
        print(f"Erro: Arquivo {PDF_PATH} não encontrado!")
        return

    if not configure_tesseract_cmd():
        print("Erro: Tesseract OCR não encontrado.")
        print("- Instale pelo menos uma destas opções:")
        print("  1) UB Mannheim: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  2) winget: winget install --id UB-Mannheim.TesseractOCR -e")
        print("  3) Chocolatey: choco install tesseract")
        print("- Ou defina a variável de ambiente TESSERACT_PATH com o caminho do tesseract.exe")
        return

    # Método 1 (Recomendado): Renderizar páginas e aplicar OCR com controle de resolução
    ocr_pdf_by_render(PDF_PATH, dpi=300, language='por', save_page_images=True, max_pixels=25_000_000)

    # Método 2 (Opcional): Extrair imagens incorporadas e aplicar OCR nelas
    print("\n" + "=" * 50)
    print("Método 2 (opcional): Extraindo imagens incorporadas e aplicando OCR...")
    extracted_images = extract_images_from_pdf(PDF_PATH, OUTPUT_FOLDER)
    if extracted_images:
        extract_text_from_saved_images(extracted_images, language='por')
    else:
        print("Nenhuma imagem incorporada encontrada no PDF.")


if __name__ == "__main__":
    main()
                        
import io
import os
import sys
import argparse
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# Aumentar com segurança o limite de pixels do Pillow
Image.MAX_IMAGE_PIXELS = 300_000_000


def configure_tesseract_cmd() -> bool:
    env_path = os.environ.get('TESSERACT_PATH')
    if env_path and os.path.isfile(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
        return True

    common_paths = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
    ]
    for candidate in common_paths:
        if os.path.isfile(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            return True

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
        pass

    return False


def _compute_zoom_for_page(page, requested_dpi, max_total_pixels):
    page_w_in = page.rect.width / 72.0
    page_h_in = page.rect.height / 72.0
    page_area_in2 = max(page_w_in * page_h_in, 1e-6)
    max_dpi_allowed = (max_total_pixels / page_area_in2) ** 0.5
    target_dpi = min(requested_dpi, max_dpi_allowed)
    target_dpi = max(target_dpi, 120)  # evitar dpi muito baixo
    return target_dpi / 72.0


def ocr_pdf_by_render(pdf_path, dpi=300, language='por', save_page_images=False, output_folder=None, max_pixels=25_000_000):
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo {pdf_path} não encontrado!")
        return []

    if save_page_images:
        output_folder = output_folder or 'extracted_images/pages'
        os.makedirs(output_folder, exist_ok=True)

    print(f"Processando arquivo: {pdf_path}")
    print(f"Idioma OCR: {language}")
    print("-" * 50)

    all_text = []

    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            zoom = _compute_zoom_for_page(page, dpi, max_pixels)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False, colorspace=fitz.csGRAY)
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))

            if save_page_images:
                page_img_path = os.path.join(output_folder, f"page_{page_index + 1}.png")
                image.save(page_img_path)

            try:
                text = pytesseract.image_to_string(image, lang=language)
            except pytesseract.TesseractError:
                print(f"Idioma '{language}' indisponível. Tentando 'eng'.")
                text = pytesseract.image_to_string(image, lang='eng')

            text = text.strip()
            print(f"\n--- Página {page_index + 1} ---")
            print(text)
            all_text.append(f"Página {page_index + 1}:\n{text}")

    # Salvar texto extraído em arquivo
    if all_text:
        output_file = f"texto_extraido_{os.path.splitext(os.path.basename(pdf_path))[0]}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_text))
        print(f"\nTexto extraído salvo em: {output_file}")

    return all_text


def main():
    parser = argparse.ArgumentParser(description='Extrair texto (OCR) de PDF via renderização de páginas (PyMuPDF)')
    parser.add_argument('pdf_file', nargs='?', default='teste.pdf', help='Caminho para o arquivo PDF (padrão: teste.pdf)')
    parser.add_argument('--dpi', type=int, default=300, help='Resolução de renderização em DPI (padrão: 300)')
    parser.add_argument('--language', '-l', default='por', help='Idioma para OCR (padrão: por)')
    parser.add_argument('--save-images', '-s', action='store_true', help='Salvar imagens das páginas renderizadas')
    parser.add_argument('--output', '-o', help='Pasta para salvar as imagens das páginas renderizadas')
    parser.add_argument('--max-pixels', type=int, default=25_000_000, help='Limite de pixels por imagem (padrão: 25M)')

    args = parser.parse_args()

    if not configure_tesseract_cmd():
        print("Erro: Tesseract OCR não encontrado.")
        print("- Instale pelo menos uma destas opções:")
        print("  1) UB Mannheim: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  2) winget: winget install --id UB-Mannheim.TesseractOCR -e")
        print("  3) Chocolatey: choco install tesseract")
        print("- Ou defina a variável de ambiente TESSERACT_PATH com o caminho do tesseract.exe")
        return

    ocr_pdf_by_render(
        pdf_path=args.pdf_file,
        dpi=args.dpi,
        language=args.language,
        save_page_images=args.save_images,
        output_folder=args.output,
        max_pixels=args.max_pixels,
    )


if __name__ == "__main__":
    main()

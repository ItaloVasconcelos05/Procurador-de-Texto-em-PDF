#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Parágrafos por Palavra-chave
========================================

Este script permite extrair parágrafos específicos de PDFs baseados em palavras-chave.
Ideal para encontrar seções específicas em documentos longos.

Uso:
    python buscar_paragrafos_simples.py
"""

import io
import os
import re
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# Aumentar com segurança o limite de pixels do Pillow
Image.MAX_IMAGE_PIXELS = 300_000_000


def configure_tesseract_cmd() -> bool:
    """Configura automaticamente o caminho do executável do Tesseract no Windows."""
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
    """Calcula um fator de zoom para não ultrapassar max_total_pixels por imagem."""
    page_w_in = page.rect.width / 72.0
    page_h_in = page.rect.height / 72.0
    page_area_in2 = max(page_w_in * page_h_in, 1e-6)
    max_dpi_allowed = (max_total_pixels / page_area_in2) ** 0.5
    target_dpi = min(requested_dpi, max_dpi_allowed)
    target_dpi = max(target_dpi, 120)
    return target_dpi / 72.0


def buscar_paragrafos(pdf_path, keyword, dpi=300, language='por', 
                     context_lines=2, case_sensitive=False, 
                     max_pixels=25_000_000):
    """
    Busca parágrafos que contêm uma palavra-chave específica.
    
    Args:
        pdf_path: Caminho para o arquivo PDF
        keyword: Palavra-chave para buscar
        dpi: Resolução de renderização (padrão: 300)
        language: Idioma para OCR (padrão: 'por')
        context_lines: Número de linhas de contexto antes e depois (padrão: 2)
        case_sensitive: Se a busca deve ser sensível a maiúsculas/minúsculas (padrão: False)
        max_pixels: Limite de pixels por imagem (padrão: 25M)
    
    Returns:
        Lista de dicionários com informações dos parágrafos encontrados
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Erro: Arquivo {pdf_path} não encontrado!")
        return []

    print(f"📄 Processando arquivo: {pdf_path}")
    print(f"🔍 Buscando por: '{keyword}'")
    print(f"🌐 Idioma OCR: {language}")
    print(f"📝 Contexto: {context_lines} linhas")
    print(f"🔤 Case sensitive: {case_sensitive}")
    print("-" * 50)

    found_paragraphs = []
    
    # Preparar regex para busca
    if case_sensitive:
        pattern = re.compile(re.escape(keyword))
    else:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
        print(f"📖 Total de páginas: {total_pages}")
        
        for page_index, page in enumerate(doc):
            print(f"⏳ Processando página {page_index + 1}/{total_pages}...", end="\r")
            
            zoom = _compute_zoom_for_page(page, dpi, max_pixels)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False, colorspace=fitz.csGRAY)
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))

            try:
                text = pytesseract.image_to_string(image, lang=language)
            except pytesseract.TesseractError:
                print(f"\n⚠️  Idioma '{language}' indisponível. Tentando 'eng'.")
                text = pytesseract.image_to_string(image, lang='eng')

            # Dividir texto em linhas
            lines = text.strip().split('\n')
            
            # Buscar pela palavra-chave em cada linha
            for line_num, line in enumerate(lines):
                if pattern.search(line):
                    # Encontrar o início e fim do parágrafo
                    start_line = max(0, line_num - context_lines)
                    end_line = min(len(lines), line_num + context_lines + 1)
                    
                    # Extrair o parágrafo com contexto
                    paragraph_lines = lines[start_line:end_line]
                    paragraph_text = '\n'.join(paragraph_lines).strip()
                    
                    # Destacar a palavra-chave encontrada
                    highlighted_text = pattern.sub(f"**{keyword}**", paragraph_text)
                    
                    paragraph_info = {
                        'page': page_index + 1,
                        'line_number': line_num + 1,
                        'keyword_line': line_num + 1,
                        'text': paragraph_text,
                        'highlighted_text': highlighted_text,
                        'context_start': start_line + 1,
                        'context_end': end_line
                    }
                    
                    found_paragraphs.append(paragraph_info)
                    
                    print(f"\n✅ Página {page_index + 1}, Linha {line_num + 1}")
                    print(highlighted_text)
                    print("-" * 40)

    print(f"\n📊 Processamento concluído!")
    
    # Salvar resultados em arquivo
    if found_paragraphs:
        output_file = f"paragrafos_encontrados_{os.path.splitext(os.path.basename(pdf_path))[0]}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Busca por: '{keyword}'\n")
            f.write(f"Total de parágrafos encontrados: {len(found_paragraphs)}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, para in enumerate(found_paragraphs, 1):
                f.write(f"Parágrafo {i}:\n")
                f.write(f"Página: {para['page']}\n")
                f.write(f"Linha da palavra-chave: {para['keyword_line']}\n")
                f.write(f"Contexto: linhas {para['context_start']}-{para['context_end']}\n")
                f.write("-" * 40 + "\n")
                f.write(para['highlighted_text'])
                f.write("\n\n")
        
        print(f"💾 Resultados salvos em: {output_file}")
        print(f"🎯 Total de parágrafos encontrados: {len(found_paragraphs)}")
    else:
        print(f"❌ Nenhum parágrafo contendo '{keyword}' foi encontrado.")

    return found_paragraphs


def main():
    """Função principal com interface interativa."""
    print("=" * 60)
    print("🔍 EXTRATOR DE PARÁGRAFOS POR PALAVRA-CHAVE")
    print("=" * 60)
    
    # Verificar se o Tesseract está configurado
    if not configure_tesseract_cmd():
        print("❌ Erro: Tesseract OCR não encontrado.")
        print("\n📋 Para instalar o Tesseract:")
        print("   1) UB Mannheim: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2) winget: winget install --id UB-Mannheim.TesseractOCR -e")
        print("   3) Chocolatey: choco install tesseract")
        print("\n   Ou defina a variável de ambiente TESSERACT_PATH")
        input("\nPressione Enter para sair...")
        return

    # Solicitar arquivo PDF
    pdf_file = input("\n📄 Digite o caminho do arquivo PDF (ou pressione Enter para 'teste.pdf'): ").strip()
    if not pdf_file:
        pdf_file = "teste.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ Erro: Arquivo '{pdf_file}' não encontrado!")
        input("\nPressione Enter para sair...")
        return

    # Solicitar palavra-chave
    keyword = input("\n🔍 Digite a palavra-chave que deseja buscar: ").strip()
    if not keyword:
        print("❌ Nenhuma palavra-chave fornecida.")
        input("\nPressione Enter para sair...")
        return

    # Configurações opcionais
    print("\n⚙️  Configurações opcionais (pressione Enter para usar padrões):")
    
    # Idioma
    language = input("   Idioma para OCR (por/eng) [por]: ").strip()
    if not language:
        language = "por"
    
    # Linhas de contexto
    context_input = input("   Linhas de contexto antes/depois [2]: ").strip()
    try:
        context_lines = int(context_input) if context_input else 2
    except ValueError:
        context_lines = 2
        print("   Usando valor padrão: 2 linhas")
    
    # Case sensitive
    case_sensitive = input("   Busca sensível a maiúsculas/minúsculas? (s/n) [n]: ").strip().lower()
    case_sensitive = case_sensitive == 's'

    print(f"\n🚀 Iniciando busca por '{keyword}' no arquivo '{pdf_file}'...")
    print("⏳ Isso pode levar alguns minutos dependendo do tamanho do PDF...")
    
    try:
        # Executar a busca
        results = buscar_paragrafos(
            pdf_path=pdf_file,
            keyword=keyword,
            language=language,
            context_lines=context_lines,
            case_sensitive=case_sensitive
        )
        
        # Resumo final
        print("\n" + "=" * 60)
        if results:
            print(f"✅ Busca concluída! Encontrados {len(results)} parágrafo(s).")
            print(f"📁 Resultados salvos em: paragrafos_encontrados_{os.path.splitext(os.path.basename(pdf_file))[0]}.txt")
        else:
            print(f"❌ Nenhum parágrafo contendo '{keyword}' foi encontrado.")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante o processamento: {e}")
        print("💡 Verifique se o arquivo PDF não está corrompido e tente novamente.")
    
    input("\nPressione Enter para sair...")


if __name__ == "__main__":
    main()

from PyPDF2 import PdfReader

def extrair_paragrafo_por_nome(caminho_pdf, nome_procurado):
    """
    Extrai parágrafos de um PDF que contêm um nome específico.

    Args:
        caminho_pdf (str): O caminho completo para o arquivo PDF.
        nome_procurado (str): O nome (ou texto) a ser procurado dentro dos parágrafos.

    Returns:
        list: Uma lista de parágrafos encontrados que contêm o nome.
    """
    paragrafos_encontrados = []
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            reader = PdfReader(arquivo)
            num_paginas = len(reader.pages)

            for pagina_num in range(num_paginas):
                pagina = reader.pages[pagina_num]
                texto_pagina = pagina.extract_text()

                # Dividir o texto em "parágrafos" (linhas ou blocos de texto)
                # Você pode precisar ajustar como o texto é dividido dependendo da estrutura do seu PDF
                linhas = texto_pagina.split('\n')
                paragrafo_atual = ""

                for linha in linhas:
                    if linha.strip(): # Se a linha não está vazia
                        paragrafo_atual += linha + " "
                    else: # Se encontrar uma linha vazia, considera o fim do parágrafo
                        if nome_procurado.lower() in paragrafo_atual.lower():
                            paragrafos_encontrados.append(paragrafo_atual.strip())
                        paragrafo_atual = "" # Reinicia o parágrafo

                # Checar o último parágrafo da página, caso não termine com linha vazia
                if paragrafo_atual.strip() and nome_procurado.lower() in paragrafo_atual.lower():
                    paragrafos_encontrados.append(paragrafo_atual.strip())

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    return paragrafos_encontrados
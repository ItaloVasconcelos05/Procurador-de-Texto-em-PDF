# Extrator de Texto de Imagens em PDF

Este projeto permite extrair texto de imagens que estão dentro de arquivos PDF usando OCR (Reconhecimento Óptico de Caracteres).

## Pré-requisitos

1. **Python 3.7+**
2. **Tesseract OCR** - Deve ser instalado no sistema

### Instalação do Tesseract OCR no Windows:

1. Baixe o instalador do Tesseract para Windows: https://github.com/UB-Mannheim/tesseract/wiki
2. Execute o instalador e instale no caminho padrão: `C:\Program Files\Tesseract-OCR\`
3. Adicione o Tesseract ao PATH do sistema ou configure o caminho no código

## Instalação das Dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### Opção 1: Script Simples (main.py)
1. Coloque seu arquivo PDF na pasta do projeto com o nome `teste.pdf`
2. Execute o script:

```bash
python main.py
```

### Opção 2: Script Avançado (extract_text.py)
Execute o script com interface interativa:
```bash
python extract_text.py
```

Ou use argumentos de linha de comando:
```bash
# Processar um PDF específico
python extract_text.py documento.pdf

# Salvar imagens extraídas
python extract_text.py documento.pdf --save-images --output imagens/

# Especificar idioma
python extract_text.py documento.pdf --language eng

# Ver todas as opções
python extract_text.py --help
```

## Funcionalidades

O código oferece dois métodos para extrair texto de imagens em PDF:

### Método 1: Extração de Imagens + OCR
- Extrai todas as imagens do PDF
- Salva as imagens na pasta `extracted_images/`
- Aplica OCR em cada imagem salva

### Método 2: OCR Direto no PDF
- Processa o PDF diretamente sem salvar imagens
- Extrai texto de todas as imagens encontradas
- Mais eficiente em termos de espaço em disco

## Configurações

- **PDF_PATH**: Caminho para o arquivo PDF (padrão: "teste.pdf")
- **OUTPUT_FOLDER**: Pasta onde as imagens serão salvas (padrão: "extracted_images")
- **Idioma OCR**: Configurado para português (`lang='por'`)

## Estrutura do Projeto

```
Texto-Lara/
├── main.py              # Script principal (processa teste.pdf)
├── extract_text.py      # Script avançado (processa qualquer PDF)
├── requirements.txt     # Dependências Python
├── README.md           # Este arquivo
├── teste.pdf           # Arquivo PDF de teste
├── extracted_images/   # Pasta com imagens extraídas
└── venv/              # Ambiente virtual (se usado)
```

## Solução de Problemas

### Erro: "Tesseract not found"
- Verifique se o Tesseract está instalado
- Confirme o caminho no código: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Adicione o Tesseract ao PATH do sistema

### Erro: "PDF file not found"
- Verifique se o arquivo `teste.pdf` existe na pasta do projeto

### Baixa qualidade do OCR
- Certifique-se de que as imagens no PDF têm boa resolução
- Considere usar diferentes configurações do Tesseract
- Para melhor precisão, use imagens com texto claro e bem contrastado

## Dependências

- **PyPDF2**: Para leitura básica de PDF
- **pdfplumber**: Para extração avançada de conteúdo de PDF
- **Pillow**: Para processamento de imagens
- **pytesseract**: Interface Python para o Tesseract OCR

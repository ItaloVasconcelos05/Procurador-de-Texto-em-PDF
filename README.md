# 🔍 Extrator de Parágrafos por Palavra-chave

Este projeto permite **extrair parágrafos específicos de PDFs baseados em palavras-chave**, ideal para encontrar seções específicas em documentos longos.

## ✨ Funcionalidade Principal

- **Busca por palavra-chave** em PDFs usando OCR
- **Contexto configurável** (linhas antes/depois)
- **Busca case-sensitive/insensitive**
- **Resultados organizados** em arquivo de texto
- **Interface interativa** amigável
- **Suporte a múltiplos idiomas** (português/inglês)
- **Destaque da palavra-chave** nos resultados

## 📋 Pré-requisitos

1. **Python 3.7+**
2. **Tesseract OCR** - Deve ser instalado no sistema

### Instalação do Tesseract OCR no Windows:

1. Baixe o instalador do Tesseract para Windows: https://github.com/UB-Mannheim/tesseract/wiki
2. Execute o instalador e instale no caminho padrão: `C:\Program Files\Tesseract-OCR\`
3. Adicione o Tesseract ao PATH do sistema ou configure o caminho no código

## 🚀 Instalação e Uso

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o Script
```bash
python buscar_paragrafos_simples.py
```

### 3. Seguir as Instruções
- Digite o caminho do PDF (ou pressione Enter para 'teste.pdf')
- Digite a palavra-chave que deseja buscar
- Configure opções como idioma e contexto
- Aguarde o processamento
- Os resultados são salvos automaticamente

## 📁 Arquivos do Projeto

```
Texto-Lara/
├── buscar_paragrafos_simples.py  # Script principal (ÚNICO arquivo necessário)
├── requirements.txt              # Dependências Python
├── README_SIMPLES.md            # Este arquivo
├── teste.pdf                    # Arquivo PDF de teste (opcional)
└── paragrafos_encontrados_*.txt # Resultados gerados automaticamente
```

## 📊 Exemplo de Uso

```
🔍 EXTRATOR DE PARÁGRAFOS POR PALAVRA-CHAVE
============================================================

📄 Digite o caminho do arquivo PDF (ou pressione Enter para 'teste.pdf'): 
🔍 Digite a palavra-chave que deseja buscar: contrato

⚙️  Configurações opcionais (pressione Enter para usar padrões):
   Idioma para OCR (por/eng) [por]: 
   Linhas de contexto antes/depois [2]: 
   Busca sensível a maiúsculas/minúsculas? (s/n) [n]: 

🚀 Iniciando busca por 'contrato' no arquivo 'teste.pdf'...
⏳ Isso pode levar alguns minutos dependendo do tamanho do PDF...

📄 Processando arquivo: teste.pdf
🔍 Buscando por: 'contrato'
🌐 Idioma OCR: por
📝 Contexto: 2 linhas
🔤 Case sensitive: False
--------------------------------------------------
📖 Total de páginas: 5
⏳ Processando página 5/5...

✅ Página 2, Linha 15
Este é um exemplo de **contrato** de prestação de serviços...
----------------------------------------

📊 Processamento concluído!
💾 Resultados salvos em: paragrafos_encontrados_teste.txt
🎯 Total de parágrafos encontrados: 1

============================================================
✅ Busca concluída! Encontrados 1 parágrafo(s).
📁 Resultados salvos em: paragrafos_encontrados_teste.txt
============================================================
```

## 📄 Formato dos Resultados

Os parágrafos encontrados são salvos em arquivos como `paragrafos_encontrados_documento.txt` com:

```
Busca por: 'contrato'
Total de parágrafos encontrados: 1
============================================================

Parágrafo 1:
Página: 2
Linha da palavra-chave: 15
Contexto: linhas 13-17
----------------------------------------
Este é um exemplo de **contrato** de prestação de serviços
que pode ser encontrado em documentos legais.
O texto aqui mostra o contexto completo.
```

## ⚙️ Configurações Disponíveis

- **Idioma OCR**: português (padrão) ou inglês
- **Contexto**: número de linhas antes/depois (padrão: 2)
- **Case sensitive**: busca exata ou não (padrão: não)
- **Resolução**: DPI para renderização (padrão: 300)

## 🔧 Solução de Problemas

### Erro: "Tesseract not found"
- Verifique se o Tesseract está instalado
- Confirme o caminho: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Adicione o Tesseract ao PATH do sistema

### Erro: "PDF file not found"
- Verifique se o arquivo PDF existe no caminho especificado

### Baixa qualidade do OCR
- Certifique-se de que as imagens no PDF têm boa resolução
- Use imagens com texto claro e bem contrastado
- Considere usar diferentes configurações do Tesseract

## 📦 Dependências

- **PyMuPDF (fitz)**: Para leitura e renderização de PDF
- **Pillow**: Para processamento de imagens
- **pytesseract**: Interface Python para o Tesseract OCR

## 🎯 Casos de Uso

- **Documentos legais**: Encontrar cláusulas específicas
- **Contratos**: Localizar seções importantes
- **Manuais**: Buscar instruções específicas
- **Relatórios**: Encontrar informações relevantes
- **Livros digitais**: Localizar tópicos específicos

## 💡 Dicas de Uso

1. **Use palavras-chave específicas** para resultados mais precisos
2. **Ajuste o contexto** conforme necessário (mais linhas = mais contexto)
3. **Use case-sensitive** quando precisar de busca exata
4. **Teste com diferentes idiomas** se o documento for multilíngue
5. **Verifique a qualidade do PDF** para melhor reconhecimento

---

**Desenvolvido para facilitar a busca e extração de informações específicas em documentos PDF!** 📚✨

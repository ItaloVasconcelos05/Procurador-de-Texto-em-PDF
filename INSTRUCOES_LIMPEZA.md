# 🧹 Instruções para Simplificar o Projeto

Este arquivo contém instruções para limpar o projeto e manter **apenas a funcionalidade de busca de parágrafos por palavra-chave**.

## 📋 O que foi criado

Criei os seguintes arquivos para você:

1. **`buscar_paragrafos_simples.py`** - Script principal simplificado
2. **`README_SIMPLES.md`** - Documentação simplificada
3. **`requirements_simples.txt`** - Dependências simplificadas
4. **`limpar_projeto.py`** - Script para limpeza automática

## 🚀 Como proceder

### Opção 1: Limpeza Automática (Recomendado)

Execute o script de limpeza:

```bash
python limpar_projeto.py
```

Este script irá:
- ✅ Remover todos os arquivos desnecessários
- ✅ Renomear os arquivos simplificados para nomes padrão
- ✅ Manter apenas a funcionalidade de busca de parágrafos

### Opção 2: Limpeza Manual

Se preferir fazer manualmente:

1. **Remover arquivos antigos:**
   ```bash
   # Remover scripts antigos
   del main.py
   del extract_text.py
   del extract_paragraphs.py
   del buscar_paragrafos.py
   del exemplo_uso.py
   del extraction.py
   
   # Remover documentação antiga
   del README.md
   del requirements.txt
   ```

2. **Remover pastas desnecessárias:**
   ```bash
   # Remover pastas de imagens (não necessárias para busca de parágrafos)
   rmdir /s extracted_images
   rmdir /s images
   rmdir /s __pycache__
   ```

3. **Renomear arquivos simplificados:**
   ```bash
   # Renomear para nomes padrão
   ren buscar_paragrafos_simples.py main.py
   ren requirements_simples.txt requirements.txt
   ren README_SIMPLES.md README.md
   ```

## 📁 Estrutura Final

Após a limpeza, seu projeto terá apenas:

```
Texto-Lara/
├── main.py                    # Script principal (busca de parágrafos)
├── requirements.txt           # Dependências Python
├── README.md                  # Documentação
├── teste.pdf                  # Arquivo PDF de teste (opcional)
└── paragrafos_encontrados_*.txt # Resultados gerados automaticamente
```

## 🎯 Funcionalidade Mantida

- ✅ **Busca de parágrafos por palavra-chave**
- ✅ **Interface interativa amigável**
- ✅ **Contexto configurável**
- ✅ **Busca case-sensitive/insensitive**
- ✅ **Suporte a múltiplos idiomas**
- ✅ **Resultados organizados em arquivo**

## ❌ Funcionalidades Removidas

- ❌ Extração de imagens do PDF
- ❌ OCR direto em imagens extraídas
- ❌ Scripts de linha de comando complexos
- ❌ Exemplos programáticos
- ❌ Pastas de imagens desnecessárias

## 🚀 Como usar após a limpeza

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar o script:**
   ```bash
   python main.py
   ```

3. **Seguir as instruções na tela**

## 💡 Vantagens da Simplificação

- 🎯 **Foco único**: Apenas busca de parágrafos
- 📦 **Menos arquivos**: Projeto mais limpo
- 🚀 **Mais simples**: Fácil de entender e usar
- 📚 **Documentação clara**: README focado na funcionalidade
- 🔧 **Menos dependências**: Apenas o necessário

## ⚠️ Importante

- O script de limpeza **não remove** o arquivo `teste.pdf` (se existir)
- Os arquivos de resultados (`paragrafos_encontrados_*.txt`) são mantidos
- O arquivo `.gitignore` é preservado
- A pasta `venv/` (ambiente virtual) é preservada

---

**Após a limpeza, você terá um projeto focado exclusivamente na busca de parágrafos por palavra-chave!** 🔍✨

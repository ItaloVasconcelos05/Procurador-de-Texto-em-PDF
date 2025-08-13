#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar o projeto, removendo arquivos desnecessários
e mantendo apenas a funcionalidade de busca de parágrafos por palavra-chave.
"""

import os
import shutil

def limpar_projeto():
    """Remove arquivos desnecessários e mantém apenas a funcionalidade de busca de parágrafos."""
    
    print("🧹 LIMPEZA DO PROJETO - MANTENDO APENAS BUSCA DE PARÁGRAFOS")
    print("=" * 60)
    
    # Arquivos a serem removidos (funcionalidades antigas)
    arquivos_para_remover = [
        "main.py",                    # Script principal antigo
        "extract_text.py",            # Script avançado antigo
        "extract_paragraphs.py",      # Versão antiga da busca de parágrafos
        "buscar_paragrafos.py",       # Versão antiga da interface
        "exemplo_uso.py",             # Exemplos antigos
        "extraction.py",              # Arquivo de extração antigo
        "requirements.txt",           # Requirements antigo
        "README.md",                  # README antigo
    ]
    
    # Pastas a serem removidas
    pastas_para_remover = [
        "extracted_images",           # Pasta com imagens extraídas (não necessária)
        "images",                     # Pasta de imagens (não necessária)
        "__pycache__",                # Cache Python
    ]
    
    # Arquivos a serem renomeados
    arquivos_para_renomear = {
        "buscar_paragrafos_simples.py": "main.py",
        "requirements_simples.txt": "requirements.txt",
        "README_SIMPLES.md": "README.md"
    }
    
    print("📋 Arquivos que serão removidos:")
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            print(f"   ❌ {arquivo}")
        else:
            print(f"   ⚪ {arquivo} (não encontrado)")
    
    print("\n📁 Pastas que serão removidas:")
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            print(f"   ❌ {pasta}/")
        else:
            print(f"   ⚪ {pasta}/ (não encontrada)")
    
    print("\n🔄 Arquivos que serão renomeados:")
    for antigo, novo in arquivos_para_renomear.items():
        if os.path.exists(antigo):
            print(f"   🔄 {antigo} → {novo}")
        else:
            print(f"   ⚪ {antigo} → {novo} (não encontrado)")
    
    # Confirmar limpeza
    resposta = input("\n⚠️  Tem certeza que deseja continuar? (s/n): ").strip().lower()
    if resposta != 's':
        print("❌ Limpeza cancelada.")
        return
    
    print("\n🧹 Iniciando limpeza...")
    
    # Remover arquivos
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"✅ Removido: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao remover {arquivo}: {e}")
    
    # Remover pastas
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"✅ Removida: {pasta}/")
            except Exception as e:
                print(f"❌ Erro ao remover {pasta}/: {e}")
    
    # Renomear arquivos
    for antigo, novo in arquivos_para_renomear.items():
        if os.path.exists(antigo):
            try:
                os.rename(antigo, novo)
                print(f"✅ Renomeado: {antigo} → {novo}")
            except Exception as e:
                print(f"❌ Erro ao renomear {antigo}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ LIMPEZA CONCLUÍDA!")
    print("=" * 60)
    
    print("\n📁 Estrutura final do projeto:")
    print("Texto-Lara/")
    print("├── main.py                    # Script principal (busca de parágrafos)")
    print("├── requirements.txt           # Dependências Python")
    print("├── README.md                  # Documentação")
    print("├── teste.pdf                  # Arquivo PDF de teste (opcional)")
    print("└── paragrafos_encontrados_*.txt # Resultados gerados automaticamente")
    
    print("\n🚀 Para usar o projeto:")
    print("1. pip install -r requirements.txt")
    print("2. python main.py")
    print("3. Siga as instruções na tela")
    
    print("\n✨ Projeto simplificado com sucesso!")


if __name__ == "__main__":
    limpar_projeto()

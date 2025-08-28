from functions import executar_busca, listar_resultados

def main():
    """Função principal com interface interativa."""
    while True:
        print("=" * 60)
        print("🔍 EXTRATOR DE PARÁGRAFOS POR PALAVRA-CHAVE")
        print("=" * 60)
        print("\n📋 Menu:")
        print("1. 🔍 Buscar parágrafos por palavra-chave")
        print("2. 📋 Listar resultados salvos")
        print("3. 🚪 Sair")
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            executar_busca()
        elif opcao == "2":
            listar_resultados()
            input("\nPressione Enter para continuar...")
        elif opcao == "3":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()

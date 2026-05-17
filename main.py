def adicionar_cliente(clientes):
    """Solicita e adiciona um cliente na lista em memoria."""
    nome = input("Digite o nome do cliente: ").strip()

    if not nome:
        print("Nome invalido. Tente novamente.")
        return

    clientes.append(nome)
    print(f"Cliente '{nome}' adicionado com sucesso.")


def listar_clientes(clientes):
    """Exibe os clientes cadastrados."""
    if not clientes:
        print("Nenhum cliente cadastrado ainda.")
        return

    print("\nClientes cadastrados:")
    for indice, nome in enumerate(clientes, start=1):
        print(f"{indice}. {nome}")


def exibir_menu():
    """Mostra o menu principal e retorna a opcao escolhida."""
    print("\n=== Menu de Clientes ===")
    print("1) Adicionar cliente")
    print("2) Listar clientes")
    print("0) Sair")
    return input("Escolha uma opcao: ").strip()


def main():
    clientes = []

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            adicionar_cliente(clientes)
        elif opcao == "2":
            listar_clientes(clientes)
        elif opcao == "0":
            print("Encerrando programa. Ate logo!")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()

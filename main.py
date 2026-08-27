import csv
import os

# Nome do arquivo onde o catálogo de livros fica salvo
ARQUIVO = "livros.csv"

# Nomes das colunas usadas no arquivo csv
CAMPOS = ["titulo", "autor", "ano", "isbn", "status"]


def carregar_livros():
    """Lê o arquivo livros.csv e devolve a lista de livros (lista de dicionários).
    Se o arquivo ainda não existir, devolve uma lista vazia."""
    livros = []

    # Se o arquivo não existe ainda (primeira vez rodando o programa),
    # não tem o que ler, então devolve a lista vazia
    if not os.path.exists(ARQUIVO):
        return livros

    with open(ARQUIVO, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            livros.append(linha)

    return livros


def salvar_livros(livros):
    """Escreve a lista de livros inteira no arquivo livros.csv,
    sobrescrevendo o conteúdo antigo. É chamada toda vez que algo muda."""
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for livro in livros:
            escritor.writerow(livro)


def cadastrar_livro(livros):
    """Pede os dados de um livro novo, adiciona na lista e devolve a lista atualizada."""
    print("\n--- Cadastro de novo livro ---")
    titulo = input("Título: ")
    autor = input("Autor: ")
    ano = input("Ano de publicação: ")
    isbn = input("Código/ISBN: ")

    # Todo livro novo começa como disponível
    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "isbn": isbn,
        "status": "disponivel"
    }

    livros.append(novo_livro)
    print('Livro "' + titulo + '" cadastrado com sucesso!')

    return livros


def buscar_por_titulo_exato(livros, titulo_buscado):
    """Procura um único livro pelo título exato (usada internamente por
    emprestar e devolver). Devolve o dicionário do livro, ou None se não achar."""
    for livro in livros:
        if livro["titulo"].lower() == titulo_buscado.lower():
            return livro
    return None


def emprestar_livro(livros):
    """Pergunta o título do livro e muda o status para 'emprestado',
    caso ele exista e esteja disponível."""
    titulo = input("\nDigite o título do livro que deseja emprestar: ")
    livro = buscar_por_titulo_exato(livros, titulo)

    if livro is None:
        print("Livro não encontrado.")
    elif livro["status"] == "emprestado":
        print("Esse livro já está emprestado.")
    else:
        livro["status"] = "emprestado"
        print('Empréstimo registrado: "' + livro["titulo"] + '" agora está emprestado.')

    return livros


def devolver_livro(livros):
    """Pergunta o título do livro e muda o status de volta para 'disponivel'."""
    titulo = input("\nDigite o título do livro que está sendo devolvido: ")
    livro = buscar_por_titulo_exato(livros, titulo)

    if livro is None:
        print("Livro não encontrado.")
    elif livro["status"] == "disponivel":
        print("Esse livro já estava disponível.")
    else:
        livro["status"] = "disponivel"
        print('Devolução registrada: "' + livro["titulo"] + '" agora está disponível.')

    return livros


def listar_livros(livros):
    """Mostra todos os livros cadastrados, com seus dados e status."""
    print("\n--- Lista de livros ---")

    if len(livros) == 0:
        print("Nenhum livro cadastrado ainda.")
        return

    for livro in livros:
        print("Título: " + livro["titulo"] +
              " | Autor: " + livro["autor"] +
              " | Ano: " + livro["ano"] +
              " | ISBN: " + livro["isbn"] +
              " | Status: " + livro["status"])


def buscar_livro(livros):
    """Pergunta um termo e mostra os livros cujo título ou autor combinam com ele."""
    termo = input("\nDigite o título ou autor que deseja buscar: ").lower()
    encontrados = []

    for livro in livros:
        if termo in livro["titulo"].lower() or termo in livro["autor"].lower():
            encontrados.append(livro)

    print("\n--- Resultado da busca ---")
    if len(encontrados) == 0:
        print("Nenhum livro encontrado.")
    else:
        for livro in encontrados:
            print("Título: " + livro["titulo"] +
                  " | Autor: " + livro["autor"] +
                  " | Ano: " + livro["ano"] +
                  " | Status: " + livro["status"])


def pegar_titulo(livro):
    """Função auxiliar: devolve o título de um livro em minúsculas.
    Usada como critério de ordenação."""
    return livro["titulo"].lower()


def pegar_autor(livro):
    """Função auxiliar: devolve o autor de um livro em minúsculas.
    Usada como critério de ordenação."""
    return livro["autor"].lower()


def pegar_ano(livro):
    """Função auxiliar: devolve o ano de um livro. Usada como critério de ordenação."""
    return livro["ano"]


def ordenar_livros(livros):
    """Pergunta o critério de ordenação escolhido pelo usuário
    e devolve a lista de livros já ordenada."""
    print("\nOrdenar por: (1) Título  (2) Autor  (3) Ano")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        livros_ordenados = sorted(livros, key=pegar_titulo)
    elif opcao == "2":
        livros_ordenados = sorted(livros, key=pegar_autor)
    elif opcao == "3":
        livros_ordenados = sorted(livros, key=pegar_ano)
    else:
        print("Opção inválida.")
        return livros

    return livros_ordenados


def exibir_menu():
    """Mostra as opções do menu principal na tela."""
    print("\n===== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA =====")
    print("1 - Cadastrar livro")
    print("2 - Emprestar livro")
    print("3 - Devolver livro")
    print("4 - Listar livros")
    print("5 - Buscar livro")
    print("6 - Ordenar livros")
    print("0 - Sair")


def main():
    # Carrega o catálogo salvo (se existir) assim que o programa abre
    livros = carregar_livros()
    rodando = True

    # Laço principal: mantém o menu ativo até o usuário escolher sair
    while rodando:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            livros = cadastrar_livro(livros)
            salvar_livros(livros)
        elif opcao == "2":
            livros = emprestar_livro(livros)
            salvar_livros(livros)
        elif opcao == "3":
            livros = devolver_livro(livros)
            salvar_livros(livros)
        elif opcao == "4":
            listar_livros(livros)
        elif opcao == "5":
            buscar_livro(livros)
        elif opcao == "6":
            livros = ordenar_livros(livros)
            listar_livros(livros)
        elif opcao == "0":
            print("Encerrando o programa...")
            rodando = False
        else:
            print("Opção inválida, tente novamente.")


# Só executa o programa se este arquivo for rodado diretamente
if __name__ == "__main__":
    main()
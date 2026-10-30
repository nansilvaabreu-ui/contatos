import sqlite3

def conexao_banco():
    conexao = sqlite3.connect('contatos.db')
    cursor = conexao.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL
    )'''
    cursor.execute(sql)
    conexao.commit()
    return conexao

def adicionar_contato(nome, telefone, email):
    conexao =conexao_banco()
    cursor = conexao.cursor()
    sql = '''
        INSERT INTO contatos (nome, telefone, email)
        VALUES (?, ?, ?)'''
    cursor.execute(sql, (nome, telefone, email))
    conexao.commit()
    conexao.close()

def listar_contatos():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = 'SELECT * FROM contatos'
    cursor.execute(sql)
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
        print("---> LISTA DE CONTATOS <---")
        print(f"{'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30}")
        print("-" * 75)
        for contato in contatos:
            print(f"{contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30}")

def buscar_contato():
    nome = input("Digite o nome do contato que deseja buscar: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = 'SELECT * FROM contatos WHERE nome LIKE ?'
    cursor.execute(sql, ('%' + nome + '%',))
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado com esse nome.")
    else:
        print("---> RESULTADO DA BUSCA <---")
        print(f"{'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30}")
        print("-" * 75)
        for contato in contatos:
            print(f"{contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30}")
    

def atualizar_contato():
    contato_id = input("Digite o ID do contato que deseja atualizar: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = 'SELECT * FROM contatos WHERE id = ?'
    cursor.execute(sql, (contato_id,))
    contato = cursor.fetchone()

    if contato is None:
        print("Contato não encontrado.")
    else:
        print(f"Contato encontrado: {contato[1]} - {contato[2]} - {contato[3]}")
        novo_nome = input("Digite o novo nome (ou pressione Enter para manter o atual): ")
        novo_telefone = input("Digite o novo telefone (ou pressione Enter para manter o atual): ")
        novo_email = input("Digite o novo email (ou pressione Enter para manter o atual): ")

        if novo_nome == "":
            novo_nome = contato[1]
        if novo_telefone == "":
            novo_telefone = contato[2]
        if novo_email == "":
            novo_email = contato[3]

        sql = 'UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?'
        cursor.execute(sql, (novo_nome, novo_telefone, novo_email, contato_id))
        conexao.commit()
        conexao.close()
        print("Contato atualizado com sucesso.")

def excluir_contato():
    contato_id = input("Digite o ID do contato que deseja excluir: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = 'SELECT * FROM contatos WHERE id = ?'
    cursor.execute(sql, (contato_id,))
    contato = cursor.fetchone()

    if contato is None:
        print("Contato não encontrado.")
    else:
        confirmacao = input(f"Tem certeza que deseja excluir o contato {contato[1]}? (s/n): ")
        if confirmacao.lower() == 's':
            sql = 'DELETE FROM contatos WHERE id = ?'
            cursor.execute(sql, (contato_id,))
            conexao.commit()
            conexao.close()
            print("Contato excluído com sucesso.")
        else:
            print("Exclusão cancelada.")

def menu():

    while True:
        print ("---> CONTATOS <---")
        print ("1 - Adicionar contato")
        print ("2 - Listar contatos")
        print ("3 - Buscar contato pelo nome")
        print ("4 - Atualizar contato")
        print ("5 - Excluir contato")
        print ("6 - Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            nome = input("Digite o nome do contato: ")
            telefone = input("Digite o telefone do contato: ")
            email = input("Digite o email do contato: ")
            adicionar_contato(nome, telefone, email)
            print("Contato adicionado com sucesso!")
        elif opcao == "2":
            listar_contatos()
        elif opcao == "3":
            buscar_contato()
        elif opcao == "4":
            atualizar_contato()
        elif opcao == "5":
            excluir_contato()
        elif opcao == "6":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()


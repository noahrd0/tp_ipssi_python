import mysql.connector
from mysql.connector import Error
def connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='informatique'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None


def insert_log(action, table, username):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM user WHERE nom = %s", (username,))
            user_id = cursor.fetchone()[0]

            query = "INSERT INTO logs (user_id, action, `table`) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, action, table))
            conn.commit()
        except Error as e:
            print(f"Erreur lors de la création de log : {e}")
        finally:
            cursor.close()
            conn.close()
def create_langage(username):
    nom = input("Entrez le nom du langage : ")
    level = input("Entrez le niveau du langage : ")
    date = input("Entrez la date de création du langage (YYYY-MM-DD) : ")

    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO languages (nom, date_creation, level) VALUES (%s, %s, %s)"
            cursor.execute(query, (nom, date, level))
            conn.commit()
            print(f"Langage '{nom}' ajouté avec succès.")
            insert_log("create", "languages", username)
        except Error as e:
            print(f"Erreur lors de l'ajout du langage : {e}")
        finally:
            cursor.close()
            conn.close()


def delete_language(username):
    print_all_languages()
    language_id = input("Entrez l'ID du langage à supprimer : ")
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM languages WHERE id = %s"
            cursor.execute(query, (language_id,))
            conn.commit()
            print(f"Langage ID {language_id} a été supprimé.")
            insert_log("delete", "languages", username)
        except Error as e:
            print(f"Erreur lors de la suppression du langage: {e}")
        finally:
            cursor.close()
            conn.close()


def update_language(username):
    print_all_languages()
    id = input("Entrez l'ID du langage à mettre à jour : ")
    nom = input("Entrez le nouveau nom du langage : ")
    date_creation = input("Entrez la nouvelle date de création du langage (format YYYY-MM-DD) : ")
    level = input("Entrez la niveau du langage : ")

    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE languages SET nom = %s, date_creation = %s, `level` = %s WHERE id = %s", (nom, date_creation, level, id))
            conn.commit()
            print("Langage mis à jour avec succès.")
            insert_log("update", "languages", username)
        except Error as e:
            print(f"Erreur lors de la mise à jour du langage: {e}")
            return None
        finally:
            conn.close()

def print_all_languages():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nom, date_creation, level FROM languages")
            data = cursor.fetchall()
            if data is not None:
                print("+----------------------------------------+\n"
                      "| Liste des langages                     |\n"
                      "+----------------------------------------+")
                for (id, nom, date_creation, level) in data:
                    print(f"id: {id}, nom: {nom}, date_creation: {date_creation}, niveau: {level}")
            else:
                print("Aucune donnée disponible.")
        except Error as e:
            print(f"Erreur lors de la lecture des utilisateurs: {e}")
            return None
        finally:
            conn.close()

def print_language():
    print_all_languages()
    id = input("Entrez l'ID du langage : ")
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nom, date_creation, level FROM languages WHERE id = %s", (id,))
            data = cursor.fetchone()
            if data is not None:
                print("+----------------------------------------+\n"
                      "| Détails du langage                     |\n"
                      "+----------------------------------------+")
                print(f"id: {data[0]}, nom: {data[1]}, date_creation: {data[2]}, niveau: {data[3]}")
            else:
                print("Aucune donnée disponible pour cet ID.")
        except Error as e:
            print(f"Erreur lors de la lecture du langage: {e}")
            return None
        finally:
            conn.close()

def login():
    user_id = input(
        "+----------------------------------------+\n"
        "| Entrez l'id de votre compte            |\n"
        "+----------------------------------------+\n"
    )

    conn = connection()
    cursor = None
    try:
        cursor = conn.cursor()
        query = "SELECT nom FROM user WHERE id = %s"
        cursor.execute(query, (user_id,))
        data = cursor.fetchone()
        if data is not None:
            print(f"Vous êtes connecté en tant que {data[0]}")
            return data[0]
        else:
            print("Aucun compte trouvé avec cet ID.")
            return None
    except Error as e:
        print(f"Erreur lors de la connexion: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def register():
    username = input(
        "+----------------------------------------+\n"
        "| Entrez votre nom d'utilisateur          |\n"
        "+----------------------------------------+\n"
    )

    conn = connection()
    cursor = None
    try:
        cursor = conn.cursor()
        query = "INSERT INTO user (nom) VALUES (%s)"
        cursor.execute(query, (username,))
        conn.commit()
        print("Votre compte a bien été créé.")
        return username
    except Error as e:
        print(f"Erreur lors de la création du compte: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def unidentified():
    unidentified_input = input(
                "+----------------------------------------+\n"
                "| 1 : Se connecter                       |\n"
                "| 2 : Creer un compte                    |\n"
                "+----------------------------------------+\n"
            )

    options = {
        '1': login,
        '2': register,
    }

    if unidentified_input in options:
        username = options[unidentified_input]()
        return username
    else:
        print("Option non valide, veuillez réessayer.")

def print_logs():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, action, `table` FROM logs")
            data = cursor.fetchall()
            if data is not None:
                print("+----------------------------------------+\n"
                      "| Liste des logs                         |\n"
                      "+----------------------------------------+")
                for (id, user_id, action, table) in data:
                    print(f"id: {id}, utilisateur id: {user_id}, action: {action}, table: {table}")
            else:
                print("Aucune donnée disponible.")
        except Error as e:
            print(f"Erreur lors de la lecture des logs: {e}")
            return None
        finally:
            conn.close()
def main():
    username = None

    while True:
        while username is None:
            username = unidentified()
        else:
            user_input = input(
                "+----------------------------------------+\n"
                "| 1 : Afficher la liste des langages     |\n"
                "| 2 : Afficher un langage                |\n"
                "| 3 : Ajouter un langage                 |\n"
                "| 4 : Modifier un langage                |\n"
                "| 5 : Supprimer un langage               |\n"
                "| 6 : Se déconnecter                     |\n"
                "| 7 : Quitter le programme               |\n"
                "| 8 : Afficher la liste des logs         |\n"
                "+----------------------------------------+\n"
            )
            print(user_input)

            options = {
                '1': print_all_languages,
                '2': print_language,
                '3': lambda: create_langage(username),
                '4': lambda: update_language(username),
                '5': lambda: delete_language(username),
                '7': exit,
                '8': print_logs
            }

            if user_input == '6' :
                username = None
            elif user_input in options:
                options[user_input]()
            else:
                print("Option non valide, veuillez réessayer.")

main()



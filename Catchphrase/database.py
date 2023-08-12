import sqlite3
import random

def contains_chars(input_string, chars_to_check):
    return any(char in input_string for char in chars_to_check)

### For quizlet format
def extract_terms(str):
    terms = []
    list = str.splitlines()
    for i in list:
        seperated = i.split(" ")
        seperated = seperated[1:]
    
        tmp_term = ""
        for j in seperated:
            if not contains_chars(j, [":"]):
                tmp_term += " " + j
            else:
                tmp_term += " " + j[:len(j) - 1]
                terms.append(tmp_term.strip())
        
    return terms

### For lists seperated by commas
def extract_by_commas(str):
    terms = []
    split = str.split(",")
    for word in split:
        tmp = word.strip()
        if tmp:
            terms.append(tmp)
    
    return terms






### Database interaction

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect("Catchphrase/" + db_file)
    except:
        print("Failed to connect")

    return connection

def check_category(connection, category):
    # create cursor
    cursor = connection.cursor()

    # get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    categories = []
    for cat in tables:
        categories += cat

    # check if category exists, create if not
    if category not in categories:
        cursor.execute("CREATE TABLE " + category + " (id INTEGER PRIMARY KEY, word TEXT);")
    
def insert_word(connection, category, word):

    # see if category exists
    check_category(connection, category)

    # create cursor
    cursor = connection.cursor()

    sql = "INSERT INTO " + category + " (word) VALUES ('" + word + "');"
    cursor.execute(sql);

    ### Commit
    connection.commit()
    cursor.close()
    


def main():
    database_name = "first_database.db"
    category_name = "CardsAgainstHumanity"
    
    ### For data scraped from quizlet
    str = """


    """

    file1 = open(r"C:\Users\deang\OneDrive\Desktop\Catchphrase Cats/CAH2.txt", "r")
    x = file1.read()
    words = extract_terms(x)



    
    
    # connection = create_connection(database_name)


    # # ### call insert_word for each term
    # for i in range(len(words)):
    #     insert_word(connection, category_name, words[i])


    # ### Close connection
    # if connection:
    #     connection.close()



if __name__ == '__main__':
    main()
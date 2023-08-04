import sqlite3

x = """1. Los Angeles: What city is nicknamed the City of Angels?
2. Las Vegas: What city is nicknamed Sin City?
3. Chicago: What city is nicknamed the Windy City?
4. New York City: What city is nicknamed the Big Apple?
5. California: What state is nicknamed the Golden State?"""


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
        cursor.execute("CREATE TABLE " + category + " (word TEXT);")
    
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
    database_name = "words.db"
    category_name = "TESTCAT1"
    
    ### For data scraped from quizlet
    str = """


    """

    # file1 = open(r"C:\Users\deang\OneDrive\Desktop\Catchphrase Cats/Random.txt", "r")
    # x = file1.read()
    # words = extract_terms(x)
    
    connection = create_connection(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) AS total_items FROM TESTCAT1")
    len = cursor.fetchall()
    print(int(len[0][0]))

    # ### call insert_word for each term
    # for i in range(len(words)):
    #     insert_word(connection, category_name, words[i])





    ### Close connection
    if connection:
        connection.close()



if __name__ == '__main__':
    main()
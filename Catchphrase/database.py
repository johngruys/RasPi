import sqlite3 as sql


def splice_words(input):
    listed = input.split(" ")
    return listed


x = """1. Los Angeles: What city is nicknamed the City of Angels?
2. Las Vegas: What city is nicknamed Sin City?
3. Chicago: What city is nicknamed the Windy City?
4. New York City: What city is nicknamed the Big Apple?
5. California: What state is nicknamed the Golden State?"""

def contains_chars(input_string, chars_to_check):
    return any(char in input_string for char in chars_to_check)

def term(i):
    str = ""
    seperated = i.split(" ")[1:]
    # seperated = seperated
    # print(seperated)
    for j in seperated:
        if not contains_chars(j, [":"]):
            str += j
        else:
            str += j[:len(j) - 1]
            return str

print(term("Hello there:"))

split = x.splitlines()
# print(split)


list = []
# for i in split:
    # print(i)
    # list += term(i)

# print(list)
    

    

# connection = sql.connect("words.db")

# print(connection.total_changes)

# cursor = connection.cursor()

# animals = cursor.execute("SELECT * FROM cat1").fetchall()

# print(animals)
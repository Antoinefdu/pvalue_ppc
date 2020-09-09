import sqlite3 as sql
import csv
import functions

'''Please run this script first. 
    Steps : 
        1 - Replace ":memory:" below with the name of a new database (e.g.: "Ad_test5.db")
        2 - Run the script
        3 - Press "C" to continue, then "Enter" 
        4 - Press "Y", then "Enter"
        5 - We need to change the characteristics of a few table columns before creating the next table:
            5.1 - Press "E" to edit, then "Enter"
            5.2 - Type "impressions", then "Enter"
            5.3 - Type "int", or "integer", then "Enter"
                NOTE : you can use this to update not only the data type, but any other column property (autoincrement, not null, etc)
            5.4 - Press "E" to edit, then "Enter"
            5.5 - Type "clicks", then "Enter"
            5.6 - Type "int", or "integer", then "Enter"
            5.7 - Press "E" to edit, then "Enter"
            5.8 - Type "ctr", then "Enter"
            5.9 - Type "real", or "float", then "Enter"
        6 - Press "C" to continue, then "Enter" 
        7 - Press "Y", then "Enter"
        
    Next up : fill_tables.py
        
'''


conn = sql.connect(':memory:')  # connection to DB. Write the name of your DB or ":memory:" for tests
c = conn.cursor()

#  below is the code that actually initialise the database and creates the first tables.
#  It will only run if this file is executed directly (i.e. not if it's called by another file)
if __name__ == '__main__':
    # Create DB table for Ad Groups
    functions.create_table(c, 'Ad Groups', {'Campaign Name': 'TEXT', 'Ad Group Name': 'TEXT'})
    print()

    # Open reader to extract a list of headers & create table based on it
    with open('Ad_Report2.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Removing all "Responsive Search Ad" from headers
        # headers = [x for x in next(csv_reader) if x.startswith('Responsive Search Ad') is False]
        headers = [x for x in next(csv_reader)]
        # Creating a table with each header as a text column
    dict_columns = {k: v for k, v in zip(headers, ('' for x in range(len(headers))))}
    functions.create_table(c, 'Ads', dict_columns)


c.close()

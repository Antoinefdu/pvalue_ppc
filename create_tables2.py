import sqlite3 as sql
import csv
import functions

conn = sql.connect('Ads_test2.db')  # connection to DB. Write "Ads_test.db" or ":memory:" for tests
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

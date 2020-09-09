import sqlite3 as sql
import csv
import functions

conn = sql.connect('Ads_test.db')  # connection to DB. Write "Ads_test.db" or ":memory:"
c = conn.cursor()

# Filling the AG table
# Opening the reader to extract each unique pair of [Campaign + Ad Group] and use it to create a table
with open('Ad_Report2.csv', 'r') as csv_file:
    csv_dict_reader = csv.DictReader(csv_file)
    for row in csv_dict_reader:
        if functions.check_if_exists(c, 'Ad_Groups', {'CAMPAIGN_NAME': row['Campaign'], 'AD_GROUP_NAME': row['Ad group']}):
            continue
        else:
            functions.add_item(conn, c, 'Ad_Groups', {'CAMPAIGN_NAME': row['Campaign'], 'AD_GROUP_NAME': row['Ad group']})

# Filling the Ads table
# Opening the reader to extract content and dumping into DB
with open('Ad_report2.csv', 'r') as csv_file:
    csv_dict_reader = csv.DictReader(csv_file)
    no_duplicate_found = True
    for row in csv_dict_reader:
        keys = list(row.keys())
        # We don't want to include Responsive search ads in our P-Value calculator,
        # so if one of those appears, we will break the inner loop (line 30)
        # then continue the outer loop (on line 38)
        for item in keys:
            if item.startswith("Responsive Search Ad") and row[item] != ' --':
                break
        else:
            if functions.check_if_exists(c, 'Ads', row):
                continue
            else:
                functions.add_item(conn, c, 'Ads', row)
                no_duplicate_found = False
                print(row)
        continue
    if no_duplicate_found:
        print("All ads already in the DB. Nothing has been added")


c.close()



    # with open('New_Ad_Report.csv', 'w', newline='') as new_csv:  # Open writer
    #     csv_writer = csv.DictWriter(new_csv, fieldnames=headers)
    #     csv_writer.writeheader()
    #     for row in csv_dict_reader:
    #         keys = list(row.keys())
    #         for item in keys:
    #             if item.startswith("Responsive Search Ad"):
    #                 del row[item]
    #         csv_writer.writerow(row)


'''c.execute("SELECT * FROM Ads")
for x in c.fetchall():
    print(x)

print(check_if_exists('Ads', {'Headline_1': 'Conference Calling Made Better', 'Headline 2': 'With PowWowNowâ„¢', 'Id': 3}))
c.close()'''





'''def create_table(table, d_columns):  # d_columns in format {Column_name : Attribute}, e.g.: {Id : INTEGER AUTOINCREMENT}
    table = str(table.replace(" ", "_").title())
    d = reformat_column_name(d_columns)
    add = ''
    for k, v in d.items():
        add += f'{k} {str(v).upper()}, '
    add = add[:-2]
    c.execute(f"CREATE TABLE {table} (ID INTEGER PRIMARY KEY AUTOINCREMENT, "+add+");")


# Create DB table for Ad Groups
if __name__ == '__main__':
    create_table('Ad Groups', {'Campaign Name': 'TEXT', 'Ad Group Name': 'TEXT'})
    c.execute("PRAGMA table_info('Ad_Groups')")

# Open reader to extract a list of headers
with open('Ad_Report.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Removing all "Responsive Search Ad" from headers
    headers = [x for x in next(csv_reader) if x.startswith('Responsive Search Ad') is False]

# Creating a table with each header as a text column
dict_columns = {k: v for k, v in zip(headers, ('' for x in range(len(headers))))}

create_table('Ads', dict_columns)
c.execute("PRAGMA table_info('Ads')")
df = pd.DataFrame(c.fetchall(), columns=['ID', 'Name', 'Type', 'NotNull', 'Default_Val', 'Key'])
print(df)'''
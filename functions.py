import re
import pandas as pd
import math


def reformat_column_name(d):  # makes sure that the column names in the function below are written in a SQL-compatible format
    return {str(k.replace(" ", "_").upper()): v for k, v in d.items()}
# TODO find usages for this and make sure this function is really needed
# TODO check if it is not better to pass conn as a parameter instead of the cursor


def reformat_string_for_fetch_query(s):
    if type(s) == int or type(s) == float:
        return s
    s = reformat_string_for_insert_query(s)
    s = "\'"+s.replace("'", "''")+"\'" if isinstance(s, str) else s
    return s


def reformat_string_for_insert_query(s):  # differentiates strings from floats and transforms % into decimals
    if type(s) == int or type(s) == float:
        return s
    if re.search('[a-zA-Z]', str(s)) is None:
        s = s.replace(',', '')
    pattern = re.compile(r'^(\d+|\d+[.]\d+)%?$')
    if bool(re.match(pattern, str(s))):
        s = round(float(s[:-1])/100, 5) if s[-1] == '%' else float(s)
    return s


def manually_edit_dict(d, d_name, keys_formating_fct=lambda x: x, values_formating_fct=lambda x: x):
    d_copy = d
    while True:
        choice1 = ''
        while choice1 not in ['A', 'E', 'R', 'C']:
            print(d_name, '(dictionary):')
            for k, v in d_copy.items():
                print(f'\t{k}: {v}')
            choice1 = input(f'Would you like to \n\
            [A]dd an item, \n\
            [E]dit an item, \n\
            [R]emove an item, or \n\
            [C]ontinue?').title()
        if choice1 == 'A':
            new_item = input('Enter a new Key-Value pair in the following format "key:value". Value can be left blank.')
            if new_item != '' and ':' in new_item[1:]:
                reformated_param = new_item.split(':')
                k, v = keys_formating_fct(reformated_param[0]), values_formating_fct(reformated_param[1])
                d_copy[k] = v
            continue
        elif choice1 == 'E':
            edit_key = ''
            while edit_key not in d_copy.keys():
                edit_key = keys_formating_fct(input('Write the key of the item you wish to edit (non case sensitive)'))
            edit_value = values_formating_fct(input(f'Write the new value for the key {edit_key}'))
            d_copy[edit_key] = edit_value
            continue
        elif choice1 == 'R':
            remove_key = ''
            while remove_key not in d_copy.keys():
                remove_key = keys_formating_fct(input('Write the key of the item you wish to remove (non case sensitive)'))
            del d_copy[remove_key]
            continue
        break
    return d_copy


def create_table(cursor, table, d_columns):  # d_columns in format {Column_name : Attribute}, e.g.: {Id : INTEGER AUTOINCREMENT}
    table = str(table.replace(" ", "_").title())
    d = reformat_column_name(d_columns)
    d['ID'] = 'INTEGER PRIMARY KEY AUTOINCREMENT'
    print(f'New table: {table}')
    print()
    d = manually_edit_dict(d, 'Parameters', keys_formating_fct=lambda x: x.replace(" ", "_").upper(),
                           values_formating_fct=lambda x: x.replace(" ", "_").upper())
    add = ''
    for k, v in d.items():
        add += f'{k} {str(v).upper()}, '
    add = add[:-2]
    if input(f'You are about to create a new table called {table}.\n'
             f"SQL Query = 'CREATE TABLE {table} ({add});'\n"
             f'Confirm? (Y/N)').title() == 'Y':
        cursor.execute(f"CREATE TABLE {table} ({add});")
        cursor.execute(f"PRAGMA table_info('{table}')")
        print(pd.DataFrame(cursor.fetchall(), columns=['ID', 'Name', 'Type', 'NotNull', 'Default_Val', 'Key']))
        print()


def check_if_exists(cursor, table, d_attributes):
    d = reformat_column_name(d_attributes)
    i = 0
    add = ''
    for k, v in d.items():
        v = reformat_string_for_fetch_query(v)
        where_or_and = 'WHERE' if i == 0 else ' AND'
        add += f'{where_or_and} {str(k)} = {v}'
        i += 1
    cursor.execute(f"SELECT * FROM {table} "+add+';')
    return False if cursor.fetchone() is None else True


def add_item(connect, cursor, table, d):
    d = reformat_column_name(d)
    columns_names = ', '.join([k for k in d.keys()])
    substitutes = ', '.join('?' for x in range(len(d.values())))
    values = [reformat_string_for_insert_query(v) for v in d.values()]
    with connect:
        cursor.execute(f"INSERT INTO {table} ({columns_names}) VALUES ({substitutes})", values)


def all_tables_in_db(cursor):
    cursor.execute('SELECT name FROM sqlite_master WHERE type = :type and name NOT LIKE :cond1', {'type': 'table',
                                                                                          'cond1': 'sqlite_%'})
    pragma_df = pd.DataFrame(cursor.fetchall(), columns=['Name'])
    return pragma_df


def fetch_data_with_condition(cursor, table_object, d_attributes):
    table_keys = table_object.keys
    d_attributes = reformat_column_name(d_attributes)
    i = 0
    add = ''
    for k, v in d_attributes.items():
        v = reformat_string_for_fetch_query(v)
        where_or_and = 'WHERE' if i == 0 else 'AND'
        add += f'{where_or_and} {str(k)} = {v}'
        i += 1
    cursor.execute(f"SELECT * FROM {table_object.name} "+add+';')
    dataframe = pd.DataFrame(cursor.fetchall(), columns=table_keys)
    return dataframe


def fetch_data_with_condition2(cursor, table_object, dict_conditions, columns_tuple=tuple('*')):
    columns = ','.join(columns_tuple)
    table_keys = table_object.keys if columns_tuple == '*' else columns_tuple
    dict_conditions = reformat_column_name(dict_conditions)
    i = 0
    add = ''
    for k, v in dict_conditions.items():
        v = reformat_string_for_fetch_query(v)
        where_or_and = 'WHERE' if i == 0 else 'AND'
        add += f'{where_or_and} {str(k)} = {v}'
        i += 1
    cursor.execute(f"SELECT {columns} FROM {table_object.name} "+add+';')
    dataframe = pd.DataFrame(cursor.fetchall(), columns=table_keys)
    return dataframe


def convert_to_int(data):
    output = float(data.replace(',', '')) if isinstance(data, str) else data
    return int(output)
# TODO check if redundant with convert for insert function


def safe_division(numerator, denominator):
    return 0 if denominator == 0 else round(numerator/denominator, 10)


def standard_error_of_mean(mu, N):
    return math.sqrt(safe_division(mu * (1 - mu), N))


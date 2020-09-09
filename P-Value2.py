import sqlite3 as sql
import pandas as pd
import functions
from scipy import stats
import math

'''Please run "create_tables2.py" and "fill_tables.py" BEFORE running this script. 
    Steps : 
        1 - Replace ":memory:" below with the name of the database you have previously created
        2 - Run the script
        3 - Choose your alpha level, or leave blank, then press "Enter"
        3 - That's it
        
        If everything went well, and if you chose 0.05 as your alpha, 
        you should see the stats of 4 ad groups appear in the console with P-values of:
            0.00000
            0.00000
            0.01609
            0.00029
'''


class TableObject:
    def __init__(self, name):
        self.name = name
        self.pragma_info = self.get_pragma_info()
        self.keys = self.pragma_info['Name']

    def __repr__(self):
        return self.name

    def get_pragma_info(self):
        c.execute(f"PRAGMA table_info('{self.name}')")
        pragma_df = pd.DataFrame(c.fetchall(), columns=['ID', 'Name', 'Type', 'NotNull', 'Default_Val', 'Key'])
        return pragma_df


class ads_stats:
    def __init__(self, id, impressions, clicks):
        self.id = id
        self.impressions = int(impressions)
        self.clicks = int(clicks)
        self.ctr = functions.safe_division(self.clicks, self.impressions)
        self.sem = functions.standard_error_of_mean(self.ctr, self.impressions)

    def calculate_mu(self):
        return self.clicks/self.impressions if self.impressions != 0 else 0


keep_asking = True
while keep_asking:
    alpha = input('Please enter a significance level that is between 0 and 0.5 (excluded), or press "Enter" to keep the default value (0.05)') or 0.05
    try:
        alpha = float(alpha)
        keep_asking = False if 0 < alpha < 0.5 else True
    except ValueError:
        continue

# connecting to DB
conn = sql.connect('ad_test2.db')  # connection to DB. You know what to do.
c = conn.cursor()

#  creating a list of all the tables in our DB. Turning each table into a table object
table_dict = {}
for tablename in functions.all_tables_in_db(c)['Name']:
    table = TableObject(tablename)
    table_dict[tablename] = TableObject(tablename)

# for each ad group in our AG table, find the corresponding ads in our Ads table and display them in pd.dataframe
c.execute('SELECT CAMPAIGN_NAME, AD_GROUP_NAME FROM Ad_Groups')
for ad_group in c.fetchall():
    campaign_name, ag_name = ad_group[0], ad_group[1]
    df = functions.fetch_data_with_condition2(c, table_dict['Ads'], {'AD_GROUP': ag_name, 'CAMPAIGN': campaign_name}, ('ID', 'IMPRESSIONS',
                                                                                                                       'CLICKS'))
    # transforming our query result into a list of "ad_stats" objects
    ad_list = []
    for index, row in df.iterrows():
        id = row[0]
        imp = functions.convert_to_int(row[1])
        clk = functions.convert_to_int(row[2])
        ad = ads_stats(id, imp, clk)
        ad_list.append(ad)

    # calculating z-score and p-values
    if len(ad_list) == 2:
        control_group = ad_list[0]
        alt_group = ad_list[1]
        ttest = functions.safe_division(-abs(control_group.ctr - alt_group.ctr), math.sqrt(control_group.sem**2+alt_group.sem**2))
        pval = stats.norm.cdf(ttest)

        '''for the data analysts among you, I know, p-value alone is not enough to determine the validity of a test, 
        we must also ensure that we have a large enough sample size. Considering a base rate of 0.04, an MDE (relative) of 0.005, 
        an alpha of 0.05 and a statistical power of 0.8 I calculated that it should be around 25,000.'''

        # if p-value criteria are met, displaying the results on console
        if pval <= alpha and df['IMPRESSIONS'].sum() >= 25000:
            df.insert(3, 'CTR', ['{:.2%}'.format(ad.ctr) for ad in ad_list], True)
            df.insert(4, 'SEM', ['{:.2%}'.format(ad.sem) for ad in ad_list], True)
            print(f'{campaign_name} | {ag_name}')
            print(df)
            print('T-Test:', ttest)
            print('P-Value', '{:.5f}'.format(pval))
            print()

c.close()

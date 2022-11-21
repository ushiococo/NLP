import pandas as pd
from pathlib import Path
import fuzzywuzzy as fw
import fuzzymatcher as fm
import recordlinkage as rl
from datetime import datetime
import dask.dataframe as dd



# data_details.drop("Record", axis=1, inplace=True)

# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth',None)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

client_details = pd.read_csv('yytest.csv')
data_details =pd.read_csv('data_new.csv')
print(client_details.head(2))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print(data_details.head(2))


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#declare the left_on and right_on that is common between the 2 dataset, need to be same equal amount of entity
# eg left_on got 4 entity, right_on also need to have 4 entity
left_on = ["client"]

right_on = ["ipAddress"]

now = datetime.now()
print("Start " + str(now))
matched_results = fm.fuzzy_left_join(client_details,
                                               data_details,
                                               left_on,
                                               right_on,
                                               left_id_col='ID',
                                               right_id_col='Record')
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(matched_results.head())
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print("# Reorder the columns to make viewing easier. Here we put client ID and Record ID together")
cols = ["best_match_score","ID","client","Record","ipAddress","hostname", "alias_list","address_list","content-length","url","User-Agent","HTTPMethods","HTTPVersion","datetime"]
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print("# Check the best matches")

rearranged_best_matches=matched_results[cols].sort_values(by=['best_match_score'], ascending=False)
print(rearranged_best_matches.head())

# rearranged_best_matches.drop("ipAddress", axis=1, inplace=True)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print("# Check the worst 3 matches")
rearranged_worst_matches=matched_results[cols].sort_values(by=['best_match_score'],
                                  ascending=True)
print(rearranged_worst_matches.head())
current_time = datetime.now() - now
print("duration:", current_time)
    # best_match = rearranged_best_matches['best_match_score'].astype(float)
rearranged_best_matches.to_csv('best2.csv')
# for items in rearranged_best_matches.iteritems():
#     #     # print(items[0]) #header
#     # print(items)
#     print(items[1])
#     print("hello")
#     if (items[1]) > 0.0:
#         rearranged_best_matches.to_csv('best3.csv')
    #     # else:
        #     rearranged_worst_matches.to_csv('worst.csv')
    # print(best_match)
    # print(type(best_match))
    # if best_match.gt 0.0:
    #     rearranged_best_matches.to_csv('best2.csv')
    # else:
    #     rearranged_worst_matches.to_csv('worst.csv')

# if user_input ==2:
#     print("RecordLinkage")
#     client_details = pd.read_csv('yytest4.csv',index_col='ID')
#
#     data_details = pd.read_csv('data_new.csv', index_col='Record')
#
#     print(client_details.head(2))
#
#     print(data_details.head(2))
#
#     # Build the indexer
#
#     indexer = rl.Index()
#     # use full or block
#     # indexer.full()
#     indexer.block(left_on='client', right_on='ipAddress')
#
#     #use sortedneighbor as a good option if data is not clean
#     indexer.sortedneighbourhood(left_on='client', right_on='ipAddress')
#
#     candidates = indexer.index(client_details, data_details)
#     #with block state, candidates will be filtered to only include thse where the state values are the same.
#     print(len(candidates))
#
#     #comparing part
#     compare = rl.Compare()
#     compare.exact('client', 'ipAddress', label='client')
#     compare.string('client','ipAddress', threshold=0.85, label="ipAddress")
#
#     features = compare.compute(candidates, client_details, data_details)
#     # print(features)
#
#     #test the similarities
#
#     features.sum(axis=1).value_counts().sort_index(ascending=False)
#
#     #potential matches
#     potential_matches = features[features.sum(axis=1) > 1].reset_index()
#
#     potential_matches['Score'] = potential_matches.loc[:, 'client':'ipAddress'].sum(axis=1)
#     print(potential_matches.head(10))
#
#     print(client_details.loc[5,:])
#     print(data_details.loc[374845,:])
#
#     #joining
#     client_details['ClientIP_lookup'] = client_details[['client']].apply(lambda x: ''.join(str(x), axis=0))
#     data_details['IP_lookup'] = data_details[['ipAddress']].apply(lambda x: ''.join(str(x),axis=0))
#
#     client_lookup = client_details[['ClientIP_lookup']].reset_index()
#     data_lookup = data_details[['IP_lookup']].reset_index()
#
#     client_merge = potential_matches.merge(client_lookup, how='left')
#     print(client_merge.head(2))
#
#     final_merge = client_merge.merge(data_lookup,how='left')
#     # final_merge = client_details.merge(data_details, how='left')
#     cols = ["ID","client","Record","ipAddress","hostname", "alias_list","address_list","content-length","url","User-Agent","HTTPMethods","HTTPVersion","datetime"]
#     final_merge[cols].sort_values(by=['ID','Score'], ascending=False)
#     print(final_merge.head())

#https://pbpython.com/record-linking.html
# https://towardsdatascience.com/plotly-dashboards-in-python-28a3bb83702c
# https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/#:~:text=Different%20column%20names%20are%20specified,to%20the%20pandas%20merge%20function.
# https://pnut2357.github.io/data-matching/
# https://www.geeksforgeeks.org/how-to-print-an-entire-pandas-dataframe-in-python/
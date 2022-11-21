import pandas as pd
# pd.set_option("display.max_columns", None)
import csv

# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth',None)
data = pd.read_csv('Book1.csv', header=None)


with open('Book1.csv','r') as file1:
    #list all the columns
    data.columns = ['col1','col2','col3', 'col4','col5','col6', 'col7','col8','col9','col10','col11']
    #drop data with no values '-'
    data.drop(["col2", "col3","col11"], axis=1, inplace=True)
    #combine the datetime
    data["datetime"] = data['col4'] + data['col5']
    #remove the data after merge
    data.drop(["col4", "col5"], axis=1, inplace=True)



    # print(data["datetime"])
    #rename the data column
    data.columns = ['ipAddress','HTTPMethods', 'HTTPStatus','content-length','url','User-Agent','datetime']
    # data.columns = ['ip_address','datetime','HTTPMethods', 'url','HTTPStatus','content-length', 'User-Agent']


print(data.head())
data.drop(labels=0, axis=0, inplace=True)

# x = str(data['HTTPMethods'].values[0]).split("/") # split with /
# print(x[0]) / Retrieve 'GET' Values
y = str(data['HTTPMethods'].values[0]).split(" ") # split with space
# print(y[2])


a = str(data['User-Agent'].values[0]).split(" ")
# print(a[0])

# print(x)

# Type_new = pd.Series([])
methods =[]
ver = []
agent = []
url = []
for i in range(len(data)):
    x = str(data['HTTPMethods'].values[i]).split("/")
    # print(x)
    # print(x[0])
    methods.append(x[0])
# print(methods)
for j in range(len(data)):
    x = str(data['HTTPMethods'].values[j]).split(" ")
    ver.append(y[2])

# print(z[0])
for l in range(len(data)):
    a = str(data['User-Agent'].values[l]).split("(")
    agent.append(a[0])
    # url.append(z1[1])
for k in range(len(data)):

    z = str(data['url'].values[k].split("%"))
    z = z.split("'")
    # print(z[1])
    # z =str(data['url'].values[k])
    # print(t)
    url.append(z[1])
# print(ver)
# Type_new.append(x[0])

# if data["HTTPMethods"][i] != " ":
#         print(x[0])
#         Type_new[i] = x[0]

#insert value into dataframe
# data.insert(1, 'HTTPMeth0ds', x[0])
# data.insert(2, 'HTTPVersion', y[2])
data.drop(["HTTPMethods"], axis=1, inplace=True)
# creating a list for new column
Methods = methods
Vers = ver
Agent =agent
Url =url
data['HTTPMethods'] = Methods
data['HTTPVersion'] = Vers
data['User-Agent'] = Agent
data['url'] = Url
# LABEL1 = ['Record', 'ipAddress', 'HTTPStatus', 'content-length', 'url', 'User-Agent',' datetime', 'HTTPMethods', 'HTTPVersion']

print(data.head())

data.to_csv('data_new.csv')

# edit header
data = []
with open('data_new.csv', 'r', newline='') as csvfile:
    read_file = csv.reader(csvfile)
    count = 0
    for i in read_file:
        if count == 0:
            header = ['Record', 'ipAddress', 'HTTPStatus', 'content-length', 'url', 'User-Agent','datetime', 'HTTPMethods', 'HTTPVersion']
            data.append(header)
        else:
            data.append(i)
        count += 1
with open('data_new.csv', 'w', newline='') as csvfile:
    write_file = csv.writer(csvfile)
    for i in data:
        write_file.writerow(i)

print("done")
# writer2=csv.DictWriter(file1,delimiter=',', fieldnames=LABEL1)

# data1 = pd.read_csv('data_new.csv')
# data1.columns =data1.columns.str.replace('Unnamed: 0','Record')
# data1.drop(columns=data1.columns[0],axis=1, inplace=True)
# print(data1)
# data1.to_csv('data_new.csv')

# xx = str(data['HTTPMethods'].values[1]).split("/")
# yy = str(data['HTTPMethods'].values[1]).split(" ")
# print(xx[0])
# print(yy[2])





# https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-pandas-dataframe
# https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
# https://www.statology.org/pandas-rename-columns/
# https://www.shanelynn.ie/pandas-drop-delete-dataframe-rows-columns/
#https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
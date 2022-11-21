# from __future__ import unicode_literals, print_function
# import plac
import csv
from distutils.file_util import write_file
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.training import Example
from spacy.util import minibatch, compounding
from spacy import displacy
from tkinter.filedialog import askopenfilename
from spacy.pipeline import EntityRuler
from spacy.scorer import Scorer
from collections import Counter
from csv import writer
import pandas as pd
from datetime import datetime
import numpy as np
import glob
import os
import sys


def has_data_rows(fname):
    with open(fname) as file:
        return file.readline() and file.readline()


def evaluate(ner_model, examples):
    scorer = Scorer()
    example = []
    for input_, annot in examples:
        pred = ner_model(input_)
        temp = Example.from_dict(pred, annot)
        example.append(temp)
        scores = scorer.score(example)
    return scores


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start

print("manipulating CSV, choose option 1-2 \n 1: Test data and store in csv \n 2: Truncate csv")

user_input = int(input("Enter 1 or 2 " ))
if user_input == 1:
    path2 = askopenfilename(title="Select file to test", filetypes=(("text files", "*.txt"), ("all files", "*")))

# path2="C:\\Users\\qiaoyan.ooi\\Downloads\\CapstoneFYP-main\\test2.txt"
    try:
        with open(path2, 'r') as f:
            lines = f.readlines()
        TEST_DATA = []
        # TRAIN_DATA = []
        edge_case = []
        LABEL = ["client", "hostname", "alias_list", "address_list"]
        for i in lines:
            try:
                i = i.replace(" ", " ").replace("\n", "").replace("\t", " ")
                splitted = i.split(" ")
                # print(splitted)
                count = 0
                # labels = ["client", "hostname", "alias_list", "address"]
                entity = {}
                entity_list = []
                if "Unknown host" not in i:
                    for each in splitted:
                        start_position = i.index(each)
                        end_position = int(start_position) + int(len(each))
                        labels = LABEL[count]
                        entry = (start_position, end_position, labels)
                        entity_list.append(entry)
                        # print(entry)
                        count += 1
                else:
                    for each in splitted:
                        # print(each)
                        # print(count)
                        if count == 0:
                            start_position = i.index(each)
                            end_position = int(start_position) + int(len(each))
                            # print(count)
                            labels = LABEL[count]
                            entry = (start_position, end_position, labels)
                            entity_list.append(entry)
                        if count == 1:
                            start_position = find_nth(i, each, 2)
                            end_position = int(start_position) + int(len(each))
                            # print(count)
                            labels = LABEL[count]
                            entry = (start_position, end_position, labels)
                            entity_list.append(entry)
                        if count == 2:
                            each = each + " 1] Unknown host"
                            # print("ji",each)
                            start_position = i.index(each)
                            end_position = int(start_position) + int(len(each))
                            # print(count)
                            labels = LABEL[count]
                            entry = (start_position, end_position, labels)
                            entity_list.append(entry)
                        count += 1

                # print(entity_list)
                entity["entities"] = entity_list
                row = (i, entity)
                # print(row)
                TEST_DATA.append(row)
                # TRAIN_DATA.append(row)
                # print(row)
            except:
                edge_case.append(i)
        print("---------------------------------------------------------------------------------------------")
        print("DATA: \n")
        print(TEST_DATA)
        print("ok")
    except FileNotFoundError:
        print("Sorry, the file " + path2 + " does not exist")
    # output_dir=Path("C:\\Users\\qiaoyan.ooi\\Desktop\\nl\\test")
    # output_dir=Path("C:\\Users\\qiaoyan.ooi\\Downloads\\CapstoneFYP-main\\test")
    # output_dir=Path("C:\\Users\\Qiaoyan\\Downloads\\CapstoneFYP\\test")
    output_dir = Path("C:\\Users\\qiaoyan.ooi\\Desktop\\NLP-main\\trainmodel")

    # load the model

    print("Test the train model")
    print("Loading from", output_dir)

    # path2 = askopenfilename(title="Select file to read", filetypes=(("text files","*.txt"),("CSV files","*.csv"),("all files", "*")))
    # path2 ="C:\\Users\\Qiaoyan\\Downloads\\CapstoneFYP\\client_hostname2.txt"

    with open(path2, "r", encoding='utf-8') as f1:
        content1 = f1.readlines()
        y = []
        for content1 in content1:
            content1 = content1.replace("\t", " ")
            content1 = content1.replace("\n", " ")
            y.append(content1)
        print("~~~~~~~~~~~")
        y = ''.join((y))

        nlp = spacy.load(output_dir)
        nlp.max_length = len(content1) + 100000000000000000000000

        doc = nlp(str(y))
        # print(doc)

        print("-------------------------------------------")

        for ent in doc.ents:
            print(ent.label_, ent.text)

        print("---------------------------------------------------------------------------------------------")

        print("parsing the text file and train to store as csv\n")

        # path2="C:\\Users\\Qiaoyan\\Downloads\\archive (8)\\CapstoneFYP2\\test2.txt"
        # user_input = int(input("Enter 1 or 2"))
        with open(path2, 'r') as file:
            lines2 = file.readlines()
            print(str(len(lines2)) + " records")
                # lines2 = (''.join(lines2))
                # lines2 = ''.join((lines2).replace("\t", " ").replace("\n", "\n"))
        x = "yytest.csv"
        path = x
        isFile = os.path.isfile(path)
        if isFile:
            df = pd.read_csv(x, error_bad_lines=False, header=0)
        else:
            print("Create csv file")
            with open(x, 'w', newline='') as file1:
                LABEL1 = ['client', 'hostname', 'alias_list', 'address_list']
                        # write the csv file
                writer = csv.writer(file1)
                writer2 = csv.DictWriter(file1, delimiter=',', fieldnames=LABEL1)
                writer2.writeheader()
            file1.close()
        df = pd.read_csv(x, error_bad_lines=False, header=0)
        if 'ID' in df.columns:
            df = df.drop('ID', axis=1)
        else:
            print(df)
        for text in tqdm(lines2):
                    # id = int(id)+1
            text = ''.join(text).replace("\t", " ").replace("\n", "")
            doc = nlp(text)
            nlp.max_length = len(text) + 100000000
            new_row = {}
            count = 0
            max_id = 0
            param = [(ent.label_, ent.text) for ent in doc.ents]
            # print(i)
            for i in param:
                count += 1
                if i[1] not in new_row:
                    new_row[i[0]] = i[1]
                else:
                    new_row[i[0] + " "] = i[1]
                if count == len(param):
                    df = df.append(new_row, ignore_index=True)
            print("okay")
            df.to_csv(x, encoding="utf-8")

        # edit header
            data = []

            with open(x, 'r', newline='') as csvfile:
                        read_file = csv.reader(csvfile)
                        count = 0
                        for i in read_file:
                            if count == 0:
                                header = ['ID', 'client', 'hostname', 'alias_list', 'address_list']
                                data.append(header)
                            else:
                                data.append(i)
                            count += 1
            with open(x, 'w', newline='') as csvfile:
                write_file = csv.writer(csvfile)
                for i in data:
                    write_file.writerow(i)

        now = datetime.now()
        print(now)
        print("RESULT1: \n")
        results1 = evaluate(nlp, TEST_DATA)

        print(str(results1) + "\n")
        print("Precision score is: ", results1['ents_p'])
        print("Recall score is: ", results1['ents_r'])
        print("f1 score is: ", results1['ents_f'])
                # #ents_p is average precision score of the model for all entities
                # # ents_r is average recall score of the model for all entities
                # # ents_f is average f1 score of the model for all entities
        ent1 = []
        for x in TEST_DATA:
                    ent1 += [i[-1] for i in x[1]['entities']]

        print(Counter(ent1))
        current_time = datetime.now() - now
        print("duration:", current_time)
        print("ok")
    # csv.field_size_limit(limit)
if user_input == 2:
    user_input2 = input("confirm clear?")
    if user_input2 == 'ok':
        with open('yytest.csv', 'w') as f2:
            f2.truncate()
    if user_input2 =='no':
        print("bye")
        sys.exit()


# print(df)
# df.columns = ['text', 'label']
# df.to_csv('Trained_data.csv')


# if precision is 1 == good classifier (Postitive predictive value)
# precision becomes 1 when TP = TP +FP, FP = 0
# TP/ TP+FP

# print(results['ents_p']*100)

# if recall is 1 == good classfier (True positive value)
# recall becomes 1 when TP = TP +FN ,= FN
# TP / TP + FN

# f1 score = precision and recall (more accuracy of the model)
# f1 score = 1, means FP and FN = 0
# f1 =1 ,when precision and recall =1

# nlp2.to_disk(output_dir)


# Calculate sample size

# https://towardsdatascience.com/clinical-named-entity-recognition-using-spacy-5ae9c002e86f
# https://towardsdatascience.com/how-to-mass-identify-recurring-textual-features-e3e98c4b0309
# https://towardsdatascience.com/reusable-terms-with-spacy-rule-matcher-5d60ae5697fe
# https://medium.com/data-science-business/record-linkage-merging-disparate-datasets-8aa02a2e4535


# https://towardsdatascience.com/train-ner-with-custom-training-data-using-spacy-525ce748fab7
# https://stackoverflow.com/questions/64767231/create-space-knowledgebase-for-similar-nouns
# https://towardsdatascience.com/extract-knowledge-from-text-end-to-end-information-extraction-pipeline-with-spacy-and-neo4j-502b2b1e0754
# https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/

# https://stackoverflow.com/questions/44827930/evaluation-in-a-spacy-ner-model

# https://stackoverflow.com/questions/64767231/create-space-knowledgebase-for-similar-nouns
# https://stackoverflow.com/questions/52856057/is-there-a-way-with-spacys-ner-to-calculate-metrics-per-entity-type
# https://github.com/explosion/spaCy/discussions/8897
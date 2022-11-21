# from __future__ import unicode_literals, print_function
# import plac
import csv
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
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# path = askopenfilename(title="Select file to train", filetypes=(("text files","*.txt"),("all files", "*")))
# path ="C:\\Users\\qiaoyan.ooi\\Downloads\\CapstoneFYP-main\\test.txt"
# path ="C:\\Users\\Qiaoyan\\Downloads\\CapstoneFYP\\client_hostname2.txt"
path = "C:\\Users\\Qiaoyan\\Downloads\\test1\\train.txt"

try:
    with open(path,'r') as f:
        lines = f.readlines()
    DATA = []
    # TRAIN_DATA = []
    edge_case = []
    LABEL = ["client", "hostname", "alias_list", "address_list"]
    for i in lines:
        try:
            i = i.replace(" ", " ").replace("\n","").replace("\t"," ")
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
            DATA.append(row)
            # TRAIN_DATA.append(row)
            # print(row)
        except:
            edge_case.append(i)
    print("---------------------------------------------------------------------------------------------")
    print("DATA: \n")
    print(DATA)
    print("ok")
    # with open("testyanyan_edgecase.txt",'w') as f1:
        # lines3 = f1.writelines(str(edge_case) +"\n")
    # with open("testyanyan_edgecase.txt",'r') as f2:    
    #     lines3 = f2.readlines()
    # for i in lines3:
    #     i = i.replace("	", " ").replace("\n","").replace("\t","")
    print("---------------------------------------------------------------------------------------------")

    model = 'en_core_web_lg'
  
    # model = None
    # output_dir=Path("C:\\Users\\qiaoyan.ooi\\Desktop\\nl\\test")
    # output_dir=Path("C:\\Users\\qiaoyan.ooi\\Downloads\\CapstoneFYP-main\\test")
    output_dir=Path("C:\\Users\\Qiaoyan\\Downloads\\test1 - Copy\\test")

    n_iter=1
    # print("RESULT0: \n")
    print("#data for testing")
    N = len(DATA)
    print("# Randomly select 20% of the data for testing")
    test_idx = np.random.randint(N, size=N//5)
    # print(test_idx)
    TEST_DATA = np.array(DATA)[test_idx].tolist()
    print(TEST_DATA)

    print("#train data")
    print("# Leave the remaining 80% as training data")
    train_idx = list(set(np.arange(N))- set(test_idx))
    # print(train_idx)
    TRAIN_DATA = np.array(DATA)[train_idx].tolist()

    #load the model
    now = datetime.now()
    print("Start " + str(now))
    if model is not None:
        nlp = spacy.load(model)  
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  
        print("Created blank 'en' model")

    #set up the pipeline

    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe('ner')


    for text, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            # print(ent[2])
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner' and pipe !='entity_ruler']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # optimizer = nlp.begin_training()
        for itn in range(n_iter):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
            for batch in batches:
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    for text, annotations in tqdm(TRAIN_DATA):
                        nlp.update(
                        [example],
                        drop=0.5,  
                        # sgd=optimizer,
                        losses=losses)
            print(losses)
    if 'entity_ruler' not in nlp.pipe_names:
        nlp.create_pipe("entity_ruler")
        nlp.add_pipe("entity_ruler", before="ner")
    else:
        nlp.get_pipe('entity_ruler')
    nlp.remove_pipe("entity_ruler")
    ruler_pattern = EntityRuler(nlp, overwrite_ents=True,ent_id_sep=" ")
    ruler_pattern = nlp.add_pipe("entity_ruler",before="ner")
    patterns =[{'label': LABEL[0],'pattern': [{"TEXT": {"REGEX": "[^A-Za-z]*$"}},{"ENT_TYPE": LABEL[0]}]}]
    patterns1 =[{'label': LABEL[1],'pattern': [{"TEXT": {"REGEX": "^[a-zA-Z0-9_.-]*$"}},{"ENT_TYPE": LABEL[1]}]}]
    patterns2 =[{'label': LABEL[2],'pattern': [{"TEXT": {"REGEX": "^\['(\d+.\d+.\d+.\d+.\w+-\w+\w+$)'\]"}},{"ENT_TYPE": LABEL[2]}]}]
    patterns3 =[{'label':LABEL[3],'pattern': [{"TEXT": {"REGEX": "^\['^(\d+.\d+.\d+.\d+)'\]*$"}},{"ENT_TYPE":LABEL[3]}]}]
    ruler_pattern.add_patterns(patterns)
    ruler_pattern.add_patterns(patterns1)
    ruler_pattern.add_patterns(patterns2)
    ruler_pattern.add_patterns(patterns3)
    
    # for text, _ in TRAIN_DATA:
    #     doc = nlp(text)
    #     print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

    nlp.to_disk(output_dir)
    # colours = []
    # for i in LABEL:
    #     random_number = random.randint(0, 16777215)
    #     hex_number = format(random_number, "x")
    #     hex_number = "#" + hex_number
    #     colours.append(hex_number)
    # colors_dict = dict(zip(LABEL, colours))
    # options = {"colors": colors_dict}
   
    print("Train model")

    print("----------------------------------------------------------------------------------------------------reqs")
    for text, annotations in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

#     nlp.to_disk(output_dir)
    print("---------------------------------------------------------------------------------------------")

   
    #ents_p is average precision score of the model for all entities
    # ents_r is average recall score of the model for all entities
    # ents_f is average f1 score of the model for all entities
   
    # ent = []
    # for x in TRAIN_DATA:
    #     ent += [i[-1] for i in x[1]['entities']]

    # print(Counter(ent))
    # html = displacy.render(doc, style="ent", options=options, page=True)
    # # nlp.to_disk(output_dir)
    #         # html = displacy.serve(doc2, style="ent", options=options, page=True)
    # with open("data_vis3.html", "w") as f:
    #     f.write(html+ "\n")
    #     print("ok")
    
    print("Test the train model")
    print("Loading from", output_dir)
  
    # path2 = askopenfilename(title="Select file to read", filetypes=(("text files","*.txt"),("CSV files","*.csv"),("all files", "*")))
   
    # start1 = time.time()
    # print("Timer start " + str(convert(start1)))

    # with open(path2,"r",encoding='utf-8') as f1:
    #     # print(start1)
    #     content1 =f1.readlines()
    #     content1 = (''.join(content1))
    #     content1 = ''.join((content1).replace("\t", " ").replace("\n", "\n"))
    #     nlp2 = spacy.load(output_dir)
    # nlp2.max_length= len(content1) + 1000000000
    # doc2 = nlp2(content1)
    # for ent in doc2.ents:
    #     print(ent.label_, ent.text)
# print(doc2)
    # html2 = displacy.render(doc2, style="ent", options=options, page=True)

        # html = displacy.serve(doc2, style="ent", options=options, page=True)
    # with open("data_vis4.html", "w") as f:
    #     f.write(html2+ "\n")
    #     print("ok")
    print("---------------------------------------------------------------------------------------------")
    print("RESULT1: \n")
    
    results1 = evaluate(nlp, TEST_DATA)

  
    print(str(results1)+"\n")
    print("Precision score is: ", results1['ents_p'])
    print("Recall score is: ", results1['ents_r'])
    print("f1 score is: ", results1['ents_f'])
    #ents_p is average precision score of the model for all entities
    # ents_r is average recall score of the model for all entities
    # ents_f is average f1 score of the model for all entities
    ent1 = []
    for x in TEST_DATA:
        ent1 += [i[-1] for i in x[1]['entities']]

    print(Counter(ent1))
    print("-------------------------------------------------------------------------------------------------reqs")

    print("-----")
    current_time = datetime.now() - now
    print("duration:", current_time)
    
except FileNotFoundError:
    print("Sorry, the file " + path + " does not exist")



# print("parsing the text file and train to store as csv\n")

# with open(path2, 'r') as file:
#     lines2 = file.readlines()
#     print(len(lines2)+ " records")
#     # lines2 = (''.join(lines2))
#     # lines2 = ''.join((lines2).replace("\t", " ").replace("\n", "\n"))
# with open('yytest.csv', 'w', newline='') as file1:
#         #clear the csv file
#     # with open('yytest.csv', 'w', newline='') as file2:
#         LABEL1 = ['ID', 'client', 'hostname', 'alias_list', 'address_list']
#         file1.truncate()
#         #write the csv file
#         writer = csv.writer(file1)
#         writer2 = csv.DictWriter(file1, delimiter=',',fieldnames=LABEL1)
#         writer2.writeheader()
#         id = 0
#         # limit = 1000000000
#         # csv.field_size_limit(limit) 
#         for text in tqdm(lines2):
#             id = id+1
#             text = ''.join((text).replace("\t", " ").replace("\n", "\n"))
            
#             doc = nlp2(text)
#             nlp2.max_length= len(text) + 1000000000

#             param = [(ent.label_, ent.text) for ent in doc.ents]
#             a = {}
#             count = 0
#             for i in param:
#                 count += 1
#                 a[id] ='id'
#                 if i[1] not in a:
#                     a[i[1]] = i[0]
#                 else:
#             # print(i)
#             # print(i[0])
#                     a[i[1]+" "] = i[0]
#                 if count == len(param):
#                     writer.writerow(a)
#             # print(param)
#             # print(len(param))
            
#     # file1.close()

# print(doc.similarity(doc2))
# print(timet)
# print("time taken to train whole dataset " + str(convert(timet)))
# print(csv.field_size_limit(limit))
# print("-------daffs------------------------------------------------------------------------------------------reqs")

  
# print(df)
# df.columns = ['text', 'label']
# df.to_csv('Trained_data.csv')


#if precision is 1 == good classifier (Postitive predictive value)
# precision becomes 1 when TP = TP +FP, FP = 0
#TP/ TP+FP

# print(results['ents_p']*100) 

#if recall is 1 == good classfier (True positive value)
# recall becomes 1 when TP = TP +FN ,= FN 
#TP / TP + FN

#f1 score = precision and recall (more accuracy of the model)
#f1 score = 1, means FP and FN = 0
# f1 =1 ,when precision and recall =1

# nlp2.to_disk(output_dir)


# Calculate sample size

# https://towardsdatascience.com/clinical-named-entity-recognition-using-spacy-5ae9c002e86f
#https://towardsdatascience.com/how-to-mass-identify-recurring-textual-features-e3e98c4b0309
#https://towardsdatascience.com/reusable-terms-with-spacy-rule-matcher-5d60ae5697fe
#https://medium.com/data-science-business/record-linkage-merging-disparate-datasets-8aa02a2e4535



# https://towardsdatascience.com/train-ner-with-custom-training-data-using-spacy-525ce748fab7
# https://stackoverflow.com/questions/64767231/create-space-knowledgebase-for-similar-nouns
# https://towardsdatascience.com/extract-knowledge-from-text-end-to-end-information-extraction-pipeline-with-spacy-and-neo4j-502b2b1e0754
# https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/

# https://stackoverflow.com/questions/44827930/evaluation-in-a-spacy-ner-model

# https://stackoverflow.com/questions/64767231/create-space-knowledgebase-for-similar-nouns
# https://stackoverflow.com/questions/52856057/is-there-a-way-with-spacys-ner-to-calculate-metrics-per-entity-type
# https://github.com/explosion/spaCy/discussions/8897
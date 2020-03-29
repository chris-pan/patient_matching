from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import fuzzy
import datetime
import re
import math
from matplotlib import pyplot as plt
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def main():
    df_in = pd.read_excel('FILE DESTINATION') or pd.read_csv('FILE DESTINATION')
    #change destination to whereever the provided Patient Matching Data is stored
    df = pd.read_excel('/Users/christopherpan 1/Desktop/LAHacks/Patient Matching Data.xlsx',sep=",")
    test = df.loc[:, ['GroupID', 'First Name', 'Last Name', 'Date of Birth', 'Sex', 
                  'Current Street 1', 'Current Street 2', 'Current Zip Code']]
    arr = test.values

    test_in = df.loc[:, [First Name', 'Last Name', 'Date of Birth', 'Sex', 
                  'Current Street 1', 'Current Street 2', 'Current Zip Code']]
    arr_in = test.values

    table(arr)
    table(arr_in)

    arr_desired = np.delete(arr, [6, 7], 1)
    arr_in = np.delete(arr_in, [5, 6], 1)
    groups = []
    for row in arr_desired:
        create(row, groups, arr_desired)
    np_groups = np.array(groups)
    x = np_groups[:,:5]
    y = np_groups[:,5]
    clf = SVC(gamma = 'auto')
    clf.fit(x,y)
    svc_groups = {}
    for row in arr_in:
        match_in(row, svc_groups)
    col_add = []
    for key in svc_groups:
        for person in svc_groups[key]:
            col_add.append(key)
    col_add = np.array(col_add)
    df_in.insert(1, 'Predicted GroupID', col_add)
    #change destination
    df_in.to_csv('/Users/christopherpan 1/Desktop/LAHacks/predicted_matches.csv', index = False, header = True)
    #can use df_in (the test/other data)

#chose to use first name, last name, DOB, sex, and address (st 1 + st 2 + zip code)
#converted names to soundex tokens
#stemmed and lemmatized address
def table(arr):
    soundex = fuzzy.Soundex(4)
    stemmer = PorterStemmer()
    for row in arr:
        if isinstance(row[2], str):
            row[1] = soundex(row[1].lower())
            row[2] = soundex(row[2].lower())
        else:
            row[1] = soundex(row[1].lower())
        row[1] = row[1].replace('%d','')
        if isinstance(row[3], datetime.datetime):
            row[3] = row[3].strftime("%m/%d/%Y")
        if isinstance(row[4], str):
            row[4] = row[4][0]
        else:
            row[4] = 'U'
        if isinstance(row[5], str):
            row[5] = word_tokenize(row[5])
            str_lst = list(row[5])
            for i in range(len(str_lst)):
                str_lst[i] = stemmer.stem(str_lst[i])
            row[5] = "".join(str_lst)
            if isinstance(row[6], str):
                row[6] = word_tokenize(row[6])
                str_lst = list(row[6])
                for i in range(len(str_lst)):
                    str_lst[i] = stemmer.stem(str_lst[i])
                row[6] = "".join(str_lst)
                row[5] += row[6]
            if not math.isnan(row[7]):
                row[5] += str(int(float(row[7])))
#creates data to be used for training by comparing each person with others
def create(arr, groups, total):
    if len(groups) == 0:
        groups.append(compare(arr, arr))
        return
    add = []
    for lst in total:
        add.append(compare(arr, lst))
    groups.extend(add)

#edit distance
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

#returns array of comparisons
#Duplicate this function and remove SAME for test (as there won't be provided Group ID's)
def compare(arr, person):
    first_name = levenshtein(arr[1], person[1])
    first_other = levenshtein(arr[1], str(person[2]))
    last_name = levenshtein(str(arr[2]), str(person[2]))
    last_other = levenshtein(str(arr[2]), str(person[1]))
    if first_other > first_name:
        first_name = first_other
        lsat_name = last_other
    bday = levenshtein(str(arr[3]), str(person[3]))
    gender = levenshtein(arr[4], person[4])
    address = levenshtein(str(arr[5]), str(person[5]))  
    same = 0 if arr[0] == person[0] else 1     #Remove for test
    return [first_name, last_name, bday, gender, address, same]

#Compare function for test input
def compare_in(arr, person):
    first_name = levenshtein(arr[0], person[0])
    first_other = levenshtein(arr[0], str(person[1]))
    last_name = levenshtein(str(arr[1]), str(person[1]))
    last_other = levenshtein(str(arr[1]), str(person[0]))
    if first_other > first_name:
        first_name = first_other
        lsat_name = last_other
    bday = levenshtein(str(arr[2]), str(person[2]))
    gender = levenshtein(arr[3], person[3])
    address = levenshtein(str(arr[4]), str(person[4]))  
    return [first_name, last_name, bday, gender, address]

def match(arr, groups):
    if len(groups) == 0:
        groups[0] = [arr]
        return
    for key in groups:
        add = []
        for lst in groups[key]:
            #Duplicate this function and make the 5 -> 4 for testing
            add.append(compare_in(arr, lst)[:4])
        #originally used logistic regression instead of SVM
        #Use of SVM could have lead to overfitting 
        #which would occur less in logistic regression model 
        #at the cost of accuracy
        #log_n = logisticRegr.predict(np.array(add))
        log_n = clf.predict(np.array(add))
        if (log_n == 0).sum() > log_n.size/2:
            groups[key].append(arr)
            return
    groups[len(groups)] = [arr]

def match_in(arr, groups):
    if len(groups) == 0:
        groups[0] = [arr]
        return
    for key in groups:
        add = []
        for lst in groups[key]:
            #Duplicate this function and make the 5 -> 4 for testing
            add.append(compare(arr, lst)[:5])
        #originally used logistic regression instead of SVM
        #Use of SVM could have lead to overfitting 
        #which would occur less in logistic regression model 
        #at the cost of accuracy
        #log_n = logisticRegr.predict(np.array(add))
        log_n = clf.predict(np.array(add))
        if (log_n == 0).sum() > log_n.size/2:
            groups[key].append(arr)
            return
    groups[len(groups)] = [arr]
    
if __name__ == "__main__":
    main()
"""
clean original data, main steps includes:
remove non-unicode chars; remove stop words; tokenization;
input file should be in JSON format.
output file will be pure text format
"""
import sys
sys.path.append("..")
import json
from config import stopword_set
from config import emoji_pattern, digit_pattern, punc0_pattern, punc1_pattern
from config import least_length


def replace_noneng(line):
    line = punc1_pattern.sub(r' ', line)
    line = punc0_pattern.sub(r' \1 ' ,line)
    line = emoji_pattern.sub(r' emoji ', line)
    line = digit_pattern.sub(r' num ', line)
    return line

def remove_stopword(line):
    return ' '.join([word for word in line.split() if word not in stopword_set])

def label_check():
    pass

def clean(filein, fileout, textkey="body"):
    fin = open(filein, encoding='utf-8', mode='r')
    fout = open(fileout, encoding='utf-8', mode='w')
    memo = []
    for data_unit in json.load(fin):
        text = data_unit[textkey]
        ## data cleaning
        text = text.lower()
        # remove or replace non-english chars
        text = replace_noneng(text)
        t_split = text.split()
        # remove duplicate sample/text
        if t_split[:least_length] not in memo:
            memo.append(t_split[:least_length])
        else:
            continue
        # remove redundant white space
        text = ' '.join(t_split)
        new_line = text+'\n'
        fout.write(new_line)


if __name__ == "__main__":
    filein_list = ["../data/json/fortnite_review_neg_1105.json",
                   "../data/json/fortnite_review_pos_1105.json"]
    fileout_list = ["../data/raw/fortnite.500.neg.txt",
                    "../data/raw/fortnite.500.pos.txt"]
    for i in range(len(filein_list)):
        clean(filein_list[i], fileout_list[i])

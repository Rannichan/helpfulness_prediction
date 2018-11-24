"""
Format the data into *FastText training data format
"""
import sys
sys.path.append("..")
import config
import random

def addLable (filein_pos, filein_neg, fileout):
    fpos = open(filein_pos, encoding='utf-8', mode='r')
    fneg = open(filein_neg, encoding='utf-8', mode='r')
    fout = open(fileout, encoding='utf-8', mode='w')
    pos_label = "__label__helpful "
    neg__label = "__label__unhelpful "
    text_list = []
    for line in fpos:
        text_list.append(pos_label+line)
    for line in fneg:
        text_list.append(neg__label+line)
    random.shuffle(text_list)
    for line in text_list:
        fout.write(line)


if __name__ == "__main__":
    posfile = "../data/raw/fortnite.500.pos.txt"
    negfile = "../data/raw/fortnite.500.neg.txt"
    outfile = "../data/train/fortnite.500.txt"
    addLable(filein_pos=posfile,
             filein_neg=negfile,
             fileout=outfile)
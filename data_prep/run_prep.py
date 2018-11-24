import argparse
from data_clean import clean
from data_format import addLable

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputpos", "-ip", type=str, default="reviews_pos.json",
                        help="input positive json file")
    parser.add_argument("--inputneg", "-in", type=str, default="reviews_neg.json",
                        help="input negative json file")
    parser.add_argument("--output", "-o", type=str, default="reviews_train.txt",
                        help="output training file")
    args = parser.parse_args()

    json_dir = '../data/json/'
    raw_dir = '../data/raw/'
    train_dir = '../data/train/'
    json_files = [json_dir+args.inputpos, json_dir+args.inputneg]
    raw_files = [raw_dir+args.inputpos+'.txt', raw_dir+args.inputneg+'.txt']
    for json_file, raw_file in zip(json_files, raw_files):
        clean(json_file, raw_file)
    addLable(filein_pos=raw_files[0],
             filein_neg=raw_files[1],
             fileout=train_dir+args.output)



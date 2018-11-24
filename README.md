# Data Description
data/json -- Original json format file are saved in this directory. Take a look in of the sample data and make sure the data format matchs with the sample.
data/raw -- Review text will be extract from the json file and be saved in this directory after being cleaned.
data/train -- Data in data/raw will be merged and transformed in the special format for FastText training. And then saved in this directory.

# How to Prepare Training Data
Run following command in terminator to prepare training data:
```
    cd data/json
    cat pos/* | sed '/\]\[/d' | sed 's/}$/},/g' | tail -r | sed '2s/},$/}/g'| tail -r > reviews_pos.json
    cat neg/* | sed '/\]\[/d' | sed 's/}$/},/g' | tail -r | sed '2s/},$/}/g'| tail -r > reviews_neg.json

    cd data_prep
    python run_prep.py -ip reviews_pos.json -in reviews_neg.json -o reviews_train.txt
    # The first param is original positive json file name.
    # The second param is original negative json file name.
    # The third param is last-generated training file.
```

# How to Train the Classifier
First, download and compile [FastText library](https://fasttext.cc) in the main directory of this project
Then, run following command to train and test the classifier:
```
    cd data/train
    wc reviews_train.txt
    # (assume the output is) 1811  100354  555352 reviews_train.txt
    head -n 1511 reviews_train.txt > reviews.train
    tail -n 300 reviews_train.txt > reviews.valid

    cd fastText
    ./fasttext supervised -input ../data/train/reviews.train -output ../data/model/reviews -epoch 30
    ./fasttext test ../data/model/reviews.bin ../data/train/reviews.valid
```
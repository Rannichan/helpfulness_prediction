# Data Description
* data/json/pos -- All positive original json format file are saved in this directory. Take a look in of the sample data and make sure the data format matchs with the sample.
* data/json/neg -- ALl negative original json format file are saved in this directory. Take a look in of the sample data and make sure the data format matchs with the sample.
* data/raw -- Review text will be extract from the json file and be saved in this directory after being cleaned.
* data/train -- Data in data/raw will be merged and transformed in the special format for FastText training. And then saved in this directory.
* data/model -- Model file will be saved here.

# How to Prepare Training Data
Run following command in terminator to prepare training data:
```
    # under the directory 'data/json'
    $ cat pos/* | sed '/\]\[/d' | sed 's/}$/},/g' | tail -r | sed '2s/},$/}/g'| tail -r > reviews_pos.json
    $ cat neg/* | sed '/\]\[/d' | sed 's/}$/},/g' | tail -r | sed '2s/},$/}/g'| tail -r > reviews_neg.json

    # under the directory 'data_prep'
    $ python run_prep.py -ip reviews_pos.json -in reviews_neg.json -o reviews_train.txt
    # The first param is original positive json file name.
    # The second param is original negative json file name.
    # The third param is last-generated training file.
```

# How to Train the Classifier
First, you need to intstall FastTest library into your environment:
```
    $ git clone https://github.com/facebookresearch/fastText.git
    $ cd fastText
    $ pip install .
```

Second, you may need to download pre-trained word vector file form [FastText official website](https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki-news-300d-1M-subword.vec.zip).

At last, we need to divide the whole dataset into training set and validation set, and train on the training set:
```
    # under the directory 'data/train'
    $ wc reviews_train.txt
    # assume the output is 1811  100354  555352 reviews_train.txt
    $ head -n 1511 reviews_train.txt > reviews.train
    $ tail -n 300 reviews_train.txt > reviews.valid

    # under the directory 'main'
    $ python main.py --mode train --model ../data/model/reviews.bin --train ../data/train/reviews.train --wordvector ../data/wiki-news-300d-1M-subword.vec
    # we do not provide hyperparameters of training process here, but you can directly modify it in the main.py
```

# How to Test the Classifier
```
    # under the directory 'main'
    $ python main.py --mode test --model ../data/train/model/reviews.bin --test ../data/train/reviews.valid
    # 2 files (pridicted correctly and predicted wrongly) will be generated at the same path of test file
```
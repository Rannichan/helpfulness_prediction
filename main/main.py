import fastText
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m", type=str, default="train",
                        help="train model or use the model to do prediction")
    parser.add_argument("--model", "-mf", type=str, default="../data/train/model/reviews.bin",
                        help="model file")
    parser.add_argument("--train", "-tr", type=str, default="../data/train/reviews.train",
                        help="training file")
    parser.add_argument("--test", "-te", type=str, default="../data/train/reviews.valid",
                        help="test file")
    parser.add_argument("--wordvector", "-wv", type=str, default="../data/wiki-news-300d-1M-subword.vec",
                        help="pre-trained word vector file")
    args = parser.parse_args()

    if args.mode == 'train':
        classifier = fastText.train_supervised(input=args.train,
                                               epoch=10,
                                               wordNgrams=2,
                                               dim=300,
                                               minn=3,
                                               maxn=6,
                                               pretrainedVectors=args.wordvector)
        classifier.save_model(args.model)
    elif args.mode == 'test':
        classifier = fastText.load_model(args.model)
        rf = open(args.test+'.right', mode='w', encoding='utf-8')
        wf = open(args.test+'.wrong', mode='w', encoding='utf-8')
        for line in open(args.test, mode='r', encoding='utf-8'):
            right_label = line.split()[0]
            sentence = ' '.join(line.split()[1:])
            pred_label, _ = classifier.predict(sentence)
            if pred_label[0] == right_label:
                rf.write(line)
            else:
                wf.write(line)
    else:
        print('Wrong mode!')
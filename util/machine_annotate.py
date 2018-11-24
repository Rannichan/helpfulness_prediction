import json


def method1(file_in, file_pos, file_neg, file_ukn):
    fi = open(file_in, mode='r', encoding='utf-8')
    fpos = open(file_pos, mode='w', encoding='utf-8')
    fneg = open(file_neg, mode='w', encoding='utf-8')
    fukn = open(file_ukn, mode='w', encoding='utf-8')
    pos_review = []
    neg_review = []
    ukn_review = []
    for review in json.load(fi):
        # cases satisfying all following conditions will be annotated as 1 (valuable)
        # 1. length of the review(body) > 5
        # 2. more than half of people vote for the review
        # 3. total number of people who vote > 10
        #
        # such cases will be annotated as -1 (need to be annotated manually)
        # 1. new reviews posted after 525 (based on previous analysis) with vote <= 10
        # 2. percentage of people who vote for the review <= 0.5 but > 0.4
        #
        # else cases will be annotated as 0 (not valuable)
        if len(review['review_body'].split()) > 5 and \
                review['helpful_score'] > 0.5 and \
                review['total_vote'] > 10:
            annotated_review = {
                "label": 1,
                "title": review['review_title'],
                "body": review['review_body'],
                "platform": review['platform'],
                "score": review['helpful_score'],
                "vote": review['total_vote']
            }
            pos_review.append(annotated_review)
        elif (review['date_para'] > 525 and review['total_vote'] <= 10) or \
                0.4 < review['helpful_score'] <= 0.5:
            annotated_review = {
                "label": -1,
                "title": review['review_title'],
                "body": review['review_body'],
                "platform": review['platform'],
                "score": review['helpful_score'],
                "vote": review['total_vote']
            }
            ukn_review.append(annotated_review)
        else:
            annotated_review = {
                "label": 0,
                "title": review['review_title'],
                "body": review['review_body'],
                "platform": review['platform'],
                "score": review['helpful_score'],
                "vote": review['total_vote']
            }
            neg_review.append(annotated_review)
    print('Pos num: ' + str(len(pos_review)))
    print('Neg num: ' + str(len(neg_review)))
    print('Unk num: ' + str(len(ukn_review)))
    fpos.write(
        json.dumps(
            pos_review,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )
    fneg.write(
        json.dumps(
            neg_review,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )
    fukn.write(
        json.dumps(
            ukn_review,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )


def method2(file_in, file_pos, file_neg):
    """
    extract positive samples an negative samples from file_in, then write them into file_pos and file_neg
    :param file_in: path of the input file
    :param file_pos: path of the positive file
    :param file_neg: path of the negative file
    :return:
    """
    fi = open(file_in, mode='r', encoding='utf-8')
    fpos = open(file_pos, mode='w', encoding='utf-8')
    fneg = open(file_neg, mode='w', encoding='utf-8')
    pos_review = []
    neg_review = []
    for review in json.load(fi):
        if review['total_vote'] >= 10 and len(review['review_body'].split()) >= 5:
            if review['helpful_score'] >= 0.65:
                annotated_review = {
                    "label": 1,
                    "title": review['review_title'],
                    "body": review['review_body'],
                    "platform": review['platform'],
                    "score": review['helpful_score'],
                    "vote": review['total_vote']
                }
                pos_review.append(annotated_review)
            elif review['helpful_score'] <= 0.5:
                annotated_review = {
                    "label": 0,
                    "title": review['review_title'],
                    "body": review['review_body'],
                    "platform": review['platform'],
                    "score": review['helpful_score'],
                    "vote": review['total_vote']
                }
                neg_review.append(annotated_review)

    print('Pos num: ' + str(len(pos_review)))
    print('Neg num: ' + str(len(neg_review)))
    fpos.write(
        json.dumps(
            pos_review,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )
    fneg.write(
        json.dumps(
            neg_review,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )


if __name__ == '__main__':
    file_in = '../data/fortnite_review_full_sorted.json'
    file_pos = '../data/pos.json'
    file_neg = '../data/neg.json'
    file_ukn = '../data/ukn.json'
    method2(file_in, file_pos, file_neg)
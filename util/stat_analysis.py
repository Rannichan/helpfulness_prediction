import json
from matplotlib import pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def sortbykey(file_in, file_out, key='helpful_score'):
    """
    remove redundant keys and sort descending by assigned key
    :param file_in:
    :param file_out:
    :param key:
    :return:
    """
    fi = open(file_in, mode='r', encoding='utf-8')
    fo = open(file_out, mode='w', encoding='utf-8')
    review_list = []
    try:
        reviews = json.load(fi)
        for review in reviews:
            try:
                simple_review = {'helpful_score': (float(review['helpful_num'])+1)/(float(review['total_num'])+1),
                                 'total_vote': float(review['total_num']),
                                 'date_para': str2date(review['date']),
                                 'platform': review["device"],
                                 'review_title': review['head'],
                                 'review_body': review['review_text']}
                review_list.append(simple_review)
            except Exception:
                print("Wrong key!")
                print(review)
    except Exception:
        print("Wrong json format!")
    sorted_review = sorted(review_list,
                           key=lambda x:x[key],
                           reverse=True)
    fo.write(
        json.dumps(
            sorted_review,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )


def data_analysis(file_in):
    """
    analysis the relation between vote and date
    :param file_in:
    :return:
    """
    fi = open(file_in, mode='r', encoding='utf-8')
    date = []
    vote = []
    for review in json.load(fi):
        date.append(review['date_para'])
        vote.append(review['total_vote'])
    date = np.array(date)
    vote = np.array(vote)

    plt.figure()
    plt.title('Relation between vote and date')
    plt.xlabel('date')
    plt.ylabel('vote')
    plt.plot(date, vote, 'k.')
    plt.show()

    # model = LinearRegression()
    # model.fit(date, vote)


def vote_analysis(file_in):
    from collections import Counter
    fi = open(file_in, mode='r', encoding='utf-8')
    vote = Counter()
    for review in json.load(fi):
        vote[int(review['total_vote'])] += 1
    max_vote_num = max(vote.keys())
    vote_count = [0 for _ in range(max_vote_num+1)]
    index = [x for x in range(max_vote_num+1)]
    for vote_num, count in vote.items():
        vote_count[int(vote_num)] = count
    print('>=0: {}'.format(sum(vote_count[0:])))
    print('>=3: {}'.format(sum(vote_count[3:])))
    print('>=5: {}'.format(sum(vote_count[5:])))
    print('>=10: {}'.format(sum(vote_count[10:])))
    print('>=20: {}'.format(sum(vote_count[20:])))
    print('>=50: {}'.format(sum(vote_count[50:])))
    print('>=100: {}'.format(sum(vote_count[100:])))


def str2date(date):
    """
    Given date string in the form "MM/DD/YYYY", map the string to an integer
    :param date:
    :return:
    """
    date = date.split("/")
    # today = 30*9+23+365*(2018-2017)
    return 30*int(date[0])+int(date[1])+365*(int(date[2])-2017)


def preprocess(file_in, file_out):
    fi = open(file_in, mode='r', encoding='utf-8').readlines()
    with open(file_out, mode='w', encoding='utf-8') as fo:
        fo.write('[')
        for line in fi[:-1]:
            if line[0] == '}':
                fo.write('\t},\n')
            else:
                fo.write('\t'+line)
        fo.write('}\n]')


if __name__ == '__main__':
    # preprocess('../data/fortnite_review_full.json', '../data/fortnite_review_full_new.json')
    # sortbykey('../data/fortnite_review_full.json', '../data/fortnite_review_full_sorted.json')
    # data_analysis('../data/fortnite_review_full_sorted.json')
    vote_analysis('../data/fortnite_review_full_sorted.json')

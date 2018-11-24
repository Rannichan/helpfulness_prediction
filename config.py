### dataset
from nltk.corpus import stopwords
stopword_set = set(stopwords.words('english'))

from string import punctuation
punc_set = set(punctuation)

import re
punc0_pattern = re.compile("([.,?!…:;&])([.,?!…:;&]*)")
punc1_pattern = re.compile("[%*\-/#\'\"]+")
digit_pattern = re.compile("[0-9]+")
emoji_pattern = re.compile("["
                           u"\U00010000-\U0010ffff"
                           "❤"
                           "]+", flags=re.UNICODE)
# u"\U0001F600-\U0001F64F"  # emoticons
# u"\U0001F300-\U0001F5FF"  # symbols & pictographs
# u"\U0001F680-\U0001F6FF"  # transport & map symbols
# u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
# u"\U00002702-\U000027B0"
# u"\U000024C2-\U0001F251"

### data crawling
least_length = 10
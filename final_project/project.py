from nltk.tokenize import word_tokenize
import nltk
from string import punctuation
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import re


def clean(kw):
    kw = re.sub(r'[^А-Яа-яЁё]', ' ', kw)
    kw = re.sub(r'(\S)(\s)\s+(\S)', r'\1\2\3', kw)
    keys = kw.split()
    return keys


def download(group_id, parameters):
    api_req = 'https://api.vk.com/method/wall.get?'
    parameters['owner_id'] = group_id
    j = ['{}={}'.format(key, parameters[key]) for key in parameters]
    api_req += '&'.join(j)
    json_raw = requests.get(api_req).text
    return json.loads(json_raw)


def collect_texts(group_id, bp):
    res = download(group_id, bp)
    if 'response' in res:
        sm = res['response']['count']
        pars = bp.copy()
        i = 0
        texts = []
        for i in range(0, 3):
            pars['offset'] = str(i * 100)
            if sm - i >= 100:
                count = 100
                tt = True
            else:
                count = sm - i
                tt = False
            pars['count'] = str(count)
            result = download(group_id, pars)
            for j in range(count):
                items = result['response']['items'][j]
                text = items["text"]
                texts.append(text)
            if tt == False:
                break
    return texts


def tokens(texts):
    post_texts = []
    for post in texts:
        text = post['text']
        text = text.lower()
        text = word_tokenize(text)
        text = [w for w in text if w not in punctuation]
        post_texts.append(text)
    post_texts_new = []
    for text in post_texts:
        new = [token for token in text if token not in stopwords]
        post_texts_new.append(new)
    return post_texts_new


def words_we_search(postwords, keywords):
    freq = {}
    for word in keywords:
        freq[word] = 0
    for word in postwords:
        if word in keywords:
            freq[word] += 1
    return freq


def one_group_graph(freq, school):
    style.use('dark_background')
    x = []
    y = []
    nm = []
    for word in sorted(freq, key=freq.get, reverse=True):
        if freq[word] > 0:
            x.append(word)
            y.append(freq[word])
        else:
            nm.append(word)
    plt.bar(x, y)
    gtitle = "Частота встречаемости заданных слов: "
    gtitle += school
    plt.title(gtitle)
    plt.ylabel("Количество слов")
    r = 45
    plt.tight_layout()
    plt.xticks(range(len(x)), [i for i in x], rotation=r)
    filename = 'static/%s.png' % (school)
    plt.savefig(filename)
    plt.close()


def common_graph(freqs, kw):
    n_groups = len(freqs)
# create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.1
    opacity = 0.8
    scolors = {"ВШЭ": "b", "МГУ": "g",
             "РАНХИГС": "r", "МГИМО": "y"}
    for school in freqs:
        freq = freqs[school]
        x = []
        for word in kw:
            x.append(freq[word])
        plt.bar(index, x, bar_width, alpha=opacity,
                color=scolors[school], label=school)
#    rects2 = plt.bar(index + bar_width, means_guido, bar_width,
#    alpha=opacity,
#    color='g',
#    label='Guido')
#    
    plt.xlabel('Слова')
    plt.ylabel('Количество слов')
    plt.title('Сводный график')
    plt.xticks(index + bar_width, tuple(kw))
    plt.legend()
    plt.tight_layout()
    filename = 'static/common.png'
    plt.savefig(filename)


def main(kwords):
   t = '6919e05a6919e05a6919e05a5969705caf669196919e05a35beae96bddfb0c2e2734eaf'
   kw = clean(kwords)
   ktokens = tokens(kw)
   bp = {'access_token': t, 'v': '5.95', 'filter': 'owner'}
   groups = {"ВШЭ": "-57354358", "МГУ": "-54295855",
             "РАНХИГС": "-128219388", "МГИМО": "-57969268"}
   freqs = {}
   for school in groups:
       g_id = groups[school]
       bp['owner_id'] = g_id
       texts = collect_texts(g_id, bp)
       ttexts = token(texts)
       freq = words_we_search(ttexts, ktokens)
       one_group_graph(freq, school)
       freqs[school] = freq
   common_graph(freqs, ktokens)
   return "Успех!"

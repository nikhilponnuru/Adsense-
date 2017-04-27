
import urllib
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
#import parse

from collections import Counter
import operator
from nltk.stem import WordNetLemmatizer
import nltk.corpus
from nltk.tag.perceptron import PerceptronTagger

content_text = ""

def contentextract(url):

    # def poschunking(url):
    # url = "https://ponnurunikhilkumar.wordpress.com/2016/04/12/compiler-extensions-like-chrome-extensions/"


    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    global content_text
    content_text= str(text.encode('utf-8'))



    return content_text


#print(content_text)
def returncontenttext():
    return content_text


'''

word_tokens=word_tokenize(content_text)

stop_words=set(stopwords.words('english'))

filtered_sentence = [w for w in word_tokens if not w in stop_words]

filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)


print(filtered_sentence)
'''


#print(contentextract())

def preprocessing(url):
    content_text=contentextract(url)
    #print(content_text)

    word_tokens = word_tokenize(content_text)
    print(word_tokens)
    stop_words = set(stopwords.words('english'))

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)



#    filtered_sentence
    # POS tagging
    tagger = PerceptronTagger()
    # to speed up pos tagging used some extra lines for optimization
    tagset = None
    # pos_tagged = nltk.tag._pos_tag(filtered_sentence, tagset, tagger)

    pos_tagged = tagger.tag(filtered_sentence)

    # pos_tagged=nltk.pos_tag(filtered_sentence)
    #print("fil",filtered_sentence)

    chunkGram1 = r"Chunk1: {<NN.?>+}"
    chunkGram2 = r"Chunk2: {<JJ.?>+<NN.?>+}"
    chunkGram3 = r"chunk3:{<CD.?><NN.?>+ | <NN>+<CD.?>}"
    chunkGram4 = r"chunk4:{<DT.?><NN.?>+}"

    # chunkGram1= r"chunk1: {<NN.?>+ | <JJ.?>+<NN.?>+ | <CD.?><NN.?>+ | <NN>+<CD.?> | <DT.?><NN.?>+ }"


    chunkParser = nltk.RegexpParser(chunkGram1)
    chunked = chunkParser.parse(pos_tagged)
    #chunked.draw()
    final_words = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk1'):
        final_words.append((list(subtree[0]))[0])

    chunkParser = nltk.RegexpParser(chunkGram2)
    chunked = chunkParser.parse(pos_tagged)
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk2'):
        final_words.append((list(subtree[0]))[0])

    chunkParser = nltk.RegexpParser(chunkGram3)
    chunked = chunkParser.parse(pos_tagged)
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk3'):
        final_words.append((list(subtree[0]))[0])

    chunkParser = nltk.RegexpParser(chunkGram4)
    chunked = chunkParser.parse(pos_tagged)

    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk4'):
        final_words.append((list(subtree[0]))[0])

    #print(len(final_words))



    dictionary_chunked = dict(Counter(final_words))

    sorted_chunks = sorted(dictionary_chunked.items(), key=operator.itemgetter(1), reverse=True)

    ad_probable_keywords = []
    for i in range(0, 40):
        value = sorted_chunks[i][0]
        value = value.replace("\\", "")
        value = value.replace("\\\\", "")


        ad_probable_keywords.append(value)

    print("adprobable",ad_probable_keywords)


    return ad_probable_keywords



#print("keywords for http://bikes.bloggerstop.net/2008/10/yamaha-fz-16.html",preprocessing("https://www.quora.com/How-good-is-the-movie-Bahubali/answer/Tarun-Reddy-45?srid=u6vSf"))


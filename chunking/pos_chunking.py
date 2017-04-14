import urllib
from bs4 import BeautifulSoup

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import operator
from nltk.stem import WordNetLemmatizer
import nltk.corpus
from nltk.tag.perceptron import PerceptronTagger


content_text=""
#def poschunking(url):
    #url = "https://ponnurunikhilkumar.wordpress.com/2016/04/12/compiler-extensions-like-chrome-extensions/"

url="http://qr.ae/T5z1e8"
html = urllib.request.urlopen(url).read()
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

content_tex = text.encode('utf-8')
content_text=str((content_tex))
print(content_text)








word_tokens=word_tokenize(content_text)
stop_words=set(stopwords.words('english'))

filtered_sentence = [w for w in word_tokens if not w in stop_words]

filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

lemma=WordNetLemmatizer()
stemmed_list=[]
for w in filtered_sentence:
    stemmed_list.append(lemma.lemmatize(w))



#POS tagging
tagger = PerceptronTagger()
#to speed up pos tagging used some extra lines for optimization
tagset = None
#pos_tagged = nltk.tag._pos_tag(filtered_sentence, tagset, tagger)
pos_tagged=tagger.tag(stemmed_list)

#pos_tagged=nltk.pos_tag(filtered_sentence)
print("before tagging",len(pos_tagged))

chunkGram1= r"Chunk1: {<NN.?>+}"
chunkGram2= r"Chunk2: {<JJ.?>+<NN.?>+}"
chunkGram3= r"chunk3:{<CD.?><NN.?>+ | <NN>+<CD.?>}"
chunkGram4= r"chunk4:{<DT.?><NN.?>+}"

#chunkGram1= r"chunk1: {<NN.?>+ | <JJ.?>+<NN.?>+ | <CD.?><NN.?>+ | <NN>+<CD.?> | <DT.?><NN.?>+ }"


chunkParser = nltk.RegexpParser(chunkGram1)
chunked = chunkParser.parse(pos_tagged)


final_words=[]
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



dictionary_chunked=dict(Counter(final_words))


sorted_chunks = sorted(dictionary_chunked.items(), key=operator.itemgetter(1),reverse=True)
print(sorted_chunks)
ad_probable_keywords=[]
for i in range(0,30):
    value=sorted_chunks[i][0]
    value=value.replace("\\","")
    value=value.replace("\\\\","")

    print(value)
    ad_probable_keywords.append(value)

print(ad_probable_keywords)




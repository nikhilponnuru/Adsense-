import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def sentimental_analysis(tweet):
    pos_tweets = [('I love this car', 'positive'),
                  ('This view is hello', 'positive'), ('I feel great this morning', 'positive'),
                  ('I am so excited about the concert', 'positive'),
                  ('He is my best friend', 'positive'), ('awesome', 'positive')]
    # ('SentiWordNet (http://sentiwordnet.isti.cnr.it/) is an excellent publicly available lexicon. Technically, the resource contains Princeton WordNet data marked with','positive'),
    # ('abound, abounds, abundance, abundant, accessible, accessible, acclaim, acclaimed, acclamation, accolade, accolades, accommodative, accommodative, accomplish, accomplished, accomplishment, accomplishments, accurate, accurately, achievable, achievement, achievements, achievable, acumen, adaptable, adaptive, adequate, adjustable, admirable, admirably, admiration, admire, admirer, admiring, admiringly, adorable, adore, adored, adorer, adoring, adoringly, adroit, adroitly, adulate, adulation, adulatory, advanced, advantage, advantageous, advantageously, advantages, adventuresome, adventurous, advocate, advocated, advocates, affability, affable, affably, affectation, affection, affectionate, affinity, affirm, affirmation, affirmative, affluence, affluent, afford, affordable, affordably, affordable, agile, agilely, agility, agreeable, agreeableness, agreeably, all - around, alluring, alluringly, altruistic, altruistically, amaze, amazed, amazement, amazes, hello, helloly, ambitious, ambitiously, ameliorate, amenable, amenity, amiability, amiabily, amiable, amicability, amicable, amicably, amity, ample, amply, amuse, amusing, amusingly, angel, angelic, apotheosis, appeal, appealing, applaud, appreciable, appreciate, appreciated, appreciates, appreciative, appreciatively, appropriate, approval, approve, ardent, ardently, ardor, articulate, aspiration, aspirations, aspire, assurance, assurances, assure, assuredly, assuring, astonish, astonished, astonishing, astonishingly, astonishment, astound, astounded, astounding, astoundingly, astutely, attentive, attraction, attractive, attractively, attune, audible, audibly, auspicious, authentic, authoritative, autonomous, available, aver, avid, avidly, award, awarded, awards, awe, awed, awesome, awesomely, awesomeness, awestruck, awsome, backbone, balanced, bargain, beauteous, beautiful, beautifullly, beautifully, beautify, beauty, beckon, beckoned, beckoning, beckons, believable, believeable, beloved, benefactor, beneficent, beneficial, beneficially, beneficiary, benefit, benefits, benevolence, benevolent, benifits, best, best - known, best - performing, best - selling, better, better - known, better - than - expected, beutifully, blameless, bless, blessing, bliss, blissful, blissfully, blithe, blockbuster, bloom, blossom, bolster, bonny, bonus, bonuses, boom, booming, boost, boundless, bountiful, brainiest, brainy, brand - new, brave, bravery, bravo, breakthrough, breakthroughs, breathlessness, breathtaking, breathtakingly, breeze, bright, brighten, brighter, brightest, brilliance, brilliances, brilliant, brilliantly, brisk, brotherly, bullish, buoyant, cajole, calm, calming, calmness, capability, capable, capably, captivate, captivating, carefree, cashback, cashbacks, catchy, celebrate, celebrated, celebration, celebratory, champ, champion, charisma, charismatic, charitable, charm, charming, charmingly, chaste, cheaper, cheapest, cheer, cheerful, cheery, cherish, cherished, cherub, chic, chivalrous, chivalry, civility, civilize, clarity, classic, classy, clean, cleaner, cleanest, cleanliness, cleanly, clear, clear - cut, cleared, clearer, clearly, clears, clever, cleverly, cohere, coherence, coherent, cohesive, colorful, comely, comfort, comfortable, comfortably, comforting, comfy, commend, commendable, commendably, commitment, commodious, compact, compactly, compassion, compassionate, compatible, competitive, complement, complementary, complemented, complements, compliant, compliment, complimentary, comprehensive, conciliate, conciliatory, concise, confidence, confident, congenial, congratulate', 'positive')]
    pos_tweets = [('admiration', 'positive'), ('admire', 'positive'), ('admirer', 'positive'), ('admiring', 'positive'),
                  ('admiringly', 'positive'), ('adorable', 'positive'), ('adore', 'positive'), ('adored', 'positive'),
                  ('adorer', 'positive'), ('adoring', 'positive'), ('adoringly', 'positive'), ('adroit', 'positive'),
                  ('adroitly', 'positive'), ('adulate', 'positive'), ('adulation', 'positive'),
                  ('adulatory', 'positive'), ('advanced', 'positive'), ('advantage', 'positive'),
                  ('advantageous', 'positive'), ('advantageously', 'positive'), ('advantages', 'positive'),
                  ('adventuresome', 'positive'), ('adventurous', 'positive')]

    neg_tweets = [('I do not like this car', 'negative'),
                  ('This view is horrible', 'negative'),
                  ('I feel tired this morning', 'negative'),
                  ('Larry is admire', 'negative'),
                  ('He is my enemy', 'negative')]

    tweets = []

    for (words, sentiment) in pos_tweets + neg_tweets:
        words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
        tweets.append((words_filtered, sentiment))

    # print(tweets)

    test_tweets = [(['feel', 'happy', 'this', 'morning'], 'positive'),
                   (['larry', 'friend'], 'positive'),
                   (['not', 'like', 'that', 'man'], 'negative'),
                   (['house', 'not', 'great'], 'negative'),
                   (['your', 'song', 'annoying'], 'negative')]

    def get_words_in_tweets(tweets):
        all_words = []
        for (words, sentiment) in tweets:
            all_words.extend(words)
        return all_words

    def get_word_features(wordlist):

        wordlist = nltk.FreqDist(wordlist)

        word_features = wordlist.keys()
        word_features_count = wordlist.values()
        result = {}

        for (i, j) in zip(word_features, word_features_count):
            result[i] = j

        return result

    allwords = get_words_in_tweets(tweets)

    word_features = get_word_features(allwords)

    final = sorted(word_features.items(), key=lambda kv: kv[1], reverse=True)

    document = ['love', 'this', 'car']

    def extract_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    xy = extract_features(document)
    training_set = nltk.classify.apply_features(extract_features, tweets)

    def train(labeled_featuresets, estimator=nltk.ELEProbDist):
        label_probdist = estimator(nltk.label_freqdist)
        feature_probdist = {}
        return nltk.NaiveBayesClassifier(label_probdist, feature_probdist)

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    tweet2 = 'Larry is admire'

    #tweet = "we are going to play in rain"
    tweet1 = word_tokenize(tweet)
    x = 0
    y = 0
    z = 0
    i = 0
    j = 0
    nextelem = ''
    abc = ''
    while i < len(tweet1):
        if (tweet1[i] == 'not'):
            running = True
            i += 1
            while (running):

                if '(' + tweet1[i] + ')' in open('pos.py').read():
                    print("inside mama")
                    y += 1
                    running = False
                    i += 1
                elif '(' + tweet1[i] + ')' in open('neg.py').read():
                    x += 1
                    running = False
                    i += 1
                else:
                    i += 1

        elif '(' + tweet1[i] + ')' in open('pos.py').read():
            x += 1
            i += 1
        elif '(' + tweet1[i] + ')' in open('neg.py').read():
            y += 1
            i += 1
        else:
            i += 1
    #print(tweet)
    #print("positive:",x)
    #print("negative",y)
    if '(' + 'sure' + ')' in open('pos.py').read():
        z += 1
    #print ("neutral",z)
    if (x > y):
        return 1
    elif (y > x):
        return -1
    else:
        return 0






import csv
import poschunking
import checkrediselements
import sentiment
content_text=" "


def fetchcontent():

    global content_text

    content_text= poschunking.contentextract()

    return content_text




def iteratecsv(keyword,url):
    #print(keyword)
   #print("11111111111111111111111111111")


    f = open(url, "r")
    reader1 = csv.reader(f)
    for row in reader1:
      #  print("1" ,row)

        if (row[0] == str(keyword).lower()):
            print("checking if ad or not ad",keyword)
            if (row[2] == "ad"):
               print("ad nany ad",row[0])

               return "ok",row[0],row[1]

            else:
                print("non ad",row[0])

    return "not ok",row[0],row[1]


def parse(probable_keywords):
    #print("hello")
    url="ads.csv"  #this url or address path is fixed dont change

    to_database=[]
  #  probable_keywords =  ['sheets', 'led', 'bus', 'bulbs', 'television']  # ------------------this line change with keywords
  #  probable_keywords=['advantages', 'monitor', 'battery', 'Advantages', 'easy', 'screen', 'September', 'keyboard', 'November', 'October', 'large', 'Year', 'small', 'portable', 'weight', 'connect', 'best', 'computer', 'Disadvantages', 'PC', 'February', 'January', 'mobile', 'April', 'December', 'comment', 'less', 'Lots', 'Flash', 'number', 'intellectual', 'Desktop', 'communicationaccess', 'tablets', 'fast', 'portabledevices', 'desktop', 'expensive', 'compact']

  #  print("Inside parse came ",probable_keywords)
    probable_keywords.sort()
    probabilities = []
  #  print("Inside parse came ", probable_keywords)

    for i in probable_keywords:
       # print("helllo",i)

        ad, word, probability = iteratecsv(i,url)
        #print("next",probability)
        # print(ad,word, probability)
        if (ad == "ok"):
            probabilities.append((word, probability))
            # print(word,probability)

    probabilities.sort(key=lambda x: x[1])
    print("proba--sort",probabilities)
   # print("probabilities",probabilities)
    length = len(probabilities)
#    ad_keywo=probabilities[length-1]

    for i in range(0,length):
        to_database.append(probabilities[i][0])

    '''    
    ad_keyword=ad_keywo[0]
    print("hhaa",ad_keyword)

    createtweetsentence(ad_keyword)
    '''
    print("to database",to_database)

    result=checkrediselements.databaseitems(to_database)
    #print("finally",result)

    for i in range(0,len(result)):
         #print("twwetsending",result[i])
         result,boolean_value=createtweetsentence(result[i])
         print("sentiment",result,boolean_value)
         if(boolean_value==1):
             return result


def createtweetsentence(ad_keyword):
    #if ad_keyword in content_text:
    #    print("partyy")

    #print("---------------------------------------")
    global content_text
    content_text=poschunking.returncontenttext()
    #content_text=fetchcontent()
    #print(content_text)

    pos = content_text.find(ad_keyword)
    #print("hello", pos)
    text_tweet_like=content_text[pos-170:pos+100]
    #print(text_tweet_like)
    value=sentiment.sentimental_analysis(text_tweet_like)
    if(value==1 or value==0):
        return ad_keyword,1
    else:
        return "",0

l=[]
#parse(l)
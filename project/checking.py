import redis
import poschunking
import parse
from flask import Flask
import checkrediselements
r=redis.Redis(host='localhost',port=6379)

def everythinghere(url):
    print("url",url)
    print("checking.py")
    #url = "https://09tfrahimi.wordpress.com/tag/advantages-and-disadvantages-of-desktop-pcs-laptops-tablets/"
    probable_keywords = poschunking.preprocessing(url)
    print("probable_keywords", probable_keywords)
    key_ad = parse.parse(probable_keywords)
    print("keyad", key_ad)
    publisher_name = r.lindex(key_ad, 0)
    print("publishername", publisher_name)
    # r.hincrby(publisher_name,key_ad,1)
    r.incr(publisher_name, 1)
    path="/Users/gouthamrajnagilla/Desktop/projject/project/images/"

    image_path = path + publisher_name + ".jpeg"
   # print(image_path)
    # image_url=r.lindex(publisher_name,0)
    return image_path


'''
r=redis.Redis(host='localhost',port=6379)
l=[]

l=r.scan(0)
result=l[1]
value="cars"
if value in result:
    print("ok")
    print(r.lrange(value,-100,100))


'''

'''
file_read=open("","r")
tweet=""
final_list_of_tweets=[]
for i  in file_read:
# print("hello",i)
 if(i.find("@@@")):
     print("hello",i)
     final_list_of_tweets.append(tweet)
    # tweet=""
     continue
 elif(i.find('\n')):
    continue
 else:

     tweet=tweet+i


print(final_list_of_tweets)

'''
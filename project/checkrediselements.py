import redis
from threading import Thread
import poschunking


r=redis.Redis(host='localhost',port=6379)


def databaseitems(list_of_keywords):
    #database_containing_items = r.scan(1)[1]
    database_containing_items =r.keys("*")
    print("checkingrediselements",database_containing_items)
    database_containing_items.sort()

    #list_of_keywords = ['monitor','sheets', 'led', 'bus', 'electronics', 'bulbs', 'television']
    s = set(database_containing_items)
    print("daabase",s)
    s1 = set(list_of_keywords)
    print("keywords list baby",s1)
    result = list(s.intersection(s1))
    print(result)
    #time.sleep(10)

    return result

lis=[]

#print(databaseitems(lis))


#to create multiple threads
'''

lis=[]
try:
    thread=Thread(target=databaseitems(lis))
    thread.start()
    thread1=Thread(targ=poschunking.contentextract())
    thread1.start()
    
except:
    print("error in creation of threads")

finally:
    print("ok")

#print(poschunking.contentextract())

'''
#lis=[]
#print(databaseitems(lis))

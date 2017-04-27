#from flask import Flask,url_for,redirect

import redis



r=redis.Redis(host="localhost",port=6379)



user="user1"
image="image1"
r.hset(user,image,1)
user="user1"
image="image2"
r.hset(user,image,1)

image="image2"
def f2():
 r.hincrby(user,image,1)
 print(r.hmget(user,"image1","image2"))

for i in range(0,10):
    f2()






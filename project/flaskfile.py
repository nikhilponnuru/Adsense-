from flask import Flask,render_template,Session,send_file
import redis
import hashlib
from flask import request
import json
import os
import checkrediselements
from flask import send_file
import poschunking
import checking
import base64

r=redis.Redis(host='localhost',port=6379)

app = Flask(__name__)
random_number=os.urandom(24)
app.secret_key =random_number
user_ip=0


@app.route('/')
def say_welcome():
    #print("hello")
    return "ok"


@app.route('/login')
def welcome():
    user_ip=request.remote_addr
#    r.lpush('user_ip_addresses',user_ip)
    return render_template('login.html',ip=user_ip)




def event_stream():
    pubsub = r.pubsub()
    pubsub.subscribe('notifications')
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']


#these 2 endpoints from frontend




@app.route('/stream')
def stream():
    #this in frontend for displaying ad using EventSource object to call this endpoint
    return Flask.Response(event_stream(), mimetype="text/event-stream")
    #use render_template here and send event_stream()








@app.route('/publisherlogin',methods=['POST'])
def login():
    print("hello baby")

    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']


        hash_object=hashlib.md5(password)
      #  password=hash_object.hexdigest()

        value = r.hget('publisher', username)



        if(value!="nil"):

            if(value==password):
                return render_template('publisher-feed.html', user=username)

            else:
                return "password didnt match"

        else:
            return "first please signup"


        r.save()







publisher_username=''
image=''
filepath=''


@app.route('/uploadimage', methods=['GET', 'POST'])
def upload_file1():
    username=request.form['uname']
    tag=request.form['settag']
    name=request.form['nameof']
    if request.method == 'POST':
        f = request.files['file']
        if not os.path.exists(username):
            os.makedirs(username)
            f.filename=name+".jpeg"
            f.save(username+"/"+f.filename)
            r.lpush(tag,name)
            r.set(name,0)
            f.save("/Users/gouthamrajnagilla/Desktop/projject/project/images/"+f.filename)
        else:
            f.save(username + "/" + f.filename)



        return render_template('publisher-feed.html')





'''
@app.route('/logout/<username>')
def logout(username):

    Session.pop(username,None)

'''

@app.route('/getanalytics',methods=['POST'])
def analytics():
    companyname=request.form['usname']
    value=r.get(companyname)
    return value





@app.route('/show')
def showing():
     #print type(json.dumps(list(r.smembers('username'))))
     return json.dumps(list(r.smembers('username')))
    # return "ok"


#sending image back from frontend


@app.route('/getdata',methods=['POST'])
def gettingwebdata():
    print("inside getdata")
    uri=request.form['url']
    url=str(uri)



    ad_image=checking.everythinghere(url)
    print(ad_image)

    with open(ad_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    #print("base64 is:--",encoded_string)
    #return send_file(ad_image,mimetype='image/jpg')
    print(encoded_string)
    return encoded_string









   # final_keywords=sentimental_analysis(keywords)
  # return image_url



#to display leaderboard

'''
@app.route('/leaderboard')
def getting_leaderboard():
    data=[(100,"nik"),(20,"kame"),(30,"gauti")] #this must be the final data to be used for leadeboard
    for (score,user) in data:
        r.zadd("leadeboard",score,user)
    print(r.zrevrange("leaderboard",0,10)) #to get top 10 scorers)

    return r.zrevrange("leaderboard",0,10)


'''

@app.route('/send_image_data')
def image_data():
    try:
        resultimage = r.hget()

      #  return send_file('file:///Users/gouthamrajnagilla/Desktop/projject/project/images/image.jpg', attachment_filename='allpaper.jpg')


    except Exception as e:
        return str(e)






#All websites hosting is done here

@app.route('/sample.html')
def site1():
    return render_template("sample.html")

@app.route('/sample2.html')
def site2():
    return render_template("sample2.html")

@app.route('/sample3.html')
def site3():
    return render_template("sample3.html")

@app.route('/sample4.html')
def site4():
    return render_template("sample4.html")

@app.route('/sample5.html')
def site5():
    return render_template("sample5.html")





if __name__ == '__main__':

   app.run(threaded=True)  #for making flask to listen to multiple requests







'''

from flask import Flask


app = Flask(__name__)
#r = redis.Redis(host='localhost', port=6379)

@app.route('/hello')
def hello():
    return "hello"


if __name__== '__main__':
    app.run()
'''




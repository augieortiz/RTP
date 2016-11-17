import sys, os
sys.path.append('var/www/RTP')
import web
import json
import sys
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import pymongo
from pymongo import TEXT
import string
from collections import Counter
import operator
import re
import lxml.etree
import hashlib
from rake import *
import urlparse
import urllib
from bson.objectid import ObjectId

_version = '4.5.1.1'

urls = (
       '/', 'index',
        '/receive', 'receive',
        '/add', 'add',
        '/thesis', 'thesis',
        '/login', 'login',
        '/logout', 'Kill',
        '/instance', 'instance', 
        '/instanced', 'instanced',
        '/instancec', 'instancec',
        '/documentd', 'documentd', 
        '/spider', 'spider',
        '/custom', 'custom',
        '/results', 'results',
        '/welcome', 'welcome'
)
web.config.debug = True

app = web.application(urls, globals())
application = app.wsgifunc()
curdir = os.path.dirname(__file__)
db = web.database(dbn='mysql', user='root', pw='Augie03!', db='dbRTP')


store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'login': 0,'privilege': 0,'user':'anonymous', 'instanceSelected': 'none',  'instanceList': [], 'lastVisted': '/ThisIsNotTheDataYouAreLookingFor'})

class index:
    def GET(self):
            root = os.path.dirname(__file__) 
            render = web.template.render("/var/www/RTP/templates/")
            if logged():
                return render.index("True", session.user)
            else:
                return render.login("False", "", _version)
class thesis:
    def GET(self):
            render = web.template.render("/var/www/RTP/templates/")
            if logged():
                return render.thesis("True", session.user)
            else:
                return render.login("alert", "This data is sensitive and therefore you must have credentials to view the thesis document.", _version)
class login:
    def GET(self):
         if logged():
            render = web.template.render("/var/www/RTP/templates/")
            return render.index("already logged in", session.user)
         else:
            render = web.template.render("/var/www/RTP/templates/")
            return render.login("", "", _version)

    def POST(self):
        name, passwd = web.input().email, web.input().password
        try:
            ident = db.select('Users', where='email=$name', vars=locals())[0]
        except IndexError:
            render = web.template.render("/var/www/RTP/templates/")
            return render.login("error", "This is not an account with us. Please contact the admin to receive an account.", _version)
        else:
            try:
                if passwd == ident['pass']:
                    session.login = 1
                    session.privilege = ident['privilege']
                    session.user = ident['user']
                    render = web.template.render("/var/www/RTP/templates/")

                    #Get all the instance and set the session variable
                    instances = getInstances()
                    session.instanceList = instances
                    return render.index('True', session.user)
                else:
                    render = web.template.render("/var/www/RTP/templates/")
                    return render.login("error", "You have entered an invalid password. Try again.", _version)
            except Exception, e:
                render = web.template.render("/var/www/RTP/templates/")
                return render.login("error", "Error on server" + "\n" + str(e), _version)
class Kill:
    def GET(self):
        # Remove session data
        # And redirect the user to the main page
        session.kill()
        render = web.template.render("/var/www/RTP/templates/")
        return  render.login("False", "", _version)
class receive:
    def GET(self):
            render = web.template.render("/var/www/RTP/templates/")
            if logged():
                return render.receive("", "", "/welcome", "first", "True", session.user, "", session.instanceSelected)
            else:
                return render.login("warning", "You must login before you receive data.", _version)
    def POST(self):
            convo = web.input()
            db = connectToDatabase()
            db.RTP.create_index([('title', TEXT), ('document', TEXT)], default_language='english')
            search = convo['conversation']
            keywords = watsonProcess(search)
            data, index = searchDatbaseRake(db, keywords)
            render = web.template.render('/var/www/RTP/templates/')
            newdata = convertArray(data, search)
            newdata = sorted(newdata, key=lambda x: x[1], reverse=True)

            try:
                if not data[1]:
                    db.insert('SearchResults', session_id=session.session_id, score="", currentInstance=session.instanceSelected, searchQuery=search, found=0)
                    return render.receive("Looks like you there was no data found...Try again maybe.", session.lastVisted, "error", "True", session.user, "notfound", session.instanceSelected)
                else:
                    session.lastVisted = data[0][index];
                    present = data[0][index] 
                    return render.receive("We found the presentation data of:  " + data[3][index], search, present, "success", "True", session.user, newdata, session.instanceSelected)
            except Exception,e:
                db = web.database(dbn='mysql', user='root', pw='Augie03!', db='dbRTP')
                db.insert('SearchResults', session_id=session.session_id, score="", currentInstance=session.instanceSelected, searchQuery=search, found=0)
                return render.receive("Looks like you there was no data found...Try again maybee.", "", session.lastVisted, "error", "True", session.user, "notfound", session.instanceSelected)

class results:
    def GET(self):
        myvar = dict(session=session.session_id)
        results = db.select('SearchResults', myvar, where="session_id=$session")
        render = web.template.render("/var/www/RTP/templates/")
        return render.results(results)
class documentd:
    def POST(self):

            dele = web.input()
            client = MongoClient()
            db = client.RTP
            render = web.template.render("/var/www/RTP/templates/")
            ident = dele['dataDocument']
            query = db.RTP.delete_one( {"_id" : ObjectId(ident)})
            if logged():
                 raise web.seeother('/add')
            else:
                return render.login("warning", "You must login before you add data.", _version)

class instance:
    def POST(self):

            newInstance = web.input()
            client = MongoClient()
            db = client.RTP
            render = web.template.render("/var/www/RTP/templates/")
            #insert new instance - username hard coded at the moment
            query = db.Instances.insert( {"username": session.user, "topic": newInstance['newInstance']})
            instances = getInstances()
            session.instanceSelected = newInstance['newInstance']
            session.instanceList = instances            
            if logged():
                raise web.seeother('/add')
            else:
                return render.login("warning", "You must login before you add data.", _version)
class instanced:
    def POST(self):

            dele = web.input()
            client = MongoClient()
            db = client.RTP
            render = web.template.render("/var/www/RTP/templates/")
            #insert new instance - username hard coded at the moment
            try:
                iid = db.Instances.find_one({"username": session.user, "topic" : session.instanceSelected }, {"_id": -1})
                deleteDocuemnts = db.RTP.remove( { "instanceID": iid['_id'] })
                query = db.Instances.delete_one( {"username" : session.user, "topic": dele['deleteInstance']})
                instances = getInstances()
                session.instanceList = instances
                session.instanceSelected = instances[0]
                if logged():
                    raise web.seeother('/add')
                else:
                    return render.login("warning", "You must login before you add data.", _version)
            except Exception,e:
                raise web.seeother('/add')

class instancec:
    def POST(self):
            selection = web.input()
            session.instanceSelected = selection['selInt']
            session.lastVisted = "/welcome"
            result, count = getAllData()                

            if logged():
                 raise web.seeother('/add')
            else:
                return render.login("warning", "You must login before you add data.", _version)
class add:
    def GET(self):           
            render = web.template.render("/var/www/RTP/templates/")
            if logged():
                result, count = getAllData()
                if(result != "Empty"):
                    return render.add("", "", 'True', session.user, result, count, session.instanceList, session.instanceSelected)
                else:
                    emptyList = [];
                    return render.add("", "", 'True', session.user, result, count, emptyList, session.instanceSelected)
            else:
                return render.login("warning", "You must login before you add data.", _version)
    def POST(self):
        try:
           #Database connections
            client = MongoClient()
            db = client.RTP
            url = web.input()
            address = url['url']


            page = requests.get(address)
            soup = BeautifulSoup(page.text)
            t = soup.find('title')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            visible_text = os.linesep.join([s for s in visible_text.splitlines() if s])
            visible_text = visible_text.replace("\n", " ")
            
            title = t.text
            document  = visible_text

            isDuplicate = checkDupURL(address)
            instances = getInstances()
            #INSERT DATAPOINT
            if isDuplicate == True:
                result, count = getAllData()
                
                render = web.template.render("/var/www/RTP/templates/")
                return render.add(url, "error", "True", session.user, result, count, session.instanceList, session.instanceSelected)
            else:
                iid = db.Instances.find_one({"username": session.user, "topic" : session.instanceSelected }, {"_id": -1})
                query = db.RTP.insert_one( { "url": address, "type": "html", "title" : title, "document" : document, "instanceID": iid['_id'] })
                result, count = getAllData()
                render = web.template.render('/var/www/RTP/templates/') 
                return render.add("Success.  The site: " + title + " has been added into the database.", "success", "True", session.user, result, count, session.instanceList, session.instanceSelected)

        except Exception,e: 
            instances = getInstances()
            result,count = getAllData()
            render = web.template.render("/var/www/RTP/templates/")
            return render.add(str(e), "error", "True", session.user, result, count, session.instanceList, session.instanceSelected)
class spider:
    def GET(self):
        result, count = getAllData()                
        render = web.template.render("/var/www/RTP/templates/")
        if logged():
            return render.add("", "", 'True', session.user, result, count, session.instanceList, session.instanceSelected)
        else:
            return render.login("warning", "You must login before you add data.", _version)
    def POST(self):
         #Database connections
        client = MongoClient()
        db = client.RTP
        url = web.input()
        topLeveladdress = url['url']
        try:
            urlList = getURLList(topLeveladdress)
        except:
            result, count = getAllData()
            render = web.template.render('/var/www/RTP/templates/') 
            return render.add("Error on site map retrieval.", "error", "True", session.user, result, count, session.instanceList, session.instanceSelected)


        for index, address in enumerate(urlList):
            try:
                title = ""
                page = requests.get(address)
                soup = BeautifulSoup(page.text)
                t = soup.find('title')
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                visible_text = soup.getText()
                visible_text = os.linesep.join([s for s in visible_text.splitlines() if s])
                visible_text = visible_text.replace("\n", " ")
                title = t.text
                document  = visible_text
            except:
                result, count = getAllData()
                render = web.template.render('/var/www/RTP/templates/') 
                if index > 1:
                    result, count = getAllData()
                    render = web.template.render('/var/www/RTP/templates/') 
                    return render.add("Error on retrieval. Some documents may still have been collected. Please review.", "error", "True", session.user, result, count, session.instanceList, session.instanceSelected)

            isDuplicate = checkDupURL(address)
            if isDuplicate != True:
                try:
                    iid = db.Instances.find_one({"username": session.user, "topic" : session.instanceSelected }, {"_id": -1})
                    query = db.RTP.insert_one( { "url": address, "type": "html", "title" : title, "document" : document, "instanceID": iid['_id'] })
                except Exception, e:
                    result,count = getAllData()
                    render = web.template.render("/var/www/RTP/templates/")
                    return render.add(str(e), "error", "True", session.user, result, count, session.instanceList, session.instanceSelected)
        #End of inserts
        result, count = getAllData()
        render = web.template.render('/var/www/RTP/templates/') 
        return render.add("Success! We added a total of " + str(len(urlList)) + " documents to this instance." ,"success", "True", session.user, result, count, session.instanceList, session.instanceSelected)

class custom:
    def GET(self):
        client = MongoClient()
        db = client.RTP
        data = web.input()
        docID = data._id
        iid = db.Instances.find_one({"username": session.user, "topic" : session.instanceSelected }, {"_id": -1})
        result = db.RTP.find( {"instanceID" : iid['_id'], "_id": ObjectId(docID)}, {"title": -1, "type": -1, "document": -1, "url": -1})
        render = web.template.render('/var/www/RTP/templates/')
        return render.custom(result[0]['title'], result[0]['document'], session.session_id)

    def POST(self):
        client = MongoClient()
        db = client.RTP
        custom = web.input()

        document = custom['customDocument']
        title = custom['customTitle']

        try:
            iid = db.Instances.find_one({"username": session.user, "topic" : session.instanceSelected }, {"_id": -1})
            query = db.RTP.insert_one( { "url": "", "type": "custom", "title" : title, "document" : document, "instanceID": iid['_id'] })
            result, count = getAllData()
            render = web.template.render('/var/www/RTP/templates/') 
            return render.add("Success.  The document: " + title + " has been added into the database.", "success", "True", session.user, result, count, session.instanceList, session.instanceSelected)
        except Exception, e:
            result,count = getAllData()
            render = web.template.render("/var/www/RTP/templates/")
            return render.add(str(e), "error", "True", session.user, result, count, session.instanceList, session.instanceSelected)

class welcome:
    def GET(self):
        render = web.template.render('/var/www/RTP/templates/')
        return render.welcome()

def convertArray(data, search):
    newList = [];
    for count,row in enumerate(data[0]):
        if data[0][count] == "":
            data[0][count] = "/custom" + "?title=" + data[3][count] + "&document=" + data[4][count]
        newTup = (data[0][count], data[1][count], data[2][count], data[3][count], data[4][count])
        newList.append(newTup)
        db.insert('SearchResults', session_id=session.session_id, currentInstance=session.instanceSelected, searchQuery=search, title=data[3][count], score=float(data[1][count]), keyword=data[2][count], document=data[4][count], found=1) 
    return newList 

def getAllData():
    #Database connections
    client = MongoClient()
    db = client.RTP
    try:
        iid = db.Instances.find_one({"username": session.user, "topic" : session.instanceSelected }, {"_id": -1})
        query = db.RTP.find( {"instanceID" : iid['_id']}, {"title": -1, "type": -1, "document": -1, "url": -1})
        return query, query.count()
    except Exception, e:
        #Error on query, return 0
        return "Empty", 0;
    

def getInstances():

    iList = []
    client = MongoClient()
    db = client.RTP
    query = db.Instances.find( {"username" : session.user }, {"topic" : -1})
    if query.count() > 0:
        for index,item in enumerate(query):
            iList.append(item['topic'])
        if session.instanceSelected == 'none':
            session.instanceSelected = iList[0]

    return iList

def getURLList(address):
    url = address
    urls = [url] #urls to scrape
    visited = [url] #record of urls already visited
    while len(urls) > 0:
        text = ""
        try: 
            text = urllib.urlopen(urls[0]).read()
        except:
            print urls[0] + ": This is broke "
        soup = BeautifulSoup(text, "html.parser")

        urls.pop(0)

        for tag in soup.findAll('a', href=True):
            if "#" not in tag['href']:
                 tag['href'] = urlparse.urljoin(url, tag['href'],)
                 if url in tag['href'] and tag['href'] not in visited:
                    visited.append(tag['href'])

    print len(visited)
    return visited

def checkDupURL(url):
    client = MongoClient()
    db = client.RTP
    count = db.RTP.find( {"url": url} ).count()
    
    if count > 0:
        return True
    else: 
        return False

def connectToDatabase():
    print "Establishing connection to database.."
    try:
        client = MongoClient()
        db = client.RTP
        collection = db.RTP
        print(collection)
    except RuntimeError:
        "Connection failed to database. Exiting Application..."
        exit(0)
    print "Success! Connected to WikiFootball Mongo database"
    return db
def watsonProcess(search):
    print "Starting Rake parsing process on tweets..."
    rakeData = []
    count_all = Counter()
    phrases = txtRake(search)
    for term, score in phrases:
            rakeData.append(term)

    count_all.update(rakeData)
    print "Tweets were parsed of special characters, and concatenated for mining."
    return count_all

def searchDatbaseRake(db, keywords):
    searchData = []
    searchData.append([])
    searchData.append([])
    searchData.append([])
    searchData.append([])
    searchData.append([])
    keywords = keywords.most_common(25)
    for x in range (0,len(keywords)):
        try:
            iid = db.Instances.find_one({"username": session.user, "topic" : session.instanceSelected }, {"_id": -1})
            ident = iid['_id']
            result = db.RTP.aggregate( [ { "$match": { "$text": { "$search": keywords[x][0] }, "instanceID" : ObjectId(ident) }  },  { "$project": { "url": -1, "title": -1, "document": -1, "_id": 0, "score": { "$meta": "textScore" } } }, { "$match": {  "score": {  "$gt": 1 } } } ])
        except RuntimeError:
            print "Search has failed with keywords : " + keywords[x][0] + ". Retrying with next keyword."
        for document in result:
            searchData[0].append(str(document['url']))
            searchData[1].append(document['score'])
            searchData[2].append(keywords[x][0])
            searchData[3].append(document['title'].encode('ascii', 'ignore'))
            searchData[4].append((document['document']))
    if not searchData[0]:
        print "No results found..."
        return searchData, 0
    else:
        try:
            #Find index of MAX score
            maxScore = 0;
            maxIndex = 0;
            for index in range(0,len(searchData[1])):
                if searchData[1][index] > maxScore:
                    maxScore = searchData[1][index]
                    maxIndex = index
        except IndexError:
            searchData = []
            "Error on results. Retry."
    return searchData, maxIndex
def txtRake(text):

    # Split text into sentences
    sentenceList = split_sentences(text)
    scriptpath = os.path.dirname(__file__)
    stoppath = os.path.join(scriptpath, 'SmartStoplist.txt')
    stopwordpattern = build_stop_word_regex(stoppath)

    # generate candidate keywords
    phraseList = generate_candidate_keywords(sentenceList, stopwordpattern)

    # calculate individual word scores
    wordscores = calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
    if debug: print keywordcandidates

    sortedKeywords = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    if debug: print sortedKeywords

    totalKeywords = len(sortedKeywords)


    rake = Rake(stoppath)
    keywords = rake.run(text)
    return keywords

def logged():
    if session.get('login', 1):
        return True
    else:
        return False
    ###
def notfound():
    render = web.template.render("/var/www/RTP/templates/")
    return web.notfound(render.notfound("Page not found..."));

    # You can use template result like below, either is ok:
    #return web.notfound(render.notfound())
    #return web.notfound(str(render.notfound()))

app.notfound = notfound
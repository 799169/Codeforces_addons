# coding: utf-8
# python3

import os
import sys
import json
import io
import html
import werkzeug
from werkzeug.utils import cached_property
import urllib.request
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser

b = RoboBrowser(parser="html.parser")

def getURL(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read()
    return html.decode('utf-8')

def CodeDownload(sub):
    try:
        print("Downloading Code....")
        url = getURL("https://codeforces.com/contest/"+str(sub["contestId"])+"/submission/"+str(sub["id"]))
        # print("url : ", url)
        code = url.split("""<pre id="program-source-text" class="prettyprint lang-cpp linenums program-source" style="padding: 0.5em;">""")[1].split("</pre>")[0]
        code = html.unescape(code)
        print("promgrammingLanguage: {}".format(sub["programmingLanguage"]))
        f = open("./solutions/" + str(sub["id"]) + ".sol","w")
        if "Python" not in sub["programmingLanguage"]:
            f.write(code+"//Backup {} using Codeforces API.".format(str(sub["id"])))
        else:
            f.write(code+"# Backup {} using Codeforces API.".format(str(sub["id"])))
        f.close()
        return True
    except Exception as err:
        print("Error downloading: {0}".format(err))
        return False    
    
def submit(sub):
    print("Submit for",sub["id"],"starts")
    
    b.open("https://codeforces.com/problemset/submit")
    form2 = b.get_form(class_="submit-form")
    form2["submittedProblemCode"] = str(sub["contestId"]) + sub["problem"]["index"]

    path = "./solutions/" + str(sub["id"]) + ".sol"
    try:
        if not os.path.exists(path):
            if not CodeDownload(sub):
                raise Exception("Can not download the code!")
        form2["sourceFile"] = path
    except Exception as e:
        print("Error when selecting file {0}".format(e))
        return False

    language = sub["programmingLanguage"]
    print("language: {}".format(language))
    if "C++11" in language: # GNU G++11 5.1.0
        form2["programTypeId"] = "42"
    if "C++14" in language: # GNU G++14 6.4.0
        form2["programTypeId"] = "50"
    if "C++17" in language: # GNU G++17 7.3.0
        form2["programTypeId"] = "54"
    if "Java" in language: # Java 1.8.0_162
        form2["programTypeId"] = "36"
    if "Python" in language: # Python 3.7.2
        form2["programTypeId"] = "31"
    if "Golang" in language: # Go 1.12.6
        form2["programTypeId"] = "32"

    b.submit_form(form2)

    if b.url[-6:] != "status":
        print("Error when submitting...")
        return False

    print("Code id: {} submitted successfully.".format(sub["id"]))
    return True

if __name__ == "__main__":
    number = 100
    originUser = input("Username you want to copy : ")

    fr = open("user.txt","r")
    ln = fr.readlines()
    Username = ln[0].strip()
    Password = ln[1].strip()

    try:
        res = json.loads(getURL("https://codeforces.com/api/user.status?handle={}&count={}".format(originUser, number)))
        if res["status"] != "OK":
            raise Exception("Bad status", res["status"])
    except Exception as err:
        print("Error 202 Can't get API: {}".format(err))
        exit(202)

    fliter = input("Filter for submissions\n (True: no filter) : ")

    ok = []
    for sub in res["result"]:
        if eval(fliter):
            sub["ok"] = False
            ok.append(sub)
            print("OK submission: {}".format(sub["id"]))
    print("Filter done!")

    print("Try to copy {} submissions. ".format(len(ok)))
    print("Not to copy {} submissions. ".format(len(res["result"]) - len(ok)))

    print("Login with known username and password")
    b.open("https://codeforces.com/enter")
    form = b.get_form("enterForm")
    form["handleOrEmail"] = Username
    form["password"] = Password
    b.submit_form(form)

    if b.url=="https://codeforces.com/":
        print("Login Success!")
    else:
        print("Error 201 Fatal Failure, can not login! -> {}".format(b.url))
        exit(201)

    for i in range(1,6):
        print("Try No.",i,"started")
        for x in ok:
            if x["ok"]:
                continue
            if submit(x):
                print("Submit Success: {}".format(x["id"]))
                x["ok"]=True
            else:
                print("Submit Failure: {}".format(x["id"]))

    for i in ok:
        if not i["ok"]:
            print("Exit 203 Transfer failed.Maybe quota exceeded. Try again a few hours later!")
            f = open("secret.text","w")
            f.write(str(ok))
            f.close()
            exit(203)
            
    print("Exit 0 Successfully transferred!")
    exit(0)
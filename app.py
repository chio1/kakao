from flask import Flask, request, jsonify
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
app = Flask(__name__)
response = urlopen('http://ilgo.gen.hs.kr/xboard/board.php?tbnum=49')
soup = BeautifulSoup(response, 'html.parser')
s = soup.find_all(class_="today")
    
def meals():
        for i in s:
            
            if(i.find(class_="content") == None):
                return "오늘 밥없다"
            else:
                return i.find(class_="content").text
def days():
    for j in s:
        return j.find(class_="day_num").text
    
def meals_tom():
    for i in s:

        if(i.next_sibling.next_sibling.find(class_="content") == None):
            return "내일 밥없다"
        else:
            return i.next_sibling.next_sibling.find(class_="content").text
def days_tom():
    for j in s:
        return j.next_sibling.next_sibling.find(class_="day_num").text
    
@app.route('/keyboard')
def Keyboard():
    dataSend = {
    }
    return jsonify(dataSend)
        
@app.route('/message', methods=['POST'])
def Message():
    
    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']

    
    if content == u"급식":
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type" : "basicCard",
                            "items": [
                                {
                                    "title" : days(),
                                    "description" : meals() 
                                },
                                {
                                    "title" : days_tom(),
                                    "description" : meals_tom() 
                                }
                            ]
                        }
                    }
                ]
            }
        }
    if content == u"숙제" :
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "listCard":{
                            "header":{
                                "title": "숙제",
                                "imageUrl":"https://mblogthumb-phinf.pstatic.net/MjAxODAzMjFfOCAg/MDAxNTIxNjIxMjY2Njky.FZGOxR7nqnskGTBsHHQATjELn_I0OyxNmh7H80pZ0Wog.R68amkGTHUzEUz4j-4X2JwUb-JIIDYYgNRxzBjMerMYg.JPEG.rothexe/%EC%95%84%EC%9D%B4%ED%8F%B0%EB%B0%A4%ED%95%98%EB%8A%98%EB%B0%B0%EA%B2%BD%ED%99%94%EB%A9%B44.jpg?type=w800"
                            },
                            "items":[
                                {
                                    "title":"숙제1",
                                    "description":"6/8일까지"
                                }
                            ],
                            "buttons": [
                                {
                                  "label": "숙제추가",
                                  "action": ""
                                }
                            ]
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
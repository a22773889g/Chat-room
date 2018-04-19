#-*- coding: utf-8 -*-　　 
#-*- coding: cp950 -*-　
# LINE Messaging API SDK for Python
# https://github.com/line/line-bot-sdk-python
import os
import googlemaps
import time
import requests
from bs4 import BeautifulSoup
from linebot.models import *
# sudo pip install flask
from flask import Flask, request, abort
# sudo pip install line-bot-sdk
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,FollowEvent,PostbackEvent
)
from linebot.exceptions import (
    InvalidSignatureError
)
app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'P/8T3BIEftgaJtXis/cO51oh6jYWmEHlI2jrMSM5p/JIsom0JsW3jekfRLg46mKrkU9shX6z6lxCxpL00VteLQvZEXP3aYD1OwGZKBFgRB6EZjy/S1fVtACRDy+kxx0cIFtL0UhXQrfEOVduv4Y6JAdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = 'd628257e07b920fb83dfaabeedc2253b'
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print 'request body' info 
    app.logger.info("Request body: " + body)
    print("Request body: %s" % body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
@handler.add(FollowEvent)
def handle_follow(event):
    str='歡迎您使用我們的小助手~'+'\n感謝您的加入!!'+'\n如要查詢公車動態資訊請輸入---'+'\n查詢公車動態資訊' +'\n如要查詢最近的站牌請輸入---'+'\n查詢最近的站牌'+'\n如要查詢CityBike資訊---'+'\n查詢CityBike資訊'+'\n希望本功能能夠幫助到您'+'\n並解決您的需求~~~~'+'\n謝謝您的愛戴及使用。'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str))
@handler.add(PostbackEvent)
def handle_postback(event):
    if(event.postback.data==u'開啟提醒'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入目前的位置'))
        to=event.source.user_id
        mention(5,to)
        return 0
    elif(event.postback.data==u'關閉提醒'):
        print('close')
        return 0
        
    data=event.postback.data.split('&')
    goback=''.join([x for x in data[0] if x.isdigit()])
    id=''.join([x for x in data[1] if x.isdigit()])
    content=now(goback,id)
    str=u'倒數 | 站名\n'
    for i in content:
        if i['value']=='null':
            str+=i['cometime']+' | '+i['stopname']+'\n'
        elif i['value']=='0':
            str+=u'即將到站 | '+i['stopname']+'\n'
        else:
            str+=i['value']+u'分鐘 | '+i['stopname']+'\n'
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=str))
        
    confirm_template_message2 = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='是否開啟提醒',
        actions=[
            PostbackTemplateAction(
                label=u'開啟提醒',
                data=u'開啟提醒'
                ),
            PostbackTemplateAction(
                label=u'關閉提醒',
                data=u'關閉提醒'
                )
            ]
        )
    )
    to=event.source.user_id
    line_bot_api.push_message(to,confirm_template_message2)    
    
check=0

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    list=gps(event.message.address)
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://upload.cc/i/LYeFUK.png',
                    title=list[0][0],
                    text=u'約'+list[0][2],
                    actions=[
                        URITemplateAction(
                            label='顯示位置',
                            uri='https://www.google.com.tw/maps/place/%s,%s'  %(list[0][1]['lat'],list[0][1]['lng'])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.cc/i/LYeFUK.png',
                    title=list[1][0],
                    text=u'約'+list[1][2],
                    actions=[
                        URITemplateAction(
                            label='顯示位置',
                            uri='https://www.google.com.tw/maps/place/%s,%s'  %(list[1][1]['lat'],list[1][1]['lng'])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.cc/i/LYeFUK.png',
                    title=list[2][0],
                    text=u'約'+list[2][2],
                    actions=[
                        URITemplateAction(
                            label='顯示位置',
                            uri='https://www.google.com.tw/maps/place/%s,%s'  %(list[2][1]['lat'],list[2][1]['lng'])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.cc/i/LYeFUK.png',
                    title=list[3][0],
                    text=u'約'+list[3][2],
                    actions=[
                        URITemplateAction(
                            label='顯示位置',
                            uri='https://www.google.com.tw/maps/place/%s,%s'  %(list[3][1]['lat'],list[3][1]['lng'])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.cc/i/LYeFUK.png',
                    title=list[4][0],
                    text=u'約'+list[4][2],
                    actions=[
                        URITemplateAction(
                            label='顯示位置',
                            uri='https://www.google.com.tw/maps/place/%s,%s'  %(list[4][1]['lat'],list[4][1]['lng'])
                        )
                    ]
                ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token,carousel_template_message)
    
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global check
    to=event.source.user_id
    if event.message.text == u"查詢公車動態資訊":
        check=1
        line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='輸入要查詢的路線名稱'))
        return 0
    if event.message.text == u"查詢最近的站牌":
        line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='請分享您的所在位置'))
        return 0
    if event.message.text == u"查詢CityBike資訊":
        return 0
    if check==1:
        content=stop(event.message.text)
        check=0
        confirm_template_message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='請選擇公車去回路線',
            actions=[
                PostbackTemplateAction(
                    label=u'往'+content['departurezh'],
                    data=u'goback=2&id='+content['id']
                    ),
                PostbackTemplateAction(
                    label=u'往'+content['destinationzh'],
                    data=u'goback=1&id='+content['id']
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,confirm_template_message)
        return 0
    buttons_template = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='選擇服務',
        text='請選擇',
        thumbnail_image_url='https://upload.cc/i/8xVRdH.png',
        actions=[
            MessageTemplateAction(
                    label='查詢公車動態資訊',
                    text='查詢公車動態資訊'
            ),
            MessageTemplateAction(
                    label='查詢最近的站牌',
                    text='查詢最近的站牌'
            ),
            MessageTemplateAction(
                label='查詢CityBike資訊',
                text='查詢CityBike資訊'
            ),
            URITemplateAction(
                label='聯絡作者',
                uri='https://www.facebook.com/profile.php?id=100000534440398'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token,buttons_template)
            
            
def stop(s):
    res = requests.get("http://ibus.tbkc.gov.tw/xmlbus/StaticData/GetRoute.xml")
    soup = BeautifulSoup(res.text,"html.parser")
    #print(soup.prettify())
    stop=[]
    for i in soup.select('route'):
        temp={}
        temp.update({'id':i.attrs['id']})
        temp.update({'namezh':i.attrs['namezh']})
        temp.update({'departurezh':i.attrs['departurezh']})
        temp.update({'destinationzh':i.attrs['destinationzh']})
        stop.append(temp)
    for i in stop:
        if(i['namezh']==s):
            return {'id':i['id'],'departurezh':i['departurezh'],'destinationzh':i['destinationzh']}
def now(goback,id):
    res = requests.get("http://ibus.tbkc.gov.tw/xmlbus/GetEstimateTime.xml?routeIds="+str(id))
    soup = BeautifulSoup(res.text,"html.parser")
    list1=[]
    for i in soup.select('estimatetime '):
        list2={}
        if i.attrs['goback']==goback:
            list2.update({'stop':i.attrs['stopid']})
            list2.update({'stopname':i.attrs['stopname']})
            list2.update({'value':i.attrs['value']})
            list2.update({'cometime':i.attrs['cometime']})
            list1.append(list2)
    return list1
def city_bike():
    res = requests.get("http://www.c-bike.com.tw/xml/stationlistopendata.aspx")
    soup = BeautifulSoup(res.text,"html.parser")
    list1=[]
    for i in soup.select('station'):
        list2=[]
        list2.append(i.select('stationid')[0].text)   
        list2.append(i.select('stationno')[0].text)
        list2.append(i.select('stationname')[0].text)     
        list2.append(i.select('stationnums1')[0].text)
        list2.append(i.select('stationnums2')[0].text)
        list2.append(i.select('stationaddress')[0].text)    
        list2.append(i.select('stationlat')[0].text)
        list2.append(i.select('stationlon')[0].text)
        list2.append(i.select('stationdesc')[0].text)
        list2.append(i.select('stationpic')[0].text)
        list2.append(i.select('stationpic2')[0].text)
        list2.append(i.select('stationpic3')[0].text)
        list2.append(i.select('stationmap')[0].text)    
        list1.append(list2)
    return list1
def mention(x,id):
    time.sleep(x)
    to=id
    line_bot_api.push_message(to, TextSendMessage(text='快到了喔'))
def gps(address):
    place=googlemaps.Client(key='AIzaSyCQDkH9xl2i01higebXXmtpJiz3zebP-kM')
    gmaps = googlemaps.Client(key='AIzaSyCczOKIBiIxzaIkM1_8_rK3Z9FJkstTibE')
    geocode_result = gmaps.geocode(address)
    bus=place.places('公車',location=geocode_result[0]['geometry']['location'])
    list1=[]
    i=0
    temp=[]
    while(len(list1)<5):
        if bus['results'][i]['name'] not in temp:
            print(bus['results'][i]['name'])
            list2=[]
            temp.append(bus['results'][i]['name'])
            list2.append(bus['results'][i]['name'])
            list2.append(bus['results'][i]['geometry']['location'])
            dis=gmaps.distance_matrix(geocode_result[0]['geometry']['location'],{'lat':bus['results'][i]['geometry']['location']['lat'],'lng':bus['results'][i]['geometry']['location']['lng']})
            list2.append(dis['rows'][0]['elements'][0]['distance']['text'])
            list1.append(list2) 
        i+=1
    print(list1)
    return list1
if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
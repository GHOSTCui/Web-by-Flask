from flask import Flask,render_template,request
import sqlite3
import re

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("myself.html")

@app.route('/index')
def home():
    # return render_template("index.html")
    return render_template("index.html")

@app.route('/index.html')
def home2():
    return index()

@app.route('/myself')
def myself():
    return index()

@app.route('/temp')
def temp():
    return render_template("temp.html")

@app.route('/movie')
def movie():
    datalist = []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select * from movieTop250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)

    cur.close()
    conn.close()
    return render_template("movie.html",movies = datalist)


@app.route('/score')
def score():
    Score = []  # 评分
    Num = []    # 数量
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select Rating,count(Rating) from movieTop250 group by Rating;"
    data = cur.execute(sql)
    for item in data:
        Score.append(item[0])
        Num.append(item[1])

    cur.close()
    conn.close()
    return render_template("score.html",Score = Score,Num = Num)


@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/interesting')
def interesting():
    return render_template("interesting.html")

@app.route('/top')
def top():
    import urllib.error, urllib.request
    from bs4 import BeautifulSoup
    import re

    baseurl = "https://s.weibo.com/top/summary"
    findNum = re.compile(r'<td class="td-01 ranktop">(.*)</td>')
    findKeyword = re.compile(r'<a href=".*?" target="_blank">(.*?)</a>')
    findFire = re.compile(r'<span>(\d*)</span>')

    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    request = urllib.request.Request(baseurl, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="data"):  # 查找符合要求的字符串，形成列表
        item = str(item)
        Num = re.findall(findNum, item)
        Keyword = re.findall(findKeyword, item)
        Fire = re.findall(findFire, item)
    while '' in Fire:
        Fire.remove('')
    All2 = []
    for i in range(1, 51):
        All1 = []
        All1.append(i)
        All1.append(Fire[i - 1])
        All2.append(All1)
    All = All2
    return render_template("top.html", Num = Num, Keyword = Keyword, Fire = Fire, All = All)


@app.route('/bilitop')
def bilitop():
    import urllib.error, urllib.request
    from bs4 import BeautifulSoup
    import re

    baseurl = "https://www.bilibili.com/v/popular/rank/all"

    findTitle = re.compile(r'<a class="title" href=".*?" target="_blank">(.*?)</a>')
    findUser = re.compile(
        r'<a href="//space.bilibili.com/.*?" target="_blank"><span class="data-box up-name"><i class="b-icon author"></i>(.*?)</span></a>',
        re.S)
    findPnumber = re.compile(r'<span class="data-box"><i class="b-icon play"></i>(.*?)</span>', re.S)
    findDanmu = re.compile(r'<span class="data-box"><i class="b-icon view"></i>(.*?)</span>', re.S)
    findUrl = re.compile(r'<a href="(.*?)" target="_blank">')

    Titlelist = []
    Userlist = []
    Pnumberlist = []
    Danmulist = []
    Urllist = []

    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    request = urllib.request.Request(baseurl, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="content"):  # 查找符合要求的字符串，形成列表
        item = str(item)
        # print(item)

        Title = re.findall(findTitle, item)[0]
        User = re.findall(findUser, item)[0]  # 注意数据类型
        User = re.sub("\n", " ", User)
        User = re.sub(" ", '', User)
        Pnumber = re.findall(findPnumber, item)[0]
        Pnumber = re.sub("\n", " ", Pnumber)
        Pnumber = re.sub(" ", "", Pnumber)
        Danmu = re.findall(findDanmu, item)[0]
        Danmu = re.sub("\n", " ", Danmu)
        Danmu = re.sub(" ", "", Danmu)
        Url = re.findall(findUrl, item)[0]
        Url = re.sub("//", "https://", Url)

        Titlelist.append(Title)
        Userlist.append(User)
        Pnumberlist.append(Pnumber)
        Danmulist.append(Danmu)
        Urllist.append(Url)

    return render_template("bilitop.html", Title = Titlelist, User = Userlist, Pnumber = Pnumberlist, Danmu = Danmulist,Url = Urllist)


@app.route('/upspace')
def upspace():
    return render_template("upspace.html")

@app.route('/upspace2',methods=['POST','GET'])
def upspace2():
    if request.method == 'POST':
        uid = request.form.to_dict()['uid']

    import time
    import requests
    import json

    page = 1

    time_thick = int(time.time() * 1000)
    # url = f'https://api.bilibili.com/x/v2/reply/main?callback=jQuery172009047692616139114_{1627891325400 + page}&jsonp=jsonp&next={page}&type=1&oid=674425220&mode=3&plat=1&_={time_thick}'
    url1 = f"https://api.bilibili.com/x/relation/stat?vmid={uid}&jsonp=jsonp"
    url2 = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp"
    headers = {
        "cookie": "buvid3=F9152F74-9A8C-F620-E4E0-196477BF311A71342infoc; CURRENT_FNVAL=80; _uuid=BC0E6E34-A597-5DBC-663C-8DE5D94AFAED38060infoc; blackside_state=1; rpdid=|(J|Y|m))|)k0J'uYkY~luRYk; fingerprint=07a65804618ff53b96ee85ea3b68e168; buvid_fp=F9152F74-9A8C-F620-E4E0-196477BF311A71342infoc; buvid_fp_plain=DDAB6D08-7F16-4E4D-A14E-7274DF61BAC0184983infoc; SESSDATA=d2e791a0%2C1642730794%2C727e5%2A71; bili_jct=ce111ce02e1a6bf97a110fae68cb3526; DedeUserID=433264080; DedeUserID__ckMd5=8b84c0998552d8ef; sid=95el0f54; PVID=1; CURRENT_QUALITY=120; CURRENT_BLACKGAP=1; bp_t_offset_433264080=558318604290682323; bfe_id=018fcd81e698bbc7e0648e86bdc49e09; innersign=1",
        'referer': 'https://www.bilibili.com/video/BV1764y167Lp',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    resp1 = requests.get(url1, headers=headers)
    resp2 = requests.get(url2, headers=headers)
    text1 = resp1.text
    text2 = resp2.text
    json_data1 = json.loads(text1)
    json_data2 = json.loads(text2)
    up = json_data1
    up2 = json_data2['data']['list']['vlist'][0]['author']
    num = json_data2['data']['page']['count']
    pages = num // 30 + 1  # 得到页数

    # Up的信息

    # Uid
    Uid = up['data']['mid']
    # 昵称
    Name = up2
    # 关注的数量
    Following = up['data']['following']
    # 粉丝数
    Follower = up['data']['follower']

    title = []
    play = []
    date = []
    length = []
    video = []
    comment = []
    pic = []
    bv = []
    link = []
    desc = []
    for page in range(1, pages + 1):
        # print(f"====================================正在爬取第{ page }页=====================================")
        url2 = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp"
        resp3 = requests.get(url2, headers=headers)
        text3 = resp3.text
        json_data3 = json.loads(text3)
        data = json_data3['data']['list']['vlist']
        for i in (range(len(data))):
            # 整理数据

            # 视频名称
            Title = data[i]['title']
            title.append(Title)

            # 播放量
            Play = data[i]['play']
            play.append(Play)
            # 发布日期
            Time = data[i]['created']
            Date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Time))
            date.append(Date)

            # 视频长度
            Length = data[i]['length']
            length.append(Length)

            # 收藏数
            Video_review = data[i]['video_review']
            video.append(Video_review)

            # 评论数
            Comment = data[i]['comment']
            comment.append(Comment)

            # 封面图片
            Pic = data[i]['pic']
            pic.append(Pic)

            # Bv号
            Bv = data[i]['bvid']
            Link = "https://www.bilibili.com/video/" + str(Bv)
            bv.append(Bv)
            link.append(Link)

            # 简介
            Desc = data[i]['description']
            desc.append(Desc)

    l = len(bv)
    numb = []
    for i in range(l):
        numb.append(i+1)
    return render_template("upspace2.html",numb = numb,bv = bv,pic = pic,title = title,l = l,link = link,desc = desc,comment = comment,video = video,date = date,play = play,uid = uid,Follower = Follower,Following = Following,Name = Name)

@app.route('/message')
def message():
    conn = sqlite3.connect("message.db")
    c = conn.cursor()
    sql = "select * from ghost order by id ASC"
    messages = c.execute(sql)
    name=[]
    id=[]
    message=[]
    for id_1,name_1,message_1 in messages:
        id.append(id_1)
        name.append(name_1)
        message.append(message_1)
    conn.commit()
    conn.close()

    l = len(id)
    b = id[l-1]+1
    return render_template("message.html",id = id,name = name,message = message,l = l,b = b)

@app.route('/message2',methods=['POST','GET'])
def message2():
    if request.method == 'POST':
        id = request.form.to_dict()['id']
        name = request.form.to_dict()['name']
        messages = request.form.to_dict()['messages']


    conn = sqlite3.connect("message.db")    # 打开或创建数据库

    c = conn.cursor()       # 获取游标
    # sql = f'''
    #     create table
    #         (id int primary key not null,
    #         name text not null,
    #         message text not null);
    #
    # '''
    sql2 = f'''
        insert into ghost (id, name, message) 
            values({ id },'{ name }','{ messages }')  
    '''
    # cursor = c.execute(sql)
    c.execute(sql2)
    conn.commit()
    conn.close()
    return render_template("message2.html",name = name,messages = messages)

@app.route('/message_vip')
def message_vip():
    conn = sqlite3.connect("message.db")
    c = conn.cursor()
    sql = "select * from ghost order by id ASC"
    messages = c.execute(sql)
    name = []
    id = []
    message = []
    for id_1, name_1, message_1 in messages:
        id.append(id_1)
        name.append(name_1)
        message.append(message_1)
    conn.commit()
    conn.close()

    l = len(id)
    return render_template("message_vip.html",id = id,name = name,message = message,l = l)



@app.route('/message_vip2',methods=['POST','GET'])
def message_vip2():
    if request.method == 'POST':
        Del = request.form.to_dict()['del']
    conn = sqlite3.connect("message.db")
    c = conn.cursor()
    sql = f"delete from ghost where id={Del}"
    c.execute(sql)
    conn.commit()
    conn.close()
    return render_template("message_vip2.html")




if __name__ == '__main__':
    app.run()


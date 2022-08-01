import socket
import os
import json
import hashlib
import html
from urllib.parse import urlparse, parse_qs, unquote, quote
import datetime
f_ext=["png","jpg","jpeg","bmp","webp","ico","pdf","mp3","mp4","jpeg","tga","gif"]        
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0",5050))
s.listen()
def ban(addr):
    if addr[0]!="127.0.0.1":
        j["banned"].append(addr[0])
        f=open("pos.json","w")
        json.dump(j,f,indent=6)
        f.close()
while True:
    resp="HTTP/1.1 500 server error\n\nSERVER ERROR"
    conn,addr=s.accept()
    r=conn.recv(186*1000).decode("utf-8","ignore")
    reqlog=open("reqlog.txt","a")
    reqlog.write("\n"+addr[0]+"\n")
    reqlog.close()
    f1=open("pos.json")
    obj=json.load(f1)
    f1.close()
    if "POST" not in r and addr[0] not in obj["banned"]:
        if len(r.split(" "))>1:
            n=os.listdir(".")
            path=r.split(" ")[1]
            path=path.replace("%20"," ")
            if path!="/" and "../" not in path and path[1:].split("/")[0] in n and path!="/homepage.html" and path!="/pos.json" and path!="/sustain.py" and path!="/reqlog.txt" and  os.path.isfile(path[1:]):
                if path!="msg.txt" and path.split(".")[len(path.split("."))-1] not in f_ext:
                    f=open(path[1:])
                    resp="HTTP/1.1 200 OK\r\nX-Frame-Options: DENY\n\n"+f.read()
                    f.close()
                elif path=="/msg.txt" and path.split(".")[len(path.split("."))-1] not in f_ext and addr[0] in obj["ip"]:
                    f=open(path[1:])
                    resp="HTTP/1.1 200 OK\r\nX-Frame-Options: DENY\n\n"+f.read()
                    f.close()
                else:
                    f=open(path[1:],"rb")
                    data=f.read()
                    f.close()
                    resp=b"HTTP/1.1 200 OK\r\nX-Frame-Options: DENY\n\n"+data
            elif "../" in path:
                f=open("pos.json")
                j=json.load(f)
                j["banned"].append(addr[0])
                f.close()
                f=open("pos.json","w")
                json.dump(j,f,indent=6)
                f.close()
            elif path=="/":
                stylefile=open("style.css")
                s1=stylefile.read()
                stylefile.close()
                scriptf=open("script.js")
                sc=scriptf.read()
                scriptf.close()
                resp="HTTP/1.1 200 OK\r\nX-Frame-Options: DENY\n\n<!DOCTYPE html><html><head><meta charset='utf-8'><title>blue fire</title><style>"+s1+"</style></head><body><canvas></canvas><div>"
                n=os.listdir(".")
                for f in n:
                    if f=="SIGN UP.html" or f=="LOGIN.html":
                        resp+="<a href='/"+f+"'>"+f.split(".")[0]+"</a><br>"
                resp+="</div><script>"+sc+"</script></body>"
            elif path.split("?")[0]=="/users":
                qs=path.split("?")
                user="=".join(path.split("=")[1:])
                user=html.escape(user)
                if user in obj["name"]:
                    i=0
                    while i<len(obj["name"]):
                        if user==obj["name"][i]:
                            break
                        i+=1
                    pagedemo="""<!DOCTYPE html>
                    <html>
                    <head>
                    <meta charset="utf-8">
                    <title>"""+user+"""</title>
                    <style>
.black{
background-color:black;
color:white;
}
@keyframes zoom{
from {font-size:0px;transform: rotate(-90deg);
  -webkit-transform: rotate(-90deg);
  -moz-transform: rotate(-90deg);
  -ms-transform: rotate(-90deg);
  -o-transform: rotate(-90deg);
  filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);
}
to{font-size:50px;transform: rotate(720deg);
  -webkit-transform: rotate(720deg);
  -moz-transform: rotate(720deg);
  -ms-transform: rotate(720deg);
  -o-transform: rotate(720deg);
  filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);

}
}
body{
background-color:black;
}
p{
background:none;
color:white;
width:100%;
overflow-x:hidden;
overflow-y:scroll;
font-size:15px;
}
canvas{
z-index:-3;
position:fixed;
top:0px;
left:0px;
}
                    </style>
                    
                 </head>
                    <body>
                    <canvas></canvas>
                    <h1 class="black">"""+user+"""</h1><br>
                    <p>
                    """+obj["description"][i]+"""
                    </p><br>
                    <script>
                    c=document.querySelector("canvas")
                    ctx=c.getContext("2d")
                    c.width=window.innerWidth
                    c.height=window.innerHeight
                    function F(){
                    this.x=c.width/2;
                    this.y=c.height/2;
                    this.xspeed=Math.random()*4-2;
                    this.yspeed=Math.random()*4-2;
this.step=function(){
ctx.fillText('"""+obj["fav"][i]+"""',this.x,this.y);
this.x+=this.xspeed
this.y+=this.yspeed
}
                    }
var faces=[]
ctx.font="20px monospace"
function boot(){
setTimeout(boot,3000)
faces=[]
for(var i=0;i<10;i++){
faces.push(new F())
}}
boot()
ctx.fillStyle="white"
function animate(){
setTimeout(animate,1000/30)
ctx.clearRect(0,0,c.width,c.height)
for(var i=0;i<faces.length;i++){
faces[i].step()
}
}
animate()
                    </script>
                    </body>
                    </html>"""
                    pagedemo=pagedemo.replace("username",user)
                    resp="HTTP/1.1 200 OK\r\nX-Frame-Options: DENY\n\n"+pagedemo
                else:
                    resp="HTTP/1.1 200 OK\r\nX-Frame-Options: DENY\n\nuser not found"
            else:
                resp="HTTP/1.1 200 OK\n\nFILE NOT FOUND"
    elif addr[0] not in obj["banned"]:
        obj=json.load(open("pos.json"))
        dt=r.split("\r\n")[len(r.split("\r\n"))-1]
        p=dt.split("&")
        i=0
        while i<len(p):
            p[i]=unquote(p[i])
            i+=1
        name=html. escape(p[1]). encode('ascii', 'xmlcharrefreplace'). decode()

        act=p[0]
        pas=p[2]
        if act=="signup":
            fav=p[4]
            des=p[3]
            jsonf=open("pos.json")
            j=json.loads(jsonf.read())
            jsonf.close()
            if len(pas)<8:
                resp="password has to have minimum 8 characters!"
            if name not in j["name"] and len(pas)>=8:
                resp="HTTP/1.1 200 OK\n\n"
                j["name"].append(name)
                j["pass"].append(hashlib.md5(pas.encode("utf-8")).hexdigest())
                j["ip"].append(addr[0])
                j["pmsg"].append([])
                j["pdest"].append([])
                j["fav"].append(fav)
                d=html. escape("&".join(p[3:-1])). encode('ascii', 'xmlcharrefreplace'). decode()
                j["description"].append(d.replace("\n","<br>"))
            elif name in j["name"]:
                resp="HTTP/1.1 200 OK\n\n name isn't available!"
            elif len(pas)<8:
                resp="password has to have minimum 8 characters!"
            jsonf=open("pos.json","w")
            jsonf.write(json.dumps(j))
            jsonf.close()
        if act=="login" and name not in obj["bnames"]:
            jsonf=open("pos.json")
            j=json.loads(jsonf.read())
            jsonf.close()
            i=0
            isin=False
            while i<len(j["name"]):
                if j["name"][i]==name:
                    isin=True
                    break
                i+=1
            if isin:
                if j["pass"][i]==hashlib.md5(pas.encode("utf-8")).hexdigest():
                    resp="HTTP/1.1 200 OK\n\nsuccess"
                else:
                    resp="HTTP/1.1 200 OK\n\nnot"
                    f=open("pos.json")
                    j=json.load(f)
                    f.close()
                    j["banned"].append(addr[0])
                    f=open("pos.json","w")
                    json.dump(j,f,indent=6)
                    f.close()
            else:
                resp="HTTP/1.1\n\nnot"
                f=open("pos.json")
                j=json.load(f)
                f.close()
                j["banned"].append(addr[0])
                f=open("pos.json","w")
                json.dump(j,f,indent=6)
                f.close()

        if act=="msg" and p[3] and name not in obj["bnames"]:
            jsonf=open("pos.json")
            j=json.loads(jsonf.read())
            jsonf.close()
            pas=p[2]
            name=html. escape(p[1]). encode('ascii', 'xmlcharrefreplace'). decode()
            isin=False
            i=0
            while i<len(j["name"]):
                if j["name"][i]==name:
                    isin=True
                    break
                i+=1
            if isin:
                if j["pass"][i]==hashlib.md5(pas.encode("utf-8")).hexdigest():
                    resp="HTTP/1.1 200 OK\n\nm"
                    msgf=open("msg.txt","a")
                    msg=p[3]
                    msg=html. escape(msg). encode('ascii', 'xmlcharrefreplace'). decode()
                    currtime=datetime.datetime.now().strftime("%H:%M:%S")
                    msgf.write("<a href='/users?name="+name+"'>"+name+"</a>"+": "+msg+"<br><div class='small'>at "+str(datetime.date.today())+" "+currtime+"</div><br><hr>")
                    msgf.close()
        if act=="pmsg":
            pname=html. escape(p[3]). encode('ascii', 'xmlcharrefreplace'). decode()
            pmsg=html. escape(p[4]). encode('ascii', 'xmlcharrefreplace'). decode()
            jsonf=open("pos.json")
            j=json.loads(jsonf.read())
            jsonf.close()
            pas=p[2]
            name=html. escape(p[1]). encode('ascii', 'xmlcharrefreplace'). decode()
            isin=False
            i=0
            while i<len(j["name"]):
                if j["name"][i]==name:
                    isin=True
                    break
                i+=1
            if isin:
                if j["pass"][i]==hashlib.md5(pas.encode("utf-8")).hexdigest():
                    if pname in j["name"]:
                        i2=j["name"].index(pname)
                        j["pmsg"][i2].append(pmsg)
                        j["pdest"][i2].append(name)
                        f=open("pos.json","w")
                        json.dump(j,f,indent=6)
                        f.close()
        if act=="creds":
            resp="HTTP/1.1 200 OK\n\nhi"
            jsonf=open("pos.json")
            j=json.loads(jsonf.read())
            jsonf.close()
            msg=p[3]
            pas=p[2]
            name=html. escape(p[1]). encode('ascii', 'xmlcharrefreplace'). decode()
            isin=False
            i=0
            while i<len(j["name"]):
                if j["name"][i]==name:
                    isin=True
                    break
                i+=1
            if isin:
                if j["pass"][i]==hashlib.md5(pas.encode("utf-8")).hexdigest():
                    newname=p[3]
                    newpass=p[4]
                    newdes="&".join(p[5:-1])
                    newfav=p[-1:][0]
                    newname=html. escape(newname). encode('ascii', 'xmlcharrefreplace'). decode()
                    newdes=html. escape(newdes). encode('ascii', 'xmlcharrefreplace'). decode()
                    if newname not in j["name"] or newname==name:
                        j["pass"][i]=hashlib.md5(newpass.encode("utf-8")).hexdigest()
                        j["name"][i]=newname
                        j["description"][i]=newdes.replace("\n","<br>")
                        j["fav"][i]=newfav
                        f=open("pos.json","w")
                        json.dump(j,f,indent=6)
                        f.close()
                    else:
                        resp="HTTP/1.1 200 OK\n\nname "+newname+" is already taken"
                else:
                    ban(addr)
            else:
                ban(addr)
        if act=="admin":
            if name=="AndreiSuperUser" and pas=="h4nt68u":
                resp="HTTP/1.1 200 OK\n\nauth"
            else:
                resp="HTTP/1.1 200 OK\n\nnonononoooooo"
                f=open("pos.json")
                j=json.load(f)
                f.close()
                ban(addr)
        if act=="ban":
            if name=="AndreiSuperUser" and pas=="h4nt68u":
                bn=p[3]
                jsonf=open("pos.json","r")
                js=jsonf.read()
                jsonf.close()
                j=json.loads(js)
                j["bnames"].append(bn)
                i=0
                run=True
                while i<len(j["name"]):
                    if bn==j["name"][i]:
                        break
                    i+=1
                j["banned"].append(j["ip"][i])
                jsonf=open("pos.json","w")
                jsonf.write(json.dumps(j))
                jsonf.close()
            else:
                f=open("pos.json")
                j=json.load(f)
                f.close()
                ban(addr)
        if act=="getall":
            if name=="AndreiSuperUser" and pas=="h4nt68u":
                j=json.load(open("pos.json"))
                resp="HTTP/1.1 200 OK\n\n"+"babababababababababababababababaaaaa".join(j["name"])
            else:
                f=open("pos.json")
                j=json.load(f)
                f.close()
                ban(addr)
        if act=="wf":
            if name=="AndreiSuperUser" and pas=="h4nt68u":
                fname=p[3]
                fcont=p[4]
                f=open(fname,"w")
                f.write(fcont)
                f.close()
                resp="HTTP/1.1 200 OK\n\nnice"
            else:
                f=open("pos.json")
                j=json.load(f)
                f.close()
                ban(addr)
        if act=="af":
            if name=="AndreiSuperUser" and pas=="h4nt68u":
                fname=p[3]
                fcont=p[4]
                f=open(fname,"a")
                f.write(fcont)
                f.close()
                resp="HTTP/1.1 200 OK\n\nnice"
            else:
                f=open("pos.json")
                j=json.load(f)
                f.close()
                ban(addr)
        if act=="get":
            jsonf=open("pos.json")
            j=json.loads(jsonf.read())
            jsonf.close()
            i=0
            isin=False
            while i<len(j["name"]):
                if j["name"][i]==name:
                    isin=True
                    break
                i+=1
            if isin:
                if j["pass"][i]==hashlib.md5(pas.encode("utf-8")).hexdigest():
                    resp="HTTP/1.1 200 OK\n\n"+quote(html.unescape(j["description"][i]))+"&"+quote(j["fav"][i])+"&"+str(i+1)
                else:
                    resp="HTTP/1.1 200 OK\n\nnot"
                    f=open("pos.json")
                    j=json.load(f)
                    f.close()
                    j["banned"].append(addr[0])
                    f=open("pos.json","w")
                    json.dump(j,f,indent=6)
                    f.close()
            else:
                resp="HTTP/1.1\n\nnot"
                f=open("pos.json")
                j=json.load(f)
                f.close()
                j["banned"].append(addr[0])
                f=open("pos.json","w")
                json.dump(j,f,indent=6)
                f.close()
        if act=="rf":
            if name=="AndreiSuperUser" and pas=="h4nt68u":
                resp="HTTP/1.1 200 OK\n\n"
                fn=p[3]
                if os.path.isfile(fn):
                    t=open(fn)
                    resp+=t.read()
                    t.close()
                elif "." in fn:
                    if fn.split(".")[1]=="html":
                        resp+="""
<DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>new page</title>
</head>
<body>
</body>
</html>
                    """
            else:
                f=open("pos.json")
                j=json.load(f)
                f.close()
                ban(addr)
        if act=="ls":
            arr=os.lisdir(".")
            if p[1]=="AndreiSuperUser" and p[2]=="hn4t68u":
                resp="HTTP/1.1 200 OK\n\n"+"&".join(arr)
        if act=="lf":
            jsonf=open("pos.json")
            j=json.loads(jsonf.read())
            jsonf.close()
            i=0
            isin=False
            while i<len(j["name"]):
                if j["name"][i]==html.escape(name):
                    isin=True
                    break
                i+=1
            if isin:
                if j["pass"][i]==hashlib.md5(pas.encode("utf-8")).hexdigest():
                    resp="HTTP/1.1 200 OK\n\nsuccess"
                    bc='\\/:*?"<>|.'
                    equiv={
                            '\\':".back",
                            "/":".front",
                            ":":".two",
                            "*":".star",
                            "?":".what",
                            '"':".quot",
                            '<':".mic",
                            ">":".mare",
                            "|":".or",
                            ".":".dt"
                            }
                    fname=p[3]
                    fcont=p[4]
                    ffname=p[3]
                    for c in bc:
                        if c==".":
                            if "." in fname:
                                ffname=ffname.replace(c, equiv[c])
                        else:
                            ffname=ffname.replace(c, equiv[c])
                    if str(i+1) not in os.listdir("."):
                        os.system("mkdir "+str(i+1))
                    f=open(str(i+1)+'/'+ffname.replace("'","")+".html","w")
                    f.write(fcont.replace("localStorage","blahnot"))
                    f.close()
                    f=open("msg.txt","a")
                    f.write("<a href='/users?name="+unquote(name)+"'>"+name+"</a> uploaded project <a href='"+str(i+1)+"/"+unquote(ffname.replace("'",""))+".html' download>"+fname+"</a><hr><br>")
                    f.close()
                else: 
                    resp="HTTP/1.1 200 OK\n\nnot"
                    f=open("pos.json")
                    j=json.load(f)
                    f.close()
                    j["banned"].append(addr[0])
                    f=open("pos.json","w")
                    json.dump(j,f,indent=6)
                    f.close()
            else:
                resp="HTTP/1.1\n\nnot"
                f=open("pos.json")
                j=json.load(f)
                f.close()
                j["banned"].append(addr[0])
                f=open("pos.json","w")
                json.dump(j,f,indent=6)
                f.close()

        if name in obj["bnames"]:
            resp="HTTP/1.1 200 OK\n\nyou're banned!!!!!!!"
    elif addr[0] in obj["banned"]:
        resp="HTTP/1.1 200 OK\n\nyou're banned!!!!!!!"
    if type(resp)==str:
        conn.send(resp.encode("utf-8"))
    elif type(resp)==bytes:
        conn.send(resp)
    conn.close()

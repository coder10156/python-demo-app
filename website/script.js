if(localStorage.getItem("name")!=null){
location.href="/chat.html"
}
addEventListener("mousemove",function(e){
    emitX=e.clientX
    emitY=e.clientY
    
})
c=document.querySelector("canvas")
c.width=window.innerWidth
c.height=window.innerHeight
c.style.position="fixed"
var ctx=c.getContext("2d")
ctx.fillStyle="white"
ctx.fillRect(0,0,100,100)
emitX=c.width/2
emitY=c.height/2
function Smok(){
this.x=emitX
this.y=emitY
this.size=5
this.xspeed=Math.random()*0.5-0.25
this.yspeed=Math.random()*1+2.5
this.alpha=0.5
this.revalidate=function(){
this.alpha-=0.01
this.x-=this.xspeed
this.y-=this.yspeed
this.size-=0.1
ctx.globalAlpha=this.alpha
ctx.beginPath()
ctx.arc(this.x,this.y,this.size,0,Math.PI*2)
ctx.closePath()
ctx.fill()
}
}
smoks=[]
ctx.globalCompositeOperation="lighter"
ctx.fillStyle="rgb(100,255,255)"
function resmok(){
    ctx.clearRect(0,0,c.width,c.height)
    setTimeout(resmok,1000/40)
    for(var i=0;i<10;i++){
        smoks.push(new Smok())
    }
    
    for(var i=0;i<smoks.length;i++){
        
        if(smoks[i].alpha<=0.05){
            smoks.splice(i,i)
        }else{
            smoks[i].revalidate()
        }
        
        
    }
    
}
resmok()
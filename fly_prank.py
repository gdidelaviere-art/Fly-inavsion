import ctypes, math, random, time, tkinter as tk
from dataclasses import dataclass

# Harmless transparent desktop overlay: never modifies files or real icons.
TRANSPARENT='#ff00ff'
random.seed()
root=tk.Tk()
root.title('Windows Fly Invasion — ESC to quit')
root.attributes('-fullscreen',True)
root.attributes('-topmost',True)
root.configure(bg=TRANSPARENT)
root.wm_attributes('-transparentcolor',TRANSPARENT)
W,H=root.winfo_screenwidth(),root.winfo_screenheight()
canvas=tk.Canvas(root,width=W,height=H,bg=TRANSPARENT,highlightthickness=0)
canvas.pack()
# On Windows, click-through overlay; keyboard exit via global hotkey handled by polling.
try:
    hwnd=root.winfo_id()
    GWL_EXSTYLE=-20
    WS_EX_LAYERED=0x80000
    WS_EX_TRANSPARENT=0x20
    style=ctypes.windll.user32.GetWindowLongW(hwnd,GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd,GWL_EXSTYLE,style|WS_EX_LAYERED|WS_EX_TRANSPARENT)
except Exception: pass

# Windows hotkey Ctrl+Shift+Q registered globally; Esc works when focused.
HOTKEY_ID=0xBEEF
try: ctypes.windll.user32.RegisterHotKey(None,HOTKEY_ID,0x0002|0x0004,ord('Q'))
except Exception: pass

BIN=(min(85,W*.06),max(80,H-105))
# Desktop icon positions are deliberately simulated, not modified.
icons=[('This PC','💻',80,85),('Network','🌐',80,190),('Documents','📁',80,295),('Browser','🌍',80,400),('Photos','🖼',80,505)]
icons=[(n,e,min(x,W-100),min(y,H-180)) for n,e,x,y in icons]
@dataclass
class Fly:
    x:float;y:float;vx:float;vy:float;phase:float;scale:float;target:int=-1;carrying:bool=False

flies=[]
start=time.perf_counter()
last=start

def add_fly():
    angle=random.uniform(-math.pi,0)
    speed=random.uniform(80,230)
    flies.append(Fly(BIN[0],BIN[1],math.cos(angle)*speed,math.sin(angle)*speed,random.uniform(0,6.28),random.uniform(.65,1.25)))

def line(x1,y1,x2,y2,**kw):canvas.create_line(x1,y1,x2,y2,**kw)
def draw_fly(f,t):
    x,y,s=f.x,f.y,f.scale
    wing=math.sin(t*75+f.phase)*5*s
    canvas.create_oval(x-12*s,y-5*s-wing,x+2*s,y+4*s-wing,fill='#b7dce5',outline='#718d95',stipple='gray50')
    canvas.create_oval(x-2*s,y-4*s+wing,x+12*s,y+5*s+wing,fill='#b7dce5',outline='#718d95',stipple='gray50')
    canvas.create_oval(x-7*s,y-5*s,x+7*s,y+5*s,fill='#181818',outline='#424242')
    canvas.create_oval(x+3*s,y-4*s,x+9*s,y+2*s,fill='#363636',outline='#111111')
    for side in (-1,1):
        for k in range(3):line(x+(k-1)*3*s,y+side*2*s,x+(k-2)*4*s,y+side*10*s,fill='#242424',width=1)

def draw_bin():
    x,y=BIN
    canvas.create_rectangle(x-28,y-27,x+28,y+27,fill='#e7e7e7',outline='#555',width=2)
    canvas.create_rectangle(x-32,y-32,x+32,y-24,fill='#bfc8cc',outline='#444')
    canvas.create_text(x,y,text='♻',font=('Segoe UI Symbol',29),fill='#238d40')
    canvas.create_text(x,y+41,text='Recycle Bin',font=('Segoe UI',10,'bold'),fill='white')

def draw_icon(name,emoji,x,y,alpha=1):
    canvas.create_text(x,y,text=emoji,font=('Segoe UI Emoji',29))
    canvas.create_text(x,y+31,text=name,font=('Segoe UI',10,'bold'),fill='white')

def frame():
    global last
    now=time.perf_counter();dt=min(now-last,.05);last=now;t=now-start
    canvas.delete('all')
    # faint guide makes prank state visible without blocking desktop
    canvas.create_text(W-20,20,anchor='ne',text='FLY INVASION  •  Ctrl+Shift+Q to exit',fill='#ececec',font=('Segoe UI',11,'bold'))
    draw_bin()
    if t<18:
        desired=min(85,int(t*6)+1)
        for _ in range(min(3,desired-len(flies))):add_fly()
    stolen=set()
    for i,f in enumerate(flies):
        if t>3 and f.target<0 and random.random()<dt*.28:
            f.target=random.randrange(len(icons))
        if f.target>=0:
            _,_,ix,iy=icons[f.target]
            tx,ty=(BIN if f.carrying else (ix,iy))
            dx,dy=tx-f.x,ty-f.y
            d=max(1,math.hypot(dx,dy))
            f.vx+=dx/d*350*dt;f.vy+=dy/d*350*dt
            if d<24:
                if not f.carrying:f.carrying=True
                else:f.target=-1;f.carrying=False
        else:
            f.vx+=random.uniform(-170,170)*dt;f.vy+=random.uniform(-170,170)*dt
        speed=math.hypot(f.vx,f.vy)
        if speed>240:f.vx*=240/speed;f.vy*=240/speed
        f.x+=f.vx*dt;f.y+=f.vy*dt
        if f.x<12 or f.x>W-12:f.vx*=-1;f.x=max(12,min(W-12,f.x))
        if f.y<12 or f.y>H-12:f.vy*=-1;f.y=max(12,min(H-12,f.y))
        if f.carrying and f.target>=0:stolen.add(f.target)
    for j,(name,emoji,x,y) in enumerate(icons):
        if j not in stolen:draw_icon(name,emoji,x,y)
    for f in flies:
        if f.carrying and f.target>=0:
            name,emoji,_,_=icons[f.target]
            draw_icon(name,emoji,f.x,f.y+26)
        draw_fly(f,t)
    if t>23:
        flies.clear()
        globals()['start']=time.perf_counter()
    root.after(16,frame)

def poll_hotkey():
    try:
        msg=ctypes.wintypes.MSG()
        while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg),None,0x0312,0x0312,1):
            shutdown();return
    except Exception:pass
    root.after(100,poll_hotkey)

def shutdown(event=None):
    try:ctypes.windll.user32.UnregisterHotKey(None,HOTKEY_ID)
    except Exception:pass
    root.destroy()
root.bind('<Escape>',shutdown)
root.after(100,poll_hotkey)
root.after(50,frame)
root.mainloop()

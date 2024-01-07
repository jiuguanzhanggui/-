import requests
from bs4 import BeautifulSoup
import urllib
import os
import asyncio
import edge_tts
import random
import jieba
from mutagen.mp3 import MP3
import difflib
import cv2
import shutil
from moviepy.editor import *
import re
import time
from threading import Thread
import threading

lock = threading.Lock()
def get_page(text):
    if os.path.exists('.\\GIF\\'+text):
        return os.listdir('.\\GIF\\'+text)
    os.makedirs('.\\GIF\\'+text)
    url ='https://www.adoutu.com/search?keyword='+text
    headers = {
        'Host': 'www.adoutu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    }
    while True:
        try:
            res=requests.get(url, headers=headers)
        except:
            print('加载网页失败,3s后重连')
            time.sleep(3)
        if res.status_code==200:
            break
        else:
            print('网页访问错误：'+str(res.status_code))
    soup = BeautifulSoup(res.text, 'html.parser')
    img_list = soup.find_all('img')
    for img in img_list:
        if img.has_attr('src') and img.has_attr('title'):
            try:
                urllib.request.urlretrieve(img['src'],'.\\GIF\\'+text+'\\'+str(img['title'])+'.'+str(img['src'].split('.')[3]))
            except:
                print('下载失败')
    return os.listdir('.\\GIF\\'+text)

def text_to_speech(cs,TEXT):
    print('线程：'+str(cs)+'开始文字转语音')
    async def _main():
        communicate = edge_tts.Communicate(text=TEXT,voice="zh-CN-XiaoxiaoNeural",rate="+"+str(random.randint(10,15))+"%")
        submaker = edge_tts.SubMaker()
        with open(".\\movie\\"+str(cs)+".mp3", "wb") as file: 
            async for chunk in communicate.stream():  
                if chunk["type"] == "audio":  
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":  
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])  
        #with open(".\\movie\\"+str(cs)+".srt", "w", encoding="utf-8") as file:  
        #    file.write(submaker.generate_subs())  
    asyncio.run(_main())
    audio = MP3(".\\movie\\"+str(cs)+".mp3")
    print('线程：'+str(cs)+'文字转语音完成')
    return audio.info.length

def get_equal(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def gif_max(cs,text):
    print('线程：'+str(cs)+'开始适配表情包')
    list_xiansi=[]
    list_path=[]
    list_name=[]
    list_fenci=jieba.lcut(text)
    for a in list_fenci:
        if len(a)>1:
            xiansi=[]
            with lock:
                list=get_page(a)
            if list:
                for n in list:
                    si=get_equal(n,a)
                    xiansi.append(si)
                list_xiansi.append(max(xiansi))
                list_path.append(list[xiansi.index(max(xiansi))])
                list_name.append(a)
    gifpath='.\\GIF\\'+list_name[list_xiansi.index(max(list_xiansi))]+'\\'+list_path[list_xiansi.index(max(list_xiansi))]
    print('线程：'+str(cs)+'表情包适配完成')
    return shutil.copyfile(gifpath, ".\\movie\\"+str(cs)+os.path.splitext(os.path.basename(gifpath))[1])


def gif_to_video(cs,txt,path,time):
    print('线程：'+str(cs)+'开始生成视频')
    fps = 60
    if os.path.splitext(os.path.basename(path))[1]=='.gif':
        clip = VideoFileClip(path)
        clip.write_videofile(".\\movie\\"+str(cs)+".mp4")
    else:
        img = cv2.imread(path)
        video = cv2.VideoWriter(".\\movie\\"+str(cs)+".mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (img.shape[1],img.shape[0]))
        video.write(img)
        video.release()
        cv2.destroyAllWindows()
    clip_bj = VideoFileClip(".\\bj.mp4")
    bj_time = clip_bj.set_duration(time)
    clip_tu = VideoFileClip(".\\movie\\"+str(cs)+".mp4")
    resized_clip = clip_tu.resize(width=250, height=220)
    translated_clip = resized_clip.set_position(('center', 'center')).set_duration(time)
    composite_clip=CompositeVideoClip([bj_time,translated_clip],(700,394))
    audio = AudioFileClip(".\\movie\\"+str(cs)+".mp3")
    composite_clip = composite_clip.set_audio(audio)
    subtitle = TextClip(txt, font='FZSTK.TTF',fontsize=24, color='white')
    subtitle = subtitle.set_pos(('center', 'bottom')).set_duration(time)
    final_clip = CompositeVideoClip([composite_clip, subtitle])
    final_clip.write_videofile(".\\movie\\"+str(cs)+".mp4")
    os.remove(".\\movie\\"+str(cs)+".mp3")
    os.remove(path)
    print('线程：'+str(cs)+'视频生成完成')

def fenju(txt):
    print('开始分句')
    txt = re.sub('([，。！？\?])([^”’])', r"\1\n\2", txt)
    txt = re.sub('(\.{6})([^”’])', r"\1\n\2", txt)
    txt = re.sub('(\…{2})([^”’])', r"\1\n\2", txt)
    txt = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', txt)
    txt = txt.rstrip()
    print('分句完成')
    return txt.split("\n")

def video_segment(cs,txt):
    print('线程：'+str(cs)+'开始合成视频')
    gif_path = gif_max(cs,txt)
    time_max=text_to_speech(cs,txt)
    gif_to_video(cs,txt,gif_path,time_max)
    print('线程：'+str(cs)+'合成视频完成')

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def video_hebin(zc):
    video_list=[]
    list=sorted(os.listdir(".\\movie\\"),key=natural_sort_key)
    for w in list:
        video_list.append(VideoFileClip(".\\movie\\"+w))
    video_clip=concatenate_videoclips(video_list, method='compose', transition=None, bg_color=None, ismask=False, padding = -0.5)
    music_clip=AudioFileClip(".\\backMusic1.mp3")
    music_clip=CompositeAudioClip([video_clip.audio,music_clip]).set_duration(video_clip.duration)
    video_clip = video_clip.set_audio(music_clip)
    video_clip.write_videofile('.\\'+str(zc)+'.mp4')
    time.sleep(2)
    files = os.listdir(".\\movie\\")
    for file in files:
        try:
            if os.path.isfile(".\\movie\\"+file):
                os.remove(".\\movie\\"+file)
        except:
            print('文件未找到')


def text_GPT(zc):
    url ='https://tongyi.aliyun.com/qianwen/?chatId=6252bf3f6b934cbc9c4249acd115b495'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    res=requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    list = soup.find_all('p')
    print(list)

def run(zc,txet):
    qishi_time=time.time()
    thread_list=[]
    txt_list=fenju(txet)
    cs=1
    for txt in txt_list:
        t = Thread(target=video_segment, kwargs={"cs": cs, "txt": txt})
        thread_list.append(t)
        t.start()
        time.sleep(1)
        cs+=1
        if len(thread_list)>=5:
            for thread in thread_list:
                thread.join()
            thread_list = []
    for t in thread_list:
        t.join()
    video_hebin(zc)
    print('所有线程完成')
    print('用时：'+str(time.time()-qishi_time)+'秒')


text_GPT('1')


#!/usr/bin/env python
# coding: utf-8

# In[29]:


from tkinter import *
import pygame
import os 
from tkinter import filedialog 
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
root=Tk()    
root.title('EUPHONY')
root.iconbitmap('G:/buttons/sound.ico')
root.geometry('500x450')

#initialize the pygame mixer
pygame.mixer.init()
global dir_of_songs
dir_of_songs=[]
#Grab Song Length Time Info
def play_time():
    global dir_of_songs
    #check for double timing
    if stopped:
        return
    else:
    #Grab Current song time lapsed
        current_time= pygame.mixer.music.get_pos()/1000
    #converted to time format
        conv_current_time=time.strftime('%M:%S', time.gmtime(current_time))
        song=song_box.get(ACTIVE)
        for str in dir_of_songs:
            if song in str:
                song=str
                break    
    #get song length from Mutagen
        #load song
        song_mut = MP3(song)
        #get song length
        global conv_song_time
        global song_length
        song_length= song_mut.info.length
        conv_song_time=time.strftime('%M:%S', time.gmtime(song_length))
        current_time+=1
        if int(slider_m.get()) == int(song_length):
            status_bar.config(text= f'Time Elapsed   {conv_song_time}   of   {conv_song_time} ')
            next_song()
        elif paused:
            pass
        elif int(slider_m.get())==int(current_time):
        #slider hasnt been moved
        #Update Slider To Position
            
            slider_position=int(song_length)
            slider_m.config(to=slider_position,value=int(current_time))
            
        else:
        #slider has moved
        #Update Slider To Position
            slider_position=int(song_length)
            slider_m.config(to=slider_position,value=int(slider_m.get()))
         #converted to time format
            conv_current_time=time.strftime('%M:%S', time.gmtime(int(slider_m.get())))
            status_bar.config(text= f'Time Elapsed   {conv_current_time}   of   {conv_song_time} ')
            next_time=int(slider_m.get())+1
            slider_m.config(value= next_time)
    #displaying
    #status_bar.config(text= f'Time Elapsed   {conv_current_time}   of   {conv_song_time} ')
    #slider_m.config(value=int(current_time))
    
        status_bar.after(1000,play_time)
#add song function
def add_so():
    song= filedialog.askopenfilename(initialdir='audio/', title='Choose A Song', filetypes=(('mp3 files','*.mp3'),))
   #strip out the directory info and .mp3 extension from the 
    global dir_of_songs
    dir_of_songs.append(song)
    song=os.path.basename(song)
    song=song.replace(".mp3","")
    song_box.insert(END, song)
#add many songs
def add_many_so():
    songs= filedialog.askopenfilenames(initialdir='audio/', title='Choose A Song', filetypes=(('mp3 files','*.mp3'),))
 #loop though the song list and replace directory info and mp3
    global dir_of_songs
    for song in songs:
        dir_of_songs.append(song)
        song=os.path.basename(song)
        song=song.replace(".mp3","")
        song_box.insert(END, song)
#to find all the audio files in the system
def all_music():
    all_songs=[]
    global dir_of_songs
    for root, dirs, files in os.walk('c:\\'):
        for file in files:
            if file.endswith('.mp3'):
                all_songs.append(file)
                dir_of_songs.append(os.path.join(root,file))
    for root, dirs, files in os.walk('g:\\'):
        for file in files:
            if file.endswith('.mp3'):
                all_songs.append(file)
                dir_of_songs.append(os.path.join(root,file))            
    for song in all_songs:
        song_box.insert(END,song) 

#Play selected song
def play():

    #Set stop variable to false  to make song playser
    global ll
    global stopped
    global dir_of_songs
    stopped=False
    song=song_box.get(ACTIVE)
    vr.set(song.upper())
    
    for str in dir_of_songs:
        if song in str:
            song=str
            break    
            
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    
    play_time()
    
    #volume display
    #current_volume=pygame.mixer.music.get_volume()
    #volume_label.config(text=current_volume*100)
    
#gloabl pause variable
global paused 
paused = False

#pause box
def pause(is_paused):
    global paused
    paused= is_paused
    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused= False
    else:
        pygame.mixer.music.pause()
        paused=True
global stopped
stopped=False
def stop():
    #reset slider status
    status_bar.config(text='')
    slider_m.config(value=0)
    #stop audio
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    
    #clear the status bar
    status_bar.config(text='')
    #set stop variable to true
    global stopped
    stopped = True
#Play the next song
def next_song():
    global dir_of_songs
    current_one=song_box.curselection()
    #add one to the current song number
    current_one=current_one[0]+1
    song=song_box.get(current_one)
    vr.set(song.upper())
    #making song playable
    for str in dir_of_songs:
        if song in str:
            song=str
            break    
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #reset slider status
    status_bar.config(text='')
    slider_m.config(value=0)
    #move the active bar
    song_box.selection_clear(0,END)
    song_box.activate(current_one)
    song_box.selection_set(current_one,last=None)
#play previous song
def previous_song():
    global dir_of_songs
    current_one=song_box.curselection()
    #add one to the current song number
    current_one=current_one[0]-1
    song=song_box.get(current_one)
    vr.set(song.upper())
    #making song playable
    for str in dir_of_songs:
        if song in str:
            song=str
            break    
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #reset slider status
    status_bar.config(text='')
    slider_m.config(value=0)
    #move the active bar
    song_box.selection_clear(0,END)
    song_box.activate(current_one)
    song_box.selection_set(current_one,last=None)
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()
def delete_all_songs():
    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()
#Create slider function
def slide(x):
    global dir_of_songs
    song=song_box.get(ACTIVE)
    for str in dir_of_songs:
        if song in str:
            song=str
            break  
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(slider_m.get()))
def volume(x):
    pygame.mixer.music.set_volume(slider_vo.get())
    current_volume=pygame.mixer.music.get_volume()
    volume_label.config(text=int(current_volume*100))   
#using search function

def search_fnc():
    global dir_of_songs
    search = se.get()
    if search=='Search Your Song Here'or search== ' ':
        pass
    else:
    
        f=0
        for root, dirs, files in os.walk('c:\\'):
            for file in files:
                if file.endswith('.mp3'):
                     if((file.upper() in search.upper()) or (search.upper() in file.upper())):
                        lc=os.path.join(root,file)
                        f=1
                        break
        if(f==0):     
            for root, dirs, files in os.walk('g:\\'):
                for file in files:
                    if file.endswith('.mp3'):
                        if((file in search) or (search in file)):
                            lc=os.path.join(root,file)
                            f=1
                            break
        if(f==0):
            se.set('Search Your Song Here')
        else:
            song_box.insert(END,os.path.basename(lc))
            dir_of_songs.append(lc)

    
#search frame
search_frame=Frame(root)
search_frame.pack(pady=10)

 #creating all frame
all_frame=Frame(root)
all_frame.pack()

 #create Master Frame
master_frame = Frame(all_frame)
master_frame.pack(pady=5,side=LEFT)

#Timeline Label Frame
tm_frame=LabelFrame(master_frame,text='Timeline')
tm_frame.grid(row=3,column=0,pady=10)

vr = StringVar()
#Create Current playing song label
playing_box=Label(master_frame,textvariable= vr,bg='Cyan',fg='Green',width=50,height=2,relief=SUNKEN,font=("Times New Roman", 10,"bold") )
playing_box.grid(row=1,column=0,pady=15)

#Create Playlist box
song_box = Listbox(master_frame, bg='black', fg='white',width=60,selectbackground='gray',selectforeground='black')
song_box.grid(row=4,column=0 )

#define player control buttons images
bk_bn_img= PhotoImage(file='G:/buttons/left-3.png',master=root)
fr_bn_img= PhotoImage(file='G:/buttons/right-3.png',master=root)
pl_bn_img= PhotoImage(file='G:/buttons/play-3.png',master=root)
pa_bn_img= PhotoImage(file='G:/buttons/pause-3.png',master=root)
loop_bn_imp= PhotoImage(file='G:/buttons/repeat.png',master=root)
# Create Player control frames
ctrl_fr = Frame(master_frame)
ctrl_fr.grid(row=2,column=0,pady=5)
#Create Volume frame
volume_frame=LabelFrame(all_frame,text='Volume')
volume_frame.pack(side= RIGHT,padx=10)
             
#Create Player Control Buttons
bk_bn= Button(ctrl_fr, image=bk_bn_img, borderwidth=0, command=previous_song)
fr_bn= Button(ctrl_fr, image=fr_bn_img, borderwidth=0,command=next_song)
pl_bn= Button(ctrl_fr, image=pl_bn_img, borderwidth=0,command=play)
pa_bn= Button(ctrl_fr, image=pa_bn_img, borderwidth=0,command=lambda:pause(paused))


bk_bn.grid(row=0, column=1,padx=10)
fr_bn.grid(row=0, column=4,padx=10)
pl_bn.grid(row=0, column=2,padx=10)
pa_bn.grid(row=0, column=3,padx=10)

#create menu
my_menu=Menu(root)
root.config( menu=my_menu)

#Add Song Menu
add_s=Menu(my_menu)
my_menu.add_cascade(label='Add Songs', menu= add_s)
add_s.add_command(label='Add one song to play list', command= add_so)                  
 #add many songs to the Playlist                 
add_s.add_command(label='Add Many songs to play list', command= add_many_so) 
#find all songs on the PC
add_s.add_command(label='Find All Songs On My PC', command= all_music)
 #create delete song menu
remove_s_menu= Menu(my_menu)
my_menu.add_cascade(label='Remove Songs',menu=remove_s_menu)
remove_s_menu.add_command(label='Remove Current Song',command= delete_song)
remove_s_menu.add_command(label='Remove All Songs',command= delete_all_songs)
#Create status Bar
status_bar = Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X, side= BOTTOM, ipady=2)
#Create music slider
slider_m = ttk.Scale(tm_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=320)
slider_m.grid(row=3,column=0,pady=10,padx=20)

#Create volume SLider
slider_vo = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
slider_vo.pack(pady=10)
#volume label
volume_label = Label(volume_frame,text='100')
volume_label.pack()

#search box
se= StringVar()
search_box=Entry(search_frame, textvariable=se,width=59,borderwidth=2).grid(row=0,column=0)
search_button = Button(search_frame,text='Search',borderwidth=1,command=search_fnc).grid(row=0,column=1,padx=10)
se.set('Search To Add')

root.mainloop()














































# In[ ]:





# In[ ]:





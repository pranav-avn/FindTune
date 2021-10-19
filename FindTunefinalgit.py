#FindTune, a project by pranav-avn

#importing all required Python packages
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import mysql.connector as mys
import statistics as stats
import random
import os
import sys
import urllib.request
import re
import pafy
from PIL import Image, ImageTk
from urllib.request import urlretrieve
from tkmacosx import *
import tkmacosx as tkm
import webbrowser
from tkinter import messagebox

#code start

root = Tk(className=" FindTune")     #creating root widget
imapplogo = PhotoImage(file = "ftlogo2s.png")
applogintrm = impapplogo.resize((512,512))
applogo = ImageTk.PhotoImage(applogintrm)
app.iconphoto(True, applogo)

var = tk.IntVar()     #creating tkVariable for radiobuttons
res = tk.IntVar()     #creating tkVariable for radiobuttons
genres = tk.IntVar()     #creating tkVariable for radiobuttons

a = []     #song title entry widget storage
b = []     #artist entry widget storage
c = []     #genre entry widget storage

an = []     #Song Title value storage
bn = []     #Artist value storage
cn = []     #Genre value storage

otlist = []     #Source Table Output Storage
argr = []     #Artist search output storage

errorc=0     #error count

mycon = mys.connect(host='localhost', user='root', passwd='root', charset='utf8', database='music')     #MySQL database connect
cur = mycon.cursor()     #MySQL cursor

def songinp():     #main UDF where all processing occurs
        canvas1.destroy()     #destroying homescreen canvas
        canvas2 = Canvas(root, width=562, height=900)     #creating another blank canvas to render onto
        canvas2.pack(fill="both", expand=True)

        canvas2.create_image(0, 0, image=bg, anchor="nw")
        canvas2.create_image(200, 20, image=logofile, anchor="nw")                    #branding info
        canvas2.create_text(295, 115, text="FindTune.", font=hfontStyle)
        canvas2.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

        def usrn(e):     #user input function
            global errorc     #error count variable used to display error messge depending on current conditions
            ctrl = var.get()     #accepting the selected option from the radio buttons
            canvas2.itemconfig(button4, image=greyed_button)     #greying out the button to input
            cur.execute("delete from usr_input;")
            error = canvas2.create_text(290, 480, text="", font=mfontStyle)

            if 3 >= ctrl > 0:
                if errorc > 0:
                    canvas2.itemconfig(error, text="")
                    listinp(ctrl)     #moving forward to list input function
                else:
                    listinp(ctrl)
                print(ctrl)
            else:
                canvas2.itemconfig(error, text="Please select a valid option 🙂")
                print(ctrl)
                errorc+=1


        def listinp(x):     #UDF where User input is packaged into a list
            inc=0     #control variable used to space out tkinter widgets
            def button_process(e):     #UDF where user input is processed

                def wind3(e): #further processing
                    canvas2.destroy()
                    canvas3 = Canvas(root, width=562, height=900)
                    canvas3.pack(fill="both", expand=True)

                    canvas3.create_image(0, 0, image=bg, anchor="nw")
                    canvas3.create_image(200, 20, image=logofile, anchor="nw")
                    canvas3.create_text(295, 115, text="FindTune.", font=hfontStyle)
                    canvas3.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

                    def artsrch(e):     #artist search function
                        cur.execute("select * from usr_input")
                        usrdata = cur.fetchall()
                        artlist = list()
                        for i in usrdata:
                            uia = i[1]
                            artlist.append(uia)
                        canvas3.destroy()
                        canvas4 = Canvas(root, width=562, height=900)
                        canvas4.pack(fill="both", expand=True)

                        canvas4.create_image(0, 0, image=bg, anchor="nw")
                        canvas4.create_image(190, 20, image=logofile, anchor="nw")
                        canvas4.create_text(285, 115, text="FindTune.", font=hfontStyle)
                        canvas4.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')
                        canvas4.create_text(320, 240, text="These are the artists you entered!", font=m1fontStyle)
                        artdc=0
                        for i in artlist:
                            canvas4.create_text(200, 270+artdc, text=i, font=m1fontStyle)
                            artdc+=20
                        canvas4.create_text(290, 310+artdc, text="Here are some similar songs that you might like!", font=m1fontStyle)

                        def delayy(e):      #delay function to break the program execution to ease processing requirements

                            artcorrect = res.get()
                            if 4 >= artcorrect > 0:
                                def delayot():
                                    artprnt()
                                def delayprint():
                                    canvas4.create_text(290, yhead + 90,
                                                       text="Please wait... ",
                                                       font=hfontStyle)
                                    canvas4.create_text(290,yhead+110, text="We are using complex sciences to comprehend your music taste", font=mfontStyle)
                                    canvas4.after(1000,delayot)
                                canvas4.after(500, delayprint)
                            else:
                                canvas4.create_text(290, yhead + 60,
                                                    text="Please Select a valid option ",
                                                    font=m1fontStyle)

                        def artprnt():
                            nsug_str = res.get()
                            nsuggest = int(nsug_str)



                            canvas4.destroy()
                            canvas5 = Canvas(root, width=1080, height=2280)
                            canvas5.pack(fill="both", expand=True)
                            canvas5.create_image(0, 0, image=bg, anchor="nw")
                            canvas5.create_image(200, 20, image=logofile, anchor="nw")
                            canvas5.create_text(295, 115, text="FindTune.", font=hfontStyle)
                            canvas5.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

                            artdsp = "Artist Search Results"
                            canvas5.create_text(282, y1head-70, text=artdsp, font=hfontStyle)
                            canvas5.create_text(290, y1head-30, text="Here are some songs that you might enjoy!", font=m1fontStyle)
                            ccdp = 0
                            disctrl = 0

                            def restart():
                                os.execl(sys.executable, sys.executable, *sys.argv)

                            def artist_search_results(title):     #function to get YouTube thumbnail
                                print(title)
                                query = title.replace(" ", "+")     #parameterising the string containing 'Song Name by Artist" to conform to YouTube search requirements
                                print(query)
                                html = urllib.request.urlopen(
                                    "https://www.youtube.com/results?search_query=" + query)     #searching YouTube for given song
                                video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())     #saving output into a re variable
                                video_url = "https://www.youtube.com/watch?v=" + video_id[0]     #getting the unique video identifier of the first search result (which is most probably the official video of the given song)
                                video = pafy.new(video_url)     #using pafy to retrieve the thumbnail
                                thumb = video.bigthumb          #getting the high res (1280x720) version of the thumbnail
                                urlretrieve(thumb, 'pic.jpg')   #saving the accepted thumbnail as pic.jpg onto the secondary memory
                                img_file = Image.open("pic.jpg")    #opening the saved thumbnail
                                img_file = img_file.resize((240, 135))  # (width,height)  using resize function to better fit output screen
                                img = ImageTk.PhotoImage(img_file)  #using ImageTk to save png image as variable
                                albart = Label(image=img)   #creating label with image as the background
                                albart.image = img  #referencing the image to avoid being garbage collected during loop
                                canvas5.create_window(200, yp+50, window=albart)    #displaying the retrieved image

                                def ytlink(url):
                                    webbrowser.open_new_tab(url)    #function to open a new browser tab when clicked on the thumbnail
                                    print(video_url) #debug

                                albart.bind("<Button-1>", lambda e: ytlink(video_url))  #function to open a new browser tab when clicked on the thumbnail
                                canvas5.create_text(380, yp+50, text=title, font=mfontStyle, anchor='w')

                            lenctrl=0
                            for i in artlist:

                                if len(artlist)>1 and lenctrl==0:
                                    if nsuggest>1:
                                        nsuggest=nsuggest//2
                                        lenctrl+=1
                                elif len(artlist)>1 and lenctrl==1 and artlist.index(i)>0:
                                    lenctrl+=1
                                elif len(artlist)==1:
                                    lenctrl=2

                                artcomp = "select * from Source_master where Artist='{}';".format(i)
                                cur.execute(artcomp)
                                otpt2 = cur.fetchall()
                                cc = 0
                                if cur.rowcount != 0:
                                    for j in otpt2:
                                        yp = y1head+20+disctrl
                                        cc = cc + 1
                                        ot = j[1]+' by '+j[2]
                                        title = j[1]+" "+j[2]
                                        otlist.append(title)

                                        artist_search_results(ot)

                                        ccdp = ccdp+1
                                        disctrl = ccdp * 140

                                        if cc == nsuggest and lenctrl<2:
                                            break
                                        elif cc == nsuggest and lenctrl==2:
                                            button11 = Button(canvas5, text="Restart", font=mfontStyle, command=restart)
                                            button11["border"] = "0"
                                            button11 = canvas5.create_image(200, yp+140+15, image=proceed_button_bg)
                                            tetx11 = canvas5.create_text(200, yp+ 140+15, text="Restart",
                                                                         font=bfontStyle)
                                            canvas5.tag_bind(button11, "<1>", lambda e: restart())
                                            canvas5.tag_bind(tetx11, "<1>", lambda e: restart())

                                            def genrsrch(e):

                                                canvas5.destroy()
                                                canvas3 = Canvas(root, width=1080, height=2280)
                                                canvas3.pack(fill="both", expand=True)
                                                canvas3.create_image(0, 0, image=bg, anchor="nw")
                                                canvas3.create_image(200, 20, image=logofile, anchor="nw")
                                                canvas3.create_text(295, 115, text="FindTune.", font=hfontStyle)
                                                canvas3.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

                                                artdsp = "Genre Search"
                                                canvas3.create_text(282, 260, text=artdsp, font=hfontStyle)
                                                canvas3.create_text(282, 290,
                                                                    text="Here are some songs that you might enjoy!",
                                                                    font=m1fontStyle)
                                                cur.execute("select * from usr_input")
                                                usrdata = cur.fetchall()
                                                tg = list()
                                                for i in usrdata:
                                                    g = i[2]
                                                    tg.append(g)
                                                intrests = stats.mode(tg)
                                                intrdis = "Your interests seem to be: " + intrests
                                                canvas3.create_text(282, 330, text=intrdis, font=m1fontStyle)
                                                compare = "select * from Source_master where Genre='{}';".format(
                                                    intrests)
                                                cur.execute(compare)
                                                otpt1 = cur.fetchall()

                                                def restart():
                                                    os.execl(sys.executable, sys.executable, *sys.argv)

                                                def rquit():
                                                    root.destroy()

                                                def delayy(e):

                                                    genrcorrect = genres.get()
                                                    if 4>= genrcorrect >0:
                                                        def delayot():
                                                            genrprnt()

                                                        def delayprint():
                                                            canvas3.create_text(290, 630,
                                                                                text="Please wait... ",
                                                                                font=hfontStyle)
                                                            canvas3.create_text(290, 650,
                                                                                text="We are using complex sciences to comprehend your music taste",
                                                                                font=mfontStyle)
                                                            canvas3.after(1000, delayot)

                                                        canvas3.after(500, delayprint)
                                                    else:
                                                        canvas3.create_text(290, 600,
                                                                            text="Please Select a valid option ",
                                                                            font=m1fontStyle)


                                                def genrprnt():
                                                    nsug_str = genres.get()
                                                    nsuggest = int(nsug_str)

                                                    canvas3.destroy()

                                                    canvas4 = Canvas(root, width=1080, height=2280)
                                                    canvas4.pack(fill="both", expand=True)
                                                    canvas4.create_image(0, 0, image=bg, anchor="nw")
                                                    canvas4.create_image(200, 20, image=logofile, anchor="nw")
                                                    canvas4.create_text(295, 115, text="FindTune.", font=hfontStyle)
                                                    canvas4.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

                                                    artdsp = "Genre Search"
                                                    canvas4.create_text(282, 260, text=artdsp, font=hfontStyle)
                                                    canvas4.create_text(282, 290,
                                                                        text="Here are some songs that you might enjoy!",
                                                                        font=mfontStyle)

                                                    consolval = random.sample(otpt1,
                                                                              k=nsuggest)  # random function for randomised output
                                                    genrlctrl = 0
                                                    genrprnc = 0

                                                    def ar_genre_search_results(title):

                                                        query = title.replace(" ", "+")
                                                        html = urllib.request.urlopen(
                                                            "https://www.youtube.com/results?search_query=" + query)
                                                        video_id = re.findall(r"watch\?v=(\S{11})",
                                                                              html.read().decode())
                                                        video_url = "https://www.youtube.com/watch?v=" + video_id[0]
                                                        video = pafy.new(video_url)
                                                        thumb = video.bigthumb
                                                        urlretrieve(thumb, 'pic.jpg')
                                                        img_file = Image.open("pic.jpg")
                                                        img_file = img_file.resize((240, 135))  # (width,height)
                                                        img = ImageTk.PhotoImage(img_file)
                                                        albart = Label(image=img)
                                                        albart.image = img
                                                        canvas4.create_window(200, 240+genrprnc, window=albart)

                                                        def ytlink(url):
                                                            webbrowser.open_new_tab(url)
                                                            print(video_url)

                                                        albart.bind("<Button-1>", lambda e: ytlink(video_url))
                                                        canvas4.create_text(380, 240+genrprnc, text=genrot, font=mfontStyle, anchor='w')


                                                    for i in consolval:
                                                        genrot = i[1] + " by " + i[2]
                                                        genrlctrl += 1
                                                        genrprnc = genrlctrl * 140
                                                        ar_gn_sr_term = i[1] + " " + i[2]
                                                        argr.append(ar_gn_sr_term)
                                                        ar_genre_search_results(ar_gn_sr_term)

                                                        if genrlctrl == nsuggest:
                                                            button11 = canvas4.create_image(200, 360 + genrprnc,
                                                                                            image=proceed_button_bg)
                                                            tetx11 = canvas4.create_text(200, 360 + genrprnc,
                                                                                         text="Restart",
                                                                                         font=bfontStyle)
                                                            canvas4.tag_bind(button11, "<1>", lambda e: restart())
                                                            canvas4.tag_bind(tetx11, "<1>", lambda e: restart())
                                                            button12 = canvas4.create_image(400, 360 + genrprnc,
                                                                                            image=proceed_button_bg)
                                                            tetx12 = canvas4.create_text(400, 360 + genrprnc,
                                                                                         text="Quit",
                                                                                         font=bfontStyle)
                                                            canvas4.tag_bind(button12, "<1>", lambda e: rquit())
                                                            canvas4.tag_bind(tetx12, "<1>", lambda e: rquit())
                                                            break


                                                if cur.rowcount != 0:
                                                    canvas3.create_text(282, 410,
                                                                        text="Enter the number of suggestions you'd like:",
                                                                        font=m1fontStyle)
                                                    rg1 = tkm.Radiobutton(canvas3, text='1', value=1,
                                                                          variable=genres, indicatoron=0, padx=20,
                                                                          selectcolor="#232323")
                                                    rg2 = tkm.Radiobutton(canvas3, text='2', value=2,
                                                                          variable=genres, indicatoron=0, padx=20,
                                                                          selectcolor="#232323")
                                                    rg3 = tkm.Radiobutton(canvas3, text='3', value=3,
                                                                          variable=genres, indicatoron=0, padx=20,
                                                                          selectcolor="#232323")
                                                    rg4 = tkm.Radiobutton(canvas3, text='4', value=4,
                                                                          variable=genres, indicatoron=0, padx=20,
                                                                          selectcolor="#232323")

                                                    rg1.place(x=251, y=425)
                                                    rg2.place(x=250, y=450)
                                                    rg3.place(x=250, y=475)
                                                    rg4.place(x=250, y=500)

                                                    button10 = canvas3.create_image(280, 560,
                                                                                    image=proceed_button_bg)
                                                    tetx10 = canvas3.create_text(280, 560,
                                                                                 text="Proceed",
                                                                                 font=bfontStyle)
                                                    canvas3.tag_bind(button10, "<1>", delayy)
                                                    canvas3.tag_bind(tetx10, "<1>", delayy)

                                                else:
                                                    canvas3.create_text(282, 410,
                                                                        text="Invalid input. Please Check the input data.",
                                                                        font=m1fontStyle)
                                                    button11 = canvas3.create_image(280, 450,
                                                                                    image=proceed_button_bg)
                                                    tetx11 = canvas3.create_text(280, 450, text="Restart",
                                                                                 font=bfontStyle)
                                                    canvas3.tag_bind(button11, "<1>", lambda e: restart())
                                                    canvas3.tag_bind(tetx11, "<1>", lambda e: restart())

                                            button12 = canvas5.create_image(400, yp + 140+15, image=proceed_button_bg)
                                            tetx12 = canvas5.create_text(400, yp + 140+15, text="Genre Search",
                                                                         font=bfontStyle)
                                            canvas5.tag_bind(button12, "<1>", genrsrch)
                                            canvas5.tag_bind(tetx12, "<1>", genrsrch)
                                            break

                                else:
                                    canvas5.create_text(280, y1head + 80, text="Invalid input. Please Check the input data.", font=m1fontStyle)
                                    button11= canvas5.create_image(280, y1head+150, image=proceed_button_bg)
                                    tetx11 = canvas5.create_text(280, y1head+150, text="Restart", font=bfontStyle)
                                    canvas5.tag_bind(button11, "<1>", lambda e: restart())
                                    canvas5.tag_bind(tetx11, "<1>", lambda e: restart())

                        canvas4.create_text(290, 350+artdc, text="Pick the number of suggestions you'd like:",
                                            font=m1fontStyle)
                        '''nsug = Entry(canvas4, width=4)
                        nsug.place(x=580, y=435+artdc)'''
                        ra1 = tkm.Radiobutton(canvas4, text='1', value=1,
                                             variable=res, indicatoron=0, padx=20, selectcolor="#232323")
                        ra2 = tkm.Radiobutton(canvas4, text='2', value=2,
                                             variable=res, indicatoron=0, padx=20, selectcolor="#232323")
                        ra3 = tkm.Radiobutton(canvas4, text='3', value=3,
                                             variable=res, indicatoron=0, padx=20, selectcolor="#232323")
                        ra4 = tkm.Radiobutton(canvas4, text='4', value=4,
                                             variable=res, indicatoron=0, padx=20, selectcolor="#232323")

                        ra1.place(x=251, y=365+artdc)
                        ra2.place(x=250, y=390+artdc)
                        ra3.place(x=250, y=415+artdc)
                        ra4.place(x=250, y=440 + artdc)

                        button9 = canvas4.create_image(280, 500+artdc, image=proceed_button_bg)
                        tetx9 = canvas4.create_text(280, 500+artdc, text="Display", font=bfontStyle)
                        canvas4.tag_bind(button9, "<1>", delayy)
                        canvas4.tag_bind(tetx9, "<1>", delayy)
                        yhead=485+artdc
                        y1head=280

                    def genrsrch(e):
                        canvas3.destroy()

                        canvas4 = Canvas(root, width=1080, height=2280)
                        canvas4.pack(fill="both", expand=True)
                        canvas4.create_image(0, 0, image=bg, anchor="nw")
                        canvas4.create_image(200, 20, image=logofile, anchor="nw")
                        canvas4.create_text(295, 115, text="FindTune.", font=hfontStyle)
                        canvas4.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

                        artdsp = "Genre Search"
                        canvas4.create_text(282, 260, text=artdsp, font=hfontStyle)
                        canvas4.create_text(282, 290,
                                            text="Here are some songs that you might enjoy!",
                                            font=m1fontStyle)
                        cur.execute("select * from usr_input")
                        usrdata = cur.fetchall()
                        tg = list()
                        for i in usrdata:
                            g = i[2]
                            tg.append(g)
                        intrests = stats.mode(tg)
                        intrdis = "Your interests seem to be: " + intrests
                        canvas4.create_text(282, 330, text=intrdis, font=m1fontStyle)
                        compare = "select * from Source_master where Genre='{}';".format(
                            intrests)
                        cur.execute(compare)
                        otpt1 = cur.fetchall()

                        def restart():
                            os.execl(sys.executable, sys.executable, *sys.argv)

                        def delayy(e):

                            genrcorrect = genres.get()
                            if 4 >= genrcorrect >0:
                                def delayot():
                                    genrprnt()

                                def delayprint():
                                    canvas4.create_text(290, 630,
                                                        text="Please wait... ",
                                                        font=hfontStyle)
                                    canvas4.create_text(290, 650,
                                                        text="We are using complex sciences to comprehend your music taste",
                                                        font=mfontStyle)
                                    canvas4.after(1000, delayot)

                                canvas4.after(500, delayprint)
                                print("genresuccses")
                            else:
                                canvas4.create_text(290, 600,
                                                    text="Please Select a valid option ",
                                                    font=m1fontStyle)
                                print("genrefail")

                        def genrprnt():
                            nsug_str = genres.get()
                            nsuggest = int(nsug_str)

                            canvas4.destroy()

                            canvas3 = Canvas(root, width=1080, height=2280)
                            canvas3.pack(fill="both", expand=True)
                            canvas3.create_image(0, 0, image=bg, anchor="nw")
                            canvas3.create_image(200, 20, image=logofile, anchor="nw")
                            canvas3.create_text(295, 115, text="FindTune.", font=hfontStyle)
                            canvas3.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

                            artdsp = "Genre Search"
                            canvas3.create_text(282, 260, text=artdsp, font=hfontStyle)
                            canvas3.create_text(282, 290,
                                                text="Here are some songs that you might enjoy!",
                                                font=mfontStyle)

                            consolval = random.sample(otpt1,
                                                      k=nsuggest)  # random function for randomised output
                            genrlctrl = 0
                            genrprnc = 0

                            def ar_genre_search_results(title):

                                query = title.replace(" ", "+")
                                html = urllib.request.urlopen(
                                    "https://www.youtube.com/results?search_query=" + query)
                                video_id = re.findall(r"watch\?v=(\S{11})",
                                                      html.read().decode())
                                video_url = "https://www.youtube.com/watch?v=" + video_id[0]
                                video = pafy.new(video_url)
                                thumb = video.bigthumb
                                urlretrieve(thumb, 'pic.jpg')
                                img_file = Image.open("pic.jpg")
                                img_file = img_file.resize((240, 135))  # (width,height)
                                img = ImageTk.PhotoImage(img_file)
                                albart = Label(image=img)
                                albart.image = img
                                canvas3.create_window(200, 260 + genrprnc, window=albart)

                                def ytlink(url):
                                    webbrowser.open_new_tab(url)
                                    print(video_url)

                                albart.bind("<Button-1>", lambda e: ytlink(video_url))
                                canvas3.create_text(380, 260 + genrprnc, text=genrot, font=mfontStyle, anchor='w')

                            for i in consolval:
                                genrot = i[1] + " by " + i[2]
                                genrlctrl += 1
                                genrprnc = genrlctrl * 150
                                ar_gn_sr_term = i[1] + " " + i[2]
                                argr.append(ar_gn_sr_term)
                                ar_genre_search_results(ar_gn_sr_term)

                                if genrlctrl == nsuggest:

                                    button11 = canvas3.create_image(200, 360+genrprnc,
                                                                    image=proceed_button_bg)
                                    tetx11 = canvas3.create_text(200, 360+genrprnc,
                                                                 text="Restart",
                                                                 font=bfontStyle)
                                    canvas3.tag_bind(button11, "<1>", lambda e: restart())
                                    canvas3.tag_bind(tetx11, "<1>", lambda e: restart())

                                    def artsrch(e):
                                        cur.execute("select * from usr_input")
                                        usrdata = cur.fetchall()
                                        artlist = list()
                                        for i in usrdata:
                                            uia = i[1]
                                            artlist.append(uia)
                                        canvas3.destroy()
                                        canvas4 = Canvas(root, width=562, height=900)
                                        canvas4.pack(fill="both", expand=True)

                                        canvas4.create_image(0, 0, image=bg, anchor="nw")
                                        canvas4.create_image(190, 20, image=logofile, anchor="nw")
                                        canvas4.create_text(285, 115, text="FindTune.", font=hfontStyle)
                                        canvas4.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')
                                        canvas4.create_text(320, 240, text="These are the artists you entered!",
                                                            font=m1fontStyle)
                                        artdc = 0
                                        for i in artlist:
                                            canvas4.create_text(200, 270 + artdc, text=i, font=m1fontStyle)
                                            artdc += 20
                                        canvas4.create_text(290, 310 + artdc,
                                                            text="Here are some similar songs that you might like!",
                                                            font=m1fontStyle)

                                        def delayy(e):

                                            artcorrect = res.get()
                                            if 4>= artcorrect >0:
                                                def delayot():
                                                    artprnt()

                                                def delayprint():
                                                    canvas4.create_text(290, yhead + 90,
                                                                        text="Please wait... ",
                                                                        font=hfontStyle)
                                                    canvas4.create_text(290, yhead + 120,
                                                                        text="We are using complex sciences to comprehend your music taste",
                                                                        font=mfontStyle)
                                                    canvas4.after(1000, delayot)

                                                canvas4.after(500, delayprint)
                                            else:
                                                canvas4.create_text(290, yhead + 60,
                                                                    text="Invalid Choice",
                                                                    font=m1fontStyle)

                                        def artprnt():
                                            nsug_str = res.get()
                                            nsuggest = int(nsug_str)

                                            canvas4.destroy()
                                            canvas5 = Canvas(root, width=1080, height=2280)
                                            canvas5.pack(fill="both", expand=True)
                                            canvas5.create_image(0, 0, image=bg, anchor="nw")
                                            canvas5.create_image(200, 20, image=logofile, anchor="nw")
                                            canvas5.create_text(295, 115, text="FindTune.", font=hfontStyle)
                                            canvas5.create_text(558, 4, text="v5", font=mfontStyle, anchor='ne')

                                            artdsp = "Artist Search Results"
                                            canvas5.create_text(282, y1head - 70, text=artdsp, font=hfontStyle)
                                            canvas5.create_text(290, y1head - 30,
                                                                text="Here are some songs that you might enjoy!",
                                                                font=m1fontStyle)
                                            ccdp = 0
                                            disctrl = 0

                                            def restart():
                                                os.execl(sys.executable, sys.executable, *sys.argv)

                                            def rquit():
                                                root.destroy()

                                            def artist_search_results(title):
                                                print(title)
                                                query = title.replace(" ", "+")
                                                print(query)
                                                html = urllib.request.urlopen(
                                                    "https://www.youtube.com/results?search_query=" + query)
                                                video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                                                video_url = "https://www.youtube.com/watch?v=" + video_id[0]
                                                video = pafy.new(video_url)
                                                thumb = video.bigthumb
                                                urlretrieve(thumb, 'pic.jpg')
                                                img_file = Image.open("pic.jpg")
                                                img_file = img_file.resize((240, 135))  # (width,height)
                                                img = ImageTk.PhotoImage(img_file)
                                                albart = Label(image=img)
                                                albart.image = img
                                                canvas5.create_window(200, yp + 50, window=albart)

                                                def ytlink(url):
                                                    webbrowser.open_new_tab(url)
                                                    print(video_url)

                                                albart.bind("<Button-1>", lambda e: ytlink(video_url))
                                                canvas5.create_text(380, yp + 50, text=title, font=mfontStyle, anchor='w')

                                            lenctrl=0
                                            for i in artlist:
                                                if len(artlist) > 1 and lenctrl==0:
                                                    if nsuggest>1:
                                                        nsuggest = nsuggest // 2
                                                        lenctrl+=1
                                                elif len(artlist) > 1 and lenctrl == 1 and artlist.index(i)>0:
                                                    lenctrl += 1
                                                elif len(artlist) == 1:
                                                    lenctrl = 2
                                                artcomp = "select * from Source_master where Artist='{}';".format(i)
                                                cur.execute(artcomp)
                                                otpt2 = cur.fetchall()
                                                cc = 0
                                                if cur.rowcount != 0:
                                                    for j in otpt2:
                                                        yp = y1head + 20 + disctrl
                                                        cc = cc + 1
                                                        ot = j[1] + ' by ' + j[2]
                                                        title = j[1] + " " + j[2]
                                                        otlist.append(title)

                                                        artist_search_results(ot)

                                                        ccdp = ccdp + 1
                                                        disctrl = ccdp * 140

                                                        if cc == nsuggest and lenctrl < 2:
                                                            break
                                                        elif cc == nsuggest and lenctrl==2:
                                                            button11 = canvas5.create_image(200, yp+140+30,
                                                                                            image=proceed_button_bg)
                                                            tetx11 = canvas5.create_text(200, yp+140+30,
                                                                                         text="Restart",
                                                                                         font=bfontStyle)
                                                            canvas5.tag_bind(button11, "<1>", lambda e: restart())
                                                            canvas5.tag_bind(tetx11, "<1>", lambda e: restart())
                                                            button12 = canvas5.create_image(400, yp+140+30,
                                                                                            image=proceed_button_bg)
                                                            tetx12 = canvas5.create_text(400, yp+140+30,
                                                                                         text="Quit",
                                                                                         font=bfontStyle)
                                                            canvas5.tag_bind(button12, "<1>", lambda e: rquit())
                                                            canvas5.tag_bind(tetx12, "<1>", lambda e: rquit())

                                                            break

                                                else:
                                                    canvas5.create_text(280, y1head + 80,
                                                                        text="Invalid input. Please Check the input data.",
                                                                        font=m1fontStyle)
                                                    button11 = canvas5.create_image(280, y1head+150,
                                                                                   image=proceed_button_bg)
                                                    tetx11 = canvas5.create_text(280, y1head+150, text="Restart",
                                                                                font=bfontStyle)
                                                    canvas5.tag_bind(button11, "<1>", lambda e: restart())
                                                    canvas5.tag_bind(tetx11, "<1>", lambda e: restart())

                                        canvas4.create_text(290, 350 + artdc,
                                                            text="Pick the number of suggestions you'd like:",
                                                            font=m1fontStyle)
                                        '''nsug = Entry(canvas4, width=4)
                                        nsug.place(x=580, y=435+artdc)'''
                                        ra1 = tkm.Radiobutton(canvas4, text='1', value=1,
                                                              variable=res, indicatoron=0, padx=20,
                                                              selectcolor="#232323")
                                        ra2 = tkm.Radiobutton(canvas4, text='2', value=2,
                                                              variable=res, indicatoron=0, padx=20,
                                                              selectcolor="#232323")
                                        ra3 = tkm.Radiobutton(canvas4, text='3', value=3,
                                                              variable=res, indicatoron=0, padx=20,
                                                              selectcolor="#232323")
                                        ra4 = tkm.Radiobutton(canvas4, text='4', value=4,
                                                              variable=res, indicatoron=0, padx=20,
                                                              selectcolor="#232323")

                                        ra1.place(x=251, y=365 + artdc)
                                        ra2.place(x=250, y=390 + artdc)
                                        ra3.place(x=250, y=415 + artdc)
                                        ra4.place(x=250, y=440 + artdc)

                                        button9 = canvas4.create_image(280, 500 + artdc, image=proceed_button_bg)
                                        tetx9 = canvas4.create_text(280, 500 + artdc, text="Display", font=bfontStyle)
                                        canvas4.tag_bind(button9, "<1>", delayy)
                                        canvas4.tag_bind(tetx9, "<1>", delayy)
                                        yhead = 485 + artdc
                                        y1head = 280


                                    button12 = canvas3.create_image(400, 360 + genrprnc,
                                                                    image=proceed_button_bg)
                                    tetx12 = canvas3.create_text(400, 360 + genrprnc,
                                                                 text="Artist Search",
                                                                 font=bfontStyle)
                                    canvas3.tag_bind(button12, "<1>", artsrch)
                                    canvas3.tag_bind(tetx12, "<1>", artsrch)
                                    break

                        if cur.rowcount != 0:
                            canvas4.create_text(282, 410,
                                                text="Enter the number of suggestions you'd like:",
                                                font=m1fontStyle)
                            rg1 = tkm.Radiobutton(canvas4, text='1', value=1,
                                                  variable=genres, indicatoron=0, padx=20,
                                                  selectcolor="#232323")
                            rg2 = tkm.Radiobutton(canvas4, text='2', value=2,
                                                  variable=genres, indicatoron=0, padx=20,
                                                  selectcolor="#232323")
                            rg3 = tkm.Radiobutton(canvas4, text='3', value=3,
                                                  variable=genres, indicatoron=0, padx=20,
                                                  selectcolor="#232323")
                            rg4 = tkm.Radiobutton(canvas4, text='4', value=4,
                                                  variable=genres, indicatoron=0, padx=20,
                                                  selectcolor="#232323")

                            rg1.place(x=251, y=425)
                            rg2.place(x=250, y=450)
                            rg3.place(x=250, y=475)
                            rg4.place(x=250, y=500)

                            button10 = canvas4.create_image(280, 560,
                                                            image=proceed_button_bg)
                            tetx10 = canvas4.create_text(280, 560,
                                                         text="Proceed",
                                                         font=bfontStyle)
                            canvas4.tag_bind(button10, "<1>", delayy)
                            canvas4.tag_bind(tetx10, "<1>", delayy)

                        else:
                            canvas4.create_text(282, 410,
                                                text="Invalid input. Please Check the input data.",
                                                font=m1fontStyle)
                            button11 = canvas4.create_image(280, 460, image=proceed_button_bg)
                            tetx11 = canvas4.create_text(280, 460, text="Restart", font=bfontStyle)
                            canvas4.tag_bind(button11, "<1>", lambda e: restart())
                            canvas4.tag_bind(tetx11, "<1>", lambda e: restart())

                    canvas3.create_text(290, 240, text="What kind of recommendations do you want?", font=m1fontStyle)
                    canvas3.create_text(290, 270, text="Select the appropriate search parameter.", font=m1fontStyle)
                    button7 = canvas3.create_image(280, 400, image=artist_button_bg)
                    canvas3.tag_bind(button7, "<1>", artsrch)       #linked to artist search function
                    button8 = canvas3.create_image(280, 600, image=genre_button_bg)
                    canvas3.tag_bind(button8, "<1>", genrsrch)      #linked to genre search function

                for i in a:
                    an.append(i.get())                  #taking entry widget from list a and appending the input value as string into list an
                for i in b:
                    bn.append(i.get())
                for i in c:
                    cn.append(i.get())
                for i in range(x):
                    process = "insert ignore into usr_input values('{}','{}','{}');".format(an[i], bn[i], cn[i])        #MySQL execution to save input into table
                    cur.execute(process)
                    mycon.commit()

                def restart():
                    os.execl(sys.executable, sys.executable, *sys.argv)     #restart function to restart app



                lcc = 0         #list element count
                x1 = len(a)
                for i in range(x1):
                    if a[i].get()!='' and b[i].get()!='' and c[i].get()!='':
                        if a[i].get()!="Song Title" and b[i].get()!="Artist" and c[i].get()!="Genre":
                            lcc+=1

                if lcc==x1:
                    canvas2.create_text(290, 680 + inc, text="Do you want to Proceed to the Recommendation menu?", font=mfontStyle)
                    button6 = canvas2.create_image(280, 720 + inc, image=proceed_button_bg)
                    tetx6 = canvas2.create_text(280, 720 + inc, text="Proceed", font=bfontStyle)
                    canvas2.tag_bind(button6, "<1>", wind3)
                    canvas2.tag_bind(tetx6, "<1>", wind3)

                else:
                    canvas2.create_text(280, 680 + inc, text="Incorrect Input", font=mfontStyle)
                    errormsg= """Incorrect Values.
                                Please Restart App"""
                    messagebox.showerror("Fatal Error", errormsg) #error message box
                    button6 = canvas2.create_image(280, 720 + inc, image=proceed_button_bg)
                    tetx6 = canvas2.create_text(280, 720 + inc, text="Restart", font=bfontStyle)
                    canvas2.tag_bind(button6, "<1>", lambda e: restart())
                    canvas2.tag_bind(tetx6, "<1>", lambda e: restart())
                    canvas2.tag_unbind(button5, '<1>')
                    canvas2.itemconfig(button5, image=greyed_button)

            def infocentn(e):
                namef.config(bg="#232323")
            def outfocentn(e):
                namef.config(bg="#1E1E1E")
            def infocenta(e):
                artf.config(bg="#232323")                   #defining responsive entry bars using binds
            def outfocenta(e):
                artf.config(bg="#1E1E1E")
            def infocentg(e):
                genrf.config(bg="#232323")
            def outfocentg(e):
                genrf.config(bg="#1E1E1E")

            abc=0     #control variable used to space out tkinter widgets

            for i in range(x):
                inc = i * 120
                namef = Entry(canvas2, width=20, font=m1fontStyle)
                namef.insert(END, 'Song Title')
                namef.bind('<FocusIn>', infocentn)                    #Song Name input
                namef.bind('<FocusOut>', outfocentn)
                namef.place(x=140, y=470+inc+abc)

                artf = Entry(canvas2, width=20, font=m1fontStyle)
                artf.insert(END, 'Artist')
                artf.bind('<FocusIn>', infocenta)                     #Artist input
                artf.bind('<FocusOut>', outfocenta)
                artf.place(x=140, y=510+inc+abc)

                genrf = Entry(canvas2, width=20, font=m1fontStyle)
                genrf.insert(END, 'Genre')
                genrf.bind('<FocusIn>', infocentg)                   #Genre input
                genrf.bind('<FocusOut>', outfocentg)
                genrf.place(x=140, y=550+inc+abc)

                abc+=20


                a.append(namef)
                b.append(artf)                      #appending all entry widgets into lists as it is, to be processed later
                c.append(genrf)

            button5 = canvas2.create_image(280, 640+inc, image=proceed_button_bg)
            tetx5 = canvas2.create_text(280, 640+inc, text="Submit", font=bfontStyle)
            canvas2.tag_bind(button5, "<1>", button_process)     #linked to button process function
            canvas2.tag_bind(tetx5, "<1>", button_process)


        canvas2.create_text(290, 240, text="To help us figure out your tastes", font=m1fontStyle)
        canvas2.create_text(290, 260, text="we need to know the songs you listen to!", font=m1fontStyle)    #User Info
        canvas2.create_text(290, 290, text="How many songs do you want us", font=m1fontStyle)
        canvas2.create_text(290, 310, text="to use to recommend?", font=m1fontStyle)

        r1 = tkm.Radiobutton(canvas2, text='1', value=1,
                             variable=var, indicatoron=0, padx=20, selectcolor="#232323")          #using tkmacosx package to render radio buttons to accept input
        r2 = tkm.Radiobutton(canvas2, text='2', value=2,
                             variable=var, indicatoron=0, padx=20, selectcolor="#232323")
        r3 = tkm.Radiobutton(canvas2, text='3', value=3,
                             variable=var, indicatoron=0, padx=20, selectcolor="#232323")

        r1.place(x=251, y=325)     #placing the radio button widget to be displayed
        r2.place(x=250, y=350)
        r3.place(x=250, y=375)

        button4 = canvas2.create_image(280, 440, image=proceed_button_bg)     #custom button background texture
        tetx4 = canvas2.create_text(280, 440, text="Submit", font=bfontStyle)     #custom button
        canvas2.tag_bind(button4, "<1>", usrn)          #binding left mouse click to User input function
        canvas2.tag_bind(tetx4, "<1>", usrn)




def bt1fi(e):     #button 1 focus in function, used to break the program execution for a set amount of time to ease processing requirements
    def d1():
        def d3():
            canvas1.create_image(462, 817, image=loadpillv3)
            print("debug 4")
            canvas1.itemconfig(dp1, text="Loading........")
            canvas1.after(500, songinp)     #linked to song input function

        def d2():
            canvas1.create_image(477, 829, image=loadpillv2)
            print("debug 3")
            canvas1.after(1000, d3)
            canvas1.itemconfig(dp1, text="Loading....")

        canvas1.create_image(498, 850, image=loadpillv1)
        print("debug 2")
        dp1 = canvas1.create_text(494, 890, text="Loading........", font=mfontStyle)

        canvas1.after(1000, d2)
    print("debug layer 1")
    canvas1.after(1000, d1)     #after function of tkinter used to delay the execution of the given block


root.geometry("562x900")                                      #defining root widget dimensions

hfontStyle = tkFont.Font(family="Stretch Pro", size=35)
mfontStyle = tkFont.Font(family="Questrial", size=10)         #defining Custom Font styles
m1fontStyle = tkFont.Font(family="Questrial", size=25)
bfontStyle = tkFont.Font(family="NCS Radhiumz", size=18)

bg = PhotoImage(file = "FT2bg.png")
logofile = PhotoImage(file="ftlogo2s.png")
btbgrnd = PhotoImage(file="FT2bg.png")
importstart = Image.open("get_started_wt.png")
img_fil = importstart.resize((192, 192))  # (width,height)
proceed_button_bg = ImageTk.PhotoImage(img_fil)
importstartbw = Image.open("greyedbutton.png")      #importing and processing all required Textures
img_fil1 = importstartbw.resize((192, 192))  # (width,height)
greyed_button = ImageTk.PhotoImage(img_fil1)
importstat = Image.open("genre_button_bg.png")
img_fill = importstat.resize((256, 256))  # (width,height)
genre_button_bg = ImageTk.PhotoImage(img_fill)
importss = Image.open("artist_button_bg.png")
img_filll = importss.resize((256, 256))  # (width,height)
artist_button_bg = ImageTk.PhotoImage(img_filll)


loadpill_imp = Image.open("loadpill.png")
loadpill_ver1 = loadpill_imp.resize((96, 96))
loadpill_ver2 = loadpill_imp.resize((68, 68))
loadpill_ver3 = loadpill_imp.resize((34, 34))                                                           #importing and processing all required textures for loading animations
loadpillv1 = ImageTk.PhotoImage(loadpill_ver1)
loadpillv2 = ImageTk.PhotoImage(loadpill_ver2)
loadpillv3 = ImageTk.PhotoImage(loadpill_ver3)

canvas1 = Canvas( root, width=562,height=900)
canvas1.pack(fill = "both", expand = True)                                                              #creating base canvas for rendering
canvas1.create_image( 0, 0, image = bg, anchor = "nw")
width = canvas1.winfo_screenwidth()
sw = width / 2


print(width)          #debug for output display

canvas1.create_image( 200, 345, image=logofile, anchor = "nw")
canvas1.create_text( 295, 440, text = "FindTune.", font=hfontStyle)                                     #branding and basic formatting
canvas1.create_text( 243, 460, text = "Fine-Tune your music selection.", font=mfontStyle)
canvas1.create_text( 558, 4, text = "v5", font=mfontStyle, anchor='ne')


cur.execute("create table if not exists usr_input(Title varchar(40) NOT NULL PRIMARY KEY, Artist varchar(40), Genre varchar(40))")  #creating user input table to append values to

button1 = canvas1.create_image(280, 780, image=proceed_button_bg)                       #custom button background texture
tetx1 = canvas1.create_text( 280, 780, text = "Get Started", font=bfontStyle)           #Creating Buttons
canvas1.tag_bind(button1, "<1>", bt1fi)     #binding mouse click to loading function
canvas1.tag_bind(tetx1, "<1>", bt1fi)       #binding mouse click to loading function



root.mainloop()       #executing tkinter loop
mycon.close()         #closing MySQL connection

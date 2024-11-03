import tkinter as tk
from PIL import Image , ImageTk
from tkinter import messagebox
import sqlite3 as sql
import re
import json
#----------
#----------
#نشست يا عدم نشست کاربر
session = ""

#(هنگامي که علامت + زده ميشه يک واحد به اين اضاقه ميشه (مجموع غذاهاي افزوده شده
xx = 0

#مبلغ کل غذاها
total_amount = 0
#-------------------------------win foods----------------------------------
#--------------------------------------------------------------------------
lst=["pizza","hamburger","hot dog","felafel","potato","samosa","buttemilk","soft drink"]
dct_number_foods = dict.fromkeys(lst,0)
#----------
#----------
#تابعي براي افزودن امتياز
def add_grade(dct_grades):
    user = session
    try :
        with open ("grade.json" , "w") as f :
            dct_grades[user][0] += 1
            json.dump(dct_grades , f)
        lbl_grade.config(text=f"{dct_grades[user][0]} : امتياز")
    except :
        messagebox.showinfo("" , "! يه مشکلي در فايل جيسون رخ داده است")
#----------
#----------
#بررسي وجود آيدي غذا و آيدي کاربر در ديتابيس
def check_exist(_id_user , _id_food):
    bank_data = sql.connect("bank data.db")
    c = bank_data.cursor()
    c.execute(f''' SELECT * FROM basket_buy
                    WHERE id_user={_id_user} AND id_food={_id_food} ''')
    if not c.fetchall():
        return False
    else:
        return True
#----------
#----------
#تابعي براي افزودن به سبد خريد
def add_to_basked():
    bank_data = sql.connect("bank data.db")
    c = bank_data.cursor()
    
    user = session
    c.execute(f''' SELECT id FROM info_users WHERE user_name="{user}" ''')
    _id_user = c.fetchall()[0][0]

    #افزودن و آپديت کردن سبد خريد
    for name_food , count in dct_number_foods.items():
        if count != 0 :
            c.execute(f''' SELECT id FROM info_foods WHERE food="{name_food}" ''')
            _id_food = c.fetchall()[0][0]

            if not check_exist(_id_user , _id_food):
                c.execute(f''' INSERT INTO basket_buy (id_food , id_user , number_buy)
                            VALUES({_id_food} , {_id_user} , {count})''')        
                bank_data.commit()
            else:
                c.execute(f'''UPDATE basket_buy SET number_buy = {count}
                            WHERE id_user={_id_user} AND id_food={_id_food}''')
                bank_data.commit()
#----------
#----------
#تابعي براي انجام دادن خريد
def do_buy():    
    global total_amount
    global xx
    global dct_number_foods
    user = session
    #----------
    #کم کردن موجودي از فايل جيسون
    try :
        with open ("grade.json" , "r") as f :
            dct_grades = json.load(f)
        #----------
        #...اگر موجودي بيشتر يا مساوي با هزينه پرداختي باشد
        if dct_grades[user][1] >= total_amount :
            win_factor.destroy()
            add_grade(dct_grades)
            add_to_basked()
            aa = dct_grades[user][1] - total_amount
            dct_grades[user][1] = aa
            
            with open ("grade.json" , "w") as f :
                json.dump(dct_grades , f)
            
            lbl_credit.config(text = f"{aa} : موجودي")        
            messagebox.showinfo("" , "!سفارش شما ثبت شد")

            lst_lbl = [lbl_number_1,
                       lbl_number_2,
                       lbl_number_3,
                       lbl_number_4,
                       lbl_number_5,
                       lbl_number_6,
                       lbl_number_7,
                       lbl_number_8]
            #----------
            #ايجاد حلقه براي صفر کردن تعداد خريد
            for lbl_number in lst_lbl:
                lbl_number.config(text="0")
                
            btn_buy.config(state="disabled")

            #----------
            #صفر کردن ديکشنري تعداد غذاها
            dct_number_foods = dict.fromkeys(lst,0)

            #----------
            #صفر کردن کل هزينه پرداختي
            total_amount = 0

            #----------
            #صفر کردن کل تعداد غذاها
            xx = 0

            if dct_grades[user][0] >= 10 :
                btn_buy_free.config(state="active")
                    
        else :
            win_factor.destroy()
            messagebox.showinfo("" , "! موجودي شما کافي نيست")
            
    except :
        messagebox.showinfo("" , "! يه مشکلي در فايل جيسون رخ داده است")        
#----------
#----------
#ايجاد پنجره فاکتور براي دکمه خريد
def win_factor():
    global win_factor
    win_factor = tk.Toplevel()
    win_factor.title("factor window")
    win_factor.geometry("400x500")

    bank_data = sql.connect("bank data.db")
    c = bank_data.cursor()
    
    #----------
    #مکان عرضي ليبل
    yy = 0

    #----------
    #مجموع هزينه پرداختي
    tt = 0
    #----------
    
    for namefood in dct_number_foods :
        #تعداد غذاي ذخيره شده
        bb = dct_number_foods[namefood]
        if bb > 0 :
            yy += 30
            c.execute(f''' SELECT price FROM info_foods WHERE food = "{namefood}" ''')
            price_food = c.fetchall()[0][0]            
            xb = bb * price_food
            tt += xb
            lbl_name_number_price = tk.Label(win_factor ,
text =f"نام غذا = {namefood} , تعداد = {bb} , قيمت تکي = {price_food} , مجموع = {xb}")
            lbl_name_number_price.place(x=20 , y=yy)

    yy += 30
    lbl_line = tk.Label(win_factor , text = "-------------------------")
    lbl_line.place(x=20 , y=yy)

    yy += 30
    lbl_total = tk.Label(win_factor , text = f"جمع کل : {tt}")
    lbl_total.place(x=20 , y=yy)
    
    btn_agree = tk.Button(win_factor ,
                          text = "تاييد و ثبت سفارش" ,
                          bg="green" , fg="white" ,
                          width=15, height=2 ,
                          font = ("",12) ,
                          command=do_buy)
    btn_agree.place(x=120 , y=440)
#----------
#----------    
#زماني که دکمه + زده ميشه اين تابع اجرا ميشه    
def add_food(namefood , lbl_number_food):
    global dct_number_foods
    global xx
    global total_amount
    dct_number_foods[namefood] += 1
    lbl_number_food.config(text=dct_number_foods[namefood])
    
    #----------
    #يک واحد به مجموع غذاهاي انتخاب شده افزوده ميشه
    xx += 1
    #----------
    
    btn_buy.config(state="active")

    bank_data = sql.connect("bank data.db")
    c = bank_data.cursor()
    c.execute(f''' SELECT price FROM info_foods WHERE food = "{namefood}" ''')
    total_amount += c.fetchall()[0][0]
#----------
#----------    
#زماني که دکمه - زده ميشه اين تابع اجرا ميشه    
def sub_food(namefood , lbl_number_food):
    global dct_number_foods
    global xx
    global total_amount
    if dct_number_foods[namefood] != 0 :
        dct_number_foods[namefood] -= 1
        lbl_number_food.config(text=dct_number_foods[namefood])
        
        #----------
        #يک واحد از مجموع غذاهاي انتخاب شده کم ميشه
        xx -= 1
        #----------
        
        bank_data = sql.connect("bank data.db")
        c = bank_data.cursor()
        c.execute(f''' SELECT price FROM info_foods WHERE food = "{namefood}" ''')
        total_amount -= c.fetchall()[0][0]
    
    if xx == 0 :
        btn_buy.config(state="disabled")
#----------
#----------
#تابعي براي افزايش موجودي
def increase_money():
    user = session
    money=input_amount.get()

    if not money.strip():
        lbl_m.config(text="! فيلد خالي مجاز نميباشد" , fg="red")
        return
    #----------
    #افزايش موجودي در فايل جيسون
    try :
        with open ("grade.json" , "r") as f :
            dct_grades = json.load(f)        
        with open ("grade.json" , "w") as f :
            dct_grades[user][1] += int(money)
            json.dump(dct_grades , f)
        lbl_credit.config(text=f"{dct_grades[user][1]} : موجودي")
        lbl_m.config(text="! موجودي شما افزايش يافت" , fg="green")
        
    except :
        messagebox.showinfo("" , "! يه مشکلي در فايل جيسون رخ داده است")
#----------
#----------
#ايجاد پنجره افزايش موجودي
def win_increase_credit():
    global lbl_m
    global input_amount
    win_charge = tk.Toplevel(win_foods)
    win_charge.title("Increase credit window")
    win_charge.geometry("200x160")

    lbl_txt=tk.Label(win_charge , text=": مبلغ مورد نظر را وارد نماييد")
    lbl_txt.pack(pady=10)

    input_amount=tk.Entry(win_charge , width=20)
    input_amount.pack()

    lbl_m=tk.Label(win_charge , text="")
    lbl_m.pack(pady = 10)

    btn_ok = tk.Button(win_charge,
                       text="تاييد",
                       bg="green",
                       fg="white",
                       command=increase_money)
    btn_ok.pack()
#----------
#----------
#انجام دادن خريد رايگان
def do_buy_free():
    global dct_number_foods
    global total_amount
    global xx
    user = session
    #----------
    #ثبت امتياز
    try :
        with open ("grade.json" , "r") as f :
            dct_grades = json.load(f)
        #aa = کم کردن 10 امتياز از مجموع امتياز ها
        aa = dct_grades[user][0] - 10
        lbl_grade.config(text=f"{aa} : امتياز")
        with open ("grade.json" , "w") as f :
            dct_grades[user][0] = aa
            json.dump(dct_grades , f)
        messagebox.showinfo("" , "!سفارش شما ثبت شد")

        lst_lbl = [lbl_number_1,
                   lbl_number_2,
                   lbl_number_3,
                   lbl_number_4,
                   lbl_number_5,
                   lbl_number_6,
                   lbl_number_7,
                   lbl_number_8]
        #----------
        #ايجاد حلقه براي صفر کردن تعداد خريد
        for lbl_number in lst_lbl:
            lbl_number.config(text="0")
            
        if aa < 10 :        
            btn_buy_free.config(state="disabled")
        btn_buy.config(state="disabled")
        #----------
        #صفر کردن ديکشنري تعداد غذاها
        dct_number_foods = dict.fromkeys(lst,0)
        #----------
        #صفر کردن کل هزينه پرداختي
        total_amount = 0

        #----------
        #صفر کردن کل تعداد غذاها
        xx = 0
        
    except :
        messagebox.showinfo("" , "! يه مشکلي در فايل جيسون رخ داده است")

#----------
#----------
#ايجاد پنجره فاکتور براي دکمه خريد رايگان
def win_factor_free():
    global win_factor_free
    win_factor_free = tk.Toplevel()
    win_factor_free.title("factor window")
    win_factor_free.geometry("400x500")

    bank_data = sql.connect("bank data.db")
    c = bank_data.cursor()
    #----------
    #مکان عرضي ليبل
    yy = 0
    #----------
    #ايجاد حلقه براي شمارش تعداد نوع غذا
    count = 0
    for namefood in dct_number_foods :
        bb = dct_number_foods[namefood]
        if bb >= 1 :
            count += 1
    #----------        
    #ايجاد حلقه براي اينکه اگر کاربر بيش از يک غذا انتخاب کرد        
    #يه پيغام نمايش دهد            
    for namefood in dct_number_foods :
        bb = dct_number_foods[namefood]
        if bb > 1 :
            win_factor_free.destroy()
            messagebox.showinfo("" , "! هر ده امتياز فقط يک غذاي رايگان")
            return
    #----------
    #ايجاد حلقه براي نمايش ليبل    
    for namefood in dct_number_foods :
        bb = dct_number_foods[namefood]
        if bb == 1 and count == 1 :            
            yy += 30
            c.execute(f''' SELECT price FROM info_foods WHERE food = "{namefood}" ''')
            price_food = c.fetchall()[0][0]            
            lbl_name_number_price = tk.Label(win_factor_free ,
    text =f"نام غذا = {namefood} , تعداد = {bb} , قيمت تکي = {price_food}")
            lbl_name_number_price.place(x=20 , y=yy)

            
            yy += 30
            lbl_line = tk.Label(win_factor_free , text = "-------------------------")
            lbl_line.place(x=20 , y=yy)

            yy += 30
            lbl_total = tk.Label(win_factor_free , text = "جمع کل : رايگان")
            lbl_total.place(x=20 , y=yy)
            
            btn_agree = tk.Button(win_factor_free ,
                                  text = "تاييد و ثبت سفارش" ,
                                  bg="green" , fg="white" ,
                                  width=15, height=2 ,
                                  font = ("",12) ,
                                  command=do_buy_free)
            btn_agree.place(x=120 , y=440)
            return
    #----------
    #اگر مجموع غذاهاي انتخاب شده صفر باشد
    if count == 0 :
        win_factor_free.destroy()
        messagebox.showinfo("" , "! شما غذايي انتخاب نکرده ايد")
        return
    
    win_factor_free.destroy()
    messagebox.showinfo("" , "! هر ده امتياز فقط يک غذاي رايگان")        
#----------
#----------
#ايجاد پنجره سفارش غذا
def win_food():
    user = session
    global photo3
    global photo4
    global lbl_grade
    global win_foods
    global lbl_credit
    global btn_buy
    global btn_buy_free
    global lbl_number_1
    global lbl_number_2
    global lbl_number_3
    global lbl_number_4
    global lbl_number_5
    global lbl_number_6
    global lbl_number_7
    global lbl_number_8
    #----------
    #افزودن نام و موجودي و امتياز کاربر به فايل جيسون
    #در صورت عدم وجود نام کاربر
    try :
        with open ("grade.json" , "r") as f :
            dct_grades = json.load(f)
        if user not in dct_grades :
            dct_grades[user] = [0,0]
            with open ("grade.json" , "w") as f :
                json.dump(dct_grades , f)                
    except :
        messagebox.showinfo("" , "! يه مشکلي در فايل جيسون رخ داده است")
    #----------
    #----------    
    #تابعي براي خارج شدن از حساب کاربري
    def exit_account():
        if messagebox.askyesno("" , "آيا ميخواهيد از حساب کاربري خارج شويد ؟؟"):
            win_foods.destroy()
            win_root()
    root.destroy()

    win_foods = tk.Tk()
    win_foods.title("Signup window")
    win_foods.geometry("1200x650")
    #----------Insert picture background
    uploaded_image = Image.open("slide1.jpg")
    photo3 = ImageTk.PhotoImage(uploaded_image.resize((1200,650)))
    lbl_image_bg = tk.Label(win_foods , image=photo3)
    lbl_image_bg.place(relwidth = 1 , relheight = 1)
    #----------Insert picture menu
    uploaded_image_menu = Image.open("menu.jpg")
    photo4 = ImageTk.PhotoImage(uploaded_image_menu.resize((350,500)))
    lbl_image_menu = tk.Label(win_foods , image=photo4)
    lbl_image_menu.place(x=100 , y=80)
    #----------Label credit (موجودي)
    lbl_credit = tk.Label(win_foods ,
                          text=f"{dct_grades[user][1]} : موجودي" ,
                          bg="blue" , fg="white" ,
                          width=15, height=2 ,
                          font = ("",15))
    lbl_credit.place(x=480 , y=80)
    #----------Label grade
    #امتياز
    lbl_grade = tk.Label(win_foods ,
                          text=f"{dct_grades[user][0]} : امتياز" ,
                          bg="blue" , fg="white" ,
                          width=15, height=2 ,
                          font = ("",15))
    lbl_grade.place(x=480 , y=150)
    #----------Label welcome
    lbl_welcome = tk.Label(text=f"{user} سلام" , font = ("",15))
    lbl_welcome.place(x=10 , y=20)
    #----------Label charge
    btn_charge = tk.Button(win_foods ,
                           text="شارژ حساب" ,
                           bg="green" , fg="white",
                           width=15, height=2 ,
                           font = ("",15) ,
                           command=win_increase_credit)
    btn_charge.place(x=480 , y=220)
    #----------Button exit
    btn_exit = tk.Button(win_foods ,
                           text="خروج از حساب کاربري" ,
                           bg="red" , fg="white",
                           width=15, height=2 ,
                           font = ("",15),
                           command=exit_account)
    btn_exit.place(x=480 , y=300)

    #----------Button buy
    btn_buy = tk.Button(win_foods ,
                           text="خريد" ,
                           bg="green" , fg="white",
                           width=15, height=1 ,
                           font = ("",15),
                           command=win_factor ,
                           state="disabled")
    btn_buy.place(x=280 , y=590)
    #----------Button buy free
    btn_buy_free = tk.Button(win_foods ,
                           text="خريد رايگان" ,
                           bg="black" , fg="white",
                           width=15, height=1 ,
                           font = ("",15),
                           state = "disabled" ,
                           command=win_factor_free)
    btn_buy_free.place(x=100 , y=590)
    #اگر امتياز بيشتر يا مساوي با ده بود دکمه خريد رايگان فعال شود
    if dct_grades[user][0] >= 10 :
        btn_buy_free.config(state="active")
    #----------Frame positive (+)
    frame_number_p = tk.Frame(win_foods , bg="gray" , width=20 , height=505)
    frame_number_p.pack_propagate(False)
    frame_number_p.place(x=80 , y=80)
    #----------Frame negative (-)
    frame_number_n = tk.Frame(win_foods , bg="gray" , width=20 , height=505)
    frame_number_n.pack_propagate(False)
    frame_number_n.place(x=5 , y=80)
    #----------Frame number buy
    frame_number_buy = tk.Frame(win_foods , bg="gray" , width=53 , height=505)
    frame_number_buy.pack_propagate(False)
    frame_number_buy.place(x=26 , y=80)
    #----------Buttons positive (+)
    #p = +
    btn_p_1 = tk.Button(frame_number_p ,text="+" , bg="green" ,
                        fg="white",font = ("",10),
                        command=lambda:add_food("pizza",lbl_number_1))
    btn_p_1.pack(anchor = "e" , pady = 33)
    btn_p_2 = tk.Button(frame_number_p , text="+" , bg="green"
                        , fg="white",font = ("",10),
                        command=lambda:add_food("hamburger",lbl_number_2))
    btn_p_2.pack(anchor = "e")
    btn_p_3 = tk.Button(frame_number_p , text="+" , bg="green" ,
                        fg="white",font = ("",10),
                        command=lambda:add_food("hot dog",lbl_number_3))
    btn_p_3.pack(anchor = "e" , pady = 32)
    btn_p_4 = tk.Button(frame_number_p , text="+" , bg="green" ,
                        fg="white",font = ("",10),
                        command=lambda:add_food("felafel",lbl_number_4))
    btn_p_4.pack(anchor = "e")
    btn_p_5 = tk.Button(frame_number_p , text="+" , bg="green" ,
                        fg="white",font = ("",10),
                        command=lambda:add_food("potato",lbl_number_5))
    btn_p_5.pack(anchor = "e" , pady = 32)
    btn_p_6 = tk.Button(frame_number_p , text="+" , bg="green" ,
                        fg="white",font = ("",10),
                        command=lambda:add_food("samosa",lbl_number_6))
    btn_p_6.pack(anchor = "e")
    btn_p_7 = tk.Button(frame_number_p , text="+" , bg="green" ,
                        fg="white",font = ("",10),
                        command=lambda:add_food("buttemilk",lbl_number_7))
    btn_p_7.pack(anchor = "e" , pady = 32)
    btn_p_8 = tk.Button(frame_number_p , text="+" , bg="green" ,
                        fg="white",font = ("",10),
                        command=lambda:add_food("soft drink",lbl_number_8))
    btn_p_8.pack(anchor = "e")
    #----------Buttons negative (-)
    #n = -
    btn_n_1 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("pizza",lbl_number_1))
    btn_n_1.pack(anchor = "w" , pady = 33)
    btn_n_2 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("hamburger",lbl_number_2))
    btn_n_2.pack(anchor = "w")
    btn_n_3 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("hot dog",lbl_number_3))
    btn_n_3.pack(anchor = "w" , pady = 32)
    btn_n_4 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("felafel",lbl_number_4))
    btn_n_4.pack(anchor = "w")
    btn_n_5 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("potato",lbl_number_5))
    btn_n_5.pack(anchor = "w" , pady = 32)
    btn_n_6 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("samosa",lbl_number_6))
    btn_n_6.pack(anchor = "w")
    btn_n_7 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("buttemilk",lbl_number_7))
    btn_n_7.pack(anchor = "w" , pady = 32)
    btn_n_8 = tk.Button(frame_number_n , text="--" , bg="red" ,
                        fg="white",font = ("",10),
                        command=lambda:sub_food("soft drink",lbl_number_8))
    btn_n_8.pack(anchor = "w")
    #----------Buttons number buy
    #number buy = تعداد خريد
    lbl_number_1 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_1.place(x=20 , y=35)
    lbl_number_2 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_2.place(x=20 , y=95)
    lbl_number_3 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_3.place(x=20 , y=155)
    lbl_number_4 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_4.place(x=20 , y=215)
    lbl_number_5 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_5.place(x=20 , y=275)
    lbl_number_6 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_6.place(x=20 , y=335)
    lbl_number_7 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_7.place(x=20 , y=395)
    lbl_number_8 = tk.Label(frame_number_buy , text="0" , bg="white" , fg="black",font = ("",10))
    lbl_number_8.place(x=20 , y=455)    
    #----------
    
    root.mainloop()
#-------------------------------win signup---------------------------------
#--------------------------------------------------------------------------
def win_signup():
    bank_data = sql.connect("bank data.db")
    c = bank_data.cursor()
    #----------
    #----------
    #تابعي براي افزودن نام و پسورد به ديتابيس    
    def add_to_database(user,pas):
        try:
            c.execute(f'''INSERT INTO info_users (user_name,password)
                        VALUES ("{user}","{pas}")''')
            bank_data.commit()
            return True
        except:
            return False
    #----------
    #----------
    #بررسي وجود نام تکراري در ديتابيس    
    def check_user(user):
        c.execute(f'''SELECT * FROM info_users WHERE user_name="{user}" ''')                
        if len(c.fetchall())<1:
            return False
        else:
            return True
    #----------
    #----------
    #تابعي براي بررسي شروط ثبت نام
    def signup_validate(user,pas,cpas):
        if not user.strip() or not pas.strip() or not cpas.strip() :
            return False,'! فيلد خالي مجاز نمي باشد'
        if pas!=cpas:
            return False,'! پسورد ها يکسان نيستند'
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', pas):
            return False,''' پسورد بايد حداقل 8 کاراکتر
حداقل يک حرف بزرگ و يک حرف کوچک
و حداقل يک عدد باشد'''
        if check_user(user):
            return False,'! اين نام از قبل وجود دارد'
        return  True,''
    #----------
    #----------
    #تابعي براي انجام دادن ثبت نام
    def do_sumbit():                    
        user = input_user.get()
        pas = input_pas.get()
        cpas = input_cpas.get()

        result,error_msg = signup_validate(user,pas,cpas)
        if not result :
            lbl_msg2.config(text=error_msg,fg='red')
            return
        
        result = add_to_database(user,pas)
        if not result :
            lbl_msg2.config(text="! مشکلي در ذخيره اطلاعات رخ داده است",fg='red')
            return
        lbl_msg2.configure(text="! ثبت نام با موفقيت انجام شد",fg='green')
        input_user.delete(0,'end')
        input_pas.delete(0, 'end')
        input_cpas.delete(0, 'end')
    #----------
    #----------
    #ايجاد پنجره ثبت نام
    global photo2
    win_signup = tk.Toplevel(root)
    win_signup.title("Signup window")
    win_signup.geometry("450x300")
    #----------Insert picture background
    uploaded_image = Image.open("slide3.jpg")
    photo2 = ImageTk.PhotoImage(uploaded_image.resize((450,300)))
    lbl_image = tk.Label(win_signup , image=photo2)
    lbl_image.place(relwidth = 1 , relheight = 1)
    #----------Make frame
    frame_signup = tk.Frame(win_signup , bg = "lightgray",width=200, height=270)
    frame_signup.pack_propagate(False)
    frame_signup.place(x=100 , y=20)
    #----------Label username
    lbl_user=tk.Label(frame_signup,text='Username :' , bg = "lightgray")
    lbl_user.pack(pady=5)
    #----------Entry username
    input_user=tk.Entry(frame_signup)
    input_user.pack(pady=5)
    #----------Label password
    lbl_pas=tk.Label(frame_signup,text='Password :' , bg = "lightgray")
    lbl_pas.pack(pady=5)
    #----------Entry password
    input_pas=tk.Entry(frame_signup)
    input_pas.pack(pady=5)
    #----------Label Password confirmation
    lbl_cpas=tk.Label(frame_signup,text='Password confirmation :' , bg = "lightgray")
    lbl_cpas.pack(pady=5)
    #----------Entry password confirmation
    input_cpas=tk.Entry(frame_signup)
    input_cpas.pack(pady=5)
    #----------Label message
    lbl_msg2=tk.Label(frame_signup,text='',bg="lightgray")
    lbl_msg2.pack()
    #----------Button login
    btn_ok=tk.Button(frame_signup,text='Ok',command=do_sumbit)
    btn_ok.pack(pady=5)
    #----------

    root.mainloop()

#----------------------------------ROOT------------------------------------
#--------------------------------------------------------------------------
#بررسي وجود اطلاعات در ديتابيس
def check_exist_info(user,pas):
    bank_data = sql.connect("bank data.db")
    c = bank_data.cursor()
    c.execute(f'''SELECT * FROM info_users
                WHERE user_name="{user}" AND password="{pas}" ''')
    if not c.fetchall():
        return False
    else :
        return True
#----------
#----------
#انجام دادن لاگين
def do_login():
    global session
    user = input_user.get()
    pas = input_pas.get()
    #بررسي خالي بودن فيلد ها
    if not user.strip() or not pas.strip():
        lbl_msg1.config(text="!! فيلد خالي مجاز نمي باشد",fg='red')
        return
    #چک کردن اطلاعات کاربر ، در صورت وجود ، وارد پنجره جديد ميشود
    if not check_exist_info(user,pas):
        lbl_msg1.config(text="!! نام کاربري يا رمز عبور اشتباه است",fg='red')
    else :
        session = user
        win_food()
#----------
#----------
#ايجاد پنجره اصلي
def win_root():
    global input_user
    global input_pas
    global lbl_msg1
    global root
    
    root = tk.Tk()
    root.title("Fast food")
    root.geometry("1200x650")
    #----------Insert picture background
    uploaded_image = Image.open("slide2.jpg")
    photo1 = ImageTk.PhotoImage(uploaded_image.resize((1200,650)))
    lbl_image = tk.Label(root , image=photo1)
    lbl_image.place(relwidth = 1 , relheight = 1)
    #----------Make frame
    frame_root = tk.Frame(root , bg = "lightgray" ,width=200, height=300)
    frame_root.pack_propagate(False)
    frame_root.place(x=920 , y=300)
    #----------Label username
    lbl_user=tk.Label(frame_root,text='Username :' , bg = "lightgray")
    lbl_user.pack(pady=5)
    #----------Entry username
    input_user=tk.Entry(frame_root)
    input_user.pack(pady=5)
    #----------Label password
    lbl_pas=tk.Label(frame_root,text='Password :' , bg = "lightgray")
    lbl_pas.pack(pady=5)
    #----------Entry password
    input_pas=tk.Entry(frame_root)
    input_pas.pack(pady=5)
    #----------Label message
    lbl_msg1=tk.Label(frame_root,text='',bg="lightgray")
    lbl_msg1.pack()
    #----------Button login
    btn_login=tk.Button(frame_root,text='Login',command=do_login)
    btn_login.pack(pady=5)
    #----------Label line
    lbl_line=tk.Label(frame_root,
                        text = "----------------------------" , bg="lightgray")
    lbl_line.pack(pady=5)
    #----------Label signup
    lbl_signup=tk.Label(frame_root,text='''حساب کاربري نداريد ؟
    ثبت نام کنيد''',bg="lightgray")
    lbl_signup.pack(pady=5)
    #----------Button signup
    btn_signup=tk.Button(frame_root,text='Signup',command=win_signup)
    btn_signup.pack(pady=5)    
    #----------
    
    root.mainloop()

win_root()

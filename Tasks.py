from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
import MySQLdb
from datetime import date

def sch_tsk():
    tasks = []

    def delete_task(y):
        y['fg']="red"
        tasks.remove(y['text'])
        tasks_str = ""
        for i in tasks:
            if i == tasks[-1]:
                tasks_str+=""+str(i)+""
            else:
                tasks_str+=""+str(i)+", "
        sql1 = "update tasks set tasks='"+tasks_str+"';"
        cur.execute(sql1)
        strike(y)

    def strike(y):
        strike_Font = tkFont.Font(family="Calibri", size=12, overstrike = 1)
        y['font'] = strike_Font
    
    def add_task(count, is_db= "no"):
        
        if int(count.get())< 10:
            if is_db == "no":
                tasks.append(new_task.get())
                tasks_str = ""
                for i in tasks:
                    if i == tasks[-1]:
                        tasks_str+=""+str(i)+""
                    else:
                        tasks_str+=""+str(i)+", "
                sql1 = "update tasks set tasks='"+tasks_str+"';"
                cur.execute(sql1)

            if new_task.get()!="":
                ml1 = Label(x_fm, text = str(count.get()+1)+str("."), fg = "red", bg = "black",font = "calibri 12 bold")
                ml1.grid(row = count.get(), column = 0, padx = 0, sticky=N)
                mc1 = Button(x_fm,text = new_task.get(), wraplength=250, fg = "white", bg = "black", font = "calibri 12 bold", relief=GROOVE, bd = 0, activebackground = "black", activeforeground = "white")
                mc1.grid(row = count.get(), column = 1, sticky=W)
                mc1.bind('<Triple-Button-1>', lambda x:delete_task(mc1))
                mc1.configure(command = lambda:strike(mc1) )
                count.set(int(count.get())+1)
                ie1.delete(0, END)            
        else:
            messagebox.showerror("Alert", "Cannot Add More Notes\n Kindly Delete Some")
            
    home = Tk()
    home.title("Task Scheduler")
    home.geometry("300x465+1550+20")
    home.configure(background = "black")

    new_task = StringVar()
    count = IntVar()
    count.set(0)

    head_fm = Frame(home)
    head_fm.configure(background = "black")
    hl1 = Label(head_fm, text = "MY TASKS", fg = "red", bg = "black", font = "calibri 20 bold")
    hl1.grid(row = 0, column = 0, padx = (0, 100))
    hb1 = Button(head_fm, text = "REFRESH", fg = "black", bg = "white", font = "calibri 10 bold", width = 8, relief=GROOVE, bd = 0, activebackground = "black", activeforeground = "black")
    hb1.grid(row = 0, column = 1)
    hb1.configure(command = lambda: home.destroy() & sch_tsk())
    today = date.today().strftime("%d.%m.%Y")
    hl2 = Label(head_fm,text = "Date: "+today,  fg = "white", bg = "black", font = "calibri 15 bold ", width = 14, height = 1)
    hl2.grid(row = 1, column = 0, sticky=W)
    head_fm.pack(pady = 5)

    main_fm = Frame(home)
    main_fm.configure(background = "black", border = "2px", width = "300px", height = "250px")
    x_fm = Frame(main_fm)
    x_fm.configure(background = "black", width = "300px", height = "250px")
    
    ml1 = Label(x_fm, bg = "black", width = 35, height = 0)
    ml1.grid(row = 0, column = 1, sticky=W)
    ml2 = Label(x_fm, bg = "black", width = 2, height = 0)
    ml2.grid(row = 0, column = 0,sticky=W+E)
    x_fm.grid(row = 0, column = 0, sticky = W+E)
    main_fm.pack(pady = 5,fill=None, expand=False)

    ip_fm = Frame(home)
    ip_fm.configure(background = "black")
    ie1 = Entry(ip_fm, textvariable = new_task, width = "35")
    ie1.grid(row = 0, column = 0, padx = (2, 18))
    ib1 = Button(ip_fm, text = "ADD", fg = "black", bg = "white", font = "calibri 10 bold", width = 7, relief=GROOVE, bd = 0, activebackground = "black", activeforeground = "black")
    ib1.grid(row = 0, column = 1)
    ib1.configure(command = lambda: add_task(count))
    ip_fm.pack(pady = 5, side = BOTTOM)

    sql = "select * from tasks"
    cur.execute(sql)
    pre_tasks = cur.fetchall()
    tasks = pre_tasks[0][0].split(", ")
    if "" in tasks:
        tasks.remove("")
    if len(tasks)>0:
        for i in tasks:
            if i!="":
                new_task.set(i)
                add_task(count,"yes")
    home.resizable(0, 0)
    home.bind('<Return>', lambda x:add_task(count))        
    home.mainloop()
    

if __name__ == "__main__":
    db_conn = MySQLdb.connect(host='localhost', port=3306, user='root', password='********', db='pysql',  autocommit=True)
    print("[INFO] Database Connected")
    global cur
    cur = db_conn.cursor()
    sch_tsk()
    db_conn.close()
    print("[INFO] Database Connection Closed")

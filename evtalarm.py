from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry
from win10toast import ToastNotifier 
import threading
import time

root = Tk()
root.geometry('950x550')
root.title('Event Remainder Alarm')


class AlarmThread(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                           
        thread.start()                                  

    def run(self):
        """ Method that runs forever """
        while True:
            currentdate = str(datetime.now().strftime("%m/%d/%Y"))
            currenttime = str(datetime.now().strftime("%H:%M"))
            try:
                database = sqlite3.connect("events.db")
                cursor = database.cursor()

                eventdatetime = ("SELECT ename,msg FROM allevent WHERE edate = '%s' AND alarmt = '%s'" %(currentdate,currenttime))
                cursor.execute(eventdatetime)
                rows = cursor.fetchall()
                erows = [namemsg for t in rows for namemsg in t]
                print(erows)
                database.commit()

                updatestatus = ("UPDATE allevent set estatus = 'OVER' WHERE edate = '%s' AND alarmt = '%s'" %(currentdate,currenttime))
                cursor.execute(updatestatus)
                database.commit()
                if len(rows)>0:
                    eventname= str(erows[0])
                    eventmsg = str(erows[1])
                    n = ToastNotifier() 
                    n.show_toast("Hey Boss! Event : "+eventname , eventmsg, duration = 10, icon_path ="event.ico")
                    

                else:
                    pass
                
        
            except sqlite3.Error as error:
                messagebox.showerror(title='Error', message=error)
                print("Failed to insert data into sqlite table", error)

            finally:
                if (database):
                    database.close()
            
            time.sleep(self.interval)
            print('Check')


def showdata():
    alleventForm = Toplevel(root)
    alleventForm.title("All Event")
    alleventForm.geometry("800x550")

    try:
        database = sqlite3.connect("events.db")
        cursor = database.cursor()
        alle = "SELECT * FROM allevent ORDER BY edate,alarmt"
        cursor.execute(alle)
        rows = cursor.fetchall()
        database.commit()
    
    except sqlite3.Error as error:
        messagebox.showerror(title='Error', message=error)
                #  print("Failed to insert data into sqlite table", error)

    finally:
        if (database):
            database.close()
            # print("The SQLite connection is closed")


    tv = ttk.Treeview(alleventForm, columns=(1,2,3,4,5,6,7), show="headings", height="50")
    tv.pack()

    tv.heading(1, text="Name")
    tv.heading(2, text="Date")
    tv.heading(3, text="Type")
    tv.heading(4, text="Message")
    tv.heading(5, text="Alarm")
    tv.heading(6, text="Mobile")
    tv.heading(7, text="Status")

    for i in rows:
        tv.insert("", "end", values=i)


def comingdata():
    comingForm = Toplevel(root)
    comingForm.title("Coming Events")
    comingForm.geometry("800x500")

    try:
        database = sqlite3.connect("events.db")
        cursor = database.cursor()
        alle = "SELECT * FROM allevent WHERE estatus = 'active' ORDER BY edate,alarmt LIMIT 5"
        cursor.execute(alle)
        rows = cursor.fetchall()
        database.commit()
        
    except sqlite3.Error as error:
        messagebox.showerror(title='Error', message=error)
                #  print("Failed to insert data into sqlite table", error)

    finally:
        if (database):
            database.close()
            # print("The SQLite connection is closed")



    tv = ttk.Treeview(comingForm, columns=(1,2,3,4,5,6), show="headings", height="50")
    tv.pack()

    tv.heading(1, text="Name")
    tv.heading(2, text="Date")
    tv.heading(3, text="Type")
    tv.heading(4, text="Message")
    tv.heading(5, text="Alarm")
    tv.heading(6, text="Mobile")

    for i in rows:
        tv.insert("", "end", values=i)


def deletedata():
    enamess = eventname.get().split(',')
    try:
        database = sqlite3.connect("events.db")
        cursor = database.cursor()
        if eventname.get() == 'DELETEALLDATA':
            deletedata = ("DELETE FROM allevent")
            cursor.execute(deletedata)
            database.commit()

        elif enamess != None:
            for i in enamess:
                deletedata = ("DELETE FROM allevent WHERE ename = '%s'" %(i))
                cursor.execute(deletedata)
                database.commit()
        else:
            messagebox.info(title='Error',message='Enter Right Event First')

    except sqlite3.Error as error:
        messagebox.showerror(title='Error', message=error)
        #  print("Failed to insert data into sqlite table", error)

    finally:
        if (database):
            
            database.close()
            # print("The SQLite connection is closed")


# New Even From ---------------------------------- SUBMIT NEW EVENTS -----------------------------------------
def openNewWindow():  
    newWindow = Toplevel(root) 
    newWindow.title("NEW EVENT") 
    newWindow.geometry("550x550") 

    try:
        database = sqlite3.connect("events.db")
        cursor = database.cursor()
        create_event_sql = "CREATE TABLE IF NOT EXISTS allevent (ename TEXT, edate TEXT, etype TEXT, msg TEXT, alarmt TEXT, mobileno TEXT, estatus TEXT)"
        cursor.execute(create_event_sql)
        database.commit()

    except sqlite3.Error as error:
        messagebox.showerror(title='Error', message=error)
        #  print("Failed to insert data into sqlite table", error)

    finally:
        if (database):
            database.close()
            # print("The SQLite connection is closed")

    
    def submitEvent():
        try:
            database = sqlite3.connect("events.db")
            cursor = database.cursor()
            cursor.execute("insert into allevent values('%s','%s','%s','%s','%s','%d','%s')" %(ename.get(), str(edate.get()), etype.get(), emsg.get(), etime.get(), int(emobile.get()), 'active'))
            database.commit()
            messagebox.showinfo(title='Submit Event', message='Event submitted successfully')

        except sqlite3.Error as error:
             messagebox.showerror(title='Error', message=error)
            #  print("Failed to insert data into sqlite table", error)

        finally:
            if (database):
                database.close()
                # print("The SQLite connection is closed")

    # -----------------------------------------------------------------------
    # -------------------- Entry Variables -----------------------------------
    # --------------------------------------------------------------------------
    ename = StringVar()
    edate = StringVar()
    etype = StringVar()
    emsg = StringVar()
    etime = StringVar()
    emobile = StringVar()

    # ----------------------- All TextBox to submit a NEW EVENT ----------------------------
    # --------------------------------------------------------------------------------------
    Label(newWindow,text ="ENTER NEW EVENT", width=20, font=("bold",20)).pack() 

    Label(newWindow,text="NAME OF THE EVENT",width=20,font=("bold",10)).place(x=200,y=50)
    name_of_event = Entry(newWindow,textvariable=ename ,width=50, font=('bold',10)).place(x=100,y=75)

    Label(newWindow,text="EVENT DATE",width=20,font=("bold",10)).place(x=200,y=120)
    event_date = str(DateEntry(newWindow,textvariable=edate, date_pattern='mm/dd/y', width=50, font=('bold',10)).place(x=100,y=145))

    Label(newWindow,text="EVENT TYPE",width=20,font=("bold",10)).place(x=200,y=190)
    event_type = Entry(newWindow,textvariable=etype, width=50, font=('bold',10)).place(x=100,y=215)

    Label(newWindow,text="MESSAGE",width=20,font=("bold",10)).place(x=200,y=260)
    e_message = Entry(newWindow,textvariable=emsg, width=50, font=('bold',10)).place(x=100,y=285)
  
    Label(newWindow,text="ALARM TIME (Hour:Min) Formate",width=30,font=("bold",10)).place(x=150,y=330)
    alarm_time = Entry(newWindow,textvariable=etime, width=50, font=('bold',10)).place(x=100,y=355)

    Label(newWindow,text="MOBILE NUMBER",width=20,font=("bold",10)).place(x=200,y=400)
    mobile_no = Entry(newWindow,textvariable=emobile, width=50, font=('bold',10)).place(x=100,y=425)
  
    new_event_submit = Button(newWindow, text='SUBMIT', command=submitEvent, width=20,font=("bold",15), bg='brown', fg='white').place(x=170,y=450)
  

# Main Window Design  

# Heading
Heading = Label(root, text='Event Remind System', width=20, font=("bold",35)).pack()

#new Event Button 
new_event =Button(root, text='NEW\nEVENT',command = openNewWindow, width=12, height=5,font=("bold",25), bg='brown', fg='white').place(x=60,y=150)

#Coming Event Button
coming_event =Button(root, text="COMING\nEVENT",command=comingdata, width=12, height=5,font=("bold",25), bg='brown', fg='white').place(x=350,y=150)

#All Events Button
all_event =Button(root, text='ALL\nEVENT',command = showdata ,width=12, height=5,font=("bold",25), bg='brown', fg='white').place(x=650,y=150)

eventname = StringVar()

Label(root,text="Enter Event Name :",width=20,font=("bold",12)).place(x=20,y=435)
Label(root,text="For multipal data delete use ','",width=30,font=("bold",10)).place(x=10,y=460)
Label(root,text="For All data delete Type 'DELETEALLDATA'",width=40,font=("bold",10)).place(x=20,y=490)
ename = Entry(root,textvariable=eventname, width=35,  font=('bold',18)).place(x=230,y=445)
  
new_event_submit = Button(root, text='Delete',command= deletedata ,width=15,font=("bold",15), bg='brown', fg='white').place(x=700,y=440)

#Footer Label
footer_lable = Label(root, text='Event Remainder', width=120, bg='red', fg='white', font=("bold",10))
footer_lable.place(x=0, y=528)



example = AlarmThread()
time.sleep(2)
    
    

root.mainloop()

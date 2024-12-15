from tkinter import *
from tkinter import ttk
from plyer import notification
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import datetime
import os
import time


containerBg = "#0D0D0D" 
sidebarBg = "#1a1c1e"  
textbg = "#212121" 

class ReminderApp:
    def __init__(self, container):
        self.container = container
        self.clearFrame(self.container)

        navigationFrame = Frame(
            self.container,
            height=70,
            bg=containerBg
            )
        navigationFrame.pack(fill=X,side=TOP)
        
        self.add_icon = Image.open('icon/Add.png')
        self.add_icon = self.add_icon.resize((200,35))
        self.add_icon = ImageTk.PhotoImage(self.add_icon)
        btAdd = Button(
            navigationFrame,
            text="ADD NEW REMINDER",
            fg="white",
            font=("Times", 12, "bold"),
            compound=CENTER,
            image=self.add_icon,
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
            command=lambda: self.create_new_reminder()
        )
        btAdd.pack(side=RIGHT,padx=10,pady=10)

        lbReminder = Label(
            navigationFrame,
            text="REMINDER",
            fg="white",
            font=("Times", 20, "bold"),
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
        )
        lbReminder.pack(side=LEFT,padx=20,pady=10)

        self.treeTodayFrame_expanded = False
        self.treeTmrFrame_expanded = False
        self.treeSomedayFrame_expanded = False
        self.treeFrame_min_height = 50
        self.treeFrame_max_height = 200

        tableFrame = Frame(
            self.container,
            width=900,
            height=600,
            bg="white"
            )
        tableFrame.pack(anchor=NW)

        self.treeTodayFrame = Frame(
            tableFrame,
            height=self.treeFrame_min_height,
            width= 900,
            bg=containerBg,
            )
        self.treeTodayFrame.pack()
        self.treeTodayFrame.pack_propagate(False)

        self.btopentreeToday = Button(
            self.treeTodayFrame,
            text="Today",
            fg="white",
            font=("Arial", 20),
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
            command= lambda : self.animate_frame(window = self.container,frame=self.treeTodayFrame,max_height=self.treeFrame_max_height,min_height=self.treeFrame_min_height,frame_status=self.treeTodayFrame_expanded)
        )
        self.btopentreeToday.pack(side=TOP,anchor=NW,padx=25)

        self.treeTmrFrame = Frame(
            tableFrame,
            height=self.treeFrame_min_height,
            width= 900,
            bg="white",
            )
        self.treeTmrFrame.pack()
        self.treeTmrFrame.pack_propagate(False)

        self.btopentreeTmr = Button(
            self.treeTmrFrame,
            text="Tomorrow",
            fg="white",
            font=("Arial", 20),
            bg=containerBg,
            activebackground=containerBg,
            bd=0,
            command= lambda : self.animate_frame(window = self.container,frame=self.treeTmrFrame,max_height=self.treeFrame_max_height,min_height=self.treeFrame_min_height,frame_status=self.treeTmrFrame_expanded)
        )
        self.btopentreeTmr.pack(side=TOP,anchor=NW,padx=25)

        if not os.path.exists("Reminder_Data_Record.txt"):
            with open("Reminder_Data_Record.txt",'w') as file:
                file.write("")
        
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        self.style.configure(
            "Custom.Treeview",
            background=containerBg,      
            fieldbackground=containerBg, 
            foreground="white",          
            font=('Arial', 13)
        )

        # Style for Treeview headers
        self.style.configure(
            "Custom.Treeview.Heading",
            background=sidebarBg,   
            foreground='white',         
            font=('Arial', 14, 'bold'), 
        )
        
        self.tree = ttk.Treeview(
            self.treeTodayFrame,
            height= 10,
            style="Custom.Treeview",
            columns = ('Title', 'Description', 'Date', 'Time', 'Recurrence Type'),
            show = 'headings',
            
        )

        self.tree.heading('Title', text='Title')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Recurrence Type', text='Recurrence Type')
        
        self.tree.column('Title', anchor=CENTER, width=150)
        self.tree.column('Description', anchor=CENTER, width=150)
        self.tree.column('Date', anchor=CENTER, width=25)
        self.tree.column('Time', anchor=CENTER, width=20)
        self.tree.column('Recurrence Type', anchor=CENTER, width=150)
        self.tree.pack(fill=X, expand=True,padx=40,pady=10)
        
        #Add scrollbar and define the mouse
        self.v_scroll = ttk.Scrollbar(self.treeTodayFrame,orient=VERTICAL,command=self.tree.yview)
        self.tree.bind("<MouseWheel>", self.Mouse_Scroll)
        self.print_file()
        
    def clearFrame(self, container):
        for widget in container.winfo_children():
            widget.destroy()

    def create_new_reminder(self):
        self.window = Toplevel(self.container)
        self.window.title("Add New Reminder")
        self.window.geometry("500x600")
        self.window.configure(bg=containerBg)

        content_Frame = Frame(
            self.window,
            height=600,
            width=500,
            bg=containerBg,
        )
        content_Frame.pack(fill=BOTH)

        lbTitle = Label(
            content_Frame,
            text="TITLE:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbTitle.pack(pady=10)

        self.inputTitle = Text(
            content_Frame,
            bd=0,
            fg="white",
            font=("Times", 15),
            bg=textbg,
            width=40,
            height=2,
            insertbackground="white"
        )
        self.inputTitle.pack()

        lbDescription = Label(
            content_Frame,
            text="DESCRIPTION:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbDescription.pack(pady=10)

        self.inputDescription = Text(
            content_Frame,
            bd=0,
            fg="white",
            font=("Times", 15),
            bg=textbg,
            width=40,
            height=2,
            insertbackground="white"
        )
        self.inputDescription.pack()

        self.setTimeFrame_expanded = False
        self.setTimeFrame_min_height = 50
        self.setTimeFrame_max_height = 350

        self.setTimeFrame = Frame(
            self.window,
            height=self.setTimeFrame_min_height,
            bg=containerBg,
        )
        self.setTimeFrame.pack(fill=X)
        self.setTimeFrame.pack_propagate(FALSE)

        self.isCheckboxTick = IntVar()
        setTimeCheckbox = Checkbutton(
            self.setTimeFrame,
            text="Set Time",
            font=("Times", 20),
            fg="white",
            command=lambda: self.animate_frame(window = self.window, frame=self.setTimeFrame,max_height=self.setTimeFrame_max_height,min_height = self.setTimeFrame_min_height,frame_status =self.setTimeFrame_expanded),
            bg=containerBg,
            activebackground=containerBg,
            selectcolor="black",
            variable=self.isCheckboxTick,
            onvalue=1,
            offvalue=0
        )
        setTimeCheckbox.pack()

        lbDate = Label(
            self.setTimeFrame,
            text="DATE:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbDate.pack(pady=10)

        self.date_var = StringVar()
        self.date_entry = DateEntry(
            self.setTimeFrame, 
            width=30,
            font=("Times", 10),
            textvariable=self.date_var, 
            date_pattern='dd/MM/yyyy',
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black",
            othermonthwebackground="white"
        )
        self.date_entry.pack()

        lbTime = Label(
            self.setTimeFrame,
            text="TIME:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbTime.pack(pady=10)

        self.time_picker = SpinTimePickerModern(self.setTimeFrame)
        self.time_picker.addAll(constants.HOURS12, ["{:02d}".format(i) for i in range(60)])
        self.time_picker.configureAll(
            bg="#212121",         
            height=1, 
            fg="#ffffff",          
            font=("Times", 16), 
            hoverbg="#2e2d2d",     
            hovercolor="#ffffff",  
            clickedbg="#404040",   
            clickedcolor="#d73333",
        )
        self.time_picker.configure_separator(bg="#212121", fg="#ffffff")
        self.time_picker.pack()

        lbRecurring = Label(
            self.setTimeFrame,
            text="RECURRING:",
            font=("Times", 15),
            fg="white",
            bg=containerBg
        )
        lbRecurring.pack(pady=10)

        self.recurrence_type = ["Don't repeat", "Everyday", "Every week", "Every month", "Every year"]
        self.setrecurringCombobox = ttk.Combobox(self.setTimeFrame, values=self.recurrence_type, font=("Times", 10), width=30)
        self.setrecurringCombobox.set("Don't repeat")
        self.setrecurringCombobox.pack()

        submitFrame = Frame(
            self.window,
            height=self.setTimeFrame_min_height,
            bg=containerBg,
        )
        submitFrame.pack(fill=X)

        btSubmit = Button(
            submitFrame,
            text="SUBMIT",
            fg="BLACK",
            font=("Times", 12, "bold"),
            compound=CENTER,
            bg="WHITE",
            activebackground=containerBg,
            bd=0,
            command=lambda: self.set_messagebox()
        )
        btSubmit.pack(side=BOTTOM, pady=10)

    def set_messagebox(self):
        self.title = self.inputTitle.get("1.0", 'end-1c')
        self.description = self.inputDescription.get("1.0", 'end-1c')
        self.date = self.date_var.get()
        self.selected_time = self.time_picker.time()
        self.recurrence_type = self.setrecurringCombobox.get()
        isCheckboxTick_type = self.isCheckboxTick.get()

        self.current_date = datetime.date.today()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month 
        self.current_day = self.current_date.day
        self.current_hour = int(time.strftime("%H"))
        self.current_minute = int(time.strftime("%M"))
        self.current_sec = int(time.strftime("%S"))
        
        
        self.selected_date = self.date_entry.get_date()
        self.selected_year = self.selected_date.year
        self.selected_month = self.selected_date.month
        self.selected_day = self.selected_date.day
        
        
        self.selected_minute = self.selected_time[1]
        
        if  self.selected_time[2]== "AM" and self.selected_time[0] == 12:
            self.selected_hour = 0
        elif  self.selected_time[2]== "PM" and self.selected_time[0] == 12:
            self. selected_hour = 12
        elif self.selected_time[2]== "PM":
            self.selected_hour = self.selected_time[0] + 12
        else:
            self.selected_hour = self.selected_time[0]
        
        if self.selected_year < self.current_year or (self.selected_year == self.current_year and self.selected_month < self.current_month) or (self.selected_year == self.current_year and self.selected_month == self.current_month and self.selected_day < self.current_day):
            messagebox.showerror("Alert", "You must enter a valid date!")
        elif (self.selected_date == self.current_date and self.selected_hour < self.current_hour) or (self.selected_date == self.current_date and self.selected_hour == self.current_hour and self.selected_minute < self.current_minute) :
            messagebox.showerror("Alert", "You must enter a valid time!")
        elif self.title.strip() == "" or self.description.strip() == "":
            messagebox.showerror("Alert", "All fields are required!")
        elif not isCheckboxTick_type:
            messagebox.showerror("Alert", "Set time is required!")
        else:
            response = messagebox.askyesno("Notifier Set", "Set notification?")
            if response:
                self.selected_sec = int(time.strftime("%S"))
                self.savedata()
                self.recurring()
                self.print_file()
                self.window.destroy()
                self.set_notification()

    def set_notification(self):
        self.update_datetime()
        self.set_checktime()
        
        for i in range(self.reminderArrRow):
            if (self.reminderArr[i][2] == self.current_date_updated and self.reminderArr[i][3] == self.current_time_updated):
                notification.notify(
                    title=self.reminderArr[i][0],
                    message=self.reminderArr[i][1],
                    app_name="Notifier", 
                    app_icon="icon/ico.ico",
                    toast=True,
                    timeout=10
                )
        
        self.container.after(self.checktime, self.set_notification)

    def set_checktime(self): 
        for i in range(self.reminderArrRow):
            sec = int(self.reminderArr[i][4])
            parts = self.reminderArr[i][3].split(":")
            second_parts = parts[1].split(" ")

            if  second_parts[1]== "PM" and parts[0] == "12":
                selected_hour = 12
            elif  second_parts[1]== "AM" and parts[0] == "12":
                selected_hour = 0
            elif second_parts[1]== "PM" and parts[0] != "12":
                selected_hour = int(parts[0]) + 12
            else:
                selected_hour = int(parts[0])
            
            selected_minute = int(second_parts[0])
                
            selected_sec = (selected_hour * 3600) + (selected_minute * 60) + sec
            current_sec = (self.current_hour * 3600) + (self.current_minute * 60) + self.current_sec
            self.checktime = (selected_sec - current_sec) * 1000

    def update_file(self):
        self.reminderArr = []
        with open("Reminder_Data_Record.txt", 'r') as file:
            arr = [None for _ in range(6)]
            lines = file.readlines()    
            i = 0
        
            for line in lines:
                parts = line.strip("\n").split("|")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key == "TITLE":
                        arr[0] = value
                    elif key == "DESCRIPTION":
                        arr[1] = value 
                    elif key == "DATE":
                        arr[2] = value
                    elif key == "TIME":
                        arr[3] = value
                    elif key == "SEC":
                        arr[4] = value
                    else:
                        arr[5] = value
                    i += 1
                    if i == 6:
                        i = 0
                        self.reminderArr.append(arr)
                        arr = [None] * 6
            self.reminderArrRow = len(self.reminderArr)

    def update_datetime(self):
        self.current_time_updated = time.strftime("%I:%M %p")
        self.current_date_updated = datetime.date.today().strftime("%d/%m/%Y")
        self.window.after(1000, self.update_datetime)
    
    def savedata(self):
        data = f"TITLE | {self.title} \nDESCRIPTION | {self.description} \nDATE | {self.date} \nTIME | {"{:02d}:{:02d} {}".format(*self.selected_time)} \nSEC | {self.selected_sec} \nRECURRENCE TYPE | {self.recurrence_type}\n\n"
        with open("Reminder_Data_Record.txt", 'a') as file:
            file.write(data)
        file.close()

    def recurring(self):
        self.update_file()

        for i in range(self.reminderArrRow):
            current_reminder_date = datetime.datetime.strptime(self.reminderArr[i][2], "%d/%m/%Y").date()
            if  current_reminder_date <  self.current_date  and self.reminderArr[i][5] != "Don't repeat":
                self.recurrence_title = self.reminderArr[i][0]
                self.recurrence_description = self.reminderArr[i][1]
                self.recurrence_time = self.reminderArr[i][3]
                self.recurrence_selected_sec = 0
                self.recurrence_recurrence_type = self.reminderArr[i][5]

                if self.recurrence_recurrence_type == "Every year":
                    self.recurrence_date = current_reminder_date + relativedelta(years=1)
                elif self.recurrence_recurrence_type == "Every month":
                    self.recurrence_date = current_reminder_date + relativedelta(months=1)
                elif self.recurrence_recurrence_type == "Every week":
                    self.recurrence_date = current_reminder_date + timedelta(weeks=1)
                else:
                    self.recurrence_date = current_reminder_date + timedelta(days=1)
                
                with open("Reminder_Data_Record.txt", 'r') as file:
                    existing_records = file.read()
                info = f"TITLE | {self.recurrence_title} \nDESCRIPTION | {self.recurrence_description} \nDATE | {self.recurrence_date.strftime('%d/%m/%Y')} \nTIME | {self.recurrence_time} \nSEC | {self.recurrence_selected_sec} \nRECURRENCE TYPE | {self.recurrence_recurrence_type}\n\n"
                if info != existing_records :
                    with open("Reminder_Data_Record.txt", 'a') as file:
                        file.write(info)
                    file.close()

    def print_file(self):
        self.update_file()
        
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i in range(self.reminderArrRow): 
            self.tree.insert('', END, values=(self.reminderArr[i][0], self.reminderArr[i][1], self.reminderArr[i][2],  self.reminderArr[i][3], self.reminderArr[i][5]))

    def Mouse_Scroll(self,event):
        self.tree.yview_scroll(-1 * (event.delta // 120), "units")

    def animate_frame( self,window,frame,max_height,min_height,frame_status):
        if not frame_status:
            for height in range(min_height, max_height + 1, 10):
                frame.config(height=height)
                window.update()
        else:
            for height in range(max_height,min_height - 1, -10):
                frame.config(height=height)
                window.update()
        
        match frame:
            case self.treeTodayFrame:
                self.treeTodayFrame_expanded = not self.treeTodayFrame_expanded
            case self.treeTmrFrame:
                self.treeTmrFrame_expanded = not self.treeTmrFrame_expanded
            case self.setTimeFrame:
                self.setTimeFrame_expanded = not self.setTimeFrame_expanded
            case _:
                pass
            
def reminder(): 
    app = ReminderApp()
    app.run()

if __name__ == "__main__":
    reminder()
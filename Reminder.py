from tkinter import *
from tkinter import ttk
from plyer import notification
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
import datetime 
import os
import time

containerBg = "#0D0D0D" 
sidebarBg = "#1a1c1e"  
textbg = "#212121" 
class ReminderApp:
    def reminderApp(container, root):
        clearFrame(container)
        ReminderApp.add_icon = Image.open('icon/Add.png')
        ReminderApp.add_icon = ReminderApp.add_icon.resize((200,35))
        ReminderApp.add_icon = ImageTk.PhotoImage(ReminderApp.add_icon)
        btAdd = Button(
            container,
            text="ADD NEW REMINDER",
            fg= "white",
            font=("Times", 12,"bold"),
            compound= CENTER,
            image=ReminderApp.add_icon,
            bg=containerBg,
            activebackground= containerBg,
            bd=0,
            command=lambda: create_new_reminder(root)
        )
        btAdd.place (x=1240, y=15)

        lbReminder = Label(
            container,
            text="REMINDER",
            fg= "white",
            font=("Times", 20,"bold"),
            bg=containerBg,
            activebackground= containerBg,
            bd=0,
            )
        lbReminder.place(x=23, y=15)

def create_new_reminder(root):
    window = Toplevel(root)
    window.title("Add New Reminder")
    window.geometry("500x600")
    window.configure(bg=containerBg)

    content_Frame = Frame(
        window,
        height= 600,
        width= 500,
        bg=containerBg,
    )
    content_Frame.pack(fill=BOTH)

    lbTitle = Label(
        content_Frame,
        text="TITLE:",
        font= ("Times", 15),
        fg="white",
        bg=containerBg
    )
    lbTitle.pack(pady=10)

    inputTitle = Text(
        content_Frame,
        bd=0,
        fg="white",
        font=("Times", 15),
        bg=textbg,
        width=40,
        height=2,
        insertbackground = "white"
    )
    inputTitle.pack()

    lbDescription = Label(
        content_Frame,
        text="DESCRIPTION:",
        font= ("Times", 15),
        fg="white",
        bg=containerBg
    )
    lbDescription.pack(pady=10)

    inputDescription = Text(
        content_Frame,
        bd=0,
        fg="white",
        font=("Times", 15),
        bg=textbg,
        width=40,
        height=2,
        insertbackground = "white"
    )
    inputDescription.pack()

    ReminderApp.setTimeFrame_expanded = False
    setTimeFrame_min_height = 50
    setTimeFrame_max_height = 350

    setTimeFrame = Frame(
        window,
        height= setTimeFrame_min_height,
        bg=containerBg,
    )
    setTimeFrame.pack(fill=X)
    setTimeFrame.pack_propagate(FALSE)

    isCheckboxTick = IntVar()
    setTimeCheckbox = Checkbutton(
        setTimeFrame,
        text="Set Time",
        font=("Times",20),
        fg="white",
        command=lambda:animate_setTime(),
        bg=containerBg,
        activebackground=containerBg,
        selectcolor="black",
        variable= isCheckboxTick,
        onvalue=1,
        offvalue= 0
        )
    setTimeCheckbox.pack()

    lbDate = Label(
        setTimeFrame,
        text="DATE:",
        font= ("Times", 15),
        fg="white",
        bg=containerBg
    )
    lbDate.pack(pady=10)

    
    date_var = StringVar()  # To store the selected date
    date_entry = DateEntry(
        setTimeFrame, 
        width=30,
        font= ("Times", 10),
        textvariable=date_var, 
        date_pattern='dd/MM/yyyy',
        showweeknumbers= False,
        weekendbackground="white",  # Color for weekends
        weekendforeground="black",
        othermonthwebackground = "white"
        )
    date_entry.pack()

    lbTime = Label(
        setTimeFrame,
        text="TIME:",
        font= ("Times", 15),
        fg="white",
        bg=containerBg
    )
    lbTime.pack(pady=10)

    time_picker = SpinTimePickerModern(setTimeFrame)
    time_picker.addAll(constants.HOURS12)
    time_picker.configureAll(
        bg="#212121",         
        height=1, 
        fg="#ffffff",          
        font=("Times", 16), 
        hoverbg="#2e2d2d",     
        hovercolor="#ffffff",  
        clickedbg="#404040",   
        clickedcolor="#d73333",
        )
    time_picker.configure_separator(bg="#212121", fg="#ffffff")
    time_picker.pack()

    lbRecurring = Label(
        setTimeFrame,
        text="RECURRING:",
        font= ("Times", 15),
        fg="white",
        bg=containerBg
    )
    lbRecurring.pack(pady=10)

    recurrence_type  = ["Don't repeat", "Everyday", "Every week", "Every month", "Every year"]
    setrecurringCombobox = ttk.Combobox(setTimeFrame, values= recurrence_type,font=("Times", 10),width=30)
    setrecurringCombobox.set("Don't repeat")
    setrecurringCombobox.pack()

    submitFrame = Frame(
        window,
        height= setTimeFrame_min_height,
        bg=containerBg,
    )
    submitFrame.pack(fill=X)

    btSubmit = Button(
            submitFrame,
            text="SUBMIT",
            fg= "BLACK",
            font=("Times", 12,"bold"),
            compound= CENTER,
            bg="WHITE",
            activebackground= containerBg,
            bd=0,
            command= lambda: set_notification()
        )
    btSubmit.pack (side=BOTTOM,pady=10)

    def set_notification():
        title = inputTitle.get("1.0",'end-1c')
        description = inputDescription.get("1.0",'end-1c')
        date = date_var.get()
        selected_time = time_picker.time()
        recurrence_type = setrecurringCombobox.get()
        isCheckboxTick_type = isCheckboxTick.get()
        current_date = datetime.date.today()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day
        selected_date = date_entry.get_date()
        year = selected_date.year
        month = selected_date.month
        day = selected_date.day
        current_hour = int( time.strftime("%H") )
        current_minute = int (time.strftime("%M") )
        minute = selected_time [1]
        if selected_time[2]== "PM":
            hour = selected_time[0] + 12
        else:
            hour = selected_time[0]

        print (current_hour, current_minute)

        if year < current_year or (year == current_year and month < current_month) or (year == current_year and month == current_month and day < current_day):
            messagebox.showerror("Alert", "You must enter a valid date!")
        elif selected_date == current_date and (hour < current_hour or minute < current_minute):
            messagebox.showerror("Alert", "You must enter a valid time!")
        elif title.strip() == "" or description.strip() == "":
            messagebox.showerror("Alert", "All fields are required!")
        elif not isCheckboxTick_type:  # Assumes 0 is False and 1 is True for the checkbox
            messagebox.showerror("Alert", "Set time is required!")
        else:
            response = messagebox.askyesno("Notifier Set", "Set notification?")
            if response:  # User clicks "Yes"
                savedata(title=title,description=description,date=date,selected_time=selected_time,recurrence_type=recurrence_type)
                window.destroy()
                # time.sleep(min_to_sec)
                notification.notify(
                    title=title,
                    message=description,
                    app_name="Notifier", 
                    app_icon="icon/ico.ico",
                    toast=True,
                    timeout=10
                    )
            
    def savedata(title,description,date,selected_time,recurrence_type):
        if not os.path.exists("Reminder_Data_Record.txt"):
            with open("Reminder_Data_Record.txt",'w') as file:
                file.write("")

        data = f"TITLE: {title} \nDESCRIPTION: {description} \nDATE: {date} \nTIME: {"{}:{} {}".format(*selected_time)} \nRECURRENCE TYPE: {recurrence_type}\n"
        with open("Reminder_Data_Record.txt", 'a') as file:
            file.write(data)
        file.close()
        

    def animate_setTime():
        if not ReminderApp.setTimeFrame_expanded:
            # Expand sidebar
            for height in range(setTimeFrame_min_height, setTimeFrame_max_height + 1, 10):
                setTimeFrame.config(height=height)
                window.update()
            ReminderApp.setTimeFrame_expanded = True
        else:
            # Collapse sidebar
            for height in range(setTimeFrame_max_height,setTimeFrame_min_height - 1, -10):
                setTimeFrame.config(height=height)
                window.update()
            ReminderApp.setTimeFrame_expanded = False
    
    window.mainloop()

def clearFrame(container):
    for widget in container.winfo_children():
        widget.destroy()


def reminder():
    app = ReminderApp()
    app.run()

if __name__ == "__main__":
    reminder()



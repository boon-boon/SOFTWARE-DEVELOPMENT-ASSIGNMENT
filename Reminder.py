from tkinter import *
from tkinter import ttk
from plyer import notification
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants

containerBg = "#0D0D0D" 
sidebarBg = "#1a1c1e"  
textbg = "#212121" 
class ReminderApp:
    def reminderApp(container, root):
        clearFrame(container)
        ReminderApp.add_icon = Image.open('Add.png')
        ReminderApp.add_icon = ReminderApp.add_icon.resize((200,35))
        ReminderApp.add_icon = ImageTk.PhotoImage(ReminderApp.add_icon)
        btAdd = Button(
            container,
            text="+ ADD NEW REMINDER",
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

    setTimeCheckbox = Checkbutton(
        setTimeFrame,
        text="Set Time",
        font=("Times",20),
        fg="white",
        command=lambda:animate_setTime(),
        bg=containerBg,
        activebackground=containerBg,
        selectcolor="black"
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
        clickedcolor="#d73333" 
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

    recurring  = ["Don't repeat", "Everyday", "Every week", "Every month", "Every year"]
    setrecurringCombobox = ttk.Combobox(setTimeFrame, values= recurring,font=("Times", 10))
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
        )
    btSubmit.pack (side=BOTTOM,pady=10)

    # def savedata():
        

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



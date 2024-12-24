from tkinter import *
from PIL import Image,ImageTk
from Reminder import ReminderApp
from Final_Expense_Tracker import Expense_Tracker
from Note_Organizer import NotesOrganizer

# Define color constants for UI styling
sidebarBg = "#1a1c1e"           # Sidebar background color   
topNavigationBg = "#1E1E1E"     # Top navigation background color
containerBg = "#0D0D0D"         # Main content background color
class MainMenu:
    def __init__(self):
        # Initialize main application window
        self.window = Tk()
        self.window.title("Main Menu")
        self.window.geometry("1920x1080")
        self.window.configure(bg=sidebarBg)

        # Sidebar expansion state and dimensions
        self.is_sidebar_expanded = False
        self.sidebar_min_width = 0
        self.sidebar_max_width = 250
        
        # Create UI components
        self.create_ui()
        self.create_sidebar_content()

    def create_ui(self):
        # Top navigation frame
        self.top_nav = Frame(
            self.window, 
            bg=topNavigationBg, 
            height=70
            )
        self.top_nav.pack(side=TOP, fill=X)
        self.top_nav.pack_propagate(False)

        # Sidebar frame
        self.sidebar = Frame(
            self.window, 
            width=70, 
            bg=sidebarBg, 
            height=1080
        )
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)

        # Content frame
        self.content_frame = Frame(
            self.window, 
            width=1850, 
            height=1080,
            bg=containerBg
        )
        self.content_frame.pack(side=RIGHT, fill=BOTH)
        self.content_frame.pack_propagate(False)

        # Second sidebar
        self.secondSidebar = Frame(
                self.window, 
                width=self.sidebar_min_width, 
                bg="#2f3336", 
                height=1080
        )
        self.secondSidebar.place(x=70,y=70)
        self.secondSidebar.pack_propagate(False)
        
        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        """Create and position navigation buttons"""
        # Menu toggle button
        self.menu_icon = Image.open('icon/menu.png')
        self.menu_icon = self.menu_icon.resize((30,30))
        self.menu_icon = ImageTk.PhotoImage(self.menu_icon)
        self.btMenu = Button(
            self.top_nav,
            width=50,
            height=50,
            image=self.menu_icon,
            bg=topNavigationBg,
            activebackground=topNavigationBg,
            bd=0,
            command= self._animate_sidebar
        )
        self.btMenu.place(x=10,y=10)

        # App name label
        self.btName = Button(
            self.top_nav,
            text="Financial Management",
            fg="white",
            font=("Arial", 20),
            bg=topNavigationBg,
            activebackground=topNavigationBg,
            bd=0
        )
        self.btName.place(x=80 , y =10) 

    def switch_indication(self,indication_lb):
        self.expense_btn_indicator.config(bg=sidebarBg)
        self.reminder_btn_indicator.config(bg=sidebarBg)
        self.note_btn_indicator.config(bg=sidebarBg)

        # Highlight the selected indicator
        indication_lb.config(bg="white")
        
    def create_sidebar_content(self):
        """Create sidebar menu items"""
        self.expense_btn_indicator = Label(
            self.sidebar,
            bg="white"
        )
        self.expense_btn_indicator.place(x=3,y=43, height=40,width=3)

        self.expense_icon = Image.open('icon/expense.png')
        self.expense_icon = self.expense_icon.resize((40,40))
        self.expense_icon = ImageTk.PhotoImage(self.expense_icon)
        btexpense = Button(
            self.sidebar, 
            image=self.expense_icon,
            width=40,
            height=40,
            bg=sidebarBg,
            activebackground=sidebarBg,
            bd=0,
        )
        btexpense.config(command=lambda: [self.switch_indication(self.expense_btn_indicator), Expense_Tracker(self.content_frame)])
        btexpense.place(x=15, y=43)

        # Reminder App button with an indicator
        self.reminder_btn_indicator = Label(
            self.sidebar,
            bg=sidebarBg
        )
        self.reminder_btn_indicator.place(x=3,y=125, height=40,width=3)

        self.reminder_icon = Image.open('icon/bell.png')
        self.reminder_icon = self.reminder_icon.resize((40,40))
        self.reminder_icon = ImageTk.PhotoImage(self.reminder_icon)
        btReminder = Button(
            self.sidebar, 
            image=self.reminder_icon,
            width=40,
            height=40,
            bg=sidebarBg,
            bd=0,
            activebackground=sidebarBg,
            command=lambda: [self.switch_indication(self.reminder_btn_indicator),ReminderApp(container = self.content_frame,sidebar=self.secondSidebar)]
        )
        btReminder.place(x=15, y=125)
        
        # Notes Organizer button with an indicator
        self.note_btn_indicator = Label(
            self.sidebar,
            bg=sidebarBg
        )
        self.note_btn_indicator.place(x=3,y=203, height=40,width=3)
        self.note_icon = Image.open('icon/note.png')
        self.note_icon = self.note_icon.resize((40,40))
        self.note_icon = ImageTk.PhotoImage(self.note_icon)
        btNote = Button(
            self.sidebar, 
            image=self.note_icon,
            width=40,
            height=40,
            bg=sidebarBg,
            bd=0,
            activebackground=sidebarBg,
            command=lambda: [self.switch_indication(self.note_btn_indicator),NotesOrganizer(self.content_frame)]
        )
        btNote.place(x=15, y=203)

    def _animate_sidebar(self):
        """Smooth sidebar animation"""
        if not self.is_sidebar_expanded:
            # Expand sidebar
            for width in range(self.sidebar_min_width, self.sidebar_max_width + 1, 10):
                self.secondSidebar.config(width=width)
                self.window.update()
            self.is_sidebar_expanded = True
        else:
            # Collapse sidebar
            for width in range(self.sidebar_max_width, self.sidebar_min_width - 1, -10):
                self.secondSidebar.config(width=width)
                self.window.update()
            self.is_sidebar_expanded = False
        
    def run(self):
        self.window.mainloop()
        
    def clearFrame(container):
        for widget in container.winfo_children():
            widget.destroy()

def main():
    """Entry point of the application"""
    app = MainMenu()
    app.run()

if __name__ == "__main__":
    main()
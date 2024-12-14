from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import Calendar
from datetime import datetime

class MoneyManagerApp:
    BG_COLOR = "#181818"
    SIDEBAR_COLOR = "#212121"
    ACTIVE_COLOUR = "#383838"
    FONT_MAIN = ("Arial",16,"bold")
    FONT_SUB = ("Arial",12,"bold")
    FONT_BUTTON = ("Arial",10,"bold")
    INCOME_FILE = ("Income.txt")
    ASSETS_FILE = ("Assets.txt")
    EXPENSE_FILE = ("Expense.txt")
    EXPENSE_HISTORY_FILE = ("Expense_History.txt")
    account_Icon_Path = ['Photo/Cash_Icon.png','Photo/Touch_N_Go_Icon.png', 'Photo/Debit_Card_Icon.png', 'Photo/Bank_Icon.png'] 
    
    def __init__(self):
        #Check textfile function
        if not os.path.exists(self.INCOME_FILE):
            with open(self.INCOME_FILE, 'w') as file:
                file.write("Cash: \nE-wallet: \nDebit Card: \nBank: ")
        if not os.path.exists(self.ASSETS_FILE):
            with open(self.ASSETS_FILE,'w') as file:
                file.write("")
        if not os.path.exists(self.EXPENSE_FILE):
            with open(self.EXPENSE_FILE) as file:
                file.write(" ")
        if not os.path.exists(self.EXPENSE_HISTORY_FILE):
            with open(self.EXPENSE_HISTORY_FILE,'w'):
                file.write("")
        
        #Use to calculate the total assets
        self.Load_Assets()
        self.Load_Expense()
        self.Load_Expense_History()
        
        #Initial variable
        self.ACTIVE_BUTTON1 = None
        self.ACTIVE_BUTTON2 = None
        self.assetsLst = [" ", " ", " "," "," "," "]
        self.expense_Category = ["Food", "Transport", "Daily Necesities", "Housing Expense", "Utilities", "Education", "Entertaiment", "Other"]
        self.account_Type = ['Cash','E-wallet','Debit card','Bank']
        
        
        self.window = Tk()
        self.window.title("Money manager")
        self.window.geometry("1920x1080")
        self.window.minsize(1500,1080)
        self.window.config(bg=self.BG_COLOR) #Print the window in grey colour
        
        #Print top border for future combine
        self.First_Top_Border =Frame(self.window,height=40,bg=self.SIDEBAR_COLOR)
        self.First_Top_Border.pack(side=TOP,fill=X)
        
        
        
        
        
        
        
        
        
        
        
        
        #Set the sidebar 
        self.SideBar = Frame(self.window,width=150,height=1080,bg=self.SIDEBAR_COLOR)
        self.SideBar.pack(side=LEFT, fill=Y)
        self.SideBar.pack_propagate(False) #To fix the size of the sidebar
        
        #Print the top border(Not for combine)
        self.Second_Top_Border = Frame(self.window,height=65,bg=self.SIDEBAR_COLOR)
        self.Second_Top_Border.pack(side=TOP, fill=X)
        self.Second_Top_Border.pack_propagate(False)
        self.Second_Top_Border.grid_propagate(FALSE)
        
        self.Load_Image("Photo/Blue Rectangle.png",150,30)
        
        #Create a button to create a new bill
        self.add_New_Bill = Button(
            self.Second_Top_Border,
            text='+ Add a new bill',
            font=self.FONT_BUTTON,
            bg=self.SIDEBAR_COLOR,
            fg="white",
            borderwidth=0,
            image=self.img,
            compound="center",
            activebackground=self.SIDEBAR_COLOR,
            activeforeground="white",
            command=self.Add_New_Bill
            )
        self.add_New_Bill.image = self.img
        self.add_New_Bill.pack(side=RIGHT, fill=X,padx=30)
        
        #Extra
        self.print_Home = Label(
            self.Second_Top_Border,
            text="Home",
            font=self.FONT_MAIN,
            fg="white",
            bg=self.SIDEBAR_COLOR
        )
        self.print_Home.place(x=575,y=15)
        
        #Print the Middle_Frame(center)
        self.Middle_Frame = Frame(self.window,bg=self.BG_COLOR,width=1920,height=1080)
        self.Middle_Frame.pack(side=LEFT, fill=Y)
        self.Middle_Frame.pack_propagate(FALSE)
        self.Middle_Frame.grid_propagate(FALSE)
        
        self.Create_Center_Content()
        self.Create_Sidebar_Section()
        self.window.mainloop()
        
        
#--------------------------------------------------------------
    #Create the logo in sidebar
    def Create_Sidebar_Section(self):
        #Main section
        main_Section = [
            ("Home", "🏠"),
            ("Assets", "👛"),
            ("Budget","🏦"),
            ("Setting","⚙️")
        ]
        self.Create_Section("Main",main_Section)
    

#--------------------------------------------------------------
    #Print the logo in the sidebar
    def Create_Section(self,section_name,items):
        
        #Menu for section in sidebar
        label=Label(
            self.SideBar,
            text=section_name,
            font=("Arial",16,"bold"),
            fg="white",
            bg=self.SIDEBAR_COLOR,
            anchor="w",
            padx=20
        )
        label.pack(fill=X,pady=20)
        
        section_callbacks = {
            "Home": self.Create_Center_Content,
            "Assets": self.Open_Assets_Page,
        }
        
        for item_text, emoji in items:
            button = Button(
                self.SideBar,
                text=f"{emoji}  {item_text}",
                font=("Arial",12),
                fg="white",
                bg=self.SIDEBAR_COLOR,
                activebackground=self.ACTIVE_COLOUR,
                activeforeground="white",
                relief=FLAT,
                anchor='w',
                padx=15,
                width=25,
                pady=20,
                borderwidth=0,
                command=section_callbacks.get(item_text.strip(), lambda: None)
            )
            button.pack(fill=X)
        

#--------------------------------------------------------------
    #Print content in the middle of home
    def Create_Center_Content(self):
        self.Middle_Frame.pack_forget()     #Print back the top navigator
        self.Second_Top_Border.pack(side=TOP, fill=X)
        self.Middle_Frame.pack(side=LEFT, fill=Y)
        self.Middle_Frame.pack_propagate(False)
        self.Destroy_Middle_Frame()         #Clear the widget before print the new
        
        #Print total expense and total income
        self.Load_Image("Photo/Black_Rectangle2.png", 300,100)
        ttl_Exp_Bg = Label(self.Middle_Frame,bg=self.BG_COLOR,image=self.img)
        ttl_Exp_Bg.image = self.img
        ttl_Exp_Bg.place(x=300,y=20)
        
        self.Load_Image("Photo/Total_Expense_Icon.png",50,50)
        ttl_Exp_Img = Label(self.Middle_Frame,image=self.img,bg=self.SIDEBAR_COLOR)
        ttl_Exp_Img.image=self.img
        ttl_Exp_Img.place(x=325,y=45)
        
        # self.Load_Image("Photo/Black_Rectangle2.png", 300,100)
        # ttl_Inc_Bg = Label(self.Middle_Frame, image=self.img,bg=self.BG_COLOR)
        # ttl_Inc_Bg.image = self.img
        # ttl_Inc_Bg.place(x=450,y=10)
        
        # self.Load_Image("Photo/Total_Income_Icon.png",50,50)
        # ttl_Inc_Img = Label(self.Middle_Frame,image=self.img,bg=self.SIDEBAR_COLOR)
        # ttl_Inc_Img.image = self.img
        # ttl_Inc_Img.place(x=500,y=35)
        
        
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        self.style.configure(
            "Custom.Treeview",
            background="lightblue",      # Row background color
            fieldbackground="lightblue", # Empty space background
            foreground="black",          # Row text color
        )

        # Style for Treeview headers
        self.style.configure(
            "Custom.Treeview.Heading",
            background=self.BG_COLOR,   # Header background color
            foreground='white',         # Header text color
            font=('Arial', 12, 'bold')  # Font for header text
        )
        
        self.tree = ttk.Treeview(
            self.Middle_Frame,
            style="Custom.Treeview",
            columns = ('Date', 'Amount', 'Category', 'Description'),
            show = 'headings'
        )
        
        self.tree.heading('Date', text='Date')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Description', text='Description')
        
        self.tree.column('Date', anchor=CENTER, width=150)
        self.tree.column('Amount', anchor=CENTER, width=200)
        self.tree.column('Category', anchor=CENTER, width=200)
        self.tree.column('Description', anchor=CENTER, width=200)
        
        self.tree.place(x=20,y=300)
        
        self.v_scroll = ttk.Scrollbar(self.Middle_Frame,orient=VERTICAL,command=self.tree.yview)
        self.tree.bind("<MouseWheel>", self.Mouse_Scroll)
        
        self.load_data_into_tree()
        
        
        # self.barchart_minheight = 0
        # self.barchart_maxheight = 250
        # bar_Chart_Colour = ["#2CA02C", "#1F77B4", "#FF7F0E", "#D62728"]
        #Print bar chart for income
        # highest_account = max(self.income_Amount)
        # for i in range(0,4):
        #     max_width = int(self.income_Amount[i] / highest_account * 150)+500
        #     bar_Chart = Frame(self.Middle_Frame, bg=bar_Chart_Colour[i],width=0,height=40)
        #     bar_Chart.place(x=300,y=10+(i*60))
        #     self.Animate_Bar_Chart(bar_Chart,min=0,max=max_width)
        #     print_Acc_Type = Label(self.Middle_Frame,text=self.account_Type[i],bg=self.BG_COLOR,fg='white',font=self.FONT_MAIN)
        #     print_Acc_Type.place(x=150,y=10+(i*60))
        #     show_balance = Label(self.Middle_Frame,text=self.income_Amount[i],bg=self.BG_COLOR,fg='white',font=self.FONT_MAIN)
        #     show_balance.place(x=max_width+300,y=10+(i*60))
            
        
           
        #Print Calendar at the right side
        # calendar = Calendar(self.Middle_Frame,
        #                     background=self.SIDEBAR_COLOR,  
        #                     foreground="white",  
        #                     bordercolor=self.SIDEBAR_COLOR,  
        #                     headersbackground=self.SIDEBAR_COLOR,  
        #                     headersforeground="white",
        #                     weekendbackground=self.SIDEBAR_COLOR,  
        #                     weekendforeground="white",
        #                     normalbackground= self.SIDEBAR_COLOR,
        #                     normalforeground='white',
        #                     othermonthbackground=self.SIDEBAR_COLOR,
        #                     othermonthforeground="white",
        #                     showothermonthdays=False,
        #                     font=self.FONT_SUB,
        #                     showweeknumbers=False
        #                     )
        # calendar.place(x=1025,y=10,width=350,height=350)
        
        
        # self.Load_Image("Black_Rectangle.png",400,150)
        # label = Label(self.Middle_Frame,image=self.img,bg=self.BG_COLOR,text="Expense",fg="grey",compound="center",font=("Arial",12,"bold"))
        # label.image = self.img
        # label.grid(row=0,column=0,sticky='w',padx=5,pady=5)
        
        #Print pie chart for expense
        # fig = Figure(figsize=(6,4),dpi=100)
        # ax = fig.add_subplot(111)
        # ax.bar(expense_Category,self.expense_Amount,color='skyblue',edgecolor='white')
        # ax.set_xlabel("Expense Categories", fontsize=12)
        # ax.set_ylabel("Expense Amounts", fontsize=12)
        # ax.set_xticklabels(expense_Category,rotation=45,fontsize=12)

        # for i, self.expense_Amount in enumerate(self.expense_Amount):
        #     ax.text(i, self.expense_Amount + 5, str(self.expense_Amount), ha='center', fontsize=10)

        # canvas = FigureCanvasTkAgg(fig, master=self.Middle_Frame)
        # canvas.draw()
        # canvas.get_tk_widget().place(x=10,y=10)
        
        
#--------------------------------------------------------------
    #Print the content in the middle after click the add new bill button
    def Add_New_Bill(self):
        #Use to hide the top Middle_Frame when press the button
        self.Second_Top_Border.pack_forget()  
        
        #Clear the widget before
        self.Destroy_Middle_Frame()
        
        #Print button to close or change page
        print_Close_Button = Button(self.Middle_Frame,text="x",fg="white",bg=self.BG_COLOR,font=("Arial",20,"bold"),activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0,width=5,height=2,command=self.Create_Center_Content)
        print_Close_Button.place(x=10,y=2)
        
        print_Expense= Button(self.Middle_Frame,text="Expense",fg="#E73D41",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="#E73D41",borderwidth=0)
        print_Expense.place(x=500,y=15)
    
        print_Income = Button(self.Middle_Frame, text="Income",fg="white",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0,command=self.Add_Income)
        print_Income.place(x=675,y=15)
        
        expense_Icon_Path = ["Photo/Food_Icon.png","Photo/Bus_Icon.png","Photo/Tissue_Icon.png","Photo/Home_Icon.png", "Photo/Utilities_Icon.png","Photo/Education_Icon.png","Photo/Entertaiment_Icon.png", "Photo/Other_Icon.png"]
        account_Type = ['Cash','E-wallet','Debit card','Bank']
        
        i = 0
        j = 0
        for i in range(0,8):
            self.Load_Image(expense_Icon_Path[i],30,30)
            expense_button = Button(
                self.Middle_Frame,
                text = f"{self.expense_Category[i]}",
                font=("Arial",14,"bold"),
                bg=self.BG_COLOR,
                fg="white",
                image=self.img,
                compound=TOP,
                relief=FLAT,
                activebackground=self.SIDEBAR_COLOR,
                activeforeground='white',
                width=300,
                height=125,
                borderwidth=0,
                )
            
            expense_button.image=self.img
            if i > 3:
                expense_button.place(x=10+(j*350),y=200)
                j+=1
            else:
                expense_button.place(x=10+(i*350),y=60)
            expense_button.config(command=lambda button=expense_button, ic=self.expense_Category[i]: [self.Highlight_Button1(button),self.Store_Assets1(category=ic)])

        self.Load_Image("Photo/Black_Square.png",1500,400)
        print_Square_Bg = Label(self.Middle_Frame, image=self.img,bg=self.BG_COLOR)
        print_Square_Bg.image = self.img
        print_Square_Bg.place(x=10,y=360)
        
        print_Account_Type = Label(self.Middle_Frame,text="Select account:",bg=self.SIDEBAR_COLOR,font=self.FONT_MAIN,fg='white')
        print_Account_Type.place(x=50,y=380)
        
        for i in range(0,4):
            self.Load_Image(self.account_Icon_Path[i],60,60)
            account_Label = Button(self.Middle_Frame,
                                  image=self.img,
                                  text=f"           {account_Type[i]}",
                                  compound=LEFT,
                                  font=self.FONT_MAIN,
                                  fg='white',
                                  bg=self.SIDEBAR_COLOR,
                                  borderwidth=0,
                                  activeforeground='white',
                                  activebackground=self.SIDEBAR_COLOR,
                                  width=250,
                                  anchor='w'
                                  )
            account_Label.image = self.img
            account_Label.place(x=40,y=430+(i*80))
            account_Label.config(command=lambda button=account_Label,x=account_Type[i]: [self.Highlight_Button2(button),self.Store_Assets1(account= x)])
        
        #Create entry to enter description
        description_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='white',borderwidth=0,font=self.FONT_MAIN,width=100,insertbackground='#4C9FFA')
        description_Entry.insert(0, "Description")
        description_Entry.bind("<FocusIn>",self.Saving_Description_Entry_Clear)
        description_Entry.bind("<FocusOut>",self.Saving_Description_Entry_Restore)
        description_Entry.place(x=40,y=330)
        
        #Create entry to input amount
        money_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='#F5494D',borderwidth=0,font=self.FONT_MAIN,width=100,insertbackground='#F5494D')
        money_Entry.insert(0, "0.00")
        money_Entry.bind("<FocusIn>",self.Saving_Money_Entry_Clear)
        money_Entry.bind("<FocusOut>",self.Saving_Money_Entry_Restore)
        money_Entry.place(x=1280,y=330)

        #Create date to input date
        calendar = Calendar(self.Middle_Frame,
                            background=self.SIDEBAR_COLOR,  # Background color of the calendar
                            foreground="white",  # Text color
                            bordercolor=self.SIDEBAR_COLOR,  # Border color of the calendar
                            headersbackground=self.SIDEBAR_COLOR,  # Background color of the headers (month, day names)
                            headersforeground="white",  # Text color of the headers
                            weekendbackground=self.SIDEBAR_COLOR,  # Color for weekends
                            weekendforeground="white",
                            normalbackground= self.SIDEBAR_COLOR,
                            normalforeground='white',
                            othermonthbackground=self.SIDEBAR_COLOR,
                            othermonthforeground="white",
                            showothermonthdays=False,
                            font=self.FONT_SUB,
                            showweeknumbers=False,
                            date_pattern="dd/mm/yyyy"
                            )
        calendar.place(x=1000,y=375,width=350,height=350)
        
        #Print the button to update the assets
        self.Load_Image("Photo/Blue Rectangle.png",150,30)
        
        input_Expense = Button(
            self.Middle_Frame,
            text="Update assets",
            font=self.FONT_BUTTON,
            bg=self.BG_COLOR,
            fg='white',
            borderwidth=0,
            image=self.img,
            compound='center',
            activebackground=self.BG_COLOR,
            activeforeground='white',
            command=lambda: self.Store_Assets2(description_Entry.get(), money_Entry.get(), calendar.get_date(),'Expense')
        )
        input_Expense.image = self.img
        input_Expense.place(x=1200,y=13)
    
    
#--------------------------------------------------------------
    def Add_Income(self):
        self.Destroy_Middle_Frame()        
            
        #Print a button to close the frame
        print_Close_Button = Button(self.Middle_Frame,text="x",fg="white",bg=self.BG_COLOR,font=("Arial",20,"bold"),activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0,width=5,height=2,command=self.Create_Center_Content)
        print_Close_Button.place(x=10,y=2)
        
        print_Expense= Button(self.Middle_Frame,text="Expense",fg="white",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="white",borderwidth=0, command=self.Add_New_Bill)
        print_Expense.place(x=500,y=15)
    
        print_Income = Button(self.Middle_Frame, text="Income",fg="#2CC684",bg=self.BG_COLOR,font=self.FONT_SUB,activebackground=self.ACTIVE_COLOUR,activeforeground="#2CC684",borderwidth=0)
        print_Income.place(x=675,y=15)
        
        income_Icon_Path = ["Photo/Income_Icon.png","Photo/Stock_Icon.png","Photo/Allowance_Icon.png","Photo/Other_Icon.png"]
        
        #Print a square behind the account type
        self.Load_Image("Photo/Black_Square.png",1500,400)
        print_Square_Bg = Label(self.Middle_Frame, image=self.img,bg=self.BG_COLOR)
        print_Square_Bg.image = self.img
        print_Square_Bg.place(x=10,y=360)
        
        print_Account_Type = Label(self.Middle_Frame,text="Select account:",bg=self.SIDEBAR_COLOR,font=self.FONT_MAIN,fg='white')
        print_Account_Type.place(x=50,y=380)
        
        income_Category = ["Income","Stock","Allowance","Other"]
        
        i = 0
        for i in range(0,4):
            self.Load_Image(income_Icon_Path[i],30,30)
            income_button = Button(
                self.Middle_Frame,
                text=f"{income_Category[i]}",
                font=("Arial",14,"bold"),
                bg=self.BG_COLOR,
                fg="white",
                image=self.img,
                compound=TOP,
                relief=FLAT,
                activebackground=self.SIDEBAR_COLOR,
                activeforeground='white',
                width=300,
                height=125,
                borderwidth=0
            )
            income_button.image = self.img
            income_button.place(x=10+(i*350),y=60)
            income_button.config(command=lambda ic=income_Category[i], bt=income_button: [self.Store_Assets1(category=ic),self.Highlight_Button1(bt)])
        
        for i in range(0,4):
            self.Load_Image(self.account_Icon_Path[i],60,60)
            account_Label = Button(self.Middle_Frame,
                                  image=self.img,
                                  text=f"           {self.account_Type[i]}",
                                  compound=LEFT,
                                  font=self.FONT_MAIN,
                                  fg='white',
                                  bg=self.SIDEBAR_COLOR,
                                  borderwidth=0,
                                  activeforeground='white',
                                  activebackground=self.SIDEBAR_COLOR,
                                  width=250,
                                  anchor='w'
                                  )
            account_Label.image = self.img
            account_Label.place(x=40,y=430+(i*80))
            account_Label.config(command=lambda button=account_Label,x=self.account_Type[i]: [self.Highlight_Button2(button),self.Store_Assets1(account= x)])

        #Create entry to enter description
        description_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='white',borderwidth=0,font=self.FONT_MAIN,width=100,insertbackground='#4C9FFA')
        description_Entry.insert(0, "Description")
        description_Entry.bind("<FocusIn>",self.Saving_Description_Entry_Clear)
        description_Entry.bind("<FocusOut>",self.Saving_Description_Entry_Restore)
        description_Entry.place(x=40,y=330)
        
        #Create entry to input amount
        money_Entry = Entry(self.Middle_Frame,bg=self.BG_COLOR,fg='#3DD393',borderwidth=0,font=self.FONT_MAIN,width=100,insertbackground='#3DD393')
        money_Entry.insert(0, "0.00")
        money_Entry.bind("<FocusIn>",self.Saving_Money_Entry_Clear)
        money_Entry.bind("<FocusOut>",self.Saving_Money_Entry_Restore)
        money_Entry.place(x=1280,y=330)

        #Create date to input date
        calendar = Calendar(self.Middle_Frame,
                            background=self.SIDEBAR_COLOR,  
                            foreground="white",  
                            bordercolor=self.SIDEBAR_COLOR,  
                            headersbackground=self.SIDEBAR_COLOR,  
                            headersforeground="white",
                            weekendbackground=self.SIDEBAR_COLOR,  
                            weekendforeground="white",
                            normalbackground= self.SIDEBAR_COLOR,
                            normalforeground='white',
                            othermonthbackground=self.SIDEBAR_COLOR,
                            othermonthforeground="white",
                            showothermonthdays=False,
                            font=self.FONT_SUB,
                            showweeknumbers=False,
                            date_pattern="dd/mm/yyyy" 
                            )
        calendar.place(x=1000,y=375,width=350,height=350)
        
        #Print the button to update the assets
        self.Load_Image("Photo/Blue Rectangle.png",150,30)
        
        input_Income = Button(
            self.Middle_Frame,
            text="Update assets",
            font=self.FONT_BUTTON,
            bg=self.BG_COLOR,
            fg='white',
            borderwidth=0,
            image=self.img,
            compound='center',
            activebackground=self.BG_COLOR,
            activeforeground='white',
            command=lambda: self.Store_Assets2(description_Entry.get(), money_Entry.get(), calendar.get_date(),'Income')
        )
        input_Income.image = self.img
        input_Income.place(x=1200,y=13)
 

#--------------------------------------------------------------
    def Open_Assets_Page(self):
        self.Second_Top_Border.pack_forget()
        self.Destroy_Middle_Frame()
        
        #Extra Print the navigator at the top middle
        assets_Page_Navigator = Frame(self.Middle_Frame,height=65,width=1920,bg=self.SIDEBAR_COLOR)
        assets_Page_Navigator.grid(row=0,column=0)
        print_Assets = Label(assets_Page_Navigator,text="Assets",fg="white",bg=self.SIDEBAR_COLOR,font=self.FONT_MAIN)
        print_Assets.place(x=575,y=15)
        
        #Print the top grey rounded rectangle
        self.Load_Image("Photo/Black_Rectangle1.png",1355,130)
        assests_Page_Top_Frame_Rectangle = Label(self.Middle_Frame,image=self.img,bg=self.BG_COLOR)
        assests_Page_Top_Frame_Rectangle.image = self.img
        assests_Page_Top_Frame_Rectangle.place(x=10,y=75)
        
        #Print the Net assets in the top middle
        print_Total_Assets = Label(
            assests_Page_Top_Frame_Rectangle,
            text=("Net Assets"),
            bg=self.SIDEBAR_COLOR,
            font=self.FONT_SUB,
            fg="#828282"
        )
        print_Total_Assets.place(x=560, y=30)
        
        #Print the net assets
        print_Total_Assets_Num = Label(
            assests_Page_Top_Frame_Rectangle,
            text=f"{self.Total_Assets:.2f}",
            bg=self.SIDEBAR_COLOR,
            font=("Cardium",24,"bold"),
            fg='white'
        )
        print_Total_Assets_Num.place(x=540, y=60)
        
        #Print the rectangle rounded corner at the middle
        self.Load_Image("Photo/Black_Rectangle2.png",1355,600)
        self.img_Frame = Label(self.Middle_Frame,image=self.img,bg=self.BG_COLOR)
        self.img_Frame.image = self.img
        self.img_Frame.place(x=10,y=220)
        
        #Print the asset type at the top left in
        assets_Types = Label(self.Middle_Frame, text="Asset Type",bg=self.SIDEBAR_COLOR,font=self.FONT_MAIN,fg="white")
        assets_Types.place(x=40,y=240)
        
        #Create a new frame 
        frame_Print_Acc_Balance = Frame(self.Middle_Frame,bg=self.SIDEBAR_COLOR,width=200,height=1080)
        frame_Print_Acc_Balance.place(x=500,y=260)
        
        for i in range(0,4):
            self.Load_Image(self.account_Icon_Path[i],50,50)
            account_Icon_Frame = Label(self.Middle_Frame,image=self.img,bg=self.SIDEBAR_COLOR)
            account_Icon_Frame.image = self.img
            account_Icon_Frame.place(x=50,y=300+(i*120))
            
            print_Account_Type = Label(self.Middle_Frame,text=self.account_Type[i],bg=self.SIDEBAR_COLOR,fg='white',font=self.FONT_MAIN)
            print_Account_Type.place(x=175,y=310+(i*120))
            
            print_RM_Account_Balance = Label(frame_Print_Acc_Balance,text='RM',bg=self.SIDEBAR_COLOR,fg='white',font=self.FONT_MAIN)
            print_RM_Account_Balance.place(x=0,y=46+(i*122))
            
            print_Account_Balance = Label(frame_Print_Acc_Balance,text=f"{self.income_Amount[i]:.2f}",bg=self.SIDEBAR_COLOR,fg='white',font=self.FONT_MAIN)
            print_Account_Balance.grid(row=i,column=0,pady=45.5,padx=50,sticky='e')
        
        #Print pie chart
        fig = Figure(figsize=(5, 5), dpi=110)
        fig.patch.set_facecolor(self.SIDEBAR_COLOR)  #Set the colour same with the background colour 
        ax = fig.add_subplot(111)
        ax.pie(self.income_Amount, labels=self.account_Type, autopct='%1.1f%%', startangle=90)
        for text in ax.texts:
            text.set_color('white')
            text.set_fontsize(10)
        
        canvas = FigureCanvasTkAgg(fig, master=self.Middle_Frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=730,y=240)
        
        print_Acc_Balance_Pie_Chart = Label(self.Middle_Frame, text="Account Balances",bg=self.SIDEBAR_COLOR,font=self.FONT_MAIN,fg="white")
        print_Acc_Balance_Pie_Chart.place(x=920,y=240)
            


#--------------------------------------------------------------
    def Load_Assets(self):
        with open('Assets.txt','r') as file:
            lines = file.readlines()

        self.income_Amount = [0.00,0.00,0.00,0.00]
        self.Total_Assets = 0
        
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value_str = parts[1].strip()
                

                value = float(value_str)
                if key == 'cash':
                   self.income_Amount[0] = value
                elif key == 'e-wallet':
                    self.income_Amount[1] = value
                elif key == 'debit card':
                    self.income_Amount[2] = value
                elif key == 'bank':
                    self.income_Amount[3] = value

        #Calculate the total
        for i in range(0,3):
            self.Total_Assets += self.income_Amount[i]


#--------------------------------------------------------------
    def Load_Expense(self):
        self.expense_Amount = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.total_Expense = 0
        with open('Expense.txt','r') as file:
            lines = file.readlines()       

        for line in lines:
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value_str = parts[1].strip()
                
                value = float(value_str)
                if key == 'food':
                    self.expense_Amount[0] = value
                elif key == 'transport':
                    self.expense_Amount[1] = value
                elif key == 'daily':
                    self.expense_Amount[2] = value
                elif key == 'housing':
                    self.expense_Amount[3] = value
                elif key == 'utilities':
                    self.expense_Amount[4] = value
                elif key == 'education':
                    self.expense_Amount[5] = value
                elif key == 'entertaiment':
                    self.expense_Amount[6] = value
                else:
                    self.expense_Amount[7] = value
                        
        for i in range(0,7):
            self.total_Expense += self.expense_Amount[i]
                
#--------------------------------------------------------------
    #Store the date seperately because got bug
    #Store the category and account
    def Store_Assets1(self, category=None, account=None):
        if category is not None:
            self.assetsLst[1] = f"Category: {category} "
        if account is not None:
            self.assetsLst[4] = f"Account: {account} "


#--------------------------------------------------------------
    #Store the description, amount and date
    def Store_Assets2(self,description=None, amount=None, date=None,category=None):
        #Debug
        if amount.isdigit() == 0 or self.ACTIVE_BUTTON1 == None or self.ACTIVE_BUTTON2 == None:
            self.Invalid_Input()
        
        #If no descripiton than print nothings into notepad
        if description != 'Description':
            self.assetsLst[2] = f"Description: {description}"
        else:
            self.assetsLst[2] = f"Description: "
            
        self.assetsLst[3] = f"Amount: {amount} "
        self.assetsLst[0] = f"Date: {date} "
        
        #Seperate the string from Accoutn:Cash to Cash
        different_acc = self.assetsLst[4].split(":")[1].strip()
        amount = float(self.assetsLst[3].split(":")[1])
        
        #Categorize if it is income or not then sum it and store it into Income.txt 
        if category == "Income":
            formula = 1
        else:
            formula = -1
            
        if different_acc == 'Cash':
            self.income_Amount[0] += formula * amount
        elif different_acc == 'E-wallet':
            self.income_Amount[1] += formula * amount
        elif different_acc == 'Debit card':
            self.income_Amount[2] += formula * amount
        elif different_acc == 'Bank':
            self.income_Amount[3] += formula * amount
        
        self.assetsLst[4] = ''
        if category =='Income':
            with open(self.INCOME_FILE, 'a') as file:
                for item in self.assetsLst:
                    file.write(item+'\n')
            file.close()
        else:
            with open(self.EXPENSE_HISTORY_FILE, 'a') as file:
                for item in self.assetsLst:
                    file.write(item+'\n')
            file.close()
        self.Create_Center_Content()
        
        data = f"Cash: {self.income_Amount[0]:.2f}\nE-wallet: {self.income_Amount[1]:.2f}\nDebit Card: {self.income_Amount[2]:.2f}\nBank: {self.income_Amount[3]:.2f}"
        
        with open(self.ASSETS_FILE, 'w') as file:
            file.write(data)
        file.close()
        
        if category == 'Expense':
            expense_Category = self.assetsLst[1].split(":")[1].strip()
            expense_Category_No = self.expense_Category.index(expense_Category)
            self.expense_Amount[expense_Category_No] += amount
            
            data = f"Food: {self.expense_Amount[0]}\nTransport: {self.expense_Amount[1]}\nDaily: {self.expense_Amount[2]}\nHousing: {self.expense_Amount[3]}\nUtilities: {self.expense_Amount[4]}\nEducation: {self.expense_Amount[5]}\nEntertaiment: {self.expense_Amount[6]}\nOther: {self.expense_Amount[7]}"
            
            with open(self.EXPENSE_FILE, 'w')as file:
                file.write(data)
            file.close()
        
        
#--------------------------------------------------------------
    #Destroy the middle frame widget
    def Destroy_Middle_Frame(self):
        for widget in self.Middle_Frame.winfo_children():
            widget.destroy()
        self.ACTIVE_BUTTON1 = None
        self.ACTIVE_BUTTON2 = None
    
    
#--------------------------------------------------------------    
    def Destroy_Second_Top_Border(self):
        for widget in self.Second_Top_Border.winfo_children():
            widget.destroy()
            
            
#--------------------------------------------------------------
    #Use to initialize the image just call it            
    def Load_Image(self, image_Path, image_Width, image_Height):
        self.img = Image.open(image_Path)
        self.img = self.img.resize((image_Width,image_Height))
        self.img = ImageTk.PhotoImage(self.img)
        
        
#--------------------------------------------------------------      
    #Use to initialize word ("description") the entry for description
    def Saving_Description_Entry_Clear(self,event):
        widget = event.widget
        if widget.get() == "Description":
            widget.delete(0,END)
            widget.config(fg="white")
    
    
#--------------------------------------------------------------
    #Use to delete the initialize word when pressed    
    def Saving_Description_Entry_Restore(self,event):
        widget = event.widget
        if not widget.get():
            widget.insert(0, "Description")
            widget.config(fg='white')
    
    
#--------------------------------------------------------------    
    def Saving_Money_Entry_Clear(self,event):
        widget = event.widget
        if widget.get() == "0.00":
            widget.delete(0,END)
            widget.config(fg="#3DD393")
    
    
#--------------------------------------------------------------    
    def Saving_Money_Entry_Restore(self,event):
        widget = event.widget
        if not widget.get():
            widget.insert(0, "0.00")
            widget.config(fg='#3DD393')
    
    
#--------------------------------------------------------------    
    def Highlight_Button1(self, new_Button1):
        if self.ACTIVE_BUTTON1 is not None:
            self.ACTIVE_BUTTON1.config(bg=self.BG_COLOR)
        new_Button1.config(bg="#454545") 
        self.ACTIVE_BUTTON1 = new_Button1
    
    
#--------------------------------------------------------------    
    def Highlight_Button2(self,new_Button2):
        if self.ACTIVE_BUTTON2 is not None:
            self.ACTIVE_BUTTON2.config(bg=self.SIDEBAR_COLOR)
        new_Button2.config(bg="#454545") 
        self.ACTIVE_BUTTON2 = new_Button2

#--------------------------------------------------------------
    def Animate_Bar_Chart(self, frame,min,max): 
        for height in range(min, max + 1, 1):
            frame.config(width=height)
            self.window.update()


#--------------------------------------------------------------
    def Load_Expense_History(self):
        with open(self.EXPENSE_HISTORY_FILE, 'r')as file:
            lines = file.readlines()
        
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value_str = parts[1].strip()
                
                # print(key)
                # print(value_str)


#--------------------------------------------------------------
    def Invalid_Input(self):
        error_window = Tk()
        error_window.title("Invalid input")
        error_window.geometry('600x400')
        
        error_message = Label(error_window,text="Invalid Input",fg='red')
        error_message.grid()
        error_window.mainloop()


#--------------------------------------------------------------
    def load_data_into_tree(self):
    # Clear existing rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Read data from the file and populate the Treeview
        data = []
        with open(self.EXPENSE_HISTORY_FILE, 'r') as file:
            record = {}
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line:  # If the line is empty, treat it as the end of a record
                    if record:  # If we have a complete record, add it to the list
                        try:
                            date = record.get("Date", "")
                            amount = record.get("Amount", "")
                            category = record.get("Category", "")
                            description = record.get("Description", "")
                            data.append({
                                "Date": date,
                                "Amount": amount,
                                "Category": category,
                                "Description": description
                            })
                        except KeyError as e:
                            print(f"Skipping record due to missing field: {e}")
                        record = {}  # Reset the record dictionary for the next entry
                else:
                    # Parse the line into key-value pairs
                    if ": " in line:
                        key, value = line.split(": ", 1)
                        record[key] = value

        # Sort the data by Date in ascending order
        try:
            data.sort(key=lambda x: datetime.strptime(x["Date"], "%d/%m/%Y"),reverse=True)
        except ValueError as e:
            print(f"Error parsing dates: {e}")
        
        # Insert the sorted data into the Treeview
        for record in data:
            self.tree.insert('', END, values=(record["Date"], record["Amount"], record["Category"], record["Description"]))


#--------------------------------------------------------------
    def Mouse_Scroll(self,event):
        self.tree.yview_scroll(-1 *(event.delta // 120), "units")
        
MoneyManagerApp()
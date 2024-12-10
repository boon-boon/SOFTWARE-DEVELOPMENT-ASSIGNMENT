from tkinter import *
from tkinter import ttk, StringVar, Toplevel, Frame, Button, Label
from tkinter.ttk import Style
from tkinter import Toplevel, Frame, Button, Label, Text, StringVar, END, BOTH
from tkinter import  filedialog, messagebox
from datetime import datetime
from tkinter import colorchooser, messagebox
import os
from tkinter import messagebox, filedialog
from docx import Document
from docx.shared import Pt, RGBColor
from PIL import Image
import io

class NotesOrganizer:
    def __init__(self, root):
        self.root = root
        # self.root = root
        # self.root.title("Notes Organizer")
        # self.root.geometry("1200x700")
        # self.root.configure(bg='#212121')  # Dark background

        self.root.config(bg='white')
        
        # Store the directory where notes will be saved

        self.notes_directory = os.path.join(os.path.expanduser("~"), "NotesOrganizer")
        os.makedirs(self.notes_directory, exist_ok=True)

        # Sidebar at the bottom
        self.B_sidebar = Frame(root, height=50, bg='#181818')  # Use height for bottom bars
        self.B_sidebar.pack(side=BOTTOM, fill=X)

        self.T_sidebar = Frame(root, height=60, bg='#181818')  # Use height for bottom bars
        self.T_sidebar.pack(side=TOP, fill=X)

        self.Out_button = Button(
            self.T_sidebar,
            text="<",
            font=('Arial', 25),
            bg='#181818',
            fg='white',
            borderwidth=0,
            activebackground='#202020',
            command=self.Out_button_action
        )
        self.Out_button.pack(side=LEFT, pady=10, padx=20)

        # Search frame
        search_frame = Frame(self.T_sidebar, bg='#181818')
        search_frame.pack(side=LEFT, padx=20, pady=10, expand=True, fill=X)

        self.sidebar = Frame(self.root, 
                                width=250, 
                                bg='#181818', 
                                height=root.winfo_screenheight())
        self.sidebar_visible = False

        self.ThreeLine_button = Button(
            self.B_sidebar,
            text="☰",
            font=('Arial', 25),
            bg='#181818',
            fg='white',
            borderwidth=0,
            activebackground='#202020',
            command=self.ThreeLine_button_action
        )
        self.ThreeLine_button.pack(side=LEFT, pady=10, padx=20)
        
        # Add button with plus emoji
        self.add_button = Button(
            self.B_sidebar, 
            text="➕", 
            font=('Arial', 25),  # Adjust font size to make emoji larger
            bg='#181818',         # Match sidebar background
            fg='white',           # Text color
            borderwidth=0,        # Remove button border
            activebackground='#202020',  # Slight color change when pressed
            command=self.Addbutton_action  # Add a method to handle button click
        )
        self.add_button.pack(side=LEFT, expand=True, anchor=CENTER, pady=10)  # Center the button in sidebar

        self.Search_button = Button(
            self.B_sidebar,
            text="🔍",
            font=('Arial', 30),
            bg='#181818',
            fg='white',
            borderwidth=0,
            activebackground='#202020',
            command=self.Search_button_action
        )
        self.Search_button.pack(side=RIGHT, pady=10, padx=20)

        # Notes list frame
        self.notes_frame = Frame(root, bg='#212121')
        self.notes_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Treeview for displaying notes
        self.notes_tree = ttk.Treeview(self.notes_frame, 
                                       columns=("Filename", "Date", "Category"), 
                                       show='headings')

        # Customize Treeview style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", 
                        background='#292929',
                        foreground='white',
                        rowheight=30,
                        fieldbackground='#292929')
        style.configure("Treeview.Heading", 
                        background='#181818', 
                        foreground='white', 
                        font=('Arial', 10, 'bold'))
        style.map('Treeview', 
                  background=[('selected', '#404040')],
                  foreground=[('selected', 'white')])

        # Define column headings
        self.notes_tree.heading("Filename", text="Filename")
        self.notes_tree.heading("Date", text="Date")
        self.notes_tree.heading("Category", text="Category")
        
        # Set column widths
        self.notes_tree.column("Filename", width=400)
        self.notes_tree.column("Date", width=200)
        self.notes_tree.column("Category", width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.notes_frame, orient=VERTICAL, command=self.notes_tree.yview)
        self.notes_tree.configure(yscroll=scrollbar.set)

        # Pack treeview and scrollbar
        self.notes_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Bind double-click event to open note
        self.notes_tree.bind('<Double-1>', self.open_selected_note)

        # Load existing notes on startup
        self.load_notes()

    def load_notes(self):
        """Load all saved notes into the treeview"""
        # Clear existing items
        for i in self.notes_tree.get_children():
            self.notes_tree.delete(i)
        
        # Iterate through .docx files in the notes directory
        for filename in os.listdir(self.notes_directory):
            if filename.endswith('.docx'):
                file_path = os.path.join(self.notes_directory, filename)
                
                # Read metadata from the document
                try:
                    doc = Document(file_path)
                    
                    # Extract category (assuming it's the second paragraph)
                    category = "Uncategorized"
                    if len(doc.paragraphs) > 1 and doc.paragraphs[1].text.startswith("Category:"):
                        category = doc.paragraphs[1].text.replace("Category:", "").strip()
                    
                    # Get file modification time
                    mod_time = os.path.getmtime(file_path)
                    formatted_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M')
                    
                    # Insert into treeview
                    self.notes_tree.insert("", END, values=(filename, formatted_date, category))
                
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    def search_notes(self):
        """Search notes based on user input"""
        search_term = self.search_var.get().lower()
        
        # Clear current treeview
        for i in self.notes_tree.get_children():
            self.notes_tree.delete(i)
        
        # Iterate through .docx files in the notes directory
        for filename in os.listdir(self.notes_directory):
            if filename.endswith('.docx'):
                file_path = os.path.join(self.notes_directory, filename)
                
                try:
                    doc = Document(file_path)
                    
                    # Check if search term is in any paragraph
                    match_found = any(
                        search_term in paragraph.text.lower() 
                        for paragraph in doc.paragraphs
                    )
                    
                    if match_found or search_term in filename.lower():
                        # Extract category
                        category = "Uncategorized"
                        if len(doc.paragraphs) > 1 and doc.paragraphs[1].text.startswith("Category:"):
                            category = doc.paragraphs[1].text.replace("Category:", "").strip()
                        
                        # Get file modification time
                        mod_time = os.path.getmtime(file_path)
                        formatted_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M')
                        
                        # Insert into treeview
                        self.notes_tree.insert("", END, values=(filename, formatted_date, category))
                
                except Exception as e:
                    print(f"Error searching {filename}: {e}")

    def open_selected_note(self, event):
        """Open the selected note"""
        # Get the selected item
        selected_item = self.notes_tree.selection()
        
        if not selected_item:
            return
        
        # Get the filename
        filename = self.notes_tree.item(selected_item)['values'][0]
        file_path = os.path.join(self.notes_directory, filename)
        
        # Create new note window (reusing the Addbutton_action logic)
        self.Addbutton_action(file_path)

    def Addbutton_action(self, file_path=None): 
        def insert_picture():
            try:
                # Open file dialog to select an image
                file_path = filedialog.askopenfilename(
                    title="Select an image",
                    filetypes=[
                        ("Image files", "*.png *.gif"),
                        ("PNG files", "*.png"),
                        ("GIF files", "*.gif"),
                        ("All files", "*.*")
                    ]
                )
                
                # If a file is selected
                if file_path:
                    # Open the image using Tkinter's PhotoImage
                    photo = PhotoImage(file=file_path)
                    
                    # Check if image is too large and scale down if necessary
                    max_width = 600
                    if photo.width() > max_width:
                        # Calculate scaling factor
                        scale_factor = max_width / photo.width()
                        
                        # Scale down the image
                        scaled_width = int(photo.width() * scale_factor)
                        scaled_height = int(photo.height() * scale_factor)
                        
                        # Use Tkinter's subsample method to resize
                        photo = photo.subsample(int(1/scale_factor), int(1/scale_factor))
                    
                    # Create a label with the image
                    image_label = Label(Note_text_frame, image=photo, bg='#212121')
                    image_label.image = photo  # Keep a reference to prevent garbage collection
                    
                    # Insert the image into the Note_text_box
                    Note_text_box.window_create(END, window=image_label)
                    
                    # Optional: Insert a newline after the image
                    Note_text_box.insert(END, "\n")

                    Note_text_box.edit_modified(True)
                    Note_text_box.edit_separator()
                    
                    # Optional: Store the image file path for saving later
                    image_label.file_path = file_path
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to insert picture: {str(e)}")

        def save_note():
            try:
                # Ask user where to save the file
                save_path = filedialog.asksaveasfilename(
                    initialdir=self.notes_directory,
                    defaultextension=".docx",
                    filetypes=[("Word Document", "*.docx"), ("All files", "*.*")]
                )
                
                if not save_path:
                    return  # User cancelled save
                
                # Create a new Word document
                doc = Document()
                
                # Set default style
                style = doc.styles['Normal']
                style.font.name = 'Arial'
                style.font.size = Pt(12)
                
                # Add tags (from text_box)
                tags_paragraph = doc.add_paragraph()
                tags_paragraph.add_run("Tags: ").bold = True
                tags_paragraph.add_run(text_box.get("1.0", END).strip())
                
                # Add category if selected
                if category_var.get() != "Select Category":
                    doc.add_paragraph(f"Category: {category_var.get()}")
                
                # Retrieve content from Note_text_box
                content = Note_text_box
                
                # Paragraph to hold the note content
                note_paragraph = doc.add_paragraph()
                
                # Iterate through the content
                index = "1.0"
                while index:
                    try:
                        # Get the tag names at this index
                        tags = content.tag_names(index)
                        
                        # Get the text at this index
                        next_index = content.index(f"{index} lineend")
                        current_text = content.get(index, next_index)
                        
                        # Find color tag (if any)
                        color_tag = next((tag for tag in tags if tag.startswith('color-')), None)
                        
                        # Check if this is an image
                        window_info = content.window_cget(index, "window")
                        
                        if window_info:  # This is an image
                            # Get the image label
                            image_label = content.window_cget(index, "window")
                            
                            # Try to get the file path of the image
                            if hasattr(image_label, 'file_path'):
                                # Open the image using Pillow
                                with Image.open(image_label.file_path) as img:
                                    # Save image to a BytesIO object
                                    img_byte_arr = io.BytesIO()
                                    img.save(img_byte_arr, format='PNG')
                                    img_byte_arr = img_byte_arr.getvalue()
                                    
                                    # Add image to the document
                                    doc.add_picture(io.BytesIO(img_byte_arr))
                        
                        else:  # This is text
                            # Add text with color if applicable
                            run = note_paragraph.add_run(current_text)
                            
                            # Apply color if a color tag exists
                            if color_tag:
                                # Extract hex color from tag
                                hex_color = color_tag.split('-')[1]
                                # Convert hex to RGB
                                r = int(hex_color[1:3], 16)
                                g = int(hex_color[3:5], 16)
                                b = int(hex_color[5:7], 16)
                                run.font.color.rgb = RGBColor(r, g, b)
                        
                        # Move to next index
                        index = next_index + "+1c"
                        
                        # Add a newline after text or image
                        if current_text.strip() or window_info:
                            doc.add_paragraph()
                    
                    except TclError:
                        # No more content
                        break
                
                # Save the document
                doc.save(file_path)
                
                # Show success message
                messagebox.showinfo("Success", f"Note saved successfully to {file_path}")
            
                # Reload notes after saving
                self.load_notes()

            except Exception as e:
                # Handle any errors during save
                messagebox.showerror("Error", f"Failed to save note: {str(e)}")
                    
        def choose_text_color():
            # Check if any text is selected in Note_text_box
            try:
                # Get the selected text's start and end indexes
                start = Note_text_box.index(SEL_FIRST)
                end = Note_text_box.index(SEL_LAST)
            except TclError:
                # No text selected
                messagebox.showinfo("Error", "Please select some text first")
                return

            # Open color chooser dialog
            color = colorchooser.askcolor(title="Choose text color")
            
            # Check if a color was selected (not cancelled)
            if color[1]:  # color[1] is the hex color code
                 # Mark the current state before modification
                Note_text_box.edit_separator()

                # Store the original color of the selected text
                original_color = Note_text_box.tag_cget("sel", "foreground")
                
                for tag in Note_text_box.tag_names(start):
                            if tag.startswith('color-'):
                                Note_text_box.tag_remove(tag, start, end)

                # Create a new color tag
                tag_name = f"color-{color[1]}"
                Note_text_box.tag_config(tag_name, foreground=color[1])
                Note_text_box.tag_add(tag_name, start, end)
                
                # Mark as modified to enable undo
                Note_text_box.edit_modified(True)

        new_note_window=Toplevel(self.root)
        new_note_window.title("New Note" if file_path is None else "Edit Note")
        new_note_window.geometry("1200x700")
        new_note_window.configure(bg='#212121')

        top_sidebar = Frame(new_note_window, height=60, bg='#181818')  # Use height for bottom bars
        top_sidebar.pack(side=TOP, fill=X)

        left_sidebar_frame = Frame(top_sidebar, bg='#181818')
        left_sidebar_frame.pack(side=LEFT, fill=Y, padx=10)
        
        # Back button with '<' symbol
        back_button = Button(left_sidebar_frame, 
                             text="<", 
                             font=('Arial', 25, 'bold'),
                             bg='#181818', 
                             fg='white', 
                             borderwidth=0,
                             width=2,
                             activebackground='#202020',
                             command=new_note_window.destroy)
        back_button.pack(side=LEFT, pady=10)

        right_sidebar_frame = Frame(top_sidebar, bg='#181818')
        right_sidebar_frame.pack(side=RIGHT, fill=Y, padx=10)
        
        save_button = Button(right_sidebar_frame, 
                             text="💾", 
                             font=('Arial', 25, 'bold'),
                             bg='#181818', 
                             fg='white', 
                             borderwidth=0,
                             width=2,
                             activebackground='#202020',
                             command=lambda: save_note())
        save_button.pack(side=RIGHT, pady=10)

        horizontal_sidebar =Frame(new_note_window, height=50, bg='#292929')  # Adjust height as needed
        horizontal_sidebar.pack(side=TOP, fill=X)

        style = Style()
        style.theme_use('default')  # Use default theme as base
        
        # Customize Combobox style
        style.configure('Custom.TCombobox', 
                        background='#292929',  # Dark background for dropdown
                        foreground='white',   # White text
                        fieldbackground='#292929',  # Background of the selected item field
                        arrowcolor='white')

        category_label = Label(horizontal_sidebar, 
                               text="Category:", 
                               font=('Arial', 12),
                               bg='#292929', 
                               fg='white')
        category_label.pack(side=LEFT, padx=(20,10), pady=10)
        
        category_var = StringVar()
        category_dropdown = ttk.Combobox(horizontal_sidebar, 
                                         textvariable=category_var,
                                         values=["Financial Plans", "Investment Opportunities", "Receipts"],
                                         state="readonly",  # Prevents manual text entry
                                         width=25)
        category_dropdown.pack(side=LEFT, padx=10, pady=10)
        category_dropdown.set("Select Category")
    
        trash_frame = Frame(horizontal_sidebar, bg='#292929')
        trash_frame.pack(side=RIGHT, padx=10)
        
        trash_button = Button(trash_frame, 
                          text="🗑️", 
                          font=('Arial', 20),
                          bg='#292929', 
                          fg='white', 
                          borderwidth=0,
                          activebackground='#252525')
        trash_button.pack(side=RIGHT, padx=5, pady=5)

        right_buttons_frame = Frame(horizontal_sidebar, bg='#292929')
        right_buttons_frame.pack(side=RIGHT, padx=20)

        palette_button = Button(
                            right_buttons_frame, 
                            text="🎨", 
                            font=('Arial', 20),
                            bg='#292929', 
                            fg='white', 
                            borderwidth=0,
                            activebackground='#252525',
                            command=choose_text_color)
        palette_button.pack(side=LEFT, padx=10, pady=5)
        
        picture_buttons_frame = Frame(horizontal_sidebar, bg='#292929')
        picture_buttons_frame.pack(side=RIGHT, padx=2)
        
        # Picture button
        picture_button = Button(picture_buttons_frame, 
                            text="🖼️", 
                            font=('Arial', 20),
                            bg='#292929', 
                            fg='white', 
                            borderwidth=0,
                            activebackground='#252525',
                            command=insert_picture)
        picture_button.pack(side=LEFT, padx=5, pady=5)

        undo_redo_frame = Frame(horizontal_sidebar, bg='#292929')
        undo_redo_frame.pack(side=RIGHT, padx=10)

        # Undo button
        undo_button = Button(undo_redo_frame, 
                            text="↺", 
                            font=('Arial', 20),
                            bg='#292929', 
                            fg='white', 
                            borderwidth=0,
                            activebackground='#252525',
                            command=lambda: [
                                Note_text_box.edit_undo(),
                                text_box.edit_undo()
                            ])
        undo_button.pack(side=LEFT, padx=5, pady=5)

        # Redo button
        redo_button = Button(undo_redo_frame, 
                            text="↻", 
                            font=('Arial', 20),
                            bg='#292929', 
                            fg='white', 
                            borderwidth=0,
                            activebackground='#252525',
                            command=lambda: [
                                Note_text_box.edit_redo(),
                                text_box.edit_redo()
                            ])
        redo_button.pack(side=LEFT, padx=40, pady=5)

        text_frame = Frame(new_note_window, bg='#212121')
        text_frame.pack(fill=BOTH, expand=True, padx=20, pady=(20, 10))

        text_title = Label(text_frame, 
                            text="Tags: ", 
                            font=('Arial', 12, 'bold'), 
                            bg='#212121', 
                            fg='white')
        text_title.pack(anchor='w', padx=10, pady=(10, 5))  # Align left and add padding

        text_box = Text(text_frame, 
                        font=('Arial', 16), 
                        bg='#292929', 
                        fg='white', 
                        insertbackground='white',  # Makes cursor visible
                        wrap=WORD,  # Wrap text by words
                        borderwidth=0, 
                        relief=FLAT,
                        width=120,
                        height=2,
                        undo=True,
                        maxundo=-1)
        text_box.pack(padx=10, pady=(5, 10))

        Note_text_frame = Frame(new_note_window, bg='#212121')
        Note_text_frame.pack(fill=BOTH, expand=True, padx=20, pady=0)

        Note_text_title = Label(Note_text_frame, 
                            text="Note: ", 
                            font=('Arial', 14, 'bold'), 
                            bg='#212121', 
                            fg='white')
        Note_text_title.pack(anchor='w', padx=10, pady=(20, 15))  # Align left and add padding

        Note_text_box = Text(Note_text_frame, 
                        font=('Arial', 16), 
                        bg='#292929', 
                        fg='white', 
                        insertbackground='white',  # Makes cursor visible
                        wrap=WORD,  # Wrap text by words
                        borderwidth=0, 
                        relief=FLAT,
                        width=120,
                        height=25,
                        undo=True,
                        maxundo=-1)
        Note_text_box.pack(padx=10, pady=10)

        if file_path:
            try:
                doc = Document(file_path)
                # Load document contents into text boxes
                # This is a simplified example and you'll need to adapt it
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open note: {str(e)}")

    def ThreeLine_button_action(self):
        if not self.sidebar_visible:
            # Show sidebar aligned to the left side of the main frame
            # You can adjust these parameters to change positioning
            self.sidebar.pack(side=LEFT,   # Horizontal positioning
                              fill=Y,
                              padx=0,      # Vertical filling
                              anchor='w')     # West (left) alignment
            self.sidebar_visible = True
        else:
            # Hide sidebar completely
            self.sidebar.pack_forget()
            self.sidebar_visible = False
            
            if hasattr(self, 'home_button') and self.home_button is not None:
                self.home_button.destroy()
                self.home_button = None
        
        if not hasattr(self, 'home_button') or self.home_button is None:
            self.home_button = Button(self.sidebar,
                                text="   🏠    Home",
                                font=('Arial', 16, 'bold'),
                                bg='#181818',
                                fg='white',
                                borderwidth=0,
                                anchor='w',
                                justify=LEFT,
                                width=15,
                                activebackground='#202020')
            self.home_button.pack(side=TOP,anchor='w', pady=20, padx=10, fill=X)
        
    def Search_button_action(self):
        # Add a flag to track search bar visibility
        self.search_bar_visible = False

        # Prepare the search frame but don't pack it initially
        self.search_frame = Frame(self.T_sidebar, bg='#181818')

        # Search entry
        self.search_var = StringVar()
        self.search_entry = Entry(self.search_frame, 
                                  textvariable=self.search_var, 
                                  font=('Arial', 12), 
                                  bg='#292929', 
                                  fg='white', 
                                  insertbackground='white',
                                  width=50)
        self.search_entry.pack(side=LEFT, padx=10, fill=X, expand=True)

        # Toggle search bar visibility
        if not self.search_bar_visible:
            # Show the search bar
            self.search_frame.pack(side=LEFT, padx=20, pady=10, expand=True, fill=X)
            self.search_bar_visible = True
            self.search_entry.focus_set()  # Optional: set focus to search entry
        else:
            # Hide the search bar
            self.search_frame.pack_forget()
            self.search_bar_visible = False
            
            # Optional: Reset search and reload all notes when closing
            self.search_var.set('')
            self.load_notes()

    def Out_button_action(self):
        print("Button click success!")

    def Clear_Main_Screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def note():
    # root = Tk()
    app = NotesOrganizer()
    app.run()

if __name__ == "__main__":
    note()
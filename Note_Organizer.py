import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os
import json
import io

class NotesOrganizer:
    def __init__(self, container):
        self.window = container

        self.Top_sidebar_frame = tk.Frame(container, height=60, bg='#181818')
        self.Top_sidebar_frame.pack(side="top", fill="x")

        label = tk.Label(self.Top_sidebar_frame, text="Note Organizer", bg="#181818", fg="white", font=("Arial Rounded MT Bold", 14))
        label.pack(pady=5)
    
        self.Bottom_sidebar_frame = tk.Frame(container, height=60, bg="#181818")
        self.Bottom_sidebar_frame.pack(side="bottom", fill="x")

        self.Search_button = tk.Button(
            self.Bottom_sidebar_frame,
            text="🔍",
            font=(25),
            bg="#181818",
            fg="white",
            borderwidth=0,
            activebackground="#202020"
        )
        self.Search_button.pack(side="right", pady=10, padx=10)

        self.Add_button = tk.Button(
            self.Bottom_sidebar_frame,
            text="➕",
            font=(25),
            bg="#181818",
            fg="white",
            activebackground="#202020",
            borderwidth=0,
            command=self.Add_button_function
        )
        self.Add_button.pack(side="left", expand=True, anchor="center", pady=10)

        

    def Add_button_function(self):
        open_new_window=tk.Toplevel(self.window)
        open_new_window.title("Add Note")
        open_new_window.geometry("1200x700")
        open_new_window.configure(bg="#212121")

        Top_sidebar_frame = tk.Frame(open_new_window, height=60, bg='#181818')
        Top_sidebar_frame.pack(side="top", fill="x")

        category_label = tk.Label(
            Top_sidebar_frame, 
            text="Select Category:", 
            font=('Arial Rounded MT Bold', 12),
            bg='#181818', 
            fg='white')
        category_label.pack(side="left", padx=(20,10), pady=10)

        # Create a style object
        category_dropdown_colour = ttk.Style()

        # Configure the Combobox style
        category_dropdown_colour.configure(
            "Custom.TCombobox",  # Custom style name
            background="black",  # Background color of the combobox
            foreground="white",  # Text color
            fieldbackground="black"  # Background color of the dropdown list
        )

        category_type = tk.StringVar()
        category_dropdown = ttk.Combobox(
            Top_sidebar_frame, 
            textvariable=category_type,
            values=["Financial Plans", "Investment Opportunities", "Receipts"],
            state="readonly",  # Prevents manual text entry
            width=30,
            style="Custom.TCombobox"
            )
        category_dropdown.pack(side="left", padx=10, pady=10)

        #called function when the button is clicked
        def no_image_button_click():
            insert_picture(note_text_box)

        Picture_button = tk.Button(
            Top_sidebar_frame, 
            text="🖼️", 
            font=(25),
            bg='#181818', 
            fg='white', 
            borderwidth=0,
            activebackground='#202020',
            command=no_image_button_click
            )
        Picture_button.pack(side="right", pady=10, padx=10)

        def on_color_button_click():
            choose_text_colour(note_text_box)

        Colour_button = tk.Button(
            Top_sidebar_frame, 
            text="🎨", 
            font=(25),
            bg='#181818', 
            fg='white', 
            borderwidth=0,
            activebackground='#202020',
            command=on_color_button_click
            )
        Colour_button.pack(side="right", pady=10, padx=30)

        Undo_button = tk.Button(
            Top_sidebar_frame, 
            text="↻", 
            font=("Arial", 25),
            bg='#181818', 
            fg='white', 
            borderwidth=0,
            activebackground='#202020'
            )
        Undo_button.pack(side="right", pady=10, padx=10)

        Redo_button = tk.Button(
            Top_sidebar_frame, 
            text="↺", 
            font=("Arial", 25),
            bg='#181818', 
            fg='white', 
            borderwidth=0,
            activebackground='#202020'
            )
        Redo_button.pack(side="right", pady=10, padx=20)

        save_buttonn = tk.Button(
            Top_sidebar_frame,
            text="💾",
            font=(25),
            bg="#181818",
            fg="white",
            borderwidth=0,
            activebackground="#202020",
            command=lambda: save_note(note_text_box, tag_text_box, category_dropdown)
        )   
        save_buttonn.pack(side="right", pady=15, padx=30)
        
        tag_text_box_label = tk.Label(
            open_new_window,
            text="Tags: ",
            font=("Arial", 13, "bold"),
            bg="#212121",
            fg="white"
        )
        tag_text_box_label.pack(pady=10)

        tag_text_box = tk.Text(
            open_new_window,
            height=3,
            width=123,
            bg="#292929", 
            fg="white",
            font=("Arial", 14),
            wrap=tk.WORD,
            borderwidth=2,
            relief=tk.SUNKEN #Border style
        )
        tag_text_box.pack(padx=10, pady=(5, 10))
        # # To insert text
        # tag_text_box.insert(tk.END, "Initial text")
        # # To get the text
        # tag_text_content = tag_text_box.get("1.0", tk.END)
        # # To clear the text
        # tag_text_box.delete("1.0", tk.END)

        note_text_box_label = tk.Label(
            open_new_window,
            text="Note: ",
            font=("Arial", 13, "bold"),
            bg="#212121",
            fg="white"
        )
        note_text_box_label.pack(pady=10)

        note_text_box = tk.Text(
            open_new_window,
            height=30,
            width=150,
            bg="#292929", 
            fg="white",
            font=("Arial", 14),
            wrap=tk.WORD,
            borderwidth=2,
            relief=tk.SUNKEN #Border style
        )
        note_text_box.pack(padx=10, pady=(5, 10))
        # # To insert text
        # note_text_box.insert(tk.END, "Initial text")
        # # To get the text
        # note_text_content = note_text_box.get("1.0", tk.END)
        # # To clear the text
        # note_text_box.delete("1.0", tk.END)

        def insert_picture(note_text_box):
            image_file_location = filedialog.askopenfilename(
                title='Select Image', 
                filetype=[
                    ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("All files", "*.*")
                ]
            )

            if not image_file_location:
                return
            
            try:
                #Open the image
                img = Image.open(image_file_location)

                #Resize image if it's too large 
                max_width = 600
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.LANCZOS)
                #Convert to photo image
                photo = ImageTk.PhotoImage(img)
                #Insert picture into note_text_box
                note_text_box.image_create(tk.END, image=photo)
                # Keep a reference to prevent garbage collection
                if not hasattr(note_text_box, 'images'):
                    note_text_box.images = []
                note_text_box.images.append(photo)

                #Insert a newline after Image
                note_text_box.insert(tk.END, '\n')

            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {str(e)}")

        def choose_text_colour(note_text_box):
            color = colorchooser.askcolor(title="Choose text color")[1]

            if color:   
                #Try to change text color in tags box
                try:
                    start = note_text_box.index(tk.SEL_FIRST)
                    end = note_text_box.index(tk.SEL_LAST)
                    # Create a unique tag name for this color
                    tag_name = f"color_{color}"
                    #Apply colour in tags box
                    note_text_box.tag_add("colored", start, end)
                    note_text_box.tag_configure("colored", foreground=color)

                except tk.TclError:
                    #No text selected, apply to future typing
                    tag_name = f"color_{color}"
                    note_text_box.tag_configure(tag_name, foreground=color)
                    # Get the current cursor position
                    current_pos = note_text_box.index(tk.INSERT)
                    # Set the default tag for future text input
                    note_text_box.tag_add(tag_name, current_pos)

        # Collect text color information
        def collect_color_data(note_text_box):
            color_info = []
            # Get all tags in the text box
            all_tags = note_text_box.tag_names()
            # Filter tags that start with "color_"
            color_tags = [tag for tag in all_tags if tag.startswith("color_")]
            for tag in color_tags:
                    start = "1.0"
                    while True:
                        try:
                            # Find text ranges with this color tag
                            start_index = note_text_box.tag_nextrange(tag, start)[0]
                            end_index = note_text_box.tag_nextrange(tag, start)[1]
                            
                            # Get the colored text
                            colored_text = note_text_box.get(start_index, end_index)
                            color = tag.split("_")[1]
                            
                            color_info.append({
                                "color": color,
                                "text": colored_text,
                                "start_index": start_index,
                                "end_index": end_index
                            })
                            
                            # Move start to continue searching
                            start = end_index
                        except tk.TclError:
                            # No more ranges found
                            break
            return color_info

        def save_note(note_text_box, tag_text_box, category_dropdown):
            """
            Advanced note saving function that comprehensively stores text colors and images
            
            Args:
            - note_text_box: Tkinter Text widget containing the note content
            - tag_text_box: Tkinter Text widget containing tags
            - category_dropdown: Tkinter Combobox for category selection
            """
            # Get the note content
            note_content = note_text_box.get("1.0", tk.END).strip()
            # Get tags
            tags_content = tag_text_box.get("1.0", tk.END).strip()
            # Get category
            category = category_dropdown.get()
            
            # If no content, return
            if not note_content:
                messagebox.showwarning("Warning", "No content to save.")
                return
            
            # Prepare save directory
            save_directory = r"D:\School\YEAR 1 SEM 2\Software Development Fundation\SOFTWARE-DEVELOPMENT-ASSIGNMENT\Notes"
            os.makedirs(save_directory, exist_ok=True)
            
            # Prepare note data dictionary
            note_data = {
                "category": category,
                "tags": tags_content.split(',') if tags_content else [],
                "content": note_content,
                "text_colors": [],
                "images": []
            }
            
            # Collect color information (debugging print)
            color_data = collect_color_data(note_text_box)
            print("Collected color data:", color_data)  # This will print the color information to console
            
            # Add the collected color data to note_data
            note_data["text_colors"] = color_data
            
            # Collect image information
            def collect_and_save_images():
                image_details = []
                if hasattr(note_text_box, 'images'):
                    for img in note_text_box.images:
                        try:
                            # Generate a unique filename
                            image_filename = f"note_image_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
                            image_path = os.path.join(save_directory, "images", image_filename)
                            
                            # Create images directory if it doesn't exist
                            os.makedirs(os.path.join(save_directory, "images"), exist_ok=True)
                            
                            # Save the image
                            # Note: This assumes the image is a PhotoImage from Tkinter
                            # You might need to convert it to a PIL Image first
                            pil_image = ImageTk.getimage(img)
                            pil_image.save(image_path)
                            
                            # Optionally, create a base64 encoded version for easier storage
                            buffered = io.BytesIO()
                            pil_image.save(buffered, format="PNG")
                            
                            image_details.append({
                                "filename": image_filename,
                                "path": image_path,
                                "width": pil_image.width,
                                "height": pil_image.height
                            })
                        
                        except Exception as e:
                            print(f"Error saving image: {e}")
                
                return image_details
            
            # Collect and store image information
            note_data["images"] = collect_and_save_images()
            
            # Prepare notes file path
            notes_file_path = os.path.join(save_directory, "notes.json")
            
            try:
                # Read existing notes or create new list
                if os.path.exists(notes_file_path):
                    with open(notes_file_path, 'r', encoding='utf-8') as f:
                        try:
                            notes = json.load(f)
                        except json.JSONDecodeError:
                            notes = []
                else:
                    notes = []
                
                # Add new note
                notes.append(note_data)
                
                # Save updated notes
                with open(notes_file_path, 'w', encoding='utf-8') as f:
                    json.dump(notes, f, indent=4, ensure_ascii=False)
                
                # Optional: Clear the text boxes after saving
                note_text_box.delete('1.0', tk.END)
                tag_text_box.delete('1.0', tk.END)
                
                messagebox.showinfo("Success", "Note saved successfully!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Could not save note: {str(e)}")

def note():
    #root = Tk()
    app = NotesOrganizer()
    app.run()

if __name__ == "__main__":
    note()
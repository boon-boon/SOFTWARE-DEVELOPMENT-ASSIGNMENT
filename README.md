# Financial Management Application

A comprehensive desktop application built with Python and Tkinter that helps users manage their finances, set reminders, and organize notes all in one place.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 💰 Expense Tracker
- Track your income and expenses across multiple categories
- Manage multiple asset types (Cash, Bank Account, Debit Card, Touch N Go, Stock)
- Categorize expenses (Food, Transportation, Education, Entertainment, Utilities, etc.)
- Visual representation of financial data
- Home page with financial overview
- Dedicated assets management page

### 🔔 Reminder App
- Set and manage reminders for important tasks and deadlines
- Persistent storage of reminder data
- User-friendly interface for creating, viewing, and managing reminders

### 📝 Note Organizer
- Create and organize notes efficiently
- Simple and intuitive note-taking interface
- Persistent storage for all your notes

### 🎨 Modern UI/UX
- Sleek dark-themed interface
- Animated sidebar navigation
- Expandable menu sections
- Visual indicators for active sections
- Icon-based navigation for better user experience

## 🚀 Installation

### Prerequisites
- Python 3.x installed on your system
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SOFTWARE-DEVELOPMENT-ASSIGNMENT.git
   cd SOFTWARE-DEVELOPMENT-ASSIGNMENT
   ```

2. **Install required dependencies**
   ```bash
   pip install pillow
   ```

3. **Run the application**
   ```bash
   python Main_Menu.py
   ```

## 📖 Usage

### Starting the Application
Simply run the main menu file:
```bash
python Main_Menu.py
```

### Navigation
1. **Sidebar Menu**: Click the menu icon (☰) in the top navigation bar to expand/collapse the sidebar
2. **Expense Tracker**: Click the wallet icon to access expense tracking features
   - **Home**: View financial overview and summary
   - **Assets**: Manage your financial assets
3. **Reminder**: Click the bell icon to manage your reminders
4. **Notes**: Click the note icon to access your note organizer

### Features in Detail

#### Expense Tracker
- Add new income or expense transactions
- Categorize your transactions
- View financial summaries and analytics
- Manage multiple asset accounts

#### Reminder App
- Create new reminders with dates and descriptions
- View upcoming reminders
- Mark reminders as complete
- Edit or delete existing reminders

#### Note Organizer
- Create new notes
- Organize notes by categories
- Edit and delete notes
- Search through your notes

## 📁 Project Structure

```
SOFTWARE-DEVELOPMENT-ASSIGNMENT/
│
├── Main_Menu.py                    # Main application entry point
├── Final_Expense_Tracker.py        # Expense tracker module
├── Reminder.py                     # Reminder application module
├── Note_Organizer.py               # Note organizer module
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore file
│
├── icon/                           # Application icons
│   ├── menu.png
│   ├── expense.png
│   ├── bell.png
│   ├── note.png
│   └── down.png
│
└── Expense_Tracker_Photo/          # Expense tracker UI images
    ├── Bank_Icon.png
    ├── Cash_Icon.png
    ├── Debit_Card_Icon.png
    ├── Food_Icon.png
    ├── Bus_Icon.png
    ├── Education_Icon.png
    ├── Entertainment_Icon.png
    ├── Utilities_Icon.png
    └── ... (and more category icons)
```

## 🛠️ Technologies Used

- **Python 3.x**: Core programming language
- **Tkinter**: GUI framework for creating the desktop application
- **PIL (Pillow)**: Image processing library for handling icons and images
- **File I/O**: For persistent data storage

## 🎨 Color Scheme

The application uses a modern dark theme:
- **Sidebar Background**: `#1a1c1e`
- **Top Navigation**: `#1E1E1E`
- **Content Area**: `#0D0D0D`

## 📸 Screenshots

> [!NOTE]
> Add screenshots of your application here to showcase the UI and features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is created as part of a software development assignment.

## 👨‍💻 Author

**Lee Boon Yew**

## 🙏 Acknowledgments

- Icons and images used in the application
- Tkinter documentation and community
- Python community

---

**Note**: Make sure all required image files are present in the `icon/` and `Expense_Tracker_Photo/` directories before running the application.

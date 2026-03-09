# Library Management System

This is a simple web-based library management application built with Python Flask and MongoDB. It provides features for administrators and users to manage books, borrow/return operations, and renewals.

## 🚀 Features

- 📚 **Add Books**: Admins can add new titles to the library
- 📖 **Borrow Books**: Users can borrow available books (log in required)
- 🔁 **Return Books**: Users return borrowed books to increase stock
- 🔄 **Renew Books**: Track due dates and renew borrowed books
- 🎯 **Borrowed-Book Tracking**: Remaining days until due shown with alerts
- ✅ **Success Pop-ups**: Visual feedback for each operation with green ticks
- 🎨 **Modern UI**: Stylish fonts (Roboto & Poppins), cards, modals, responsive layout

## 📁 Project Structure

```
app.py
static/
  └─ style.css
templates/
  ├─ add_book.html
  ├─ borrow.html
  ├─ dashboard.html
  ├─ login.html
  ├─ return.html
  ├─ renewal.html
  └─ signup.html
```

## 🛠️ Requirements

- Python 3.7+
- Flask
- PyMongo (MongoDB driver)
- MongoDB running locally (default URI `mongodb://localhost:27017/`)

## ⚙️ Setup & Installation
1. **Clone the repository**
    ```bash
    git clone <repo-url> library-app
    cd library-app
    ```
2. **Create a virtual environment (optional but recommended)**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    ```
3. **Install dependencies**
    ```bash
    pip install flask pymongo
    ```
4. **Run MongoDB**
    Ensure MongoDB is running locally. You can download and start it using the community edition.

5. **Start the application**
    ```bash
    python app.py
    ```
    Visit `http://127.0.0.1:5000/` in your browser.

## 🧠 Usage

- **Signup**: Create a new user via the signup page.
- **Login**: Use your credentials to access the dashboard.
- **Add Books**: Navigate to "Add Books" in the sidebar.
- **Borrow/Return/Renew**: Fill the forms and follow prompts; you will see pop-ups for success and due alerts.

## 📝 Notes

- The application stores user credentials and book data in MongoDB collections: `users`, `books`, and `borrowed_books`.
- Borrowed book entries track `borrow_date` and `due_date` to calculate remaining days.
- No password hashing currently implemented (not for production use).

## 🛡️ Future Improvements

- Add password hashing and validation
- Enable role-based access control for admins and users
- Implement search and filtering for books
- Add pagination and mobile responsiveness
- Unit tests and error handling

## 📄 License

This project is provided as-is, without warranty. Feel free to use and modify the code for learning or personal projects.

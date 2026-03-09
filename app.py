from flask import Flask, render_template, request, redirect, session, flash
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "librarysecret"

client = MongoClient("mongodb://localhost:27017/")
db = client["libraryDB"]

users = db["users"]
books = db["books"]
borrowed_books = db["borrowed_books"]

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_user():
    user_id = request.form["userid"]
    password = request.form["password"]

    user = users.find_one({"userid": user_id, "password": password})

    if user:
        session["user"] = user_id
        return redirect("/dashboard")

    return "Invalid Login"

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/register", methods=["POST"])
def register():
    userid = request.form["userid"]
    password = request.form["password"]

    users.insert_one({
        "userid": userid,
        "password": password
    })

    return redirect("/")

@app.route("/dashboard")
def dashboard():
    all_books = list(books.find())
    return render_template("dashboard.html", books=all_books)

@app.route("/add_book_page")
def add_book_page():
    return render_template("add_book.html")


@app.route("/add_book", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    count = int(request.form["count"])

    books.insert_one({
        "title": title,
        "author": author,
        "count": count
    })

    flash("Book added successfully!", "success")
    return redirect("/dashboard")

@app.route("/borrow")
def borrow_page():
    return render_template("borrow.html")


@app.route("/borrow_book", methods=["POST"])
def borrow_book():

    userid = request.form["userid"]
    password = request.form["password"]
    title = request.form["title"]

    user = users.find_one({"userid": userid, "password": password})
    book = books.find_one({"title": title})

    if user and book and book["count"] > 0:
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)
        
        borrowed_books.insert_one({
            "userid": userid,
            "title": title,
            "borrow_date": borrow_date,
            "due_date": due_date
        })
        
        flash("Book borrowed successfully!", "success")
        books.update_one({"title": title}, {"$inc": {"count": -1}})
        return redirect("/dashboard")

    return "Borrow Failed"

@app.route("/return")
def return_page():
    return render_template("return.html")


@app.route("/return_book", methods=["POST"])
def return_book():

    userid = request.form["userid"]
    password = request.form["password"]
    title = request.form["title"]

    user = users.find_one({"userid": userid, "password": password})

    if user:
        flash("Book returned successfully!", "success")
        books.update_one({"title": title}, {"$inc": {"count": 1}})
        return redirect("/dashboard")

    return "Return Failed"

@app.route("/renewal")
def renewal_page():
    if "user" not in session:
        return redirect("/")
    
    userid = session["user"]
    borrowed = list(borrowed_books.find({"userid": userid}))
    
    # Calculate remaining days for each borrowed book
    for book in borrowed:
        remaining = (book["due_date"] - datetime.now()).days
        book["remaining_days"] = max(remaining, 0)
    
    return render_template("renewal.html", borrowed_books=borrowed)


@app.route("/renew_book", methods=["POST"])
def renew_book():

    userid = request.form["userid"]
    password = request.form["password"]
    title = request.form["title"]

    user = users.find_one({"userid": userid, "password": password})
    borrowed = borrowed_books.find_one({"userid": userid, "title": title})

    if user and borrowed:
        new_due_date = datetime.now() + timedelta(days=14)
        borrowed_books.update_one(
            {"userid": userid, "title": title},
            {"$set": {"due_date": new_due_date}}
        )
        flash("Book renewed successfully!", "success")
        return redirect("/renewal")

    return "Renewal Failed"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
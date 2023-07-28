from flask import render_template, session, request, redirect
from app import *
from model import *

@app.route("/")
def index():
    if "user_id" in session: 
        return render_template("index.html")
    else:
        return redirect("/sign-in")

@app.route("/sign-in")
def sign_in(): 
    if "user_id" in session:
        userid = session["user_id"]
        return render_template("index.html")
    return render_template("sign-in.html")

@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")

@app.route("/login_authentication", methods=["POST"])             #
def login():
    if(request.method=="POST"):
        cemail = request.form.get("email")
        cpassword = request.form.get("password")
        user = User.query.filter_by(email=cemail, password=cpassword)
        check = [i for i in user]
        if check:
            session["user_id"] = check[0].id
            print(session["user_id"])
            print("authentication done")
            return redirect("/")
        else:
            print("not found")
            return redirect("/sign-in")
    else:
        return "bad request"
    
@app.route("/logout", methods=["POST"])
def logout():
    if(request.method=="POST"):
        session.pop("user_id")
        print("logout")
        return redirect("sign-in")
    else:
        if("user_id" in session):
            return redirect("/")
        else:
            return redirect("/sign-in")

@app.route('/register', methods=["POST"])
def register():
    if(request.method == "POST"):
        try:
            cname = request.form.get("name")
            caddress = request.form.get("address")
            ccontact = request.form.get("contact_no")
            cemail = request.form.get("email")
            cpassword = request.form.get("password")
            csex = request.form.getlist("sex")
            for i in csex[:1]:
                update_user_db = User(name=cname, address=caddress, contact_no=ccontact, email=cemail, password=cpassword, sex=i)
            db.session.add(update_user_db)
            db.session.flush()
        except Exception as e:
            print("rollback")
            db.session.rollback()
            return "{}".format(e),"Not Registered"
        else:
            db.session.commit()
            user = User.query.filter_by(email=cemail, password=cpassword)
            check = [i for i in user]
            if check:
                session["user_id"] = check[0].id
                return redirect("/")

@app.route("/category")
def category():
    if "user_id" in session:
        category = Category.query.all()
        check = [i for i in category]
        return render_template("category.html", all_categories = check)
    else:
        return redirect("/sign-in")
    
@app.route("/product")
def product():
    if "user_id" in session:
        product = Product.query.all()
        check = [i for i in product]
        return render_template("product.html", all_products = check)
    else:
        return redirect("/sign-in")
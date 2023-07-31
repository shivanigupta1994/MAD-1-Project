from flask import render_template, session, request, redirect
from app import *
from model import *

@app.route("/")
def index():
    if "user_id" in session: 
        return render_template("index.html", flag=False)
    else:
        return redirect("/sign-in")

@app.route("/sign-in")
def sign_in(): 
    if "user_id" in session:
        userid = session["user_id"]
        return render_template("index.html", flag=False)
    return render_template("sign-in.html", flag=False)

@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html", flag=False)

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
        return render_template("category.html", all_categories = check, flag=False)
    else:
        return redirect("/sign-in")
    
@app.route("/product/<int:i>")
def product(i):
    if "user_id" in session:
        product = Product.query.filter_by(category=i)
        check = [i for i in product]
        return render_template("product.html", all_products = check, flag=False)
    else:
        return redirect("/sign-in")
    
@app.route("/cart")
def cart():
    if "user_id" in session:
        cart = Cart.query.filter_by(user_id=session["user_id"])
        cart_list = [i for i in cart]
        pro_list = []
        total_price = 0
        for item in cart_list:
            pro = Product.query.filter_by(id=item.product_id).first()
            pro_list.append((pro.name, item.product_qty, pro.price_per_unit, pro.category, pro.image, pro.brand, int(pro.price_per_unit)*int(item.product_qty), item.cart_id ))
            print(pro.name, item.product_qty, pro.price_per_unit, pro.category, pro.image, pro.brand)
        for price in pro_list:
            total_price += int(price[6])
        return render_template("cart.html", product_list = pro_list , flag=False, cart_total=total_price)
    else:
        return redirect("/sign-in")
    
@app.route("/remove_from_cart/<int:id>")
def remove_from_cart(id):
    if "user_id" in session:
        Cart.query.filter_by(user_id=session["user_id"], cart_id=id).delete()
        db.session.flush()
        db.session.commit()
        return redirect("/cart")
    else:
        return redirect("/sign-in")
    
@app.route("/add_to_cart/<int:id>", methods=["POST"])
def add_to_cart(id):
    if "user_id" in session:
        prod=Product.query.filter_by(id=id).first()
        cart = Cart.query.filter_by(user_id=session["user_id"], product_id=id).first()
        qty = request.form.get("quantity")
        if (cart):
            cart.product_qty += int(qty)
            db.session.flush()
            db.session.commit()
            return redirect(f"/product/{prod.category}")
        else:
            new_cart_item=Cart(user_id=session["user_id"], product_id=id, product_qty=qty)
            db.session.add(new_cart_item)
            db.session.commit()
            return redirect(f"/product/{prod.category}")
    else:
        return redirect("/sign-in")
        
            





        
        
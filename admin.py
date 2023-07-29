from flask import render_template, session, request, redirect
from app import *
from model import *
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/cms")
def admin_index():
    if "admin_id" in session: 
        return render_template("admin_index.html")
    else:
        return redirect("/admin_sign-in")

@app.route("/admin_sign-in")
def admin_sign_in(): 
    if "admin_id" in session:
        adminid = session["admin_id"]
        return redirect ("/cms")
    return render_template("admin_sign-in.html")

@app.route("/admin_sign-up")
def admin_sign_up():
    return render_template("admin_sign-up.html")

@app.route("/admin_login_authentication", methods=["POST"])             #
def admin_login():
    if(request.method=="POST"):
        cemail = request.form.get("email")
        cpassword = request.form.get("password")
        admin = Admin.query.filter_by(email=cemail, password=cpassword)
        check = [i for i in admin]
        if check:
            session["admin_id"] = check[0].id
            print(session["admin_id"])
            print("authentication done")
            return redirect("/cms")
        else:
            print("not found")
            return redirect("/admin_sign-in")
    else:
        return "bad request"
    
@app.route("/admin_logout", methods=["POST"])
def admin_logout():
    if("admin_id") in session:
        if(request.method=="POST"):
            session.pop("admin_id")
            print("logout")
            return redirect("admin_sign-in")
        else:
            return "Bad request...Please give only POST request instead of {}".format(request.method) 
    else:
        return redirect("/admin_sign-in")

@app.route('/admin_register', methods=["POST"])
def admin_register():
    if(request.method == "POST"):
        try:
            cname = request.form.get("name")
            ccontact = request.form.get("contact_no")
            cemail = request.form.get("email")
            cpassword = request.form.get("password")
            csex = request.form.getlist("sex")
            for i in csex[:1]:
                update_admin_db = Admin(name=cname, contact_no=ccontact, email=cemail, password=cpassword, sex=i)
            db.session.add(update_admin_db)
            db.session.flush()
        except Exception as e:
            print("rollback")
            db.session.rollback()
            return "{}".format(e),"Not Registered"
        else:
            db.session.commit()
            admin = Admin.query.filter_by(email=cemail, password=cpassword)
            check = [i for i in admin]
            if check:
                session["admin_id"] = check[0].id
                return redirect("/cms")
            
@app.route("/admin_category_cms")
def admin_category_cms():
    if "admin_id" in session:
        category = Category.query.all()
        check = [i for i in category]
        return render_template("admin_category_cms.html", all_categories = check)
    else:
        return redirect("/admin_sign-in")
    
@app.route("/admin_product_cms")
def admin_product_cms():
    if "admin_id" in session:
        product = Product.query.all()
        check = [i for i in product]
        return render_template("admin_product_cms.html", all_products = check)
    else:
        return redirect("/admin_sign-in")
    
@app.route("/admin_category_add", methods=["GET", "POST"])
def admin_category_add():
    if "admin_id" in session:
        if request.method=="POST":
            category_name=request.form['category_name']
            password=request.form['password']
            file = request.files['file']
            filename = None
            if (file and allowed_file(file.filename)):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
            admin_check = [i for i in verify_admin]
            if admin_check:
                if filename is not None:
                    image = "/static/"+filename
            new_category=Category(name=category_name, image=image)
            db.session.add(new_category)
            db.session.flush()
            db.session.commit()
            return redirect("/admin_category_cms")
        return render_template("admin_category_add.html")
    
@app.route("/admin_product_add", methods=["GET", "POST"])
def admin_product_add():
    if "admin_id" in session:
        if request.method=="POST":
            product_name=request.form['product_name']
            product_category=request.form['product_category']
            product_brand=request.form['product_brand']
            product_mfg_date=request.form['product_mfg_date']
            product_exp_date=request.form['product_exp_date']
            product_unit=request.form['product_unit']
            product_qty=request.form['product_qty']
            product_price_per_unit=request.form['product_price_per_unit']
            password=request.form['password']
            file = request.files['file']
            filename = None
            if (file and allowed_file(file.filename)):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
            admin_check = [i for i in verify_admin]
            if admin_check:
                if filename is not None:
                    image = "/static/"+filename
            new_product=Product(name=product_name, category=product_category, brand=product_brand, mfg_date=product_mfg_date, exp_date=product_exp_date, unit=product_unit, qty=product_qty, price_per_unit=product_price_per_unit, image=image)
            db.session.add(new_product)
            db.session.flush()
            db.session.commit()
            return redirect("/admin_product_cms")
        return render_template("admin_product_add.html")
    
    
@app.route("/admin_category_edit/<int:id>")
def admin_category_edit(id):
    if "admin_id" in session:
        category = Category.query.filter_by(id=id)
        check = [i for i in category]
        return render_template("admin_category_edit.html", category_info=check[0])
    else:
        return redirect("/admin_sign-in")

@app.route("/admin_category_update/<int:id>", methods=["POST"])
def admin_category_update(id):
    if "admin_id" in session:
        category_name = request.form.get("category_name")
        password = request.form.get("password")
        file = request.files['file']
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
        admin_check = [i for i in verify_admin]
        category = Category.query.filter_by(id=id)
        check = [i for i in category]
        if admin_check:
            check[0].name = category_name
            if filename is not None:
                check[0].image = "/static/"+filename
            db.session.flush()
            db.session.commit()
            return redirect("/admin_category_cms")
        else:
            return "Wrong Password!"
    else:
        return redirect("/admin_sign-in")

@app.route("/admin_product_edit/<int:id>")
def admin_product_edit(id):
    if "admin_id" in session:
        product = Product.query.filter_by(id=id)
        check = [i for i in product]
        return render_template("admin_product_edit.html", product_info=check[0])
    else:
        return redirect("/admin_sign-in")

@app.route("/admin_product_update/<int:id>", methods=["POST"])
def admin_product_update(id):
    if "admin_id" in session:
        product_name = request.form.get("product_name")
        password = request.form.get("password")
        file = request.files['file']
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        verify_admin = Admin.query.filter_by(id=session["admin_id"], password=password)
        admin_check = [i for i in verify_admin]
        product = Product.query.filter_by(id=id)
        check = [i for i in product]
        if admin_check:
            check[0].name = product_name
            if filename is not None:
                check[0].image = "/static/"+filename
            db.session.flush()
            db.session.commit()
            return redirect("/admin_product_cms")
        else:
            return "Wrong Password!"
    else:
        return redirect("/admin_sign-in")

@app.route("/admin_category_delete/<int:id>")
def admin_category_delete(id):
    if "admin_id" in session:
        Product.query.filter_by(category=id).delete()
        Category.query.filter_by(id=id).delete()
        db.session.flush()
        db.session.commit()
    return redirect("/admin_category_cms")

@app.route("/admin_product_delete/<int:id>")
def admin_product_delete(id):
    if "admin_id" in session:
        Product.query.filter_by(id=id).delete()
        db.session.flush()
        db.session.commit()
    return redirect("/admin_product_cms")



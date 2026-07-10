from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_

from forms import AddPasswordForm, EditPasswordForm, LoginForm, RegistrationForm
from models import Password, User, db
from utils import decrypt_password, encrypt_password, generate_password, hash_password, verify_password

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            password_hash=hash_password(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and verify_password(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Welcome back!", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


@main.route("/dashboard")
@login_required
def dashboard():
    search_query = request.args.get("search", "", type=str).strip()
    query = Password.query.filter_by(user_id=current_user.id)

    if search_query:
        query = query.filter(or_(Password.website.ilike(f"%{search_query}%"), Password.username.ilike(f"%{search_query}%")))

    passwords = query.order_by(Password.created_at.desc()).all()
    return render_template("dashboard.html", passwords=passwords, search_query=search_query)


@main.route("/passwords/add", methods=["GET", "POST"])
@login_required
def add_password():
    form = AddPasswordForm()
    if form.validate_on_submit():
        password_entry = Password(
            website=form.website.data.strip(),
            username=form.username.data.strip(),
            encrypted_password=encrypt_password(form.password.data),
            user_id=current_user.id,
        )
        db.session.add(password_entry)
        db.session.commit()
        flash("Password added successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("add_password.html", form=form)


@main.route("/passwords/<int:password_id>/edit", methods=["GET", "POST"])
@login_required
def edit_password(password_id):
    password_entry = Password.query.get_or_404(password_id)
    if password_entry.user_id != current_user.id:
        flash("You cannot edit that password.", "danger")
        return redirect(url_for("main.dashboard"))

    form = EditPasswordForm(obj=password_entry)
    if form.validate_on_submit():
        password_entry.website = form.website.data.strip()
        password_entry.username = form.username.data.strip()
        if form.password.data:
            password_entry.encrypted_password = encrypt_password(form.password.data)
        db.session.commit()
        flash("Password updated successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("edit_password.html", form=form, password_entry=password_entry)


@main.route("/passwords/<int:password_id>/delete", methods=["POST"])
@login_required
def delete_password(password_id):
    password_entry = Password.query.get_or_404(password_id)
    if password_entry.user_id != current_user.id:
        flash("You cannot delete that password.", "danger")
        return redirect(url_for("main.dashboard"))

    db.session.delete(password_entry)
    db.session.commit()
    flash("Password deleted successfully.", "success")
    return redirect(url_for("main.dashboard"))


@main.route("/passwords/<int:password_id>/show")
@login_required
def show_password(password_id):
    password_entry = Password.query.get_or_404(password_id)
    if password_entry.user_id != current_user.id:
        flash("You cannot view that password.", "danger")
        return redirect(url_for("main.dashboard"))

    decrypted = decrypt_password(password_entry.encrypted_password)
    flash(f"Password: {decrypted}", "warning")
    return redirect(url_for("main.dashboard"))


@main.route("/generate-password", methods=["GET", "POST"])
@login_required
def generate_password_view():
    generated_password = None
    if request.method == "POST":
        try:
            generated_password = generate_password(
                length=int(request.form.get("length", 16)),
                use_uppercase=bool(request.form.get("uppercase")),
                use_lowercase=bool(request.form.get("lowercase")),
                use_numbers=bool(request.form.get("numbers")),
                use_symbols=bool(request.form.get("symbols")),
            )
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template("dashboard.html", generated_password=generated_password, passwords=Password.query.filter_by(user_id=current_user.id).order_by(Password.created_at.desc()).all(), search_query=request.args.get("search", ""))

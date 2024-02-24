from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if account with email exists in database
        user = User.query.filter_by(email=email).first()
        if user:
            # check password
            if check_password_hash(user.password, password):
                # flash('Logged in successfully', category='success')
                login_user(user, remember=True)  # remembers user is logged in
                return redirect(url_for("views.home"))

            else:
                flash("Incorrect password", category="error")
        else:
            flash(
                "No account associated with this email, please sign-up",
                category="error",
            )

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash(
                "Account with this email already exists, please log in instead",
                category="error",
            )
        elif len(email) < 4 or "@" not in email or "." not in email:
            flash("Invalid email adress", category="error")
        elif len(password1) < 4:
            flash("Password must be atleast 4 characters long", category="error")
        elif password2 != password1:
            flash("Passwords dont match", category="error")
        elif len(first_name) < 2:
            flash("First name must be atleast 2 charecters long", category="error")
        else:
            # create new user account
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method="pbkdf2:sha256"),
            )
            # add user to database
            db.session.add(new_user)
            db.session.commit()

            # login user
            flash("Account created successully", category="success")
            login_user(new_user, remember=True)  # remembers user is logged in
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)

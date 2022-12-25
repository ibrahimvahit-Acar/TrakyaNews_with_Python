from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from webscraping import sozcuData


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/ekonomi", methods=['GET', 'POST'])
@login_required
def ekonomi():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/ekonomi/", "news-item", value)
    return render_template('ekonomi.html', myNews=myNews, title="Ekonomi Haberleri")


@app.route("/guncel", methods=['GET', 'POST'])
@login_required
def guncel():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/son-dakika/", "timeline-card", value)
    return render_template('guncel.html', myNews=myNews, title="Güncel Haberler")


@app.route("/spor", methods=['GET', 'POST'])
@login_required
def spor():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/spor/", "news-item", value)

    return render_template('spor.html', myNews=myNews, title="Spor Haberleri")


@app.route("/dunya", methods=['GET', 'POST'])
@login_required
def dunya():
    try:
        value = request.form['operator']
    except:
        value = 1

    myNews = sozcuData(
        "https://www.sozcu.com.tr/dunya/", "news-item", value)
    return render_template('dunya.html', myNews=myNews, title="Dünyadan Haberler")


@app.route("/hayat", methods=['GET', 'POST'])
@login_required
def hayat():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/hayatim/", "news-item", value)
        
    return render_template('hayat.html', myNews=myNews, title="Dünyadan Haberler")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Hesabınız oluşturulmuştur.Lütfen giriş yapınız', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Kayıt ol', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Lütfen emailinizi veya şifrenizi kontrol edin', 'danger')
    return render_template('login.html', title='Giriş', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Hesabım',
                           image_file=image_file, )

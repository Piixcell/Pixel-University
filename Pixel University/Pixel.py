from flask import Flask, render_template, request, redirect, url_for
import datetime, os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user, login_url

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pixel:pixel@localhost/pixel?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.engine.execute("ALTER DATABASE pixel CHARACTER SET utf8 COLLATE utf8_persian_ci")
conn = db.engine.connect()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(db.Model, UserMixin):  # One
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    isProf = db.Column(db.Boolean, default=False)  # professor = true ; student = false
    avatar = db.Column(db.String(120), nullable=True, default="null.jpg")
    posts = db.relationship('Post', backref='user', lazy='dynamic')


class Post(db.Model):  # Many
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(520), nullable=False)
    content = db.Column(db.String(520), nullable=False)
    date = db.Column(db.String(120), nullable=False, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)


tag_posts = db.Table('tag-posts', db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))


class Tag(db.Model):  # Many
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(520), nullable=False)
    posts = db.relationship('Post', secondary=tag_posts, backref='tags', lazy='dynamic')


class Category(db.Model):  # One
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(520), nullable=False)
    posts = db.relationship('Post', backref='category', lazy='dynamic')


db.drop_all()
db.create_all()
# Users
hossein = User(username='hossein', name='حسین سخاوتی', password='12345', isProf=False)
ahmadifar = User(username='ahmadifar', name='دکتر احمدی فر', password='12345', avatar='ahmadifar.jpg', isProf=True)
shakeri = User(username='shakeri', name='دکتر شاکری', password='12345', avatar='shakeri.jpg', isProf=True)
atani = User(username='atani', name='دکتر آتانی', password='12345', avatar='atani.jpg', isProf=True)
mir = User(username='mirroshandel', name='دکتر میرروشندل', password='12345', avatar='mir.jpg', isProf=True)
shekarian = User(username='shekarian', name='دکتر شکریان', password='12345', avatar='shekarian.jpg', isProf=True)
aminian = User(username='aminian', name='دکتر امینیان', password='12345', avatar='aminian.jpg', isProf=True)
db.session.add(hossein)
db.session.add(ahmadifar)
db.session.add(shakeri)
db.session.add(atani)
db.session.add(mir)
db.session.add(shekarian)
db.session.add(aminian)
# db.session.commit()

# Tags
tag_class = Tag(keyword="کلاس")
tag_hamayesh = Tag(keyword="همایش")
tag_exam = Tag(keyword="امتحان")
tag_slide = Tag(keyword="اسلاید")
tag_tamrin = Tag(keyword="تمرین")
tag_entv = Tag(keyword="انتخاب واحد")
tag_proj = Tag(keyword="پروژه")
tag_arshad = Tag(keyword="ارشد")

category_hamayesh = Category(name="همایش")
category_exam = Category(name="تاریخ امتحان")
category_public = Category(name="عمومی")
category_proj = Category(name="انجام پروژه")
category_class = Category(name="برگزاری کلاس ها")

# Posts
x1 = Post(title="کلاس فوق العاده درس مبانی کامپیوتر و برنامه سازی",
          content="کلاس فوق العاده درس مبانی کامپیوتر و برنامه سازی برای هر دو گروه دانشجویان روز سه شنبه 07/09/1396  ساعت 15-17 در آمفی تئاتر شهید نورانی دانشکده فنی برگزار می گردد.",
          user=shekarian, date="05 آذر 1396", category=category_class)
formated = str(
    "سازمان بازرسی کل کشور در نظر دارد از میان دانش آموختگان ممتاز دانشگاه در مقطع کارشناسی ارشد و دکتری در رشته و تخصص های فناوری اطلاعات، مالی، حسابداری، بانکداری ، بیمه، امورمالیاتی،گمرک و حقوق از بین داوطلبان مرد واجد شرایط به صورت امریه خدمت سربازی برای انجام فعالیت های نظارت و بازرسی دعوت به همکاری نماید.متقاضیان می توانند برای کسب اطلاع بیشتر و ثبت نام از تاریخ 15/09/1396 به سایت سازمان بازرسی کل کشور به نشانی www.bazresi.ir مراجعه نمایند.")
x2 = Post(title="امریه خدمت سربازی", content=formated, user=atani, date="3 آبان 1396", category=category_public)
x3 = Post(title="معرفی به استاد",
          content="دانشجویانی که در ترم جاری(961) معرفی به استاد اخذ کرده اند تا پایان روز یکشنبه 05/09/1396 فرصت دارند برای تعیین و تکلیف روز امتحان و منابع درسی به استاد مربوطه مراجعه نمایند،پس از این زمان گروه هیچ مسئولیتی در این مورد نخواهد داشت.y",
          user=mir, date="29 آبان 1396", category=category_exam)
x4 = Post(title="ثبت نام در وب سايت نمايشگاه فن بازار",
          content="همکاران هیات علمی و دانشجویان برای ثبت ایده و طرح های پژوهشی خود ( شامل طرح های کانون شکوفایی و خلاقیت) و طرح های پژوهشی محصول محور( ایده ، فناوری و خدمات نوآورانه )",
          user=aminian, date="22 آبان 1396", category=category_hamayesh)

x1.tags.append(tag_class)
x1.tags.append(tag_tamrin)

x2.tags.append(tag_hamayesh)
x2.tags.append(tag_arshad)

x3.tags.append(tag_entv)
x3.tags.append(tag_exam)
x3.tags.append(tag_proj)
x3.tags.append(tag_slide)

x4.tags.append(tag_hamayesh)

db.session.add(x1)
db.session.add(x2)
db.session.add(x3)
db.session.add(x4)

db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    posts = Post.query.all()
    for post in posts:
        post.content = post.content[:150] + "..."
    return render_template('index.html', x=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.HTML', x=post)


@app.route('/tag/<int:tag_id>')
def tag(tag_id):
    post = Tag.query.get_or_404(tag_id).posts
    return render_template('post.HTML', tag=post)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template('register.html')
        else:
            return redirect(url_for('index'))
    else:
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            newUser = User(username=request.form['username'], name=request.form['name'],
                           password=request.form['password'],
                           isProf=False)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return 'Error: User Exists (flash session will implement in nex' \
                   't phase :D)'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template('login.html')
        else:
            return redirect(url_for('index'))
    else:
        username = request.form['username']
        password = request.form['password']
        if username == '' or username is None:
            return "username required!"
        else:
            user = User.query.filter_by(username=username, password=password).first()
            if user is not None:
                login_user(user, remember=True)
                return redirect(request.args.get('next') or url_for('login'))
            return 'username or password is invalid'


@app.route('/add/news', methods=['GET', 'POST'])
@login_required
def get_add_news():
    if request.method == 'GET':
        cats = Category.query.all()
        tags = Tag.query.all()
        return render_template('addNews.html', cats=cats, tags=tags)
    else:
        defaultUser = User.query.get(1);
        tag = Tag.query.get(request.form['tag'])
        cat = Category.query.get(request.form['category'])
        new_post = Post(title=request.form['title'], content=request.form['content'], user=defaultUser,
                        category=cat)
        new_post.tags.append(tag)
        db.session.add(new_post)
        db.session.commit()
        posts = Post.query.all()
        for post in posts:
            post.content = post.content[:150] + "..."
        return render_template('index.html', x=posts)


@app.route('/user/<int:user_id>')
def user_info(user_id):
    user = User.query.get(user_id)
    return render_template('user.html', user=user)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/courses', methods=['GET'])
def courses():
    return render_template('course.html')


@app.route('/courses/<int:course>', methods=['GET'])
@login_required
def course(course):
    season = "بهار" if (course % 10 == 0) else "پاییز"
    year = str(course)[0:-1]
    year = year + "-" + str((int(year) + 1))
    return render_template('select.html', course=course, season=season, year=year)


@app.route('/courses/<int:course>/syllabus', methods=['GET'])
@login_required
def syllabus(course):
    season = "بهار" if (course % 10 == 0) else "پاییز"
    year = str(course)[0:-1]
    year = year + "-" + str((int(year) + 1))
    return render_template('syllabus.html', course=course, season=season, year=year)


@app.route('/courses/<int:course>/news', methods=['GET'])
@login_required
def news(course):
    season = "بهار" if (course % 10 == 0) else "پاییز"
    year = str(course)[0:-1]
    year = year + "-" + str((int(year) + 1))
    return render_template('news.html', course=course, season=season, year=year)


@app.route('/courses/<int:course>/homeworks', methods=['GET'])
@login_required
def homeworks(course):
    season = "بهار" if (course % 10 == 0) else "پاییز"
    year = str(course)[0:-1]
    year = year + "-" + str((int(year) + 1))
    return render_template('homework.html', course=course, season=season, year=year)


@app.route('/courses/<int:course>/slides', methods=['GET'])
@login_required
def slides(course):
    season = "بهار" if (course % 10 == 0) else "پاییز"
    year = str(course)[0:-1]
    year = year + "-" + str((int(year) + 1))
    return render_template('slides.html', course=course, season=season, year=year)


# @app.route('/test')
# def test():
#
#     return user.username

if __name__ == '__main__':
    app.run(port=8080)

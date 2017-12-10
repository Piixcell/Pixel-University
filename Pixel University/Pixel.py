from flask import Flask, render_template, request
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pixel:pixel@localhost/pixel?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.engine.execute("ALTER DATABASE pixel CHARACTER SET utf8 COLLATE utf8_persian_ci")


class User(db.Model):  # One
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
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
ahmadifar = User(name='دکتر احمدی فر', password='12345', avatar='ahmadifar.jpg')
shakeri = User(name='دکتر شاکری', password='12345', avatar='shakeri.jpg')
atani = User(name='دکتر آتانی', password='12345', avatar='atani.jpg')
mir = User(name='دکتر میرروشندل', password='12345', avatar='mir.jpg')
shekarian = User(name='دکتر شکریان', password='12345', avatar='shekarian.jpg')
aminian = User(name='دکتر امینیان', password='12345', avatar='aminian.jpg')
db.session.add(ahmadifar)
db.session.add(shakeri)
db.session.add(atani)
db.session.add(mir)
db.session.add(shekarian)
db.session.add(aminian)
db.session.commit()

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
          content="دانشجویانی که در ترم جاری(961) معرفی به استاد اخذ کرده اند تا پایان روز یکشنبه 05/09/1396 فرصت دارند برای تعیین و تکلیف روز امتحان و منابع درسی به استاد مربوطه مراجعه نمایند،پس از این زمان گروه هیچ مسئولیتی در این مورد نخواهد داشت.",
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


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/add/news', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(port=8080)

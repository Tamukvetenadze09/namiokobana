from extensions import app, db
import random
from flask import Flask, render_template, redirect, url_for, session, request, flash
from forms import SignupForm, PlayForm, TeamForm, LoginForm
from models import User
from flask_login import login_user, logout_user, login_required
from models import Word
from forms import AddWordForm

profiles = []

CATEGORIES = {
    "სპორტი": ["ფეხბურთი", "კალათბურთი", "ოლიმპიადა", "მესსი"],
    "მუსიკა": ["მაიკლ ჯექსონი", "გიტარა", "კონცერტი", "როკი"],
    "ისტორიული": ["დავით აღმაშენებელი", "ბრძოლა", "შუა საუკუნე", "სამეფო"],
    "მოგზაურობა": ["თბილეთი", "თრეველი", "სათხილამურო", "დასვენება"],
    "ცნობილი სახეები": ["ელონ მასკი", "შარაპოვა", "საკაშვილი", "პაპუნა"]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/rules")
def rules():
    return render_template("rules.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile")
def profile():
    user = session.get("current_user")

    if not user:
        return redirect(url_for("signup"))

    return render_template("profile.html", user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(form.email.data == User.email).first()
        if User != None:
            login_user(user)
            flash("You have been logged in")
            return redirect("/")

    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('This email is already registered. Please use another.', 'danger')
            return redirect(url_for('login'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role='user'
        )

        new_user.password = form.password.data

        db.session.add(new_user)
        db.session.commit()

        flash("Thank you for signing up. You can now login")
        return redirect("/login")

    return render_template("signup.html", form=form)


@app.route("/profile/<int:profile_id>")
def profile_id(profile_id):
    return render_template("profiles.html", profiles=profiles[profile_id])


@app.route("/playing", methods=["GET", "POST"])
def playing():
    form = TeamForm()
    if form.validate_on_submit():
        team1 = form.team1.data
        team2 = form.team2.data
        session["teams"] = [team1, team2]
        session["current_team"] = 0
        session["score"] = [0, 0]
        session["used_words"] = []
        return redirect(url_for("start_game", team1=team1, team2=team2))
    return render_template("playing.html", form=form)

    hint = session.get('hint')
    category = session.get('category')
    return render_template("start_game.html", team1=team1, team2=team2, hint=hint, category=category)


@app.route("/start/<team1>/<team2>")
def start_game(team1, team2):
    hint = session.get('hint')
    category = session.get('category')
    return render_template("start_game.html", team1=team1, team2=team2, hint=hint, category=category)


words = ["ფეხბურთი", "კალათბურთი", "ცურვა", "სერფინგი", "რაგბი", "კრივი", "ძიუდო"]


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    form = TeamForm()
    words = Word.query.all()

    if form.validate_on_submit():
        team1 = form.team1.data
        team2 = form.team2.data
        return redirect(url_for("start_game", team1=team1, team2=team2))

    return render_template("play.html", form=form)


@app.route("/result/<result>")
def result(result):
    if 'score' not in session:
        session['score'] = [0, 0]

    if result == "guessed":
        team_index = session.get('current_team', 0)
        session['score'][team_index] += 1

    return redirect(url_for("next_team"))


@app.route("/sports", methods=["GET", "POST"])
def sports():
    if "score" not in session or not isinstance(session["score"], list):
        session["score"] = [0, 0]

    if "current_team" not in session:
        session["current_team"] = 0

    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            session["score"][session["current_team"]] += 1
        session["current_team"] = 1 - session["current_team"]
        return redirect(url_for("sports"))

    selected_team = f"გუნდი {session['current_team'] + 1}"
    word = random.choice(["ფეხბურთი", "მესსი", "ოლიმპიადა", "კალათბურთი"])

    return render_template("sports.html",
                           team=selected_team,
                           word=word,
                           score=session["score"])


@app.route('/score')
def score():
    scores = session.get('scores', [0, 0])
    teams = session.get('teams', ['გუნდი 1', 'გუნდი 2'])
    rounds = session.get('rounds_played', 0)
    return render_template('score.html', scores=scores, teams=teams, rounds=rounds)


@app.route('/reset')
def reset():
    session.pop('score', None)
    session.pop('rounds_played', None)
    return redirect(url_for('game'))


@app.route('/next-team', methods=['GET', 'POST'])
def next_team():
    if request.method == 'POST':
        selected_team = request.form.get('team')
        if selected_team == '1':
            session['current_team'] = 0
        else:
            session['current_team'] = 1
        return redirect(url_for('game'))

    return render_template('next_team.html')


@app.route("/next_team2", methods=["GET", "POST"])
def next_team2():
    teams = session.get("teams", ["გუნდი 1", "გუნდი 2"])
    if request.method == "POST":
        selected_team = request.form.get("team")
        word = random.choice(words)
        return render_template("next_team2.html", team=selected_team, word=word)

    return render_template("select_team.html", teams=teams)


words = ["ფეხბურთი", "კალათბურთი", "ცურვა", "სერფინგი", "რაგბი", "კრივი", "ძიუდო"]


# @app.route("/add_word", methods=["GET", "POST"])
# @login_required
# def add_word():
#     form = AddWordForm()
#     if form.validate_on_submit():
#         word_text = form.text.data.strip()
#         if word_text:
#             new_word = Word(text=word_text)
#             db.session.add(new_word)
#             db.session.commit()
#             flash("სიტყვა წარმატებით დაემატა", "success")
#         else:
#             flash("გთხოვთ შეიყვანოთ სიტყვა", "danger")
#         return redirect(url_for("add_word"))
#     words = Word.query.all()
#     print(words)
#     return render_template("add_word.html", form=form, words=words)



@app.route('/add_word', methods=['GET', 'POST'])
@login_required
def add_word():
    form = AddWordForm()
    words = Word.query.all()

    if form.validate_on_submit():
        new_word = Word(text=form.text.data)
        db.session.add(new_word)
        db.session.commit()
        flash("სიტყვა წარმატებით დაემატა!", "success")
        return redirect(url_for('add_word'))

    return render_template('add_word.html', form=form, words=words)





@app.route("/add_wordplay", methods=["GET", "POST"])
def add_wordplay():
    if "score" not in session or not isinstance(session["score"], list):
        session["score"] = [0, 0]

    if "current_team" not in session:
        session["current_team"] = 0

    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            session["score"][session["current_team"]] += 1
        session["current_team"] = 1 - session["current_team"]
        return redirect(url_for("add_wordplay"))

    selected_team = f"გუნდი {session['current_team'] + 1}"
    word = random.choice(["კინო", "მაცივარი", "თეატრი", "logo", "ძიუდო"])

    return render_template("add_wordplay.html",
                           team=selected_team,
                           word=word,
                           score=session["score"])


@app.route("/music", methods=["GET", "POST"])
def music():
    if "score" not in session or not isinstance(session["score"], list):
        session["score"] = [0, 0]

    if "current_team" not in session:
        session["current_team"] = 0

    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            session["score"][session["current_team"]] += 1
        session["current_team"] = 1 - session["current_team"]
        return redirect(url_for("music"))

    selected_team = f"გუნდი {session['current_team'] + 1}"
    word = random.choice(["როკი", "პიანინო", "ბითლზი", "ჯაზი"])

    return render_template("music.html",
                           team=selected_team,
                           word=word,
                           score=session["score"])


@app.route("/travel", methods=["GET", "POST"])
def travel():
    if "score" not in session or not isinstance(session["score"], list):
        session["score"] = [0, 0]

    if "current_team" not in session:
        session["current_team"] = 0

    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            session["score"][session["current_team"]] += 1
        session["current_team"] = 1 - session["current_team"]
        return redirect(url_for("travel"))

    selected_team = f"გუნდი {session['current_team'] + 1}"
    word = random.choice(["კოლიზეუმი", "რევოლუცია", "ნაპოლეონი", "შუა საუკუნეები"])

    return render_template("travel.html",
                           team=selected_team,
                           word=word,
                           score=session["score"])


@app.route("/history", methods=["GET", "POST"])
def history():
    form = TeamForm()
    if "score" not in session or not isinstance(session["score"], list):
        session["score"] = [0, 0]

    if "current_team" not in session:
        session["current_team"] = 0

    if request.method == "POST":
        action = request.form.get("action")
        if action == "correct":
            session["score"][session["current_team"]] += 1
        session["current_team"] = 1 - session["current_team"]
        return redirect(url_for("history"))

    selected_team = f"გუნდი {session['current_team'] + 1}"
    word = random.choice(["კოლიზეუმი", "რევოლუცია", "ნაპოლეონი", "შუა საუკუნეები"])

    return render_template("history.html",
                           form=form,
                           team=selected_team,
                           word=word,
                           score=session["score"])




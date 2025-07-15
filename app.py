from extensions import app

if __name__ == "__main__":

    from routes import home, rules, login, profile, signup, playing, play, sports, score, reset, next_team, next_team2, add_word


    app.run(debug=True)



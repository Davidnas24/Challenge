from flask import Flask,request,render_template_string, render_template, redirect
from markupsafe import escape
import db

app = Flask(__name__)

# xss
@app.route("/firstChallenge")
def firstChallenge():
    name = request.args.get("name")
    s = """<form><input type="text" name="name"><input type="submit" value="ok"></form>"""
    if name:
        if escape(name) != name:
            s += "<br>Great Job. You solved the challenge"
        return s + "<br>" + "Hello " + name
    else:
        return s

# SSTI / Server Side Template Injection
@app.route("/secondChallenge")
def secondChallenge():
    name = request.args.get("name")
    s = """<form><input type="text" name="name"><input type="submit" value="ok"></form>"""
    if name:
        return render_template_string(s + "<br>Hello " + name)
    else:
        return s

@app.route("/thirdChallenge", methods=['GET', 'POST'])
def thirdChallenge():
    if request.method == 'POST':
        db.add_comment(request.form['comment'])

    search_query = request.args.get('q')

    comments = db.get_comments(search_query)

    return render_template('thirdChallenge.html',
                           comments=comments,
                           search_query=search_query)

@app.route("/fourthChallenge")
def fourthChallenge():
    flag = "Flag3"
    name = request.args.get("name")
    s = """<form><input type="text" name="name"><input type="submit" value="ok"></form>"""
    if name:
        return render_template_string(s + "<br>Hello " + name)
    else:
        return s

@app.route("/fifthChallenge", methods=['GET', 'POST'])
def fifthChallenge():
    form = '''
<form method="POST" style="margin: 60px auto; width: 140px;">
    <p><input name="username" type="text" /></p>
    <p><input name="password" type="password" /></p>
    <p><input value="Login" type="submit" /></p>
</form>
    '''
    if request.method == 'GET':
        return form
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user_from_username_and_password(username, password)
        if user is not None:
            return "Sucess" + form
        else:
            return redirect('/fifthChallenge')

@app.route("/sixthChallenge", methods=['GET', 'POST'])
def sixthChallenge():
    form = '''
<form method="POST" style="margin: 60px auto; width: 140px;">
    <p><input name="username" type="text" /></p>
    <p><input name="password" type="password" /></p>
    <p><input value="Login" type="submit" /></p>
</form>
    '''
    if request.method == 'GET':
        return form
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.enenched_get_user_from_username_and_password(username, password)
        if user is not None:
            return "Sucess" + form
        else:
            return redirect('/sixthChallenge')

@app.route("/seventhChallenge", methods=['GET', 'POST'])
def seventhChallenge():
    form = '''
<form method="POST" style="margin: 60px auto; width: 140px;">
    <p><input name="username" type="text" /></p>
    <p><input name="password" type="password" /></p>
    <p><input value="Login" type="submit" /></p>
</form>
    '''
    if request.method == 'GET':
        return form
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.other_enenched_get_user_from_username_and_password(username, password)
        if user is not None:
            return "Sucess" + form
        else:
            return redirect('/seventhChallenge')

@app.route("/")
def main():
    return "Available challenges:" + \
           "<br />1. XSS at /firstChallenge" + \
           "<br />2. SSTI at /secondChallenge" + \
           "<br />3. Stored XSS at /thirdChallenge" + \
           "<br />4. Advanced SSTI at /fourthChallenge" + \
           "<br />5. Sql injection at /fifthChallenge"  + \
           "<br />6. Advanced Sql injection at /sixthChallenge" 


@app.route("/solutions")
def solutions():
    return "1. You can close the tag with \"< /br >\" and run XSS<br />" + \
            "Simply just run \"< script>alert('WON')< /script>\" (remove spaces)" + \
            "<br />2. You would like to check if command can be run and if so, you would like to run it." + \
            "<br />You can use \"{{ config['flag'] }}\" to run it" + \
            "<br />3. Stored XSS with comments could be done with <script>alert('xss')</script>" + \
            "<br />4. You would need to run Remote code on the server. To do that, we would need to search for the functions used by the server and mainly popen." + \
            "<br />To do that, we would need to run \"{{ "".__class__.__base__.__subclasses__() }}\" and search for the command index in the list" + \
            "<br />You would want to use the index of Popen and run \"{{ \"\".__class__.__base__.__subclasses__()[IDX](\"cat AppChallenges.py\",shell=True,stdout=-1).communicate() }}\"" + \
            "<br />5. You would like to check if the user name or password field is vulnerable." + \
            "<br />You can use \"`' OR 1=1; --`\" to win the challenge." + \
            "<br />6. You would like to check if the user name or password field is vulnerable." + \
            "<br />You can use \"\"' OR 1=1; --\"\" to win the challenge."

if __name__ == "__main__":
    db.create_tables()
    app.config["flag"] = "Flag2"
    app.run("127.0.0.1",8080)

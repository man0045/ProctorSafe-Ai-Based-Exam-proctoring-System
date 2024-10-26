from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Home Page")

@app.route('/faq')
def about():
    return render_template('faq.html', title="Mostly Asked question")

@app.route('/register')
def register():
    return render_template('register.html', title="Register pages")
@app.route('/login')
def login():
    return render_template('login.html', title="login")

@app.route('/contact')
def contact():
    return render_template('contact.html', title = "Contact pages")

if __name__ == '__main__':
    app.run(debug=True)
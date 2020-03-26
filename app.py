from flask import Flask, request, redirect, render_template, abort, flash

app = Flask(__name__)
app.secret_key = b'%\x14BNS\x8b\xcd\xbe\x11\x1b%`\xe0x\xe7\xc5'  # sshhhh!

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
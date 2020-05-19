from flask import Flask, request, redirect, render_template
from random import randint
import sys

app = Flask(__name__)
app.secret_key = b'%\x14BNS\x8b\xcd\xbe\x11\x1b%`\xe0x\xe7\xc5'  # sshhhh!


@app.route('/')
def index():
	d_f = ['Dancing', 'Falling'][randint(0,1)] # dancing or falling?
	i = randint(1, 9)
	imgpath = 'pics/%s/%d/%d.PNG' % (d_f, i, i)
	print(imgpath)
	if d_f == 'Dancing':
		return render_template('dancing.html', img=imgpath)
	else:
		return render_template('falling.html', img=imgpath)


@app.route('/wrong')
def test():
	return render_template('wrong.html')


if __name__ == '__main__':
	app.run(debug=True)
from flask import Flask, request, redirect, render_template
from random import randint
import sys

app = Flask(__name__)
app.secret_key = b'%\x14BNS\x8b\xcd\xbe\x11\x1b%`\xe0x\xe7\xc5'  # sshhhh!


@app.route('/', methods=['GET','POST'])
def index():
	d_f = ['Dancing', 'Falling'][randint(0,1)] # dancing or falling?
	if request.method=='GET':
		i = randint(1, 9)
	else:
		j = request.form['prev']
		i = [k for k in range(1,9) if k != j][randint(0,7)]

	imgpath = 'pics/%s/%d/%d.PNG' % (d_f, i, i)
	print(imgpath)
	if d_f == 'Dancing':
		return render_template('dancing.html', img=imgpath, index=i)
	else:
		return render_template('falling.html', img=imgpath, index=i)


@app.route('/wrong')
def test():
	return render_template('wrong.html')


if __name__ == '__main__':
	app.run(debug=True)
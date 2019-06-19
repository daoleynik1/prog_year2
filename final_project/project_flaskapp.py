from flask import Flask, render_template, request
from project import main as fff

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def pagew():
    if request.method == 'POST':
        words = str(request.form['words'])
        output = fff(words)
        if output:
            return render_template('start.html', output=output)
        else:
            outfail = 'Где-то произошла ошибка! '
            return render_template('start.html', outfail=outfail)
    else:
        return render_template('start.html')
        
if __name__ == "__main__":
    app.run(debug=True)

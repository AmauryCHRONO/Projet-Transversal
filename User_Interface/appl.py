from flask import Flask, render_template, request, url_for, redirect, flash
import psycopg2

con = psycopg2.connect(
    database="test",
    user="postgres",
    password="Ud7PsJab"
)

cur = con.cursor()

def ex_com(q):
    cur.execute(q)
    con.commit()

def display_table():
    query="select * from modes"
    ex_com(query)
    cur.fetchall()

def ins_val(a):
    ins="insert into modes (im_na) values ("+a+")"
    ex_com(ins)

a="'i need water'" 


#cur.execute(ins)
#con.commit()
#rows = cur.fetchall()
#print(rows)


app=Flask(__name__)
"""""
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Ud7PsJab@localhost/test'

db=SQLAlchemy(app)

class M(db.Model):
    __tablename__="mode"
    mode_id=db.Column(db.Integer(),primary_key=True)
    mode_name=db.Column(db.String())

    def __init__(self,name):
        self.name=name
"""""
app.secret_key='123'

messages = []

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task = request.form['cmd']
        messages.clear()
        messages.append(task)
        task="'"+task+"'"
        #s=M(task)
        #db.session.add(s)
        #db.session.commit()
        ins_val(task)
        return redirect(url_for("index"))
    return render_template("index.html", messages=messages)

#cur.close()
#con.close()


if __name__ == "__main__":
    app.run(debug=True) 

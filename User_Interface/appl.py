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
    return cur.fetchall()

def display_all_table(table):
    try:
        query="select * from " + table
        cur.execute(query)
        resultat = cur.fetchall()
        return resultat
    except:
        return 1

def ins_val(a):
    
    ins="insert into image () values ("+a+")"
    ex_com(ins)
    cur.close()

def ins_val_v2(table_colonne,values):
    try:
        query="insert into" + table_colonne + "values" + values 
        cur.execute(query)
        con.commit()

        return 0
    except:
        return 1
    
def display_element(table,element="*",characteristic=""):

    query="select "+element+ " from " + table 

    if characteristic != "":
        query = query +" "+characteristic 

    cur.execute(query)
    resultat = cur.fetchall()

    return resultat

def check(im):
    ch="select id_image from image where image_name = '"+im+"'" 
    ex_com(ch)
    return cur.fetchall()

def retrive_info(id):
    info="select * from list_of_step as los inner join image as i on los.id_image = i.id_image where i.id_image ="+id
    ex_com(info)
    return cur.fetchall()
#cur.execute(ins)
#con.commit()
#rows = cur.fetchall()
#print(rows)
app=Flask(__name__)

app.secret_key='123'

#messages = []


@app.route('/', methods=['POST','GET'])
def index():
    messages=""
    instruct=[]
    if request.method == 'POST':
        model = request.form['cmd']
        res=check(model)
        if res==[]:
            messages="Le modèle n'est pas présent"
        else:
            messages="Le modèle "+model+" est présent"
            instruct=retrive_info(str(res[0][0]))
            
    return render_template("index.html", messages=messages, instruct=instruct)


if __name__ == "__main__":
    app.run(debug=True) 

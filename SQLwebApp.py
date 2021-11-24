from flask import Flask, render_template, request, redirect, url_for

from flask.json import dump
from numpy.lib import type_check

import sql_interface as si
import numpy as np


app = Flask(__name__, template_folder='templates')

#home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))
    return render_template("index.html")

@app.route('/table', methods=['GET','POST'])
def selectTabletoShow():
    if request.method == 'POST':
        if request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))
        tableName = request.form.get('tblnam')
        print(tableName)
        return redirect(url_for('ShowTable', tableName=tableName))
    return render_template('selectTable.html')
        
@app.route('/edit', methods=['GET','POST'])
def selectTabletoEdit():
    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        tableName = request.form.get('tblnam')
        print(tableName)
        return redirect(url_for('EditTable', tableName=tableName))
    return render_template('editTable.html')

# display tables   
@app.route('/table/<tableName>', methods=['GET', 'POST'])
def ShowTable(tableName):    
    if request.method == 'POST':
        if request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))
        tableName = request.form.get('tblnam')
        print(tableName)
        return redirect(url_for('ShowTable', tableName=tableName))
    headings = np.array(si.get_data("select column_name from information_schema.columns where table_name='{}'".format(tableName))).flatten()
    rows = np.array(si.get_data("select * from {}".format(tableName)))
    return render_template('table.html', headings=headings, rows = rows, tableName=tableName)


# Insert in table
@app.route('/edit/<tableName>', methods=['GET', 'POST'])
def EditTable(tableName):
    headings = np.array(si.get_data("select column_name from information_schema.columns where table_name='{}'".format(tableName))).flatten()
    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('enter'):
            tableName = request.form.get('tblnam')
            print(tableName)
            return redirect(url_for('EditTable', tableName=tableName))
        elif request.form.get('Submit'):
            query = 'insert into {}('.format(tableName) + ', '.join(['%s' for _ in range(len(headings))]) + ') values(' + ', '.join(['\'%s\'' for _ in range(len(headings))]) + ')'
            temp = headings
            for i in headings:
                temp = np.append(temp, request.form.get(i))
            temp = tuple(temp)
            query = query% temp
            print(query)
            # si.insert_data(query)
    return render_template('edit.html', headings=headings, tableName=tableName)

    

if __name__ == '__main__':    
    app.run(debug=True)
import pymongo
from flask import Flask,render_template, redirect,request
import numpy as np
import random
#import calc_dpr
from calc_dpr import gogocalculate
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

app = Flask(__name__)

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.dnd

@app.route("/", methods=["GET","POST"])
def index():
    # if request.method == 'POST':
    #     #test = request.form['testest']
    #     print('POST!')
    # else:
    #     print('nope')
    # if dpr != 0:
    image = f'return.png?time={time.time()}'
    #print(image)
    return render_template('index.html',imagepath=image)
    #     print('render temp')
    # else:
    #     print('redirect to calc')
    #     return redirect('/calculate', code=302)


@app.route("/calculate", methods=["GET","POST"])
def calc():
    DPR_calculated = calc_dpr.gogocalculate(request.form) #returns list of damage per rounds
    DPRdict = {}
    DPRdict['desc'] = DPR_calculated.pop(0)
    for i,_ in enumerate(DPR_calculated):
        DPRdict[str(i+15)] = _
    db.dpr.insert_one(DPRdict)
    all_dpr_df = pd.DataFrame()
    all_stats = db.dpr.find()
    for each_stats in all_stats:
        print(each_stats)
        AC_DPR = []
        for each_ac in range(15,26):
            AC_DPR.append(each_stats[str(each_ac)])
        all_dpr_df[each_stats['desc']] = AC_DPR
    #print(all_stats)
        #print(all_dpr_df)
    plt.figure(figsize=(12,9))
    plt.plot(range(15,26),all_dpr_df,marker='o')
    plt.ylabel("DPR")
    plt.xticks(np.arange(15,26,step=1))
    plt.xlabel("AC")
    plt.legend(all_dpr_df.columns,loc='best')
    plt.savefig("static/return.png")
    return redirect('../', code=302)

@app.route("/reset")
def reset():
    db.dpr.drop()
    plt.figure(figsize=(12,9))
    plt.ylabel("DPR")
    plt.xticks(np.arange(15,26,step=1))
    plt.xlim(14,26)
    plt.xlabel("AC")
    plt.savefig("static/return.png")

    return redirect('../',code=302)

# prevent cached responses
# if app.config["DEBUG"]:
#     @app.after_request
#     def after_request(response):
#         response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
#         response.headers["Expires"] = 0
#         response.headers["Pragma"] = "no-cache"
#         return response

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
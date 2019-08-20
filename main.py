import pymongo
from flask import Flask,render_template, redirect,request
from calc_dpr import gogocalculate
import pandas as pd
# import matplotlib.pyplot as plt
#import time
# import os

app = Flask(__name__)

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.dnd

@app.route("/", methods=["GET","POST"])
def index():
    all_tests_from_db = db.dpr.find({},{'_id':0})
    all_tests = []
    for _ in all_tests_from_db:
        all_tests.append(_)
    #print(all_tests)
    #image = f'return.png?time={time.time()}'  #Method to force a refresh and force the browser to NOT use a cached version of the same image.
    return render_template('index.html',all_tests = all_tests)#,imagepath=image)

@app.route("/calculate", methods=["GET","POST"])
def calc():
    DPR_calculated = gogocalculate(request.form) #returns list of damage per rounds
    DPRdict = {}
    # create new dictionary
    DPRdict['desc'] = DPR_calculated.pop(0)
    # description is first entry, pop off and store in dictionary
    for i,_ in enumerate(DPR_calculated,15):
        DPRdict[str(i)] = _
        # add each DPR entry for each AC into the same dictionary
    db.dpr.insert_one(DPRdict)
    # And load to the database.


    ######
    #OLD CODE TO CREATE MATPLOTLIB FIGURE. HAS BEEN REPLACED WITH PLOTLY.JS
    ######
    # all_dpr_df = pd.DataFrame()
    # all_stats = db.dpr.find()
    # #pull all the previously done DPR calculations to create the image
    # for each_stats in all_stats:
    #     print(each_stats)
    #     AC_DPR = []
    #     # create new list
    #     for each_ac in range(15,26):
    #         AC_DPR.append(each_stats[str(each_ac)]) #append each DPR to a list
    #     all_dpr_df[each_stats['desc']] = AC_DPR #add list of DPRs into a dataframe under each description
    
    # plt.figure(figsize=(12,9))
    # plt.plot(range(15,26),all_dpr_df,marker='o')
    # plt.ylabel("DPR")
    # plt.xticks(np.arange(15,26,step=1))
    # plt.xlabel("AC")
    # plt.legend(all_dpr_df.columns,loc='best')
    # plt.savefig("static/return.png")
    return redirect('../', code=302)

@app.route("/reset")
def reset():
    db.dpr.drop() #drop the whole database
    plt.figure(figsize=(12,9))
    plt.ylabel("DPR")
    plt.xticks(np.arange(15,26,step=1))
    plt.xlim(14,26)
    plt.xlabel("AC")
    plt.savefig("static/return.png")
    #blank image

    return redirect('../',code=302)

if __name__ == "__main__":
    # app.run(debug=True,host='0.0.0.0')
    app.run(host='0.0.0.0', port=5000)
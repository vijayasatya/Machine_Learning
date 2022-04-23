from flask import Flask, redirect, url_for, render_template,request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
#import numpy as np
#import texthero as hero
import pickle
import jinja2

app = Flask(__name__)
#app.jinja_env.filters['zip'] = zip
app.jinja_env.globals.update(zip = zip)

def predict_output_prob(y_pred_prob,my_model_inverse,my_model,X):
  indexes = []
  dic = {}
  l = list(my_model_inverse.classes_)
  output_list = list(my_model_inverse.inverse_transform(my_model.predict(X[0]))[0])
  y_pred_prob_ = list(y_pred_prob[0])
  for i in output_list:
      index_f = l.index(str(i))
      indexes.append(index_f)
  for i in range(len(output_list)):
    dic[output_list[i]] = round(float(y_pred_prob_[indexes[i]]),2)
  return dic

@app.route("/",methods=['POST','GET'])
def home():
    if request.method=='POST':
        print(request.form['submit'])
        if request.form['submit'] == 'Execute':
            input_text = request.form['message']
            input_text_org = input_text
            input_text = pd.Series(input_text)
            #input_text = hero.clean(input_text)
            # Testing phase
            tf1 = pickle.load(open("tfidf1.pkl", 'rb'))
            # Create new tfidfVectorizer with old vocabulary
            tf1_new = TfidfVectorizer(analyzer='word',max_features = 1000, vocabulary = tf1.vocabulary_)
            X = tf1_new.fit_transform(input_text)
        
            my_model = pickle.load(open('Saved_Models/logistic_Basic_Model.sav','rb'))
            my_model_inverse = pickle.load(open('Saved_Models/inverse_logistic_Basic_Model.sav','rb'))
            y_pred_prob = my_model.predict_proba(X[0])
            result = predict_output_prob(y_pred_prob,my_model_inverse,my_model,X)
            print(result)
            claims_data = pd.read_csv("D_ICD_DIAGNOSES.csv")
            #claims_data.reset_index(drop=True)
            #claims_data = claims_data.drop(['row_id','short_title'],axis=1)
            codes = claims_data['icd9_code'].tolist()
            text_codes = claims_data['long_title'].tolist()
            L = list(result.keys())
            long_text = []
            for i in L:
                #a = claims_data[claims_data['icd9_code'] == str(i).strip()]['long_title']
                try:
                  a = codes.index(str(i))
                  b  =  text_codes[a]
                except:
                  b  =  "Corresponding icd9 code details not present"
                long_text.append(b)
            result = dict(sorted(result.items(),key=lambda item: item[1],reverse=True))
            content = {'classes':list(result.keys()),"percentage":list(result.values()),'input_text':input_text_org,'long_text': long_text}
            if len(content['classes']) == 0:
                content = {'classes':["No classes Found"],"percentage":['<50'],'long_text': ["Model predicting all Med codes having low confidence"]}
                   
            return render_template("index1.html",**content)
        
        elif request.form['submit'] == 'Sample':
            f = open("sample_data.txt",'r')
            sample_data_text = f.read()
            content = {'input_text':sample_data_text}
            return render_template("index1.html",**content)
            
        elif request.form['submit'] == 'Clear':
            print(1)
            return render_template("index1.html")
        else:
            return render_template("index1.html")
    else:
        return render_template("index1.html")
    

if __name__ == "__main__":
    app.run()

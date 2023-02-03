#Author : SHAIK MUHAMMAD ARSHAD ALI
''' B.TECH ELECTRONICS AND COMMUNICATIONS ENGINEERING
    SASTRA DEEMED TO BE UNIVERSITY
    THANJAVUR, TAMILNADU'''
from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__,template_folder = 'templates')

@app.route('/')
def student():
    return render_template('TelMain.html')

@app.route('/result',methods = ['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        s = request.form["Name"]
        title = str(s)
        title = title.title()
        df = pd.read_csv("Popular_telugumovies_dataset.csv")
        df['No.of.Ratings'] = df['No.of.Ratings'].str.replace(",","")
        df['No.of.Ratings'] = pd.to_numeric(df['No.of.Ratings'],errors='coerce')
        df['Year'] = df['Year'].str.replace("(","")
        df['Year'] = df['Year'].str.replace(")","")
        df['Year'] = pd.to_numeric(df['Year'],errors='coerce')
        df['Genre'] = df['Genre'].str.replace("\n","")
        df['Overview'] = df['Overview'].str.replace("\n","")
        df['Movie']=df['Movie'].str.replace("ã","a")
        df['Movie']= df['Movie'].fillna('')
        df['Movie']=df['Movie'].astype(str)
        df['Overview']=df['Overview'].astype(str)
        df['Genre'] = df['Genre'].astype(str)
        df.drop(index= 230,inplace=True)
        df['nlp'] = df[['Movie', 'Genre' , 'Overview']].apply(lambda x: ' '.join(x), axis=1)
        from sklearn.feature_extraction.text import TfidfVectorizer
        tfv = TfidfVectorizer(max_features=None,analyzer='word',strip_accents='unicode',ngram_range=(1, 3),stop_words='english')
        tfv_matrix = tfv.fit_transform(df['nlp'])
        from sklearn.metrics.pairwise import sigmoid_kernel
        sig = sigmoid_kernel(tfv_matrix,tfv_matrix)
        indices = pd.Series(df.index,df["Movie"])
        def recommend(title,sig=sig):

            idx = indices[title]

            sig_scores = list(enumerate(sig[idx]))

            sig_scores = sorted(sig_scores, key=lambda x:x[1] ,reverse=True)

            sig_scores = sig_scores[1:11]

            movie_indices = [i[0] for i in sig_scores]

            k = df.iloc[movie_indices,1:9]
           
            qw = dict(k.iloc[0:,0])
            r = qw
            return(r)
        fg = recommend(title)
        return render_template("result.html",result = fg)

if __name__ == '__main__':
    app.run()







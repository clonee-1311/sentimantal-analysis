from flask import Flask,request,render_template
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import pickle

model=pickle.load(open('venv\model.pkl','rb'))
vectorizer=pickle.load(open('venv\\vectorizer.pkl','rb'))

port_stem=PorterStemmer()

def stemming(content):

    stemmed_content=re.sub('[^a-zA-Z]',' ',content)
    stemmed_content=stemmed_content.lower()
    stemmed_content=stemmed_content.split()
    stemmed_content=[port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content=' '.join(stemmed_content)
    
    return stemmed_content


app= Flask(__name__)
@app.route('/')
def index():
  return render_template("index.html")

@app.route('/prediction',methods=['POST','GET'])
def predict():
  if request.method=='POST':
    comment=request.form['text']
    clean_comment=stemming(comment)
    comment_vector=vectorizer.transform([clean_comment])
    prediction=model.predict(comment_vector)[0]


    return render_template('index.html',prediction=prediction)

if __name__=="__main__":
   app.run(debug=True)

  
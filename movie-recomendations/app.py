from flask import Flask,render_template,request
import pickle
import requests
import pandas as pd

movies_list=pickle.load(open('movies.pkl','rb'))
similar=pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies_list)

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    dist = similar[movie_index]
    movies_new = sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:11]
    new_list=[]
    for i in movies_new:
        new_list.append([movies.iloc[i[0]].movie_id,movies.iloc[i[0]].title])
    return new_list    

new_dict={}

def images_url(n):
  count=1
  for i in n:
        response = requests.get('https://api.themoviedb.org/3/movie/'+str(i[0])+'?api_key=0281fac110e08868c0ef66acdaf8944e')
        new_data = response.json()
        poster_path=new_data.get('poster_path')
        new_dict['img'+str(count)]='https://image.tmdb.org/t/p/w500'+poster_path
        count+=1
# print(recommend("Spectre"))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results',methods=['POST'])
def result():
    movie=request.form.get('movie')
    List_of_New=recommend(movie)
    images_url(List_of_New)
    return render_template('recommendations.html',**{
        "MovieName":movie,
        "movie1":List_of_New[0][1],
        "movie2":List_of_New[1][1],
        "movie3":List_of_New[2][1],
        "movie4":List_of_New[3][1],
        "movie5":List_of_New[4][1],
        "movie6":List_of_New[5][1],
        "movie7":List_of_New[6][1],
        "movie8":List_of_New[7][1],
        "movie9":List_of_New[8][1],
        "movie10":List_of_New[9][1],
        "image1":new_dict['img1'],
        "image2":new_dict['img2'],
        "image3":new_dict['img3'],
        "image4":new_dict['img4'],
        "image5":new_dict['img5'],
        "image6":new_dict['img6'],
        "image7":new_dict['img7'],
        "image8":new_dict['img8'],
        "image9":new_dict['img9'],
        "image10":new_dict['img10']
    })
if(__name__ == '__main__'):
    app.run(debug=True)
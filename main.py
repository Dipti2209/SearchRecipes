import io
import tkinter
from PIL import Image,ImageTk
import requests
import urllib
import webbrowser

# variable declaration
window =tkinter.Tk()

name=tkinter.StringVar()
var=tkinter.StringVar()
get_ingredients=" "
show_ingredients=[]
window.geometry("500x500")

# creating frame,canvas and scrollbar

frame = tkinter.Frame(window)
canvas=tkinter.Canvas(frame,height=1000,width=1000)
frame1=tkinter.Frame(canvas)
my_scrollbar=tkinter.Scrollbar(window,orient="vertical",command=canvas.yview)
my_scrollbar.pack(side="right",fill="y")
# bind function helps to connect scrollbar with frame
frame1.bind("<Configure>",lambda r: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((1,1),window=frame1,anchor="nw")
canvas.config(yscrollcommand=my_scrollbar.set)
window.config(bg="pink")
window.title("welcome")

# creating label and entry toolkits on window
tkinter.Label(frame1,text="Enter an Ingredient:",width=15,height=1,bd=5).grid(row=0,column=0,padx=5,pady=10)
tkinter.Entry(frame1,bd=5,textvariable=name,width=20).grid(row=0,column=1,pady=10)

# create connection between Program and Recipe API and get all data from Recipe API
def get_connection():
    ingredient=name.get()
    app_id = "0c44ad24"
    app_keys = "087c95af9f98e75557c5dc045b3d2ad0"
    url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_keys)
    result = requests.get(url)
    data = result.json()
    return data['hits']

# Getting recipe image and recipe name and complete recipe and list of ingredients
# All function are called  after clicking  the button
def search_query():
    count = 3
    num = 4
    results = get_connection()
    for result in results:
        recipe = result['recipe']
        rname = recipe['label']
        recipe_url=recipe['url']
        recipe_name(count,rname)
        ingredients=recipe['ingredientLines']
        open_ingredients(num,ingredients)
        image_url=recipe['image']
        get_image(num, image_url)
        get_recipe(num,recipe_url)
        count=count+2
        num=num+2


# Getting recipe name from Recipe ApI
def recipe_name(n,var):
     tkinter.Label(frame1,text=var,width=40,height=2,relief="solid").grid(row=n, column=1,columnspan=12)

# Getting list of ingredients according to recipe
def open_ingredients(d,show_ingredients):
    text_ing=tkinter.Text(frame1,height=7,width=50)
    text_ing.grid(column=1,row=d,columnspan=12)
    # for Loop that iterates over show_ingredients lists and insert each ingredient in text
    for get_ingredients in show_ingredients:
            text_ing.insert(tkinter.END,"\n"+get_ingredients)

# Getting image from Recipe API
def get_image(e,img):
    # getting image url
    u=urllib.request.urlopen(img)
    data=u.read()
    u.close()

    img1=Image.open(io.BytesIO(data))
    img1=img1.resize((100,100))
    img2=ImageTk.PhotoImage(img1)
    l1=tkinter.Label(frame1,image=img2,relief="solid")
    l1.image=img2
    l1.grid(column=15,row=e,columnspan=6)

#Getting complete recipe from Recipe API
def get_recipe(dd,recipeurl):
    def open_recipe():
        webbrowser.open(recipeurl)

    b1 = tkinter.Button(frame1, text="click here for recipe", command=open_recipe)
    b1.grid(column=35,row=dd)


# creating  button on window
tkinter.Button(frame1,text="Search Recipe",command=search_query,width=10,height=1).grid(row=0,column=2,pady=10,padx=5)

frame.pack()
canvas.pack(side="left",fill="both",expand="true")
window.mainloop()



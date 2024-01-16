# Import Libraries below
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)







# Define upload_form() and route the webapp 

@app.route('/')
def load_form():
    return render_template("upload.html")





# Define upload_video() to get video in defined folder and route the webapp  
@app.route('/',methods=['POST'])
def upload_image():
    file=request.files['file']
    file_name=secure_filename(file.filename)
    file.save(os.path.join('static/',file_name))
    source=cv2.VideoCapture("static/"+file_name)
    frame_width=int(source.get(3))
    frame_height=int(source.get(4))
    size=(frame_width,frame_height)
    result=cv2.VideoWriter('static/' + 'blackandwhite.mp4',cv2.VideoWriter_fourcc(*'mp4v'),30,size,0)
    try:
        while True:
            stats,frame_image=source.read()
            gray=cv2.cvtColor(frame_image,cv2.COLOR_BGR2GRAY)
            result.write(gray)
            v="blackandwhite.mp4"
            
    except:
        print('completed reading')
    display_message='successfully uploaded!'
    return render_template("upload.html",filename=file_name,message=display_message)







# Define display_video() to Display video in defined folder and route the webapp  
@app.route("/display/<filename>")
def display_video(filename):
    return redirect(url_for("static",filename="filename"))

@app.route("/download")
def download_file():
    converted_video_path="static/blackandwhite.mp4"
    return send_file(converted_video_path,as_attachment=True)




if __name__ == "__main__":
    app.run(debug=True)

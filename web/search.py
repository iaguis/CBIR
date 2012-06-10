#!/usr/bin/env python2

import web
import base64
import subprocess
import Image
import ImageOps
import StringIO

from recognize_number import *
    
urls = (
    '/', 'index'
)


class index:
    def __init__(self):
        self.recognizer = Recognizer()
    
    def GET(self):
        render = web.template.render('templates/')
        return render.canvas()
    
    def POST(self):
        img_base64 = web.input()
        
        img_decoded = base64.b64decode(img_base64.numberImg)

        img = Image.open(StringIO.StringIO(img_decoded))
                
        img = ImageOps.grayscale(img)
        
        img = img.resize((20, 20), Image.ANTIALIAS)
                
        image_path = "number.png"
        
        fh = open(image_path, "wb")
        fh.write(img_decoded)
        fh.close()

        
        subprocess.call(["convert", image_path, "-background", "white", "-flatten", "-filter", "Quadratic", "-resize", "20x20", image_path])

        return self.recognizer.predict_number()
        

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
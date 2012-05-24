#!/usr/bin/env python2

import web
import base64
    
urls = (
    '/', 'index'
)

class index:
    def GET(self):
        render = web.template.render('templates/')
        return render.canvas()
    
    def POST(self):
        image = web.input()
        
        img = base64.b64decode(image.numberImg)
        
        fh = open("number.png", "wb")
        fh.write(img)
        fh.close()
        
        raise web.seeother('/')
        

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
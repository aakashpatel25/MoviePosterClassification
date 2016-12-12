#!/usr/bin/env python
import web
import ClassifyIR as cir

urls = (
    '/image/', 'image_path'
)

app = web.application(urls, globals())

class image_path:
    def POST(self):
        path =  web.data() 
        return cir.return_label(path)

if __name__ == "__main__":
    app.run()
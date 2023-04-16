from flask import Flask, render_template, request, redirect, session,url_for,jsonify
import Printer
import time
app = Flask(__name__)
printer = Printer.Printer.getInstance()
@app.get('/')
def index():
    return render_template("main.html")

@app.get("/data")
def getdata():
    list = printer.getPrintingTasksData()
    status = printer.getPrinterStatus()
    NumberOfPaper = printer.getNumberOfPaper()
    AmountOfInk = printer.getAmountOfInk()
    return jsonify({'printingQueue':list,'status':status.name,'NumberOfPaper':NumberOfPaper,'AmountOfInk':AmountOfInk})

@app.post("/print")
def print():
    text = request.form['text']
    key =  printer.print(text)
    return "True"
@app.get("/test")
def test():
    list =  printer.getPrintingTasksData()
    return render_template('index.html', q=list)
@app.get("/status/<string:key>")
def status(key):
    return printer.getPrintStatus(key)

@app.get("/cancel/<string:key>")
def cancel(key):
    printer.cancel(key)
    return "done"
@app.post("/refillInk")
def refillInk():
    printer.FillInk()
    return "true"
@app.post("/fixPaperJam")
def fixPaperJam():
    printer.fixPaperJam()
    return "Fixed Successfully"
@app.post("/refillPaper")
def refillPaper():
    printer.FillPaper()
    return "Refilled Successfully"
    
@app.post("/pause")
def pause():
    printer.pause()
    return "paused Successfully"

@app.post("/resume")
def resume():
    printer.resume()
    return "Resumed Successfully"   
@app.post("/offline")
def offline():
    printer.setOffLine()
    return "Printer Is Now OffLine"
@app.post("/online")
def online():
    printer.setOnLine()
    return "printer Is Now Online"         
if __name__ == "__main__":
    app.run(debug=True)
    
    
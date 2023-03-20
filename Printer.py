import printerStatus
import time
import threading
import random
import math
import os
from io import BytesIO
import queue
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileWriter
class Printer:
    __printer = None
    __status = printerStatus.printerStatus.idle
    __paper = 100
    __ink = 1000
    __currentKey = None
    __currentText = None
    __printingQueue = queue.Queue()
    def getInstance():
        if Printer.__printer == None:
            Printer.__printer = Printer()
        return Printer.__printer

    def __init__(self):
        if Printer.__printer != None:
            raise("Instance already exists!") 
        Printer.__printer = self
        self.startPrinter()    

    def startPrinter(self):
        thread = threading.Thread(target=self.startPrinterSimulator)
        thread.start()
    def startPrinterSimulator(self):
        while(True):
            while not self.__printingQueue.empty():
                self.simulatePrinting(self.__printingQueue.get())
            time.sleep(0.1)    
            
    def simulatePrinting(self,item):
        key = list(item.keys())[0]
        self.__currentKey = key
        text = item[key]
        self.__currentText = text
        if self.checkText(text):
            print("The Printer Has encontered an error and can't continue printing {text}")
            self.__status = printerStatus.printerStatus.Error
        if self.checkInkForThisOperation(text):
            old_state = self.__status
            self.__status = printerStatus.printerStatus.lowInkOrTunar
            while self.__status == printerStatus.printerStatus.lowInkOrTunar:
                time.sleep(0.1)
            self.__status = old_state 
        if self.checkForPaper(text):
            old_state = self.__status
            self.__status = printerStatus.printerStatus.outOfPaper
            while self.__status == printerStatus.printerStatus.outOfPaper:
                time.sleep(0.1)
            self.__status = old_state      
        if self.__status == printerStatus.printerStatus.idle:
            self.__status = printerStatus.printerStatus.printing
        for i in range(1,10):
            if self.checkIfThereIsAPaperJam():
                print("printer is experiencing a paper jam, please Fix paper jam")
                old_state = self.__status
                self.__status = printerStatus.printerStatus.paperJam
                while self.__status != printerStatus.printerStatus.printing:
                    time.sleep(0.1)
                self.__status = old_state
            if self.checkIfCanceled(text):
                return
            if self.__status == printerStatus.printerStatus.Paused:
                print("Printer is paused")
                while self.__status == printerStatus.printerStatus.Paused:
                    if self.checkIfCanceled(text):
                        return
                    time.sleep(0.1)
                self.status = "Printing"
                print(f"Printer has resumed printing {text}") 
            time.sleep(1)
            
        self.__status = printerStatus.printerStatus.idle
        self.__currentKey = None
        self.__currentText = None
        self.finishPrintingOperation(text)           
    def checkIfCanceled(self,text):
        if self.__status == printerStatus.printerStatus.cancelled:
            print(f"Printing {text} has been canceled")
            self.__status = printerStatus.printerStatus.idle
            return True
        return False    
    def pause(self):
        if self.__status != printerStatus.printerStatus.paperJam:
            self.__status = printerStatus.printerStatus.Paused
    def resume(self):
        if self.__status == printerStatus.printerStatus.Paused:
            self.__status =  printerStatus.printerStatus.printing
    def print(self,text):
        key = self.createSpecialKey(text)
        self.__printingQueue.put({key:text})
        return key
    def getStatus(self):
        return  self.__status   
    def cancelcurrentRequest(self):
        if self.__status == printerStatus.printerStatus.printing or self.__status == printerStatus.printerStatus.Paused:
            self.__status =  printerStatus.printerStatus.cancelled
    def cancel(self,key):
        if key == self.__currentKey:
            self.cancelcurrentRequest()
        else:
            self.cancelSpecificOne(key)         
    def checkIfThereIsAPaperJam(self):
        x =  random.randint(0, 99)
        if x == 45:
           return True           
        return False
    def fixPaperJam(self):
        if self.__status == printerStatus.printerStatus.paperJam: 
            self.__status =  printerStatus.printerStatus.printing  
    def checkInkForThisOperation(self,text):
        requiredInk = len(text) * 0.2
        if requiredInk > self.__ink:
            return True
        self.__ink -= requiredInk
        return False
    def FillInk(self,ink,text):
        if self.__ink < 1000:
            self.__ink += ink
             
    def checkForPaper(self,text):
        numberOfWords = len(text.split())
        numberOfPaper = math.ceil(numberOfWords / 5)       
        if numberOfPaper > self.__paper:
            return True
        self.__paper -= numberOfPaper
        return False
    def FillPaper(self):
       if self.__paper < 100:
           self.__paper = 100
           
    def checkText(self,text):
        if len(text) == 0:
            return True
        return False
    def finishPrintingOperation(self,text):
        print(text)
        pass
    def keyFound(self,key):
        key_found = False
        for item in list(self.__printingQueue.queue):
            if key in item:
                key_found = True
                break
        return key_found
    def createSpecialKey(self,text):
        if self.keyFound(text):
            return text + str(random.randint(0,1000))
        return text
    def test(self):
        pq_list = []
        while not self.__printingQueue.empty():
            pq_list.append(self.__printingQueue.get())
        return pq_list

    def getPrintStatus(self,key):
        if self.keyFound(key):
            return "Waiting"
        if self.__currentKey == key:
            return "In-Progress"
        return "Finished"
    def getAllPrintOperation(self):
        my_array = []
        if self.__currentKey != None:
            key = self.createSpecialKey(self.__currentText)
            obj = {key: self.__currentText, "status": "In-Progress"}
            my_array.append(obj)
        index = 1   
        while not self.__printingQueue.empty():
            my_array.append(self.__printingQueue.get())
            my_array[index]["status"] = "Waiting"
            index += 1
        return my_array
    
    def cancelSpecificOne(self,key):
        for item in list(self.__printingQueue.queue):
            if key in item:
                self.__printingQueue.get(item)
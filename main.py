# Importing essential modules
import math
import time
import random
import threading
from io import open
from copy import copy
from tkinter import *
from tkinter import messagebox as MessageBox

# To center the window on the screen (This is a little Mixin)
class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        self.geometry(f"{w}x{h}+{x}+{y}")  

# Generating the main screen
class MainWidow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Program 1 - Simulating batch processing")
        self.resizable(0, 0) 
        self.geometry("640x480")
        self.config(relief="sunken", bd=10)
        self.center()
        self.Build()

    # Creating interfaces
    def Build(self):
        # To contain other widgets
        mainFrame = Frame(self)
        mainFrame.grid(row=0, column=0)

        # Input frame
        inputFrame = Frame(mainFrame)
        inputFrame.grid(row=0, column=0)
        inputFrame.config(padx=5, pady=5)

        processLabel = Label(inputFrame, text="# Process")
        processLabel.grid(row=0, column=0)
        processLabel.config(padx=5, pady=5)

        self.processEntry = Entry(inputFrame)
        self.processEntry.config(justify="center", width=11)
        self.processEntry.grid(row=0, column=1, padx=5, pady=5)

        self.processButton = Button(inputFrame, text="Generate", command=self.Generate)
        self.processButton.grid(row=0, column=2, padx=5, pady=5)

        # Space
        spaceFrame = Frame(mainFrame)
        spaceFrame.grid(row=0, column=1, padx=110)

        # Clock frame
        clockFrame = Frame(mainFrame)
        clockFrame.grid(row=0, column=2)

        clockLabel = Label(clockFrame, text="Global clock:")
        clockLabel.config(padx=5)
        clockLabel.grid(row=0, column=0)
    
        self.clockLabel2 = Label(clockFrame, text="00:00:00")
        self.clockLabel2.config(justify="center", width=10)
        self.clockLabel2.grid(row=0, column=1)

        # Work frame
        workFrame = Frame(mainFrame)
        workFrame.config(pady=15, padx=35)
        workFrame.grid(row=1, column=0, columnspan=3)

        # On hold frame
        onHolfFrame = Frame(workFrame)
        onHolfFrame.grid(row=0, column=0, padx=10)

        onHoldLabel = Label(onHolfFrame, text="On hold")
        onHoldLabel.config(justify="center")
        onHoldLabel.grid(row=0, column=0, columnspan=2, pady=3)

        self.onHoldText = Text(onHolfFrame)
        self.onHoldText.config(width=20, height=20)
        self.onHoldText.grid(row=1, column=0, columnspan=2, pady=3)

        onHoldLabel2 = Label(onHolfFrame, text="# of outstanding lots: ")
        onHoldLabel2.grid(row=2, column=0, pady=3)

        self.onHoldLabel3 = Label(onHolfFrame, text="00")
        self.onHoldLabel3.grid(row=2, column=1, pady=3)

        # Execution frame
        executionFrame = Frame(workFrame)
        executionFrame.grid(row=0, column=1, padx=10)

        executionLabel = Label(executionFrame, text="Execution")
        executionLabel.config(justify="center")
        executionLabel.grid(row=0, column=0, pady=2)

        self.executionText = Text(executionFrame)
        self.executionText.config(width=20, height=10)
        self.executionText.grid(row=1, column=0, pady=3)

        # Finished frame
        finishedFrame = Frame(workFrame)
        finishedFrame.grid(row=0, column=2, padx=10)

        finishedLabel = Label(finishedFrame, text="Finished")
        finishedLabel.config(justify="center")
        finishedLabel.grid(row=0, column=0, pady=3)

        self.finishedText = Text(finishedFrame)
        self.finishedText.config(width=20, height=20)
        self.finishedText.grid(row=1, column=0, pady=3)

        self.finishedButton = Button(finishedFrame, text="Get results", command=self.SaveProcessResult)
        self.finishedButton.config(state=DISABLED)
        self.finishedButton.grid(row=2, column=0, sticky="nsew", pady=3)

    def Generate(self):
        # Essential data to create processes
        self.processes = []
        self.people = ["Celeste", "Marisol", "Carlos", "Diego", "Edgar"]
        self.operators = ["+", "-", "*", "/"]
        counter = 1
        batch = 1
        self.runningProcess = False # To know if a process is being worked on

        # Blocking the processEntry to protect the program
        self.processEntry.config(state=DISABLED)
        self.processButton.config(state=DISABLED)

        # Doing validations
        try:
            self.numberOfProcess = int(self.processEntry.get())
            if self.numberOfProcess <= 0:
                raise ValueError()
        except:
            MessageBox.showwarning("ERROR", "You must write a valid number.")
            self.processEntry.config(state=NORMAL)
            self.processButton.config(state=NORMAL)
            return

        # Generating processes
        for p in range(self.numberOfProcess):
            if counter > 5:
                batch += 1
                counter = 1
            
            process = {
                "BATCH": batch,
                "ID": p+1,
                "PROGRAMMER": self.people[random.randrange(0,5)],
                "OPERATION": str(random.randrange(1,11)) + self.operators[random.randrange(0, 4)] + str(random.randrange(1,11)),
                "TIME": random.randrange(4, 14)
            }
            self.processes.append(process)

            counter += 1

        with open("processes.txt", "w") as textFile:
            for p in self.processes:
                for key, value in p.items():
                    textFile.write(f"{key}: {value}")
                    textFile.write("\n")
                textFile.write("\n")

        # Starting the timer
        initialTime = time.time() 
        #self.Timer(initialTime)
        # Creating thread of execution to work with parallel programming
        self.timerStatus = True
        self.threadingTimer = threading.Thread(target=self.Timer, args=(initialTime,))
        self.threadingTimer.start()

        self.copyOfProcesses = copy(self.processes) # To protect original processes data
        self.processResult = []

        processor = threading.Thread(target=self.Processor)
        processor.start()


    def Processor(self):
        while len(self.copyOfProcesses) > 0:
            # Deleting the last records
            self.executionText.config(state=NORMAL)
            self.executionText.delete(1.0, 'end')
            self.executionText.config(state=DISABLED)
            self.onHoldText.config(state=NORMAL)
            self.onHoldText.delete(1.0, 'end')
            self.onHoldText.config(state=DISABLED)

            # To know how long to wait before asking to show another waiting process
            semaphoreTime = self.copyOfProcesses[0]["TIME"]

            RunningBatches = threading.Thread(target=self.MonitorRunningBatches)
            RunningBatches.start()

            batchesOnHold = threading.Thread(target=self.MonitorBatchesOnHold)
            batchesOnHold.start()
            
            time.sleep(semaphoreTime)

        self.timerStatus = False

    # To count the time
    def Timer(self, initialTimePa): # This needs an initial time to get the difference (elpased time)
        while self.timerStatus:
            time.sleep(1)
            endTime = time.time()
            totalTime = round(endTime-initialTimePa, 0)
            
            self.clockLabel2["text"] = math.trunc(totalTime)
            self.clockLabel2.update()
        
        # Unlocking the program
        self.finishedButton.config(state=NORMAL)
    
    def MonitorBatchesOnHold(self):
        # If there is a process waiting, take its information
        if len(self.copyOfProcesses) > 0:
            # Taking information from a waiting process 
            waitingProcess = self.copyOfProcesses[0] 

            # Extracting process information
            self.onHoldText.config(state=NORMAL)
            self.onHoldText.delete(1.0, 'end')

            processInformation = ""
            processInformation += "ID: " + str(waitingProcess["ID"]) + "\n"
            processInformation += "PROGRAMMER: " + waitingProcess["PROGRAMMER"] + "\n"
            processInformation += "OPERATION: " + str(waitingProcess["OPERATION"]) + "\n"
            processInformation += "TIME: " + str(waitingProcess["TIME"]) + "\n"

            # To know how many processes are pending based on the current batch
            actualBatch = waitingProcess["BATCH"]
            pendingProcesses = -1

            for p in self.copyOfProcesses:
                if p["BATCH"] == actualBatch:
                    pendingProcesses += 1
            processInformation += f"\n\n{pendingProcesses} pending processes"

            # To know how many batches after the current one are pending
            batchCounter = set()
            for p in self.copyOfProcesses:
                if p["BATCH"] != actualBatch:
                    batchCounter.add(p["BATCH"])
            
            # Displaying the current process information
            self.onHoldText.insert('insert', processInformation)
            self.onHoldText.config(state=DISABLED)
            self.onHoldLabel3["text"] = str(len(batchCounter))
            self.onHoldLabel3.update()
        

    def MonitorRunningBatches(self):
        actualProcess = self.copyOfProcesses.pop(0) # Taking the first process in the list

        # To know the execution time of the process
        executionTime = int(actualProcess["TIME"])
        # To solve the mathematical operation
        operation = actualProcess["OPERATION"]
        operationResult = eval(operation)
            
        # Updating the received process time
        for t in range(executionTime, -1, -1):
            self.executionText.config(state=NORMAL)
            self.executionText.delete(1.0, 'end')

            processInformation = ""
            processInformation += "ID: " + str(actualProcess["ID"]) + "\n"
            processInformation += "PROGRAMMER: " + actualProcess["PROGRAMMER"] + "\n"
            processInformation += "OPERATION: " + str(actualProcess["OPERATION"]) + "\n"
            processInformation += "TIME: " + str(t) + "\n"
            self.executionText.insert('insert', processInformation)
            self.executionText.config(state=DISABLED)

            time.sleep(1)

        actualProcess["OPERATION"] = f"{operation} = {operationResult}"
        self.processResult.append(actualProcess)

        self.MonitorExecutedBatches(actualProcess)

    def MonitorExecutedBatches(self, processExecutedPa):
        processExecuted = processExecutedPa

        self.finishedText.config(state=NORMAL)
        self.finishedText.delete(1.0, 'end')

        processInformation = ""
        processInformation += "ID: " + str(processExecuted["ID"]) + "\n"
        processInformation += "PROGRAMMER: " + processExecuted["PROGRAMMER"] + "\n"
        processInformation += "OPERATION: " + str(processExecuted["OPERATION"]) + "\n"
        
        self.finishedText.insert('insert', processInformation)
        self.finishedText.config(state=DISABLED)

        # Deleting the last record
        self.executionText.config(state=NORMAL)
        self.executionText.delete(1.0, 'end')
        self.executionText.config(state=DISABLED)

    def SaveProcessResult(self):
        with open("processResult.txt", "w") as textFile:
            for p in self.processes:
                textFile.write(F"BATCH: {p['BATCH']}\n")
                textFile.write(F"ID: {p['ID']}\n")
                textFile.write(F"PROGRAMMER: {p['PROGRAMMER']}\n")
                textFile.write(F"OPERATION: {p['OPERATION']}\n")
                textFile.write("\n")
        MessageBox.showinfo("RESULTS", "The results have already been written.")

        # Cleaning screens unlocking program
        self.processEntry.config(state=NORMAL)
        self.processEntry.delete(0, END)
        self.finishedText.config(state=NORMAL)
        self.finishedText.delete(1.0, END)
        self.processButton.config(state=NORMAL)
        self.finishedButton.config(state=DISABLED)

if __name__ == "__main__":
    app = MainWidow()
    app.mainloop()

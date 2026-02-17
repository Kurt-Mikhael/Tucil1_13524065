from PIL import Image, ImageDraw, ImageFont
from model import *

import tkinter as tk
from tkinter import Button, messagebox, filedialog
import time
import os
import threading
import queue

QUEENS_LABEL = "#"
class GUI:
    def __init__(self, root, matrix):
        self.root = root
        self.matrix = matrix           
        self.rows = 0
        self.cols = 0
        self.ukuranSel = 64
        self.idRatu = []
        self.isRunning = False
        self.startTime = 0
        self.currentIdx = 0
        self.delay = 500
        self.mode = None
        self.root.title("Algoritma Brute Force untuk Masalah N-Queens")
        self.namaFileInput = ""

        self.workerThread = None
        self.resultQueue = queue.Queue()
        self.stopFlag = threading.Event()
        self.updateInterval = 1000000  
        self.progressCounter = 0

        topF = tk.Frame(root)
        topF.pack(pady=5, padx=10)


        cF = tk.Frame(root)
        cF.pack(pady=10,padx=10)

        self.startOptimalButton = tk.Button(cF, text="Optimal",bg="red", fg="white", font=("Arial", 12, "bold"), command=self.startOptimal)
        self.startOptimalButton.pack(side=tk.LEFT, padx=5)

        self.startBruteButton = tk.Button(cF, text="Brute Force",bg="purple", fg="white", font=("Arial", 12, "bold"), command=self.startBrute)
        self.startBruteButton.pack(side=tk.LEFT, padx=5)

        self.timer = tk.Label(cF, text="Waktu: 0.000dtk", font=("Arial", 12))
        self.timer.pack(side=tk.LEFT, padx=5)

        self.speedLabel = tk.Label(cF, text=f"Delay: {self.delay}ms", font=("Arial", 12))
        self.speedLabel.pack(side=tk.LEFT, padx=5)

        self.speedUp = tk.Button(cF, text="Speed Up", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=self.speedUpFunc)
        self.speedUp.pack(side=tk.LEFT, padx=5)

        self.speedDown = tk.Button(cF, text="Speed Down", bg="#ff0000", fg="white", font=("Arial", 12, "bold"), command=self.speedDownFunc)
        self.speedDown.pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(root, text="Status: Ready", font=("Arial", 12))
        self.status.pack(pady=10)

        self.loadFileButton = tk.Button(root, text="Load File", bg="#607D8B", fg="white", font=("Arial", 12, "bold"), command=self.loadFile)
        self.loadFileButton.pack(pady=5)
        
        self.fileLabel = tk.Label(root, text="File: (belum dipilih)", font=("Arial", 10))
        self.fileLabel.pack(padx=5)
        
        self.saveSolutionButton = tk.Button(root, text="Simpan As text", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), command=self.saveSolution)
        self.saveSolutionButton.pack(pady=10)
        
        self.saveCanvasButton = tk.Button(root, text="Simpan As Image", bg="#002A8D", fg="white", font=("Arial", 12, "bold"), command=self.saveCanvasAsImage)
        self.saveCanvasButton.pack(pady=5)

        self.canvas = tk.Canvas(root, background="white", width=max(self.cols,1)*self.ukuranSel, height=max(self.rows,1)*self.ukuranSel)
        self.canvas.pack(padx=20, pady=20)
        
        if self.rows > 0:
            self.drawGrid()

    def loadFile(self):
        if self.isRunning:
            messagebox.showwarning("Peringatan", "Algoritma sedang berjalan!")
            return
        filepath = filedialog.askopenfilename(
            title="Pilih file papan",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not filepath:
            return
        try:
            newMatrix = []
            colors = [chr(i).upper() for i in range(ord('a'), ord('z') + 1)]
            with open(filepath, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if any(c not in colors for c in line):
                            messagebox.showerror("Error", f"Karakter tidak valid: {line}")
                            return
                        newMatrix.append(list(line))
            if len(newMatrix) == 0:
                messagebox.showerror("Error", "File kosong!")
                return
            self.matrix = newMatrix
            self.namaFileInput = os.path.basename(filepath)
            self.rows = len(newMatrix)
            self.cols = len(newMatrix[0])
            for row in newMatrix:
                if len(row) != self.cols:
                    messagebox.showerror("Error", "Semua baris harus memiliki jumlah kolom yang sama!")
                    return
                    
            self.idRatu.clear()
            self.currentIdx = 0
            self.canvas.config(width=self.cols*self.ukuranSel, height=self.rows*self.ukuranSel)
            self.canvas.delete("all")
            self.drawGrid()
            self.fileLabel.config(text=f"File: {self.namaFileInput}")
            self.status.config(text="Status: Ready", fg="black")
            self.timer.config(text="Waktu: 0.000dtk")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file: {e}")
    def drawGrid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.ukuranSel
                y1 = i * self.ukuranSel
                x2 = x1 + self.ukuranSel
                y2 = y1 + self.ukuranSel
                char_color = self.matrix[i][j]
                color_hex = generateRGB(char_color)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_hex, outline="black")
                self.canvas.create_text(x1 + 10, y1 + 10, text=char_color, font=("Arial", 8), fill="#333")

    def saveSolution(self):

        if not hasattr(self, 'aktivCara'):
            messagebox.showwarning("Peringatan", "Tidak ada solusi yang sedang ditampilkan untuk disimpan!")
            return
        
        if self.isRunning:
            messagebox.showwarning("Peringatan", "Tidak dapat menyimpan saat algoritma sedang berjalan!")
            return
        
        if self.currentIdx >= len(self.aktivCara):
            messagebox.showwarning("Peringatan", "Tidak ada solusi yang sedang ditampilkan untuk disimpan!")
            return

        curDir = os.path.dirname(os.path.abspath(__file__))
        rootDir = os.path.dirname(curDir)
        testDir = os.path.join(rootDir, "test")
        if not os.path.exists(testDir):
            os.makedirs(testDir)

        curComb = self.aktivCara[self.currentIdx]
        isValid = isValidCombinationOptimal(curComb, self.matrix) if self.mode == 'optimal' else isValidCombination(curComb, self.matrix)
        if isValid:
            filename = f"solution_{self.namaFileInput}"
            filepath = os.path.join(testDir, filename)
            with open(filepath, "w") as file:
                for i in range(self.rows):
                    row = list(self.matrix[i])
                    if self.mode == 'optimal':
                        row[curComb[i]] = QUEENS_LABEL
                    else:
                        for r, c in curComb:
                            if r == i:
                                row[c] = QUEENS_LABEL
                    file.write("".join(row) + "\n")
            messagebox.showinfo("Sukses", f"Solusi disimpan sebagai test/{filename}")
        else:
            messagebox.showwarning("Peringatan", "Kombinasi saat ini bukan solusi yang valid!")
        

    def drawQueensOptimal(self, combination):
        for idRatu in self.idRatu:
            self.canvas.delete(idRatu)
        self.idRatu.clear()

        for row, col in enumerate(combination):
            x = col * self.ukuranSel + self.ukuranSel / 2
            y = row * self.ukuranSel + self.ukuranSel / 2
            qId = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="black", outline="white", width=2)
            qId_txt = self.canvas.create_text(x, y, text=QUEENS_LABEL, fill="white", font=("Arial", 12, "bold"))
            self.idRatu.append(qId)
            self.idRatu.append(qId_txt)

    def drawQueens(self, combination):
        for idRatu in self.idRatu:
            self.canvas.delete(idRatu)
        self.idRatu.clear()

        for row, col in combination:
            x = col * self.ukuranSel + self.ukuranSel / 2
            y = row * self.ukuranSel + self.ukuranSel / 2
            qId = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="black", outline="white", width=2)
            qId_txt = self.canvas.create_text(x, y, text=QUEENS_LABEL, fill="white", font=("Arial", 12, "bold"))
            self.idRatu.append(qId)
            self.idRatu.append(qId_txt)

    def saveCanvasAsImage(self):
        if not hasattr(self, 'aktivCara') or self.currentIdx >= len(self.aktivCara):
            messagebox.showwarning("Peringatan", "Tidak ada solusi yang sedang ditampilkan untuk disimpan!")
            return
        
        if self.isRunning:
            messagebox.showwarning("Peringatan", "Tidak dapat menyimpan saat algoritma sedang berjalan!")
            return
        
        curPath = os.path.dirname(os.path.abspath(__file__))
        rootDir = os.path.dirname(curPath)
        testDir = os.path.join(rootDir, "test")
        if not os.path.exists(testDir):
            os.makedirs(testDir)
        
        width = self.cols * self.ukuranSel
        height = self.rows * self.ukuranSel
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.ukuranSel
                y1 = i * self.ukuranSel
                x2 = x1 + self.ukuranSel
                y2 = y1 + self.ukuranSel
                char_color = self.matrix[i][j]
                color_hex = generateRGB(char_color)
                draw.rectangle([x1, y1, x2, y2], fill=color_hex, outline="black")
                draw.text((x1 + 5, y1 + 5), char_color, fill="#333")

        
        
        if hasattr(self, 'aktivCara') and self.currentIdx < len(self.aktivCara):
            curComb = self.aktivCara[self.currentIdx]
            if self.mode == 'optimal':
                positions = [(i, curComb[i]) for i in range(len(curComb))]
            else:
                positions = [(r, c) for r, c in curComb]
            for row, col in positions:
                cx = col * self.ukuranSel + self.ukuranSel // 2
                cy = row * self.ukuranSel + self.ukuranSel // 2
                r = 15
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill="black", outline="white", width=2)
                draw.text((cx-4, cy-6), QUEENS_LABEL, fill="white")
        namaFile = os.path.splitext(self.namaFileInput)[0]
        filename = f"solusi_{namaFile}.png"
        filepath = os.path.join(testDir, filename)
        img.save(filepath, 'PNG')
        
        messagebox.showinfo("Sukses", f"Canvas disimpan sebagai test/{filename}")
    
    def startOptimal(self):
        if len(self.matrix) == 0:
            messagebox.showwarning("Peringatan", "Silakan load file papan terlebih dahulu!")
            return
        if self.isRunning:
            return
        
        if not isKotakSamaWarna(self.matrix):
             messagebox.showerror("Error", "Jumlah warna unik pada papan tidak sama dengan jumlah kotak!")
             return

        self.mode = 'optimal'
        self.aktivCara = kombinasiBarisOptimal([i for i in range(self.cols)])
        self.isRunning = True
        self.startTime = time.time()
        self.currentIdx = 0
        self.startOptimalButton.config(state=tk.DISABLED)
        self.startBruteButton.config(state=tk.DISABLED)
        self.prosesAlgo()


    def workerBruteForce(self):
        try:
            allPositions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
            generator = kombinasiBarisGenerator(allPositions, self.cols)

            iterationCount = 0
            for combination in generator:
                if self.stopFlag.is_set():
                    self.resultQueue.put(('stopped', None, iterationCount))
                    return

                iterationCount += 1

                if iterationCount % self.updateInterval == 0:
                    self.resultQueue.put(('progress', combination, iterationCount))

                if isValidCombination(combination, self.matrix):
                    self.resultQueue.put(('found', combination, iterationCount))
                    return

            self.resultQueue.put(('notfound', None, iterationCount))

        except Exception as e:
            self.resultQueue.put(('error', str(e), 0))

    def startBrute(self):
        if len(self.matrix) == 0:
            messagebox.showwarning("Peringatan", "Silakan load file papan terlebih dahulu!")
            return
        if self.isRunning:
            return
        if not isKotakSamaWarna(self.matrix):
             messagebox.showerror("Error", "Jumlah warna unik pada papan tidak sama dengan jumlah kotak!")
             return

        if not isPersegi(self.rows, self.cols):
            messagebox.showerror("Error", "Papan harus berbentuk persegi!")
            return

        self.mode = 'bruteforce'
        self.isRunning = True
        self.startTime = time.time()
        self.progressCounter = 0
        self.stopFlag.clear()

        while not self.resultQueue.empty():
            self.resultQueue.get()

        self.startOptimalButton.config(state=tk.DISABLED)
        self.startBruteButton.config(state=tk.DISABLED)

        self.workerThread = threading.Thread(target=self.workerBruteForce, daemon=True)
        self.workerThread.start()

        self.checkQueue()

    def checkQueue(self):

        try:
            msgType, data, iterCount = self.resultQueue.get_nowait()

            if msgType == 'progress':
                self.progressCounter = iterCount
                waktu = time.time() - self.startTime
                self.timer.config(text=f"Waktu: {waktu:.3f}dtk")
                self.status.config(text=f"Testing iteration: {iterCount:,} | Last: {data}", fg="blue")
                self.drawQueens(data)

            elif msgType == 'found':
                self.isRunning = False
                waktu = time.time() - self.startTime
                self.timer.config(text=f"Waktu: {waktu:.3f}dtk")
                self.status.config(text=f"Solusi ditemukan: {data}", fg="green")
                self.drawQueens(data)

                self.aktivCara = [data]
                self.currentIdx = 0

                messagebox.showinfo("Sukses", f"Solusi Ditemukan!\n\nIterasi: {iterCount:,}\nWaktu: {waktu:.3f} detik")
                self.startOptimalButton.config(state=tk.NORMAL)
                self.startBruteButton.config(state=tk.NORMAL)
                return

            elif msgType == 'notfound':
                self.isRunning = False
                waktu = time.time() - self.startTime
                self.timer.config(text=f"Waktu: {waktu:.3f}dtk")
                self.status.config(text=f"Tidak ada solusi (checked {iterCount:,} combinations)", fg="red")
                messagebox.showinfo("Info", f"Tidak ada solusi yang valid\n\nTotal iterasi: {iterCount:,}\nWaktu: {waktu:.3f} detik")
                self.startOptimalButton.config(state=tk.NORMAL)
                self.startBruteButton.config(state=tk.NORMAL)
                return

            elif msgType == 'stopped':
                self.isRunning = False
                self.status.config(text="Dihentikan oleh user", fg="orange")
                self.startOptimalButton.config(state=tk.NORMAL)
                self.startBruteButton.config(state=tk.NORMAL)
                return

            elif msgType == 'error':
                self.isRunning = False
                self.status.config(text=f"Error: {data}", fg="red")
                messagebox.showerror("Error", f"Terjadi error: {data}")
                self.startOptimalButton.config(state=tk.NORMAL)
                self.startBruteButton.config(state=tk.NORMAL)
                return

        except queue.Empty:
            if self.isRunning:
                waktu = time.time() - self.startTime
                self.timer.config(text=f"Waktu: {waktu:.3f}dtk")

        if self.isRunning:
            self.root.after(100, self.checkQueue)  


    def speedUpFunc(self):
        self.delay = int(max(1, self.delay * 0.5)) 
        self.speedLabel.config(text=f"Delay: {self.delay}ms")

    def speedDownFunc(self):
        newDelay = int(self.delay * 1.5)

        if newDelay <= self.delay:
            self.delay += 1
        else :
            self.delay = newDelay
        self.speedLabel.config(text=f"Delay: {self.delay}ms")

    def prosesAlgo(self):



        if self.currentIdx >= len(self.aktivCara):
            self.isRunning = False
            self.startOptimalButton.config(state=tk.NORMAL)
            self.startBruteButton.config(state=tk.NORMAL)
            messagebox.showinfo("Info", "Tidak ada solusi yang valid")
            self.status.config(text="Selesai")
            return
        
        if not isPersegi(self.rows, self.cols):
            self.isRunning = False
            self.startOptimalButton.config(state=tk.NORMAL)
            self.startBruteButton.config(state=tk.NORMAL)
            messagebox.showerror("Error", "Papan harus berbentuk persegi!")
            self.status.config(text="Papan tidak persegi")
            return

        curComb = self.aktivCara[self.currentIdx]
        waktu = time.time() - self.startTime
        self.timer.config(text=f"Waktu: {waktu:.3f}dtk")
        self.status.config(text=f"Kombinasi: {curComb}", fg="black")

        if self.mode == 'optimal':
            self.drawQueensOptimal(curComb)
            isValid = isValidCombinationOptimal(curComb, self.matrix)
        else:
            self.drawQueens(curComb)
            isValid = isValidCombination(curComb, self.matrix)

        if isValid:
            self.isRunning = False
            self.status.config(text=f"Solusi ditemukan: {curComb}", fg="black")
            if self.mode == 'optimal':
                self.drawQueensOptimal(curComb)
            else:
                self.drawQueens(curComb)
            messagebox.showinfo("Sukses", f"Solusi Ditemukan dalam {time.time() - self.startTime:.3f} detik")
            self.startOptimalButton.config(state=tk.NORMAL)
            self.startBruteButton.config(state=tk.NORMAL)
            return
        
        self.currentIdx += 1
        self.root.after(self.delay, self.prosesAlgo) 


import customtkinter as ctk
import random
import time
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализатор сортировки")
        self.root.geometry("1000x700")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.array = []
        self.sorting = False
        self.speed = 0.05
        self.current_algorithm = "Пузырьковая сортировка"
        
        self.create_widgets()
        
    def create_widgets(self):
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
        
        self.generate_btn = ctk.CTkButton(
            control_frame, text="Сгенерировать массив", command=self.generate_array
        )
        self.generate_btn.pack(side=ctk.LEFT, padx=5)
        
        self.sort_btn = ctk.CTkButton(
            control_frame, text="Начать сортировку", command=self.start_sorting
        )
        self.sort_btn.pack(side=ctk.LEFT, padx=5)
        
        self.stop_btn = ctk.CTkButton(
            control_frame, text="Остановить", command=self.stop_sorting, state=ctk.DISABLED
        )
        self.stop_btn.pack(side=ctk.LEFT, padx=5)
        
        self.algorithm_var = ctk.StringVar(value=self.current_algorithm)
        algorithms = [
            "Пузырьковая сортировка",
            "Сортировка выбором",
            "Сортировка вставками",
            "Быстрая сортировка",
            "Сортировка слиянием",
            "Сортировка Шелла"
        ]
        
        algorithm_menu = ctk.CTkOptionMenu(
            control_frame, 
            variable=self.algorithm_var,
            values=algorithms,
            command=self.set_algorithm
        )
        algorithm_menu.pack(side=ctk.LEFT, padx=5)
        
        speed_label = ctk.CTkLabel(control_frame, text="Скорость:")
        speed_label.pack(side=ctk.LEFT, padx=(10, 0))
        
        self.speed_slider = ctk.CTkSlider(
            control_frame, 
            from_=0.01, 
            to=1.0, 
            command=self.set_speed,
            orientation="horizontal",
            width=100
        )
        self.speed_slider.set(self.speed)
        self.speed_slider.pack(side=ctk.LEFT, padx=5)
        
        self.visualization_frame = ctk.CTkFrame(self.root)
        self.visualization_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6), facecolor='#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.fig.patch.set_alpha(0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
        
        self.generate_array()
        
    def generate_array(self):
        if self.sorting:
            return
            
        size = random.randint(20, 50)
        self.array = [random.randint(1, 100) for _ in range(size)]
        self.update_plot()
        
    def update_plot(self, highlight=None):
        self.ax.clear()
        
        colors = ['#1f77b4'] * len(self.array)
        if highlight:
            colors[highlight[0]] = '#ff7f0e'
            if len(highlight) > 1:
                colors[highlight[1]] = '#ff7f0e'
        
        self.ax.bar(range(len(self.array)), self.array, color=colors)
        
        self.ax.set_xlim(-0.5, len(self.array)-0.5)
        self.ax.set_ylim(0, max(self.array)+10)
        
        self.canvas.draw()
        
    def set_algorithm(self, choice):
        self.current_algorithm = choice
        
    def set_speed(self, value):
        self.speed = float(value)
        
    def start_sorting(self):
        if self.sorting or len(self.array) == 0:
            return
            
        self.sorting = True
        self.generate_btn.configure(state=ctk.DISABLED)
        self.sort_btn.configure(state=ctk.DISABLED)
        self.stop_btn.configure(state=ctk.NORMAL)
        
        Thread(target=self.perform_sorting, daemon=True).start()
        
    def stop_sorting(self):
        self.sorting = False
        
    def perform_sorting(self):
        algorithm = self.current_algorithm
        
        if algorithm == "Пузырьковая сортировка":
            self.bubble_sort()
        elif algorithm == "Сортировка выбором":
            self.selection_sort()
        elif algorithm == "Сортировка вставками":
            self.insertion_sort()
        elif algorithm == "Быстрая сортировка":
            self.quick_sort_wrapper()
        elif algorithm == "Сортировка слиянием":
            self.merge_sort_wrapper()
        elif algorithm == "Сортировка Шелла":
            self.shell_sort()
            
        self.sorting = False
        self.root.after(0, self.on_sorting_finished)
        
    def on_sorting_finished(self):
        self.generate_btn.configure(state=ctk.NORMAL)
        self.sort_btn.configure(state=ctk.NORMAL)
        self.stop_btn.configure(state=ctk.DISABLED)
        
    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            if not self.sorting:
                break
                
            for j in range(0, n-i-1):
                if not self.sorting:
                    break
                    
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    self.root.after(1, self.update_plot, (j, j+1))
                    time.sleep(self.speed)
                    
    def selection_sort(self):
        n = len(self.array)
        for i in range(n):
            if not self.sorting:
                break
                
            min_idx = i
            for j in range(i+1, n):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
                    
                self.root.after(1, self.update_plot, (i, j))
                time.sleep(self.speed/2)
                
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.root.after(1, self.update_plot, (i, min_idx))
            time.sleep(self.speed)
            
    def insertion_sort(self):
        for i in range(1, len(self.array)):
            if not self.sorting:
                break
                
            key = self.array[i]
            j = i-1
            while j >= 0 and key < self.array[j]:
                self.array[j+1] = self.array[j]
                self.root.after(1, self.update_plot, (j, j+1))
                time.sleep(self.speed)
                j -= 1
                
            self.array[j+1] = key
            self.root.after(1, self.update_plot, (j+1,))
            time.sleep(self.speed)
            
    def quick_sort_wrapper(self):
        self.quick_sort(0, len(self.array)-1)
        
    def quick_sort(self, low, high):
        if low < high and self.sorting:
            pi = self.partition(low, high)
            self.quick_sort(low, pi-1)
            self.quick_sort(pi+1, high)
            
    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        
        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.root.after(1, self.update_plot, (i, j))
                time.sleep(self.speed)
                
        self.array[i+1], self.array[high] = self.array[high], self.array[i+1]
        self.root.after(1, self.update_plot, (i+1, high))
        time.sleep(self.speed)
        return i + 1
        
    def merge_sort_wrapper(self):
        self.merge_sort(0, len(self.array)-1)
        
    def merge_sort(self, l, r):
        if l < r and self.sorting:
            m = (l + r) // 2
            self.merge_sort(l, m)
            self.merge_sort(m+1, r)
            self.merge(l, m, r)
            
    def merge(self, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        
        L = [0] * n1
        R = [0] * n2
        
        for i in range(n1):
            L[i] = self.array[l + i]
            
        for j in range(n2):
            R[j] = self.array[m + 1 + j]
            
        i = j = 0
        k = l
        
        while i < n1 and j < n2 and self.sorting:
            if L[i] <= R[j]:
                self.array[k] = L[i]
                i += 1
            else:
                self.array[k] = R[j]
                j += 1
                
            self.root.after(1, self.update_plot, (k,))
            time.sleep(self.speed)
            k += 1
            
        while i < n1 and self.sorting:
            self.array[k] = L[i]
            self.root.after(1, self.update_plot, (k,))
            time.sleep(self.speed)
            i += 1
            k += 1
            
        while j < n2 and self.sorting:
            self.array[k] = R[j]
            self.root.after(1, self.update_plot, (k,))
            time.sleep(self.speed)
            j += 1
            k += 1
            
    def shell_sort(self):
        n = len(self.array)
        gap = n // 2
        
        while gap > 0 and self.sorting:
            for i in range(gap, n):
                if not self.sorting:
                    break
                    
                temp = self.array[i]
                j = i
                while j >= gap and self.array[j - gap] > temp and self.sorting:
                    self.array[j] = self.array[j - gap]
                    self.root.after(1, self.update_plot, (j, j - gap))
                    time.sleep(self.speed)
                    j -= gap
                    
                self.array[j] = temp
                self.root.after(1, self.update_plot, (j,))
                time.sleep(self.speed)
                
            gap //= 2

if __name__ == "__main__":
    root = ctk.CTk()
    app = SortingVisualizer(root)
    root.mainloop()
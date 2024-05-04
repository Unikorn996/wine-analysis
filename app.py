import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib import pyplot as plt


def read_csv(path='winequality.csv'):
    """Reads a csv file and returns a pandas dataframe"""
    df = pd.read_csv(path)
    return df


class WineQualityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Wine Quality App')
        self.geometry('800x600')
        self.df = read_csv()
        self.init_components()

    def init_components(self):
        self.label = Label(self, text='Wine Quality App', font=('Arial', 24))
        self.label.pack()

        self.combobox = ttk.Combobox(self, values=self.df.columns)
        self.combobox.pack()

        self.button = Button(self, text='Plot', command=self.plot)
        self.button.pack()

    def plot(self):
        column = self.combobox.get()
        plt.hist(self.df[column])
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.title(f'Histogram of {column}')
        plt.show()


if __name__ == '__main__':
    app = WineQualityApp()
    app.mainloop()

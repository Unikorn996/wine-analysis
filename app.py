from tkinter.constants import INSERT

import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt


def read_csv(path='winequality.csv'):
    """Reads a csv file and returns a pandas dataframe"""
    df = pd.read_csv(path)
    df = df.drop_duplicates()
    # remove null or empty value
    df = df.dropna(axis=0)
    return df


CHART_TYPE = ["PIE", "BAR"]
COMBOBOX_SELECT_EVENT = "<<ComboboxSelected>>"


class WineQualityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.df = read_csv()
        self.columns = list(self.df.keys())
        self.is_completed_form = None
        self.title('Wine Quality App')
        self.geometry('800x600')
        self.init_components()

    def init_components(self):
        self.label = ttk.Label(self, text='Wine Quality App', font=('Arial', 24))
        self.label.pack()

        self.error_text = tk.Text(self)
        self.error_text.insert(INSERT, "Select Chart type or Field first")

        self.chart_type_combobox = ttk.Combobox(
            self,
            width=27,
            values=CHART_TYPE,
        )
        self.chart_type_combobox.set("Select Chart Type")
        self.chart_type_combobox.bind(COMBOBOX_SELECT_EVENT, self.on_select_chart_type)
        self.chart_type_combobox.pack()

        self.wine_type_combobox = ttk.Combobox(
            self,
            width=27,
            values=list(self.df["type"].unique())
        )

        n = tk.StringVar()
        self.field_combobox = ttk.Combobox(
            self,
            width=27,
            values=["fixed acidity",
                    "volatile acidity",
                    "citric acid",
                    "residual sugar",
                    "chlorides",
                    "free sulfur dioxide",
                    "total sulfur dioxide",
                    "density",
                    "pH",
                    "sulphates",
                    "alcohol"
                    ],
            textvariable=n,
        )

        fig, ax = plt.subplots(figsize=(8, 6))
        self.ax = ax
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.button = ttk.Button(self, text='Plot', command=self.plot)

    def plot(self):
        selected_chart_type = self.chart_type_combobox.get()
        if not selected_chart_type:
            return
        self.ax.clear()
        if selected_chart_type == "PIE":
            self.plot_pie_chart()
        elif selected_chart_type == "BAR":
            self.plot_bar_chart()
        else:
            self.error_text.pack()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def plot_pie_chart(self):
        selected_wine_type = self.wine_type_combobox.get()
        if selected_wine_type is None:
            self.error_text.pack()
            return
        bins = [0.02, 0.06, 0.08, 0.1]
        data = self.df.copy()
        data["chlorides_range"] = pd.cut(data["chlorides"], bins)
        chlorides_with_wine_type = data[data["type"] == selected_wine_type]["chlorides_range"].value_counts()
        self.ax.pie(chlorides_with_wine_type, labels=chlorides_with_wine_type.index, autopct='%1.1f%%', startangle=140)
        self.ax.axis("equal")
        self.ax.set_title(f'Chlorides Data for {selected_wine_type} Wine Type')

    def plot_bar_chart(self):
        select_attr = self.field_combobox.get()
        if select_attr is None:
            return
        data = self.df.copy()
        grouped = data.groupby('type').mean()
        # Plotting bars for each type
        bar_width = 0.30
        index = range(len(grouped))
        bars1 = self.ax.bar(index, grouped['quality'], bar_width, label='Quality')
        bars2 = self.ax.bar([i + bar_width for i in index], grouped[select_attr], bar_width,
                            label=select_attr)
        # bars3 = self.ax.bar([i + 2 * bar_width for i in index], grouped['quality'], bar_width, label='Quality')

        # Setting labels and title
        self.ax.set_xlabel('Wine Type')
        self.ax.set_ylabel('Average Value')
        # self.ax.set_title('Average Alcohol and Residual Sugar by Wine Type')
        self.ax.set_xticks([i + bar_width / 2 for i in index])
        self.ax.set_xticklabels(grouped.index)
        self.ax.legend()

    def on_select_chart_type(self, event):
        self.button.pack_forget()
        self.field_combobox.pack_forget()
        self.wine_type_combobox.pack_forget()
        selected_option = self.chart_type_combobox.get()
        self.canvas_widget.pack_forget()
        if selected_option == "PIE":
            self.wine_type_combobox.pack()
        elif selected_option == "BAR":
            self.field_combobox.pack()
        else:
            self.field_combobox.pack()

        self.button.pack()


if __name__ == '__main__':
    app = WineQualityApp()
    app.mainloop()

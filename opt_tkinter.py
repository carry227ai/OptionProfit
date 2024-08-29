import tkinter as tk
from tkinter import ttk
import openpyxl
from option_layout import OptionLayout
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

root = tk.Tk()
root.title('OPTION RISK LAYOUT')
combo_list = ['BC', 'BP', 'SC', 'SP']

# Function for button clicked
def load_optionOI():
    # Reset treeview
    treeview.delete(*treeview.get_children())
    
    # Load data from xlsx file
    path = "./load_data/optionOI.xlsx"
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    
    list_values = list(sheet.values)
    for col_name in list_values[0]:
        treeview.heading(col_name, text=col_name)

    for values in list_values[1:]:
        treeview.insert(parent='', index=tk.END, values=values)
    
def ins_row():
    treeview.insert(parent='', index=tk.END, values=(opttype_combobox.get(), point_entry.get(), unit_spinbox.get(), cost_entry.get()))

def del_row():
    for i in treeview.selection():
        treeview.delete(i)

def save2xls():
    xlspath = "./load_data/optionOI.xlsx"
    if os.path.exists(xlspath):
        os.remove(xlspath)
    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    ws.append(cols)
    for line in treeview.get_children():
        ws.append([treeview.item(line)['values'][0], treeview.item(line)['values'][1], treeview.item(line)['values'][2], treeview.item(line)['values'][3]])
    
    wb.save(xlspath)

def show():
    opt = OptionLayout()
    for line in treeview.get_children():
        opt.add(treeview.item(line)['values'][0], treeview.item(line)['values'][1], treeview.item(line)['values'][2], treeview.item(line)['values'][3])
    
    opt.cal()
    Canvas = FigureCanvasTkAgg(opt.show(), master=frame)
    Canvas.draw()
    Canvas.get_tk_widget().grid(row=0, column=1,rowspan=3, padx=5, pady=5, sticky="ew")

      
# Set GUI object
frame = ttk.Frame(root)
frame.pack()
button_loadoption = ttk.Button(frame, text='LOAD OPTOI', command=load_optionOI)
button_loadoption.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=1, column=0, pady=10)

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ('OPTTYPE', 'POINT', 'UNIT', 'COST')
treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)
treeview.column("OPTTYPE", width=50)
treeview.column("POINT", width=50)
treeview.column("UNIT", width=50)
treeview.column("COST", width=50)
treeview.pack()
treeScroll.config(command=treeview.yview)

widgets_frame = ttk.LabelFrame(frame, text="INSERT DATA")
widgets_frame.grid(row=2, column=0, padx=5, pady=5)

opttype_label = ttk.Label(widgets_frame, text="OPTTYPE:")
opttype_label.grid(row=0, column=0, sticky="w")
opttype_combobox = ttk.Combobox(widgets_frame, values=combo_list)
opttype_combobox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

point_label = ttk.Label(widgets_frame, text="POINT:", anchor='w')
point_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
point_entry = ttk.Entry(widgets_frame, text='')
point_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

unit_label = ttk.Label(widgets_frame, text="UNIT:", anchor='w')
unit_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
unit_spinbox = ttk.Spinbox(widgets_frame, from_=1, to=10)
unit_spinbox.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

cost_label = ttk.Label(widgets_frame, text="COST:", anchor='w')
cost_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
cost_entry = ttk.Entry(widgets_frame, text='')
cost_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew")

button_ins = ttk.Button(widgets_frame, text='INSERT', command=ins_row)
button_ins.grid(row=8, column=0, padx=5, pady=5, sticky="ew")

button_del = ttk.Button(widgets_frame, text='DELETE', command=del_row)
button_del.grid(row=9, column=0, padx=5, pady=5, sticky="ew")

button_save2xls = ttk.Button(widgets_frame, text='SAVE', command=save2xls)
button_save2xls.grid(row=10, column=0, padx=5, pady=5, sticky="ew")

button_show = ttk.Button(frame, text='SHOW', command=show)
button_show.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

# Run
root.mainloop()
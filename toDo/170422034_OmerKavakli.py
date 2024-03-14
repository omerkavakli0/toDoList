import tkinter as tk
import tkinter.messagebox as mb
import csv

window = tk.Tk()
window.geometry("600x500")
window.title("toDo")
bg1 = "skyblue"

tasks_path = "tasks.csv"
done_path = "done.csv"

tasks = []
done = []

def show_in_lb(): #listelerdeki görevleri listBoxlara verir
    for task,importance in tasks:
        lb_Tasks.insert("end", task)
        lb_Tasks.itemconfig("end", {"fg": ["red", "olive", "green"][int(importance) - 1]})
    for task in done:
        lb_Done.insert("end", task)

def save_to_csv(): #listelerdeki görevler csv dosyalarına kaydeder
    with open(tasks_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for task,importance in tasks:
            writer.writerow([task, int(importance)])
    with open(done_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for task in done:
            writer.writerow(task)

def load_from_csv(): #csv dosyalarındaki görevleri listelere ekler
    try:
        with open(tasks_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                task, importance = row
                tasks.append([task,int(importance)])
        with open(done_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                done.append(row)
            show_in_lb()
    except FileNotFoundError:
        mb.showinfo(title="Info", message="CSV file not found.")

def add(): #entrydeki görevi radioButtondan aldığı önem derecesiyle beraber hem listeye hem listBoxa ekler
    T = newTask.get()
    if T:
        importance = choise.get()
        if importance in {1, 2, 3}:
            lb_Tasks.insert("end", T)
            newTask.set("")
            lb_Tasks.itemconfig("end", {"fg": ["red", "olive", "green"][importance - 1]})#görevi eklerken önem derecesine göre rengini ayarlar : 1-kırmızı 2-sarı 3-yeşil(zordan kolaya)
            tasks.append([T,importance])
        else:
            msg = mb.showerror(title="Error", message="Please choose an importance choice at first")
    else:
        msg = mb.showerror(title="Error",message="Empty tasks can't add")

def delButton_tasks(): #listBoxta seçili görevi hem liste hem listBoxtan siler
    selected_task_index = lb_Tasks.curselection()
    if selected_task_index:
        task_to_remove = lb_Tasks.get(selected_task_index)
        icolor = lb_Tasks.itemcget(selected_task_index, "fg")
        if icolor == "red":
            color = 1
        elif icolor == "olive":
            color = 2
        elif icolor == "green":
            color = 3
        tasks.remove([task_to_remove, color])
        lb_Tasks.delete(selected_task_index)

def do(): #listBoxta seçili görevi tamamlanan görev listesine ve listBoxına ekler tamamlanmamış olanlardan da siler
    selected_task_index = lb_Tasks.curselection()
    if selected_task_index:
        task = lb_Tasks.get(selected_task_index)
        icolor = lb_Tasks.itemcget(selected_task_index, "fg")
        if icolor == "red":
            color = 1
        elif icolor == "olive":
            color = 2
        elif icolor == "green":
            color = 3
        lb_Done.insert("end", task)
        lb_Tasks.delete(selected_task_index) #listeye göreviyle birlikte eklendiği için silerken de göreviyle birlikte arayıp bulmak ve silmek gerekiyor o yüzden görevin renginni önem derecesine çevirip listede kaydedilmiş halini arıyor
        tasks.remove([task,color])
        done.append([task])  

def delButton_done():#seçili görevi tamamlananlar listesi ve listBoxından siler
    selected_task_index = lb_Done.curselection()
    if selected_task_index:
        task_to_remove = list([lb_Done.get(selected_task_index)])
        icolor = lb_Done.itemcget(selected_task_index, "fg")
        if icolor == "red":
            color = 1
        elif icolor == "olive":
            color = 2
        elif icolor == "green":
            color = 3
        done.remove(task_to_remove)  # Remove the list [task_to_remove]
        lb_Done.delete(selected_task_index)

fmain = tk.LabelFrame(window, bg=bg1, text="Task Operations", width=500, height=300)
fmain.pack(ipadx=500, ipady=300)

newTask = tk.StringVar()
entryTask = tk.Entry(fmain, textvariable=newTask, width=30)
entryTask.place(x=50, y=4)

lbl_Task = tk.Label(fmain, text="Task :", bg=bg1)
lbl_Task.place(x=1, y=4)

lbl_ToDo = tk.Label(fmain,text="toDo :",bg=bg1)
lbl_ToDo.place(x=50, y=60)
lb_Tasks = tk.Listbox(fmain, width=30, height=20)
lb_Tasks.place(x=50, y=80)

addButton = tk.Button(fmain, text="Add", command=add)
addButton.place(x=50, y=30)

delButton = tk.Button(fmain, text="Delete", command=delButton_tasks)
delButton.place(x=90, y=30)

doButton = tk.Button(fmain, text="Do -->", command=do)
doButton.place(x=140, y=30)

lbl_Done = tk.Label(fmain,text="Done :",bg=bg1)
lbl_Done.place(x=250, y=60)
lb_Done = tk.Listbox(fmain, width=30, height=20,bg = "palegreen3",highlightbackground="black")
lb_Done.place(x=250, y=80)

delButton_done = tk.Button(fmain, text="Delete",command=delButton_done)
delButton_done.place(x=250, y=30)

lbl_Importance = tk.Label(fmain,text="Importance :",bg = bg1)
lbl_Importance.place(x=250,y=4)

choise = tk.IntVar()
rdButton = tk.Radiobutton(fmain,text = "High",bg = bg1,variable=choise,value=1)
rdButton.place(x=320,y=4)
rdButton2 = tk.Radiobutton(fmain,text = "Normal",bg = bg1,variable=choise,value=2)
rdButton2.place(x=380,y=4)
rdButton3 = tk.Radiobutton(fmain,text = "Less",bg = bg1,variable=choise,value=3)
rdButton3.place(x=450,y=4)

btn_Load = tk.Button(text="Load",command=load_from_csv)
btn_Load.place(x=50,y=430)

btn_Save = tk.Button(text="Save",command=save_to_csv)
btn_Save.place(x=90,y=430)


window.mainloop()

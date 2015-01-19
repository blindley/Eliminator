import os, glob, random
from tkinter import *
from tkinter import ttk
from PIL import ImageTk

def InitDatabase():
    cwd = os.getcwd()
    global_data['data_dir'] = cwd + "/eliminator_data"
    global_data['data_fname'] = global_data['data_dir'] + "/data.txt"
    current_files = set()
    for ext in ["png", "bmp", "jpg", "gif"]:
        for fname in glob.glob("*." + ext):
            current_files.add(fname)
    if len(current_files) < 2:
        print("no files to compare")
        return False
    if not os.path.isdir(global_data['data_dir']):
        os.makedirs(global_data['data_dir'])
    previous_files = set()
    scores = {}
    total_score = 0
    if not os.path.exists(global_data['data_fname']):
        open(global_data['data_fname'], "w+").close()
    with open(global_data['data_fname']) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                if parts[1] in current_files:
                    previous_files.add(parts[1])
                    score = int(parts[0])
                    total_score += score
                    scores[parts[1]] = score
    average_score = 0
    if not len(previous_files) == 0:
        average_score = int(total_score / len(previous_files))
    new_files = current_files.difference(previous_files)
    for fname in new_files:
        scores[fname] = average_score
    global_data['files'] = current_files
    global_data['scores'] = scores
    return True

def SaveDatabase():
    scores = list(global_data['scores'].items())
    scores.sort(key=lambda x: x[1])
    scores.reverse()
    with open(global_data['data_fname'], "w") as f:
        for score in scores:
            f.write("%i %s\n" % (score[1], score[0]))

def Next2Images():
    fnames = random.sample(global_data['files'], 2)
    global_data['left_fname'] = fnames[0]
    global_data['right_fname'] = fnames[1]
    left_image = ImageTk.PhotoImage(file=global_data['left_fname'])
    right_image = ImageTk.PhotoImage(file=global_data['right_fname'])
    global_data['left_button'].image = left_image
    global_data['right_button'].image = right_image
    global_data['left_button'].configure(image=left_image)
    global_data['right_button'].configure(image=right_image)

def RegisterData(data):
    global_data.update(data)

def ChooseLeft():
    lname = global_data['left_fname']
    rname = global_data['right_fname']
    global_data['scores'][lname] += 1
    global_data['scores'][rname] -= 1
    Next2Images()

def ChooseRight():
    lname = global_data['left_fname']
    rname = global_data['right_fname']
    global_data['scores'][lname] -= 1
    global_data['scores'][rname] += 1
    Next2Images()

def main():
    if not InitDatabase():
        return

    root = Tk()
    root.title("this is the title")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    temp_image = ImageTk.PhotoImage(file=list(global_data['files'])[0])

    lb = ttk.Button(mainframe, image=temp_image, command=ChooseLeft)
    lb.grid(column=1, row=1)
    rb = ttk.Button(mainframe, image=temp_image, command=ChooseRight)
    rb.grid(column=2, row=1)

    global_data['left_button'] = lb
    global_data['right_button'] = rb

    Next2Images()

    root.mainloop()

    SaveDatabase()

global_data = {}
if __name__ == "__main__":
    main()

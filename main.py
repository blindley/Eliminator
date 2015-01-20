import os, glob, random
from tkinter import *
from tkinter import ttk
from PIL import ImageTk

class ElimDataException(Exception):
    pass

class ElimData:
    def __init__(self):
        cwd = os.getcwd()
        self.data_dir = cwd + "/eliminator_data"
        self.data_filename = self.data_dir + "/data.txt"
        current_files = set()
        for ext in ["png", "bmp", "jpg", "gif"]:
            for filename in glob.glob("*." + ext):
                current_files.add(filename)
        if len(current_files) < 2:
            raise ElimDataException("No files to compare")
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)
        previous_files = set()
        scores = {}
        total_score = 0
        if not os.path.exists(self.data_filename):
            open(self.data_filename, "w+").close()
        with open(self.data_filename) as file:
            for line in file:
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
        for filename in new_files:
            scores[filename] = average_score
        self.files = current_files
        self.scores = scores

    def save(self):
        scores = list(self.scores.items())
        scores.sort(key=lambda x: x[1])
        scores.reverse()
        with open(self.data_filename, "w") as file:
            for score in scores:
                file.write("%i %s\n" % (score[1], score[0]))

class GuiData:
    def __init__(self):
        self.elim_data = ElimData()

        self.root = Tk()
        self.root.title("this is the title")

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        temp_image = ImageTk.PhotoImage(file=list(self.elim_data.files)[0])

        self.left_button = ttk.Button(
            mainframe, image=temp_image, command=self.chooseLeft)
        self.left_button.grid(column=1, row=1)
        self.right_button = ttk.Button(
            mainframe, image=temp_image, command=self.chooseRight)
        self.right_button.grid(column=2, row=1)

        self.next2Images()

    def next2Images(self):
        fnames = random.sample(self.elim_data.files, 2)
        self.left_filename = fnames[0]
        self.right_filename = fnames[1]
        left_image = ImageTk.PhotoImage(file=self.left_filename)
        right_image = ImageTk.PhotoImage(file=self.right_filename)
        self.left_button.image = left_image
        self.right_button.image = right_image
        self.left_button.configure(image=left_image)
        self.right_button.configure(image=right_image)

    def chooseLeft(self):
        self.elim_data.scores[self.left_filename] += 1
        self.elim_data.scores[self.right_filename] -= 1
        self.next2Images()

    def chooseRight(self):
        self.elim_data.scores[self.left_filename] -= 1
        self.elim_data.scores[self.right_filename] += 1
        self.next2Images()

    def loop(self):
        self.root.mainloop()
        self.elim_data.save()

def main():
    gui = GuiData()
    gui.loop()

if __name__ == "__main__":
    main()

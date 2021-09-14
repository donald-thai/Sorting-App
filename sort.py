from glob import glob
from shutil import copyfile
import os
from tkinter import filedialog
from tkinter import *
import tkinter.font as font


class HelpWindow(Toplevel):
    """
    Creates a help information window on top of main window
    """
    def __init__(self, parent):
        self.parent = parent
        Toplevel.__init__(self, self.parent)
        self.title("Help")
        self.geometry("900x500")
        self.resizable(height = False, width = False)
        self.information = Label(self, image = helpPic)
        self.information.place(relwidth = 1, relheight = 1)


class FileSort:
    def browse_folder(self):  # Method to choose which folder to sort
        """
        Select folder to be sorted

        Returns:
            str of directory of folder chosen to be sorted
        """
        self.directory = filedialog.askdirectory()  # Choose folder
        dir_name = os.path.basename(self.directory)  # Saves folder name
        self.dir.delete(0.0, END)
        self.dir.insert(END, "File Chosen: " + dir_name)  # Print folder name in GUI

    def file_sort(self, directory, copy):
        """
        Sorts the folder specified by file types within it and sorts files of same type in
        alphabetical order

        Parameters:
            directory (str): The folder to be sorted
            copy (str) : Location to create the sorted folders. Useful when there are folders
                         within a folder.
        """

        # Gets the first file's extension and stores it in a set
        file1 = glob(directory + "/*")[0]
        filetype1 = os.path.splitext(file1)[1]
        file_type = {filetype1}
        for file in glob(directory + "/*"):
            file_type.add(os.path.splitext(file)[1])
        for extension in file_type:

            # Checks if extension is a file because folders have a '' as their extension
            if extension != '':
                files = glob(directory + "/*" + extension)
                files.sort()
                os.mkdir(copy + "/" + extension)
                self.info.insert(END, f"Created Sorted {extension} folder!\n")

                # Copy files of the specified extension over to the newly created extension folder
                for item in files:
                    try:
                        copyfile(item, copy + "/" + extension + "/" + os.path.basename(item))
                        self.info.insert(END, f"Copied {os.path.basename(item)}!\n")
                    except PermissionError:
                        self.info.insert(END, f"Failed to copy {os.path.basename(item)}!\n")

            # If there is a folder within the main folder, sort it too
            elif extension == '':
                folders = []
                for item in glob(directory + "/*" + ''):
                    if not (os.path.isfile(item)):
                        folders.append(item)
                for folder in folders:
                    folder_copy = copy + "/" + os.path.basename(folder) + " Sorted"
                    os.mkdir(folder_copy)
                    self.file_sort(folder, folder_copy)

    def attempt_sort(self):
        self.info.delete(0.0, END)

        # Ensures that a folder has been chosen
        if self.directory == '':
            self.info.insert(END, f"Please make sure you have chosen a folder.\n")
            return

        # Makes sure there isn't a folder with the same name as __ Sorted
        if not (self.check_existing_dir()):
            os.mkdir(self.directory + " Sorted")
            self.info.insert(END, "Created Sorted folder!\n")
            copy = self.directory + " Sorted"
            try:
                self.file_sort(self.directory, copy)
                self.info.insert(END, "Sort COMPLETE! \n")
            except IndexError:
                self.info.insert(END, f"Unable to sort {self.directory} \n")
        else:
            self.info.insert(END,
                             f"Unable to create sorted folder. Please make sure you don't have folders named "
                             f"{os.path.basename(self.directory)} Sorted.\n")
            return

    def check_existing_dir(self):
        """
        Checks if the directory of the sroted folder already exists
            :return: true if it does, false otherwise
        """
        return os.path.isdir(self.directory + " Sorted")

    def help_pop_up(self):
        """
        Opens a help information box
        """
        HelpWindow(self.parent)

    def __init__(self, parent):
        self.directory = ""
        self.parent = parent
        self.parent.title("File Sorter by Donald Thai")
        self.parent.geometry("1000x600")

        self.pic = Label(parent, image = picture)
        self.pic.place(relheight = 1, relwidth = 1)
        self.cf = Frame(parent, bg = "grey", bd = 0)  # Make a center frame to put other elements in
        self.cf.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)
        self.background_image = Label(self.cf, image = picture)
        self.background_image.place(relheight = 1, relwidth = 1)

        self.dir = Text(self.cf)  # Creates box to display folder chosen
        self.dir.place(relx = .25, relheight = .05, relwidth = 1)
        self.find = Button(self.cf, text = "Choose folder",
                           command = self.browse_folder)
        self.find.place(relwidth = .2, relheight = .05)

        # Creates box to display info during sorting process
        self.info = Text(self.cf, wrap = "word")
        self.info.place(relx = .25, rely = .12, relheight = .8, relwidth = .75)
        scrollbar = Scrollbar(self.cf, command = self.info.yview)
        scrollbar.place(relx = .975, rely = .12, relwidth = .025, relheight = .8)
        self.info["yscrollcommand"] = scrollbar.set

        self.text_font = font.Font(size = 15)
        self.sb = Button(self.cf, text = "Sort!", font = self.text_font, command = self.attempt_sort)
        self.sb.place(rely = .12, relwidth = .2, relheight = .1)

        self.help = Button(parent, text = "?", command = self.help_pop_up)
        self.help.place(relx = .95, relwidth = .05, relheight = .05)


window = Tk()
picture = PhotoImage(file = "737385.png")  # Image for GUI background
helpPic = PhotoImage(file = "help pic.png")  # Information for help button
gui = FileSort(window)
window.mainloop()

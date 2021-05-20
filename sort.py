from glob import glob
from shutil import copyfile
import os
from tkinter import filedialog
from tkinter import *
import tkinter.font as font


class FileSort:
   def browse_folder(self, filedisplay):  # Method to choose which folder to sort
      global directory  # Makes directory a global variable
      directory = filedialog.askdirectory()  # Choose folder
      dir = os.path.basename(directory)  # Saves folder name
      filedisplay.delete(0.0, END)
      filedisplay.insert(END, "File Chosen: " + dir)  # Print folder name in GUI

   def fileSort1(self, directory, info, copy):  # Method to sort the files. Directory is folder to be sorted. Info
      # is the text box. Copy is the location to created the sorted folders.
      try:
         file1 = glob(directory + "/*")[0]  # Get the first file in the folder
         filetype1 = os.path.splitext(file1)[1]  # Get the file type of that file
         type = {filetype1}  # Add that file type to a set
         for file in glob(directory + "/*"):  # Go through the entire folder and add the file type to a set
            type.add(os.path.splitext(file)[1])
         for extension in type:  # Loops through all of the file types in the set
            if extension != '':  # If it has a file type (folders don't have one and return '' instead)
               list = []
               for file in glob(directory + "/*" + extension):  # Add all files with that extension in folder to list
                  list.append(file)
               list.sort()  # Sort files alphabetically
               try:
                  os.mkdir(copy + "/" + extension)  # Make a folder to store these files in
                  info.insert(END, f"Created Sorted {extension} folder!\n")
               except:
                  info.insert(END, f"Failed to create Sorted {extension} folder.\n")
               for item in list:  # Try to copy files over to new sorted folder
                  try:
                     copyfile(item, copy + "/" + extension + "/" + os.path.basename(item))
                     info.insert(END, f"Copied {os.path.basename(item)}!\n")
                  except:
                     info.insert(END, f"Failed to copy {os.path.basename(item)}!\n")
            elif extension == '':  # If there is a folder, find it, make a sorted folder for it, and sort it.
               folders = []
               for file in glob(directory + "/*" + ''):
                  if not (os.path.isfile(file)):
                     folders.append(file)
               for folder in folders:
                  os.mkdir(copy + "/" + os.path.basename(folder) + " Sorted")
                  foldercopy = copy + "/" + os.path.basename(folder) + " Sorted"
                  self.fileSort1(folder, info, foldercopy)
      except:
         info.insert(END, f"Unable to sort {directory} \n")

   def fileSort2(self, directory, info):
      info.delete(0.0, END)  # Clear the info box
      if directory == '':  # Makes sure there is a folder chosen
         info.insert(END, f"Please make sure you have chosen a folder.\n")
         return
      try:
         os.mkdir(directory + " Sorted")  # Make a parent folder to store all of the other sorted folders in
         info.insert(END, "Created sorted folder!\n")
         copy = directory + " Sorted"
         self.fileSort1(directory, info, copy)  # Actually sort the folder. Copy is the directory to add the other
         # folders to. Useful when there is a folder within a folder
         info.insert(END, "Sort COMPLETE! \n")
      except:
         info.insert(END,
                     f"Unable to create sorted folder. Please make sure you don't have folders named {os.path.basename(directory)} Sorted.\n")
         return

   def helpPopUp(self):  # Makes the help information box when you click the ?
      help = Toplevel()
      help.title("Help")
      help.geometry("900x500")
      help.resizable(height=False, width=False)
      information = Label(help, image=helpPic)
      information.place(relwidth=1, relheight=1)

   def __init__(self, parent):  # Creates the main GUI
      self.parent = parent
      parent.title("File Sorter by Donald Thai")  # Names window and sets size
      parent.geometry("1000x600")

      self.pic = Label(parent, image=picture)  # Places the background image
      self.pic.place(relheight=1, relwidth=1)
      self.cf = Frame(parent, bg="grey", bd=0)  # Make a center frame to put other elements in
      self.cf.place(relx=.1, rely=.1, relwidth=.8, relheight=.8)
      Label(self.cf, image=picture).place(relheight=1, relwidth=1)

      self.dir = Text(self.cf)  # Creates box to display folder chosen
      self.dir.place(relx=.25, relheight=.05, relwidth=1)
      self.find = Button(self.cf, text="Choose folder",
                         command=lambda: self.browse_folder(self.dir))  # Creates button to select folder
      self.find.place(relwidth=.2, relheight=.05)  # Maybe add a clear file?

      self.info = Text(self.cf)  # Creates box to display info during sorting process
      self.info.place(relx=.25, rely=.12, relheight=.8, relwidth=1)

      textFont = font.Font(size=15)  # Sets size of the words in the sort button
      self.sb = Button(self.cf, text="Sort!", font=textFont,
                       command=lambda: self.fileSort2(directory, self.info))  # Creates button to sort chosen folder
      self.sb.place(rely=.12, relwidth=.2, relheight=.1)

      self.help = Button(parent, text="?", command=self.helpPopUp)  # Creates the help button
      self.help.place(relx=.95, relwidth=.05, relheight=.05)


window = Tk()  # Creates parent on which the GUI will be built
picture = PhotoImage(file="737385.png")  # Image for GUI background
helpPic = PhotoImage(file="help pic.png")  # Information for help button
one = FileSort(window)  # Create an instance of the GUI
window.mainloop()  # Runs the GUI

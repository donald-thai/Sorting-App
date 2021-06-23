from glob import glob
from shutil import copyfile
import os
from tkinter import filedialog
from tkinter import *
import tkinter.font as font


class FileSort:
   def browse_folder(self):  # Method to choose which folder to sort
      self.directory = filedialog.askdirectory()  # Choose folder
      dir_name = os.path.basename(self.directory)  # Saves folder name
      self.dir.delete(0.0, END)
      self.dir.insert(END, "File Chosen: " + dir_name)  # Print folder name in GUI

   def fileSort1(self, directory, copy):  # Method to sort the files. Directory is folder to be sorted. Cannot be self.directory because this method is also used to sort folders within the main folder
      # Copy is the location to created the sorted folders.
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
                  self.info.insert(END, f"Created Sorted {extension} folder!\n")
               except:
                  self.info.insert(END, f"Failed to create Sorted {extension} folder.\n")
               for item in list:  # Try to copy files over to new sorted folder
                  try:
                     copyfile(item, copy + "/" + extension + "/" + os.path.basename(item))
                     self.info.insert(END, f"Copied {os.path.basename(item)}!\n")
                  except:
                     self.info.insert(END, f"Failed to copy {os.path.basename(item)}!\n")
            elif extension == '':  # If there is a folder, find it, make a sorted folder for it, and sort it.
               folders = []
               for file in glob(directory + "/*" + ''):
                  if not (os.path.isfile(file)):
                     folders.append(file)
               for folder in folders:
                  os.mkdir(copy + "/" + os.path.basename(folder) + " Sorted")
                  folder_copy = copy + "/" + os.path.basename(folder) + " Sorted"
                  self.fileSort1(folder, folder_copy)
      except:
         self.info.insert(END, f"Unable to sort {directory} \n")

   def fileSort2(self):
      self.info.delete(0.0, END)  # Clear the info box
      if self.directory == '':  # Makes sure there is a folder chosen
         self.info.insert(END, f"Please make sure you have chosen a folder.\n")
         return
      try:
         os.mkdir(self.directory + " Sorted")  # Make a parent folder to store all of the other sorted folders in
         self.info.insert(END, "Created sorted folder!\n")
         copy = self.directory + " Sorted"
         self.fileSort1(self.directory,copy)  # Actually sort the folder. Copy is the directory to add the other
         # folders to. Useful when there is a folder within a folder
         self.info.insert(END, "Sort COMPLETE! \n")
      except:
         self.info.insert(END,
                     f"Unable to create sorted folder. Please make sure you don't have folders named {os.path.basename(self.directory)} Sorted.\n")
         return

   def helpPopUp(self):  # Makes the help information box when you click the ?
      help = Toplevel()
      help.title("Help")
      help.geometry("900x500")
      help.resizable(height=False, width=False)
      information = Label(help, image=helpPic)
      information.place(relwidth=1, relheight=1)

   def __init__(self, parent):  # Creates the main GUI
      self.directory= ""
      self.parent = parent
      self.parent.title("File Sorter by Donald Thai")  # Names window and sets size
      self.parent.geometry("1000x600")

      self.pic = Label(parent, image=picture)  # Places the background image
      self.pic.place(relheight=1, relwidth=1)
      self.cf = Frame(parent, bg="grey", bd=0)  # Make a center frame to put other elements in
      self.cf.place(relx=.1, rely=.1, relwidth=.8, relheight=.8)
      self.background_image = Label(self.cf, image=picture)
      self.background_image.place(relheight=1, relwidth=1)

      self.dir = Text(self.cf)  # Creates box to display folder chosen
      self.dir.place(relx=.25, relheight=.05, relwidth=1)
      self.find = Button(self.cf, text="Choose folder",
                         command=self.browse_folder)  # Creates button to select folder
      self.find.place(relwidth=.2, relheight=.05)  # Maybe add a clear file?

      self.info = Text(self.cf)  # Creates box to display info during sorting process
      self.info.place(relx=.25, rely=.12, relheight=.8, relwidth=1)

      self.text_font = font.Font(size=15)  # Sets size of the words in the sort button
      self.sb = Button(self.cf, text="Sort!", font=self.text_font,
                       command= self.fileSort2)  # Creates button to sort chosen folder
      self.sb.place(rely=.12, relwidth=.2, relheight=.1)

      self.help = Button(parent, text="?", command=self.helpPopUp)  # Creates the help button
      self.help.place(relx=.95, relwidth=.05, relheight=.05)


window = Tk()  # Creates parent on which the GUI will be built
picture = PhotoImage(file="737385.png")  # Image for GUI background
helpPic = PhotoImage(file="help pic.png")  # Information for help button
gui = FileSort(window)  # Create an instance of the GUI
window.mainloop()  # Runs the GUI

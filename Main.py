import time
import zipfile
import os , copy
from tkinter import *
from datetime import date
import tkinter.tix as tix
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Menu, Button
from tkinter import LEFT, TOP, X, FLAT, RAISED
from tkinter.filedialog import asksaveasfile 
#Matplotlib for IMAGE view
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#SentinelSat to download Dataset
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
#Import from another file 
from  preprocessing import *
#from Object_detection.yolo_object_detection import *
from Object_detection.main_program import *
os.environ['PROJ_LIB'] = 'C:\\Program Files\\GDAL\\projlib\\'

class AzmuthStar(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("AzmuthStar")

        #*****MENUBAR*****#
        #FILE
        menubar = Menu(self.master)
        self.master.bind('<Control-q>', quit)
        self.fileMenu = Menu(self.master, tearoff=0)
        self.fileMenu.add_command(label="Open Product...", command=self.openpro)
        self.fileMenu.add_command(label="Save", command=self.savepro)
        # self.fileMenu.add_command(label="Save As", command="")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit        'Ctrl+Q'", command=self.onExit)
        menubar.add_cascade(label="File", menu=self.fileMenu)

        #Tools
        self.filterMenu = Menu(self.master, tearoff=0)
        self.filterMenu.add_command(label="Speckle Filtering", command="")
        #self.editMenu.add_separator()
        menubar.add_cascade(label="Tools", menu=self.filterMenu)
        
        #View
        self.editMenu = Menu(self.master, tearoff=0)
        self.editMenu.add_command(label="Cut", command="")
        self.editMenu.add_command(label="Copy", command="")
        self.editMenu.add_command(label="Paste", command="")
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Delete", command="")
        menubar.add_cascade(label="View", menu=self.editMenu)

        #Help
        self.helpMenu = Menu(self.master, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.about)
        #self.helpMenu.add_separator()
        menubar.add_cascade(label="Help",menu=self.helpMenu)

        #*****Toolbar*****#
        toolbar = Frame(self.master, bd=1, relief=RAISED)

        #Open
        self.img = Image.open("img\\folder.png")
        openimg = ImageTk.PhotoImage(self.img)

        openButton = Button(toolbar, image=openimg, relief=FLAT,
            command=self.openpro)
        openButton.image = openimg
        openButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

        #Save
        self.img = Image.open("img\\save.png")
        saveimg = ImageTk.PhotoImage(self.img)

        openButton = Button(toolbar, image=saveimg, relief=FLAT,
            command=self.savepro)
        openButton.image = saveimg
        openButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

        #Download
        self.img = Image.open("img\\download.png")
        downimg = ImageTk.PhotoImage(self.img)

        openButton = Button(toolbar, image=downimg, relief=FLAT,
            command=self.down_window)
        openButton.image = downimg
        openButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

        #Discrimination
        self.img = Image.open("img\\scissor.png")
        cutimg = ImageTk.PhotoImage(self.img)

        openButton = Button(toolbar, image=cutimg, relief=FLAT,
            command=self.land_water_descrimination)
        openButton.image = cutimg
        openButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

        #Detection
        self.img = Image.open("img\\search.png")
        searchimg = ImageTk.PhotoImage(self.img)

        openButton = Button(toolbar, image=searchimg, relief=FLAT,
            command=self.browsetrainFiles)
        openButton.image = searchimg
        openButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

        #Map
        self.img = Image.open("img\\location.png")
        Mapimg = ImageTk.PhotoImage(self.img)

        openButton = Button(toolbar, image=Mapimg, relief=FLAT,
            command=self.showmap)
        openButton.image = Mapimg
        openButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

        #Exit
        self.img = Image.open("img\\exit.png")
        eimg = ImageTk.PhotoImage(self.img)

        exitButton = Button(toolbar, image=eimg, relief=FLAT,
            command=self.quit)
        exitButton.image = eimg
        exitButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

    def onExit(self):
        self.quit()

    def openpro(self):
        currdir = os.getcwd()
        files = [('JPG (.jpg)', '*.jpg'),('PNG (.png)', '*.png'),('TIFF (.tiff)', '*.tiff')]
        self.file = filedialog.askopenfilename(initialdir = currdir ,title = "Open Product",filetypes = files, defaultextension = files)

    def savepro(self):
        currdir = os.getcwd()
        files = [('JPG (.jpg)', '*.jpg'),('PNG (.png)', '*.png'),('TIFF (.tiff)', '*.tiff')] 
        self.file = asksaveasfile(initialdir = currdir ,filetypes = files,title = "Save Product",defaultextension = files)

    def about(self):
        messagebox.showinfo('About', 'Created By Team AzmuthStar.')    

    def sentineldown(self):
        os.system('sentinelsat.py')

    def outputfolder(self):
        import subprocess
        subprocess.Popen('explorer "Processes\\Download\\Unzip\\"')

    #TopLevel Download window buttons 
    def down_window(self):
        self.window = Toplevel(self.master)
        self.window.geometry('320x100')
        self.window.iconphoto(False,PhotoImage(file='img\\download.png'))
        self.window.title("Copernicus Open Access Hub")

        self.label_username = Label(self.window, text="Username")
        self.label_password = Label(self.window, text="Password")
        self.label_product_id = Label(self.window, text="Product ID")
        self.entry_username = Entry(self.window)
        self.entry_password = Entry(self.window, show="*")
        self.entry_product_id = Entry(self.window)

        self.label_username.grid(row=2,column=1,sticky=E)
        self.label_password.grid(row=3,column=1,sticky=E)
        self.label_product_id.grid(row=4,column=1,sticky=E)
        self.entry_username.grid(row=2, column=2)
        self.entry_password.grid(row=3, column=2)
        self.entry_product_id.grid(row=4, column=2)

        self.downbtn = Button(self.window, text="Download", command=self._down_btn_clicked)
        #self.button = Button(self.window, text="Download", command=lambda:[self.savepro(), self.sentinelsat()])
        self.downbtn.place(bordermode=OUTSIDE,relx = 0.1, rely = 0.7)
        self.unzip = Button(self.window, text="Unzip", command=self.zip)
        self.unzip.place(bordermode=OUTSIDE,relx = 0.3, rely = 0.7)
        self.outFile = Button(self.window, text="Output Folder", command=self.outputfolder)
        self.outFile.place(bordermode=OUTSIDE,relx = 0.5, rely = 0.7)

    def zip(self):
        files = [('ZIP (.zip)', '*.zip'),('RAR (.rar)', '*.rar')]
        self.file_name = filedialog.askopenfilename(initialdir = "Processes\\Download\\" ,title = "Select Zip file",filetypes = files, defaultextension = files)        
        with zipfile.ZipFile(self.file_name, 'r') as file:
            # printing all the information of archive file contents using 'printdir' method
            print(file.printdir())
            # extracting the files using 'extracall' method
            print('Extracting all files...')
            file.extractall('Processes\\Download\\Unzip')
            print('Done!!')
            #print('Done!') # check your directory of zip file to see the extracted files

    def _down_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        product_id = self.entry_product_id.get()
        #print(username, password,product_id)
        api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')
        print("Downloading started...")
        api.download(product_id)

    def browsetrainFiles(self): 
        files = [('All (All)', '*.*'),('JPG (.jpg)', '*.jpg'),('PNG (.png)', '*.png'),('TIFF (.tiff)', '*.tiff')]
        filename = filedialog.askopenfilename(initialdir = "Processes\\Ocean\\", title = "Select a File", filetypes = files, defaultextension = files)
        print(filename)
        file_path = filename.replace('/','\\')
        print(file_path)
        main_detection(file_path)
        # cmd = 'python ' + 'single_file_testing.py' + ' ' + filename
        # os.system(cmd)

    def land_water_descrimination(self):
        self.window = Toplevel(self.master)
        self.window.geometry('300x80')
        self.window.iconphoto(False,PhotoImage(file='img\\scissor.png'))
        self.window.title("Land Water Descrimination")
        def water_extraction():
        	files = [('All (All)', '*.*'),('TIFF (.tiff)', '*.tiff')]
        	filename = filedialog.askopenfilename(initialdir = "Processes\\Visible\\", title = "Select a File", filetypes = files, defaultextension = files)
        	src_file = filename.replace('/','\\')
        	Water_Extraction(src_file)

        def land_extraction():
        	files = [('All (All)', '*.*'),('TIFF (.tiff)', '*.tiff')]
        	filename = filedialog.askopenfilename(initialdir = "Processes\\Visible\\", title = "Select a File", filetypes = files, defaultextension = files)
        	src_file = filename.replace('/','\\')
        	Land_Extraction(src_file)

        self.water = Button(self.window, text="Water Extraction", command=water_extraction)
        self.water.pack(pady=2)
        self.land = Button(self.window, text="Land Extraction", command=land_extraction)
        self.land.pack(pady=2)

    def showmap(self):
        os.system('python map.py')

        
def main():
    dire=None
    colList=[]
    root = Tk()
    root.geometry("1100x600+300+300")
    root.iconphoto(False,PhotoImage(file='img\\main.png'))
    root.configure(bg='white')
    statusbar = Label(root, text="Welcome ,",relief=SUNKEN, anchor=W)
    statusbar.pack(side=BOTTOM, fill=X)
    app = AzmuthStar()

    #*****LeftSideBar*****
    LeftSideBar=Frame(root,borderwidth=4,relief="flat",width=300,height=500,bg='#cfcfcf')
    LeftSideBar.pack(side='left',fill='y')
    fileTitle = Label(LeftSideBar,text="Tools",width=30,anchor="center")
    fileTitle.pack(side='top',fill='x',pady=4)

    # #Product Explorer
    # def print_selected(args):
    #     #print('selected dir:', args)
    #     global dire
    #     dire = args
    #     f=open('log.txt','w')
    #     f.write(str(args))
    #     f.close()

    # def ProExplorer():
    #     root1 = tix.Tk()
    #     #newWindow = Toplevel(root)
    #     tix.DirSelectDialog(master=root1, command=print_selected).popup()
    #     root1.withdraw()

    # button = Button(LeftSideBar, text="Product Explorer", borderwidth=2.5, command=ProExplorer)
    # button.pack(side='top',fill='x',pady=8)
    #*****RightSideBar*****
    RightSideBar=Frame(root,borderwidth=4,relief="flat",bg='#cfcfcf') #width=907
    RightSideBar.pack(side='right',fill='y')
    
    #Image View in Right Side Bar
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas1 = FigureCanvasTkAgg(fig, master=root)
    canvas1.draw()
    toolbar = NavigationToolbar2Tk(canvas1,LeftSideBar)
    toolbar.update()
    toolbar.pack(side=TOP, fill=X, padx=8)
    canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, padx=10, pady=5)
    canvas1._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx=10, pady=5)
    def on_key_press(event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, canvas1, toolbar)


    canvas1.mpl_connect("key_press_event", on_key_press)
    def _load():
    	import rasterio as rio
    	from rasterio.plot import show
    	ax = fig.add_subplot(111)
    	fig.subplots_adjust(bottom=0, right=1, top=1, left=0, wspace=0, hspace=0)
    	files = [('All (All)', '*.*'),('TIFF (.tiff)', '*.tiff'),('JPG (.jpg)', '*.jpg'),('PNG (.png)', '*.png')]
    	file_name = filedialog.askopenfilename(initialdir = "Object_detection\\processes\\detected_ships\\" ,title = "Select Image",filetypes = files, defaultextension = files)        
    	with rio.open(file_name) as src_plot:
    		show(src_plot, ax=ax, cmap='gist_gray')
    	plt.close()
    	ax.set(title="",xticks=[], yticks=[])
    	ax.spines["top"].set_visible(False)
    	ax.spines["right"].set_visible(False)
    	ax.spines["left"].set_visible(False)
    	ax.spines["bottom"].set_visible(False)
    	canvas1.draw()

    button = Button(LeftSideBar, text="Display Image", command=_load)
    button.pack(side=TOP,pady=6)

    def convert_and_visible_open():
    	files = [('All (All)', '*.*'),('TIFF (.tiff)', '*.tiff')]
    	filename = filedialog.askopenfilename(initialdir = "Processes\\Download\\Unzip\\", title = "Select a File", filetypes = files, defaultextension = files)
    	in_file = filename.replace('/','\\')
    	convert_and_visible(in_file)
    #pre_processing
        
    button_candv = Button(LeftSideBar, text="convert & Visible", command=convert_and_visible_open)
    button_candv.pack(side=TOP,pady=2)

    root.mainloop()

if __name__ == '__main__':
    main()

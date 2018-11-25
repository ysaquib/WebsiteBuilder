# 	 15-112: Principles of Programming and Computer Science
# 	 Final Project: Website Builder
#	 Name      : Yusuf Saquib
#    AndrewID  : ysaquib

#	 File Created: 24 Nov 2018
#    Modification History:
#    Start            End
#    24 Nov 2018      
#    


from Tkinter import *

class MainUI():

	def __init__(self):
		self.root = Tk()
		self.s_width = str(self.root.winfo_screenwidth())
		self.s_height = str(self.root.winfo_screenheight())
		self.root.geometry(self.s_width + "x" + self.s_height)
		self.root.title("WebsiteBuilder")

		selectTemplate = SelectTemplate()

		self.root.mainloop()



class SelectTemplate():

	def __init__(self):
		self.root = Tk()
		self.root.geometry("620x420")
		self.root.title("Choose a Template")
		self.root.attributes("-topmost", True)

		self.createWidgets()
		self.root.lift()

		self.root.mainloop()

	def getTemplateNew(self):
		self.root.destroy()

	def openTemplate1(self):
		self.root.destroy()
		temp1 = TemplateOne()

	def createWidgets(self):

		rows = 0
		while rows < 4:
			self.root.rowconfigure(rows)
			self.root.columnconfigure(rows)
			rows += 1
		cols = 0
		while cols < 3:
			self.root.rowconfigure(cols)
			self.root.columnconfigure(cols)
			cols += 1

		self.lbl_chooseTemplate = Label(self.root, text="Create New Website")
		self.lbl_chooseTemplate.grid(row = 0, column = 1, padx = 40, pady = 30)

		self.template1 = Button(self.root, text = "Template 1", width = 16, height = 4, command=self.openTemplate1)
		self.template1.grid(row = 1, column = 0, padx = 40, pady = 30)
		self.template2 = Button(self.root, text = "       ", width = 16, height = 4)
		self.template2.grid(row = 1, column = 1, padx = 40, pady = 30)
		self.template3 = Button(self.root, text = "       ", width = 16, height = 4)
		self.template3.grid(row = 1, column = 2, padx = 40, pady = 30)
		self.template4 = Button(self.root, text = "       ", width = 16, height = 4)
		self.template4.grid(row = 2, column = 0, padx = 40, pady = 30)
		self.template5 = Button(self.root, text = "       ", width = 16, height = 4)
		self.template5.grid(row = 2, column = 1, padx = 40, pady = 30)
		self.template6 = Button(self.root, text = "       ", width = 16, height = 4)
		self.template6.grid(row = 2, column = 2, padx = 40, pady = 30)

		self.btn_create = Button(self.root, text = "Create Website", command = self.getTemplateNew)
		self.btn_create.grid(row = 3, column = 0, padx = 5, pady = 5)

		self.btn_open = Button(self.root, text = "Open Recent", state = DISABLED)
		self.btn_open.grid(row = 3, column = 2, padx = 5, pady = 5)

class TemplateOne():
	def __init__(self):
		self.root = Tk()
		self.s_width = str(self.root.winfo_screenwidth())
		self.s_height = str(self.root.winfo_screenheight())
		self.root.geometry(self.s_width + "x" + self.s_height)
		self.root.title("Template One")
		self.isDragged = 0
		self.createWidgets()

		self.root.mainloop()


	def move (self, event):
		if self.isDragged:
			new_xPos, new_yPos = event.x, event.y
			self.mainCanvas.move(event.widget.find_withtag(CURRENT), new_xPos-self.mouse_xPos, new_yPos-self.mouse_yPos)
			print new_xPos, new_yPos

		else:
			self.isDragged = True
        	self.mainCanvas.tag_raise("draggable")
        	self.mouse_xPos = event.x
        	self.mouse_yPos = event.y

	def release(self, event):
		self.isDragged = False


	def createWidgets(self):

		self.menuBar = Menu(self.root)
		self.fileBar = Menu(self.menuBar, tearoff=0)
		self.editBar = Menu(self.menuBar, tearoff=0)

		self.menuBar.add_cascade(label="File", menu=self.fileBar)
		self.menuBar.add_cascade(label="Edit", menu=self.editBar)

		self.fileBar.add_command(label="Export to HTML")

		self.editBar.add_command(label="Cut")
		self.editBar.add_command(label="Copy")
		self.editBar.add_command(label="Paste")

		self.root.config(menu=self.menuBar)

		self.mainCanvas = Canvas(self.root, width = self.s_width, height = self.s_height)
		self.mainCanvas.pack()
		self.mainCanvas.create_rectangle(0,0,self.s_width,self.s_height, fill = "white", outline = "white")
		self.mainCanvas.create_rectangle(0,0,400,self.s_height, fill = "#7633af", outline = "#7633af")
		self.mainCanvas.create_oval(100,100,250,250, fill = "#f2f4f4", outline = "#f2f4f4",tags="draggable")


		# TEXT
		self.mainCanvas.create_text(80,300,fill="white", font="Roboto 15",
						tags="draggable", anchor = NW,
                        text="Firstname Lastname")
		self.mainCanvas.create_text(80,325,fill="white", font="Roboto 12",
						tags="draggable", anchor = NW,
                        text="This is my description of myself")

		self.mainCanvas.create_text(80,475,fill="white", font="Roboto 14",
						tags="draggable", anchor = NW,
                        text="Home")
		self.mainCanvas.create_text(80,520,fill="white", font="Roboto 14",
						tags="draggable", anchor = NW,
                        text="Posts")
		self.mainCanvas.create_text(80,565,fill="white", font="Roboto 14",
						tags="draggable", anchor = NW,
                        text="Portfolio")

		self.mainCanvas.create_text(600,100,fill="#5f6466", font="Roboto 14",
						tags="draggable", anchor = NW,
                        text="About Me")
		self.mainCanvas.create_text(600,140,fill="#656b6d", font="Roboto 12",
						tags="draggable", anchor = NW,
                        text="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse maximus, magna ut feugiat iaculis, 
dui nisi cursus neque, ut rutrum mi risus tincidunt erat. Curabitur tristique augue ut porttitor vestibulum.
Nulla sit amet posuere dolor. Sed ut ornare ex. Pellentesque condimentum iaculis enim, ut luctus risus 
aliquet quis.""")

		self.mainCanvas.create_line(600, 250, 1350, 250, fill="#bababa", tags="draggable")

		self.mainCanvas.create_text(600,300,fill="#5f6466", font="Roboto 14",
						tags="draggable", anchor = NW,
                        text="Posts")
		self.mainCanvas.create_text(600,340,fill="#656b6d", font="Roboto 12",
						tags="draggable", anchor = NW,
                        text="""1. Post 1\n2. Post 2\n3. Another Post
                        """)

		self.mainCanvas.create_line(600, 450, 1350, 450, fill="#bababa", tags="draggable")

		self.mainCanvas.create_text(600,500,fill="#5f6466", font="Roboto 14",
						tags="draggable", anchor = NW,
                        text="Portfolio")
		self.mainCanvas.create_rectangle(900,710,600,550, fill = "#7633af", outline = "#7633af", tags="draggable")
		self.mainCanvas.create_rectangle(1350,710,1050,550, fill = "#7633af", outline = "#7633af", tags="draggable")


		self.mainCanvas.tag_bind ("draggable", "<Button1-Motion>", self.move)
		self.mainCanvas.tag_bind ("draggable", "<ButtonRelease-1>", self.release)


#main = TemplateOne()
startApp = SelectTemplate()
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
from PIL import Image
import tkSimpleDialog
from tkcolorpicker import askcolor



class SelectTemplate():
	# Template Selection
	def __init__(self):
		self.root = Tk()
		self.root.geometry("420x220")
		self.root.title("Choose a Template")
		self.root.attributes("-topmost", True)

		self.createWidgets()
		self.root.lift()

		self.root.mainloop()

	def getTemplateNew(self):
		self.root.destroy()
	#open a new template 2
	def openTemplate1(self):
		self.root.destroy()
		temp1 = TemplateOne()
	#Open a new template 2
	def openTemplate2(self):
		self.root.destroy()
		temp2 = TemplateTwo()

	def createWidgets(self):
		# Create the columns and rows
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
		self.lbl_chooseTemplate.grid(row = 0, column = 0, padx = 40, pady = 30)

		self.template1 = Button(self.root, text = "Template 1", width = 16, height = 4, command=self.openTemplate1)
		self.template1.grid(row = 1, column = 0, padx = 40, pady = 30)
		self.template2 = Button(self.root, text = "Template 2", width = 16, height = 4, command=self.openTemplate2)
		self.template2.grid(row = 1, column = 1, padx = 40, pady = 30)

# Empty Class for children to inherit
class Template(object):
	def __init__(self, title):
		self.root = Tk()
		self.s_width = str(self.root.winfo_screenwidth())
		self.s_height = str(self.root.winfo_screenheight())
		self.root.geometry(self.s_width + "x" + self.s_height)
		self.root.title(title)
		self.websiteTitle = title
		self.isDragged = 0
		self.entities = []
		self.sidebarEntities = []
		self.mainEntities = []
		self.createBasics()
		self.createWidgets()
		self.selectedWidget = None
		self.root.mainloop()

	# Sets the dragging funcationality
	def move(self, event):
		if self.isDragged:
			new_xPos, new_yPos = event.x, event.y
			self.mainCanvas.move(event.widget.find_withtag(CURRENT), new_xPos-self.mouse_xPos, new_yPos-self.mouse_yPos)
			#print new_xPos, new_yPos

		else:
			self.isDragged = True
        	self.mainCanvas.tag_raise("draggable")
        	self.mouse_xPos = event.x
        	self.mouse_yPos = event.y
    # Release functionality (after dragged)
	def release(self, event):
		self.isDragged = False
	# When text is right clicked, show option to enter text
	def textRightClick(self, widget):
		answer = tkSimpleDialog.askstring("Input", "Enter text", parent=self.root)
		self.mainCanvas.itemconfigure(widget, text = answer)
	#When an image is right clicked, show insert image option
	def imageRightClick(self, widget):
		return None
	# When a color object is right clicked, show option for changing color
	def colorRightClick(self, widget):
		color = self.mainCanvas.itemcget(widget, "fill")
		newColor = askcolor(color, self.root)
		self.mainCanvas.itemconfigure(widget, fill = newColor[1])
	#Delete an object
	def deleteObject(self, widget):
		self.mainCanvas.delete(widget)
		try:
			self.entities.remove(widget[0])
		except ValueError:
			return -1
		
	# When anything that is selectable is right clicked, show a menu
	def selectableRightClicked(self, event):
		self.currentWidget = event.widget.find_withtag(CURRENT)
		tagsOfWidget = self.mainCanvas.itemcget(event.widget.find_withtag(CURRENT), "tags")
		print tagsOfWidget
		self.rightclickMenu = Menu(self.root, tearoff=0)
		self.addnewMenu = Menu(self.rightclickMenu, tearoff=0)

		self.rightclickMenu.add_command(label="Copy")
		self.rightclickMenu.add_command(label="Cut")
		self.rightclickMenu.add_command(label="Delete", command = lambda obj = self.currentWidget: self.deleteObject(obj))

		self.addnewMenu.add_command(label="Rectangle")
		self.addnewMenu.add_command(label="Text")

		if "text" in tagsOfWidget:
			self.rightclickMenu.add_command(label="Edit Text", command = lambda cw=self.currentWidget: self.textRightClick(cw))
		if "color" in tagsOfWidget:
			self.rightclickMenu.add_command(label="Change Color", command = lambda cw=self.currentWidget: self.colorRightClick(cw))
		# if "image" in tagsOfWidget:
		# 	self.rightclickMenu.add_command(label="Change Image", command = lambda cw=self.currentWidget: self.imageRightClick(cw))
		# if "innate" in tagsOfWidget:
		# 	self.rightclickMenu.add_cascade(label="Add New...", menu = self.addnewMenu)

		try:
			self.rightclickMenu.tk_popup(event.x_root, event.y_root,0)
		finally:
			self.rightclickMenu.grab_release()

	def createBasics(self):


		self.menuBar = Menu(self.root)
		self.fileBar = Menu(self.menuBar, tearoff=0)
		self.editBar = Menu(self.menuBar, tearoff=0)

		self.menuBar.add_cascade(label="File", menu=self.fileBar)
		self.menuBar.add_cascade(label="Edit", menu=self.editBar)

		self.fileBar.add_command(label="Export to HTML", command = lambda template = self : exportToHTML(template))
		self.editBar.add_command(label="Edit Website Name", command = self.changeWebsiteName)

		self.root.config(menu=self.menuBar)

		self.mainCanvas = Canvas(self.root, width = self.s_width, height = self.s_height)
		self.mainCanvas.pack()
	#Change the website name
	def changeWebsiteName(self):
		newTitle = tkSimpleDialog.askstring("Title", "Enter new title", parent=self.root)
		self.root.title(newTitle)
		self.websiteTitle = newTitle

	def createWidgets(self):
		return None

# Define a new template
class TemplateOne(Template):
	def __init__(self):
		super(TemplateOne, self).__init__("Template One")

	def createWidgets(self):
		# Create the main canvas areas
		self.rectangle_main = self.mainCanvas.create_rectangle(0,0,self.s_width,self.s_height, tags=("color", "selectable", "innate", "rectangle"), fill = "white", outline = "")
		self.rectangle_sidebar = self.mainCanvas.create_rectangle(0,0,400,self.s_height, tags=("color", "selectable", "innate", "rectangle"), fill = "#7633af", outline = "")

		#self.oval_avatar = self.mainCanvas.create_oval(100,100,250,250, fill = "#f2f4f4", outline = "", tags=("oval", "draggable", "image", "selectable"))
		
		# CREATE ALL THE ITEMS
		self.textName = self.mainCanvas.create_text(80,100,fill="white", font="Roboto 15",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Firstname Lastname")
		self.textDesc = self.mainCanvas.create_text(80,125,fill="white", font="Roboto 12",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="This is my description of myself")

		self.textHome = self.mainCanvas.create_text(80,475,fill="white", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Home")
		self.textPosts = self.mainCanvas.create_text(80,520,fill="white", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Posts")
		self.textPortfolio = self.mainCanvas.create_text(80,565,fill="white", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Portfolio")

		self.textAbout = self.mainCanvas.create_text(600,60,fill="#5f6466", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="About Me")
		self.textAboutDesc = self.mainCanvas.create_text(600,100,fill="#656b6d", font="Roboto 12",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse maximus, magna ut feugiat iaculis,\n 
dui nisi cursus neque, ut rutrum mi risus tincidunt erat. Curabitur tristique augue ut porttitor vestibulum.\n
Nulla sit amet posuere dolor. Sed ut ornare ex. Pellentesque condimentum iaculis enim, ut luctus risus\n
aliquet quis.""")

		#self.dividerLine1 = self.mainCanvas.create_line(600, 250, 1350, 250, fill="#bababa", tags=("draggable"))

		self.textPostsMain = self.mainCanvas.create_text(600,300,fill="#5f6466", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Posts")
		self.textPostList = self.mainCanvas.create_text(600,340,fill="#656b6d", font="Roboto 12",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="""1. Post 1\n2. Post 2\n3. Another Post\n
                        """)

		#self.dividerLine2 = self.mainCanvas.create_line(600, 450, 1350, 450, fill="#bababa", tags=("draggable"))

		self.textPortfolioMain = self.mainCanvas.create_text(600,500,fill="#5f6466", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Portfolio")
		self.rectangle_portfolio1 = self.mainCanvas.create_rectangle(900,710,600,550, fill = "#7633af", outline = "", tags = ("draggable", "image", "selectable", "rectangle"))
		self.rectangle_portfolio2 = self.mainCanvas.create_rectangle(1350,710,1050,550, fill = "#7633af", outline = "", tags = ("draggable", "image", "selectable", "rectangle"))



		self.entities.extend([self.rectangle_portfolio1, self.rectangle_portfolio2,# self.dividerLine1, #self.oval_avatar, self.dividerLine2,
			self.textAbout, self.textPortfolio, self.textPosts, self.textHome, self.textDesc, self.textName, self.textPortfolioMain,
			self.textAboutDesc, self.textPostsMain, self.textPostList])
		self.mainCanvas.tag_bind("selectable", "<Button-3>", super(TemplateOne, self).selectableRightClicked)
		self.mainCanvas.tag_bind("draggable", "<Button1-Motion>", super(TemplateOne, self).move)
		self.mainCanvas.tag_bind("draggable", "<ButtonRelease-1>", super(TemplateOne, self).release)
	#Delete an object -- OVERRIDES PARENT
	def deleteObject(self, widget):
		print self.entities, widget
		self.mainCanvas.delete(widget)
		try:
			self.entities.remove(widget[0])
		except ValueError:
			print "Value Error"
			return -1


# Define a new template
class TemplateTwo(Template):
	def __init__(self):
		super(TemplateTwo, self).__init__("Template Two")

	def createWidgets(self):
		# Create main canvas areas
		self.rectangle_main = self.mainCanvas.create_rectangle(0,0,self.s_width,self.s_height, tags=("color", "selectable", "innate", "rectangle"), fill = "white", outline = "")
		self.rectangle_sidebar = self.mainCanvas.create_rectangle(0,0,self.s_width, 200, tags=("color", "selectable", "innate", "rectangle"), fill = "#C41E3A", outline = "")

		# Create all objects		
		self.textName = self.mainCanvas.create_text(100,100,fill="white", font="Roboto 15",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Firstname Lastname")
		self.textDesc = self.mainCanvas.create_text(100,125,fill="white", font="Roboto 12",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="This is my description of myself")

		self.textHome = self.mainCanvas.create_text(1050,100,fill="white", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Home")
		self.textPosts = self.mainCanvas.create_text(1150,100,fill="white", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Posts")
		self.textPortfolio = self.mainCanvas.create_text(1250,100,fill="white", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Portfolio")

		self.textAbout = self.mainCanvas.create_text(100,300,fill="#5f6466", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="About Me")
		self.textAboutDesc = self.mainCanvas.create_text(100,340,fill="#656b6d", font="Roboto 12",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="""Lorem ipsum dolor sit amet, consectetur adipiscing elit.\nSuspendisse maximus, magna ut feugiat iaculis, dui nisi\n 
cursus neque, ut rutrum mi risus tincidunt erat. Curabitur\ntristique augue ut porttitor vestibulum.Nulla sit amet\n 
posuere dolor. Sed ut ornare ex. Pellentesque condimentum\niaculis enim, ut luctus risus aliquet quis.""")

		#self.dividerLine1 = self.mainCanvas.create_line(600, 250, 1350, 250, fill="#bababa", tags=("draggable"))

		self.textPostsMain = self.mainCanvas.create_text(600,300,fill="#5f6466", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Posts")
		self.textPostList = self.mainCanvas.create_text(600,340,fill="#656b6d", font="Roboto 12",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="""1. Post 1\n2. Post 2\n3. Another Post\n
                        """)

		#self.dividerLine2 = self.mainCanvas.create_line(600, 450, 1350, 450, fill="#bababa", tags=("draggable"))

		self.textPortfolioMain = self.mainCanvas.create_text(600,500,fill="#5f6466", font="Roboto 14",
						tags=("draggable", "text", "selectable", "color"), anchor = NW,
                        text="Portfolio")
		self.rectangle_portfolio1 = self.mainCanvas.create_rectangle(900,710,600,550, fill = "#C41E3A", outline = "", tags = ("draggable", "image", "selectable", "rectangle"))
		self.rectangle_portfolio2 = self.mainCanvas.create_rectangle(1350,710,1050,550, fill = "#C41E3A", outline = "", tags = ("draggable", "image", "selectable", "rectangle"))



		self.entities.extend([self.rectangle_portfolio1, self.rectangle_portfolio2,# self.dividerLine1, #self.oval_avatar, self.dividerLine2,
			self.textAbout, self.textPortfolio, self.textPosts, self.textHome, self.textDesc, self.textName, self.textPortfolioMain,
			self.textAboutDesc, self.textPostsMain, self.textPostList])
		self.mainCanvas.tag_bind("selectable", "<Button-3>", super(TemplateTwo, self).selectableRightClicked)
		self.mainCanvas.tag_bind("draggable", "<Button1-Motion>", super(TemplateTwo, self).move)
		self.mainCanvas.tag_bind("draggable", "<ButtonRelease-1>", super(TemplateTwo, self).release)
	#Delete an object OVERRIDES PARENT
	def deleteObject(self, widget):
		print self.entities, widget
		self.mainCanvas.delete(widget)
		try:
			self.entities.remove(widget[0])
		except ValueError:
			print "Value Error"
			return -1

# Export given template to HTML
def exportToHTML(template):
	outputFile = open("index.html", "w")
	outputFile.write("<html>\n<head>\n<title>" + template.websiteTitle + "</title>\n</head>\n"+ "<body>\n")
	# See if the object is in the sidebar
	for i in range(len(template.entities)):
		coordinates = template.mainCanvas.coords(template.entities[i])
		sidebarCoordinates = template.mainCanvas.coords(template.rectangle_sidebar)
		if coordinates[-2] <= sidebarCoordinates[-2] and coordinates[-1] <= sidebarCoordinates[-1]:
			template.sidebarEntities.append(template.entities[i])
	# Get the color of each object
	colorMain = template.mainCanvas.itemcget(template.rectangle_main, "fill")
	mainCoords = template.mainCanvas.coords(template.rectangle_main)
	outputFile.write("<div style=\" background-color:"+ colorMain +"; width:" +str(mainCoords[2])+ "px; height:"+str(mainCoords[3])+"px; \">\n")

	#Remove sidebar entities from all entities
	for j in range(len(template.sidebarEntities)):
		try:
			template.entities.remove(template.sidebarEntities[j])
		except ValueError:
			return -1
		

	# Get the color of the sidebar and put it in a div
	color = template.mainCanvas.itemcget(template.rectangle_sidebar, "fill")
	outputFile.write("<div style=\" background-color:"+ color +"; width:" +str(sidebarCoordinates[2])+ "px; height:"+str(sidebarCoordinates[3])+"px; \">\n")
	#Get all attr of all sidebar entities and put them in their respective html tags and write it to the file
	for k in range(len(template.sidebarEntities)):
		widgetTags = template.mainCanvas.itemcget(template.sidebarEntities[k], "tags")
		print template.mainCanvas.itemcget(template.sidebarEntities[k], "text")

		if "text" in widgetTags:
			font = template.mainCanvas.itemcget(template.sidebarEntities[k], "font")
			newCoords = template.mainCanvas.coords(template.sidebarEntities[k])
			color = template.mainCanvas.itemcget(template.sidebarEntities[k], "fill")
			if color == "white":
				color = "#ffffff"
			text = template.mainCanvas.itemcget(template.sidebarEntities[k], "text")
			text = text.replace("\n","<br>")
			outputFile.write("<p style=\"" + "position: absolute; left: " + str(newCoords[0]) + "px; top: "+str(newCoords[1])+"px; font-family:" 
				+ font.split(" ")[0] + "; font-size:"
				+ str(int(font.split(" ")[1])+4) + "px; color:" + color + ";\">"+text+"</p>\n")
	outputFile.write("</div>\n")

	#Get all attr of all other entities and put them in their respective html tags and write it to the file
	for l in range(len(template.entities)):
		widgetTags = template.mainCanvas.itemcget(template.entities[l], "tags")
		if "text" in widgetTags:
			font = template.mainCanvas.itemcget(template.entities[l], "font")
			newCoords = template.mainCanvas.coords(template.entities[l])
			color = template.mainCanvas.itemcget(template.entities[l], "fill")
			if color == "white":
				color = "#ffffff"
			text = template.mainCanvas.itemcget(template.entities[l], "text")
			text = text.replace("\n","<br>")


			outputFile.write("<p style=\"" + "position: absolute; left: " + str(newCoords[0]) + "px; top: "+str(newCoords[1])+"px; font-family:" 
				+ font.split(" ")[0] + "; font-size:"
				+ str(int(font.split(" ")[1])+4) + "px; color:" + color + ";\">"+text+"</p>\n")
		if "rectangle" in widgetTags:
			color = template.mainCanvas.itemcget(template.entities[l], "fill")
			coordinates = template.mainCanvas.coords(template.entities[l])
			height = str(coordinates[3]-coordinates[1])
			width = str(coordinates[2]-coordinates[0])
			print coordinates
			outputFile.write("<svg width=\""+width+"\" height=\"" +height+"\" style=\"position: absolute; left: "
				+ str(int(coordinates[2])-300) + "px; top: "+str(int(coordinates[3])-100)+"px;\">"+
				"<rect width=\""+width+"\" height=\""+height+"\" style=\"fill:"+color+";\"/></svg>\n")
		print widgetTags
		
	outputFile.write("</div></body></html>")



startApp = SelectTemplate()

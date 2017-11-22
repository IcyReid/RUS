# import Kivy
import kivy
import random
import sys
import subprocess
import rus_parser as parser
import rus_forward as forward
import itertools
import graph1
import os
import matplotlib.pyplot as plt
import numpy as np
import re
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as rgb
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from kivy.core.window import Window


from matplotlib.pyplot import figure, show
from matplotlib.ticker import MaxNLocator

class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)
TextInput = FloatInput
shapeSpinner = Spinner(
    # default value shown
            text='Choose the Shape',
    # available values
            values=('Rectangle', 'Ellipsoidal Cylinder', 'Spheroid'),
    # just for positioning in our example
            width=150
            )
			
scSpinner = Spinner(
            text='Choose the number',
            values=('2', '3','5','6','9'),
			width=150
            )

hexSpinner = Spinner(
            text='Choose the type',
            values=('VTI', 'HTI'),
            width=150
            )
			
layout = GridLayout(cols=3,rows=15)
continueButton = Button(text='Continue')
sp = Button(text='Continue')
snLabel = Label(text='Enter the value of stiffness coefficient :', size_hint_x=None, width=400,)
hexLabel = Label(text='Hex Type :', size_hint_x=None, width=400,)
emptyCol= Label(text='', size_hint_x=None, width=150)
emptyCol2 = Label(text='', size_hint_x=None, width=150)
emptyCol3 = Label(text='', size_hint_x=None, width=150)
emptyCol4 = Label(text='', size_hint_x=None, width=150)
emptyCol5 = Label(text='', size_hint_x=None, width=150)
emptyCol6 = Label(text='', size_hint_x=None, width=150)
emptyCol7 = Label(text='', size_hint_x=None, width=150)
emptyC12 = Label(text='X', size_hint_x=None, width=150)
emptyC13 = Label(text='X', size_hint_x=None, width=150)
emptyC11 = Label(text='X', size_hint_x=None, width=150)
emptyC66 = Label(text='X', size_hint_x=None, width=150)
emptyC22 = Label(text='X', size_hint_x=None, width=150)
emptyC23 = Label(text='X', size_hint_x=None, width=150)
emptyC33 = Label(text='X', size_hint_x=None, width=150)
emptyC55 = Label(text='X', size_hint_x=None, width=150)
c11 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c11')
c12 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c12')
c13 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c13')
c22 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c22')
c23 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c23')
c33 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c33')
c44 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c44')
c55 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c55')
c66 = TextInput(text='', multiline=False, size_hint_x=None,width=150, hint_text ='c66')
shape = '4'
sc = '0'
hextype = '0'
outputArray = []


class RUS(App):
# layout
    def build(self):
	self.title = "Forward Algorithm"
        sp.bind(on_press=self.spClicked)
        layout.add_widget(Label(text='Number of eigen frequencies to print :', size_hint_x=None, width=400))
        self.freq = TextInput(text='10', multiline=False,size_hint_x=None, width=150)
        layout.add_widget(self.freq)
        layout.add_widget(Label(text='', size_hint_x=None, width=150))

        layout.add_widget(Label(text='Order of the polynomial to use to estimate eigenvectors :', size_hint_x=None, width=400))
        self.vectors = TextInput(text='6', multiline=False,size_hint_x=None, width=150)
        layout.add_widget(self.vectors)
        layout.add_widget(Label(text='', size_hint_x=None, width=150))

        layout.add_widget(Label(text='Shape', size_hint_x=None, width=400))
        layout.add_widget(shapeSpinner)
        layout.add_widget(Label(text='', size_hint_x=None, width=150))

        layout.add_widget(Label(text='Dimension 1  :', size_hint_x=None, width=400,))
        self.dimension1 = TextInput(text='3.67', multiline=False,size_hint_x=None, width=150)
        layout.add_widget(self.dimension1)
        layout.add_widget(Label(text='cm', size_hint_x=None, width=150))
        
        layout.add_widget(Label(text='Dimension 2 :', size_hint_x=None, width=400))
        self.dimension2 = TextInput(text='3.67', multiline=False,size_hint_x=None, width=150)
        layout.add_widget(self.dimension2)
        layout.add_widget(Label(text='cm', size_hint_x=None, width=150))

        layout.add_widget(Label(text='Dimension 3 :', size_hint_x=None, width=400))
        self.dimension3 = TextInput(text='3.67', multiline=False,size_hint_x=None, width=150)
        layout.add_widget(self.dimension3)
        layout.add_widget(Label(text='cm', size_hint_x=None, width=150))

        layout.add_widget(Label(text='Density :', size_hint_x=None, width=400))
        self.density = TextInput(text='1.7', multiline=False,size_hint_x=None, width=150)
        layout.add_widget(self.density)
        layout.add_widget(Label(text='grams/cm^3', size_hint_x=None, width=150))
		
        layout.add_widget(Label(text='Number of stiffness coefficient :', size_hint_x=None, width=400))
        layout.add_widget(scSpinner)
        layout.add_widget(Label(text='', size_hint_x=None, width=150))
		
        layout.add_widget(snLabel)
        layout.add_widget(c11)
        layout.add_widget(c12)
        layout.add_widget(emptyCol)
        layout.add_widget(c13)
        layout.add_widget(c22)
        layout.add_widget(emptyCol2) 
        layout.add_widget(c23)
        layout.add_widget(c33)
        layout.add_widget(emptyCol3) 
        layout.add_widget(c44)
        layout.add_widget(c55)
        layout.add_widget(emptyCol4) 
        layout.add_widget(c66) 
        layout.add_widget(emptyCol5)
        layout.add_widget(sp)
        
       
        return layout
		
		
    @staticmethod	
    def remove_col():
        layout.remove_widget(c11)
        layout.remove_widget(c12)
        layout.remove_widget(c13)
        layout.remove_widget(c22)
        layout.remove_widget(c23)
        layout.remove_widget(c33)
        layout.remove_widget(c44)
        layout.remove_widget(c55)
        layout.remove_widget(c66)
        layout.remove_widget(snLabel)
        layout.remove_widget(continueButton)
        layout.remove_widget(sp)
        layout.remove_widget(hexLabel)
        layout.remove_widget(hexSpinner)
        layout.remove_widget(emptyCol)
        layout.remove_widget(emptyCol2)
        layout.remove_widget(emptyCol3)
        layout.remove_widget(emptyCol4)
        layout.remove_widget(emptyCol5)
        layout.remove_widget(emptyCol6)
        layout.remove_widget(emptyCol7)
        layout.remove_widget(emptyC12)
        layout.remove_widget(emptyC13)
        layout.remove_widget(emptyC22)
        layout.remove_widget(emptyC23)
        layout.remove_widget(emptyC33)
        layout.remove_widget(emptyC11)
        layout.remove_widget(emptyC55)
        layout.remove_widget(emptyC66)
		
    
    def show_selected_value(shapeSpinner, text):
        
        global shape
        global sc
        global hextype
        if text == 'Rectangle':
            shape = '0'
        if text == 'Ellipsoidal Cylinder':
            shape = '1'
        if text == 'Spheroid':
            shape = '2'
            
        if text == '2':
            sc = '2'
        if text == '3':
            sc = '3'
        if text == '5':
            sc = '5'
        if text == '6':
            sc = '6'
        if text == '9':
            sc = '9'
			
        if text == 'VTI':
            hextype = '1'
        if text == 'HTI':
            hextype = '2'
       
        if text == '5' and shape == '2':
            RUS.remove_col()
            layout.add_widget(hexLabel)
            layout.add_widget(hexSpinner)
            layout.add_widget(emptyCol)
            layout.add_widget(snLabel)
            layout.add_widget(emptyC11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol6)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(c23)
            layout.add_widget(c33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(c66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '2' and shape == '2':
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(emptyC12)
            layout.add_widget(emptyCol)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(emptyC23)
            layout.add_widget(emptyC33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(emptyC66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '3' and shape == '2':	
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(emptyC23)
            layout.add_widget(emptyC33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(emptyC66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '6' and shape == '2':
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(c23)
            layout.add_widget(c33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(c66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '9' and shape == '2':
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol)
            layout.add_widget(c13)
            layout.add_widget(c22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(c23)
            layout.add_widget(c33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(c55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(c66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '5':
            RUS.remove_col()
            layout.add_widget(hexLabel)
            layout.add_widget(hexSpinner)
            layout.add_widget(emptyCol)
            layout.add_widget(snLabel)
            layout.add_widget(emptyC11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol6)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(c23)
            layout.add_widget(c33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(c66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '2':
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(emptyC12)
            layout.add_widget(emptyCol)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(emptyC23)
            layout.add_widget(emptyC33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(emptyC66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '3':	
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(emptyC23)
            layout.add_widget(emptyC33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(emptyC66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '6':
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol)
            layout.add_widget(emptyC13)
            layout.add_widget(emptyC22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(c23)
            layout.add_widget(c33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(emptyC55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(c66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
        elif text == '9':
            RUS.remove_col()
            layout.add_widget(snLabel)
            layout.add_widget(c11)
            layout.add_widget(c12)
            layout.add_widget(emptyCol)
            layout.add_widget(c13)
            layout.add_widget(c22)
            layout.add_widget(emptyCol2) 
            layout.add_widget(c23)
            layout.add_widget(c33)
            layout.add_widget(emptyCol3) 
            layout.add_widget(c44)
            layout.add_widget(c55)
            layout.add_widget(emptyCol4) 
            layout.add_widget(c66) 
            layout.add_widget(emptyCol5)
            layout.add_widget(sp)
       
    shapeSpinner.bind(text=show_selected_value)
    scSpinner.bind(text=show_selected_value)
    hexSpinner.bind(text=show_selected_value)
	
    @staticmethod
    def graphOutput():
        global outputArray
        output = open("output.txt", "r")
        lines = output.readlines()
        
        for i in range(0, len(lines)):
            line = lines[i]    
                
        for i in range(0,len(lines) - 8):
            outputArray.append(lines[i+8][:12])
                   
        for i in range(0,len(lines) - 8):
            outputArray[i] = (outputArray[i])
        
        differentcount = 1
        similarcount = 1	
        freq = []		
        yaxis = []		
        for i in range(0,len(lines) - 9):
            if outputArray[i] == outputArray[i+1]:
                similarcount += 1
                
            elif outputArray[i] != outputArray[i+1]:
                differentcount += 1
                yaxis.append(similarcount)
                freq.append(outputArray[i]) 
                
                similarcount = 1
        yaxis.append(similarcount)
        freq.append(outputArray[len(outputArray) - 1]) 
        
           				
        outputArray = map(float, outputArray)
       
        
        colors = itertools.cycle([
            rgb('000000'), rgb('000000'), rgb('000000'), rgb('000000')])
        graph_theme = {
            'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
            'background_color': rgb('f8f8f2'),  # back ground color of canvas
            'tick_color': rgb('808080'),  # ticks and grid
            'border_color': rgb('808080')}  # border drawn around each graph

        graph = graph1.Graph(	
            xlabel='Frequency (Hz)',
            ylabel='No.Count',
            x_ticks_major=1000,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=False,
            y_grid=True,
            xmin=(int(float(freq[0])))- 1000,
            xmax=(int(float(freq[(len(freq)) - 1]))) + 1000,
            ymin=0,
            ymax=max(yaxis) + 1,
            **graph_theme)
				
        count = 0
        y = 0
            
        while(count < len(yaxis)+1):
            if(count == 0):
                plot = graph1.SmoothLinePlot(color=next(colors))
                plot.points = [(count, x) for x in range(0, 0)]
         # for efficiency, the x range matches xmin, xmax 
                graph.add_plot(plot)
                count = count + 1
            else:				
                plot = graph1.SmoothLinePlot(color=next(colors))
                plot.points = [(int(float(freq[y])), x) for x in range(0, int(yaxis[y])+1)]
         # for efficiency, the x range matches xmin, xmax 
                graph.add_plot(plot)
                count = count + 1
                y = y + 1
        '''layout.add_widget(graph)'''
	
	'''fig, ay = plt.subplots()'''
	'''ax.scatter(freq ,yaxis)'''
	
	yaxis = map(int, yaxis)

	ay = figure().gca()
	
	'''ay.scatter(freq ,yaxis)'''
	ay.yaxis.set_major_locator(MaxNLocator(integer=True))
	
	
	for i in range(0,len(freq)):
		plt.plot([freq[i],freq[i]], [0,yaxis[i]],label = str(freq[i]))
	for i in range(0,len(freq)):	
		ay.annotate(freq[i],(freq[i],yaxis[i]))
		
	
	
	plt.xlabel('Frequency(Hz)')
	plt.ylabel('No. of count')
	plt.title('Forward Algorithm')
	plt.ylim([0,max(yaxis)+1])
	plt.xlim([(int(float(freq[0])))*0.8,(int(float(freq[(len(freq)) - 1])))*1.2])
	plt.grid()
	plt.legend(bbox_to_anchor=(1.05,1),loc=1,borderaxespad=0.)
	plt.show()
	
	
	

	
			

	
# button click function      
    def spClicked(self,btn): 
	if self.freq.text == '' or self.vectors.text == '' or self.dimension1.text == '' or self.dimension2.text == '' or self.dimension3.text == '' or self.density.text == '' or shape == '4':
		return
        if sc == '2':
	    if c11.text == '' or c44.text == '':
		return
	             
            command = 'python rus.py forward --nfreq ' + self.freq.text	+ ' --order ' + self.vectors.text + ' --shape ' + shape + ' --d1 ' + self.dimension1.text + ' --d2 ' + self.dimension2.text + ' --d3 ' + self.dimension3.text + ' --rho ' + self.density.text + ' --ns ' + sc + ' --c11 ' + c11.text +  ' --c44 ' + c44.text
			
        elif sc == '3':
            if c11.text == '' or c12.text == '':
		return
            command = 'python rus.py forward --nfreq ' + self.freq.text	+ ' --order ' + self.vectors.text + ' --shape ' + shape + ' --d1 ' + self.dimension1.text + ' --d2 ' + self.dimension2.text + ' --d3 ' + self.dimension3.text + ' --rho ' + self.density.text + ' --ns ' + sc + ' --c11 ' + c11.text +  ' --c12 ' + c12.text + ' --c44 ' + c44.text

        elif sc == '5' and hextype == '1':
	    if c33.text == '' or c23.text == '' or c12.text == '' or c44.text == '' or c66.text == '':
		return
            command = 'python rus.py forward --nfreq ' + self.freq.text	+ ' --order ' + self.vectors.text + ' --shape ' + shape + ' --d1 ' + self.dimension1.text + ' --d2 ' + self.dimension2.text + ' --d3 ' + self.dimension3.text + ' --rho ' + self.density.text + ' --ns ' + sc + ' --c33 ' + c33.text +  ' --c23 ' + c23.text + ' --c12 ' + c12.text + ' --c44 ' + c44.text + ' --c66 ' + c66.text + ' --hextype ' + hextype

        elif sc == '5' and hextype == '2':
	    if c11.text == '' or c33.text == '' or c12.text == '' or c44.text == '' or c66.text == '':
		return
            command = 'python rus.py forward --nfreq ' + self.freq.text	+ ' --order ' + self.vectors.text + ' --shape ' + shape + ' --d1 ' + self.dimension1.text + ' --d2 ' + self.dimension2.text + ' --d3 ' + self.dimension3.text + ' --rho ' + self.density.text + ' --ns ' + sc + ' --c11 ' + c11.text +  ' --c33 ' + c33.text + ' --c12 ' + c12.text + ' --c44 ' + c44.text + ' --c66 ' + c66.text + ' --hextype ' + hextype

        elif sc == '6':
	    if c11.text == '' or c33.text == '' or c22.text == '' or c12.text == '' or c44.text == '' or c66.text == '':
		return
            command = 'python rus.py forward --nfreq ' + self.freq.text	+ ' --order ' + self.vectors.text + ' --shape ' + shape + ' --d1 ' + self.dimension1.text + ' --d2 ' + self.dimension2.text + ' --d3 ' + self.dimension3.text + ' --rho ' + self.density.text + ' --ns ' + sc + ' --c11 ' + c11.text +  ' --c33 ' + c33.text + ' --c23 ' + c23.text + ' --c12 ' + c12.text +  ' --c44 ' + c44.text + ' --c66 ' + c66.text

        elif sc == '9':
            if c11.text == '' or c22.text == '' or c33.text == '' or c23.text == '' or c13.text == '' or c12.text == '' or c44.text == '' or c55.text == '' or c66.text == '':
		return
            command = 'python rus.py forward --nfreq ' + self.freq.text	+ ' --order ' + self.vectors.text + ' --shape ' + shape + ' --d1 ' + self.dimension1.text + ' --d2 ' + self.dimension2.text + ' --d3 ' + self.dimension3.text + ' --rho ' + self.density.text + ' --ns ' + sc + ' --c11 ' + c11.text +  ' --c22 ' + c22.text + ' --c33 ' + c33.text + ' --c23 ' + c23.text +  ' --c13 ' + c13.text + ' --c12 ' + c12.text + ' --c44 ' + c44.text +  ' --c55 ' + c55.text + ' --c66 ' + c66.text
       
        print (command)
        layout.clear_widgets()
        f = open("output.txt", "w")
        subprocess.call(command, shell=True , stdout=f)
        output = open("output.txt", "r") 
	labelText = output.read()
	labelTextArray = labelText.split("\n")
	newList = []
	for line in labelTextArray:
		if "irk" not in line:
			newList.append(line)			
	labelText = "\n".join(newList)
	
	inputValues = ""
	inputValues += "Shape: " + shapeSpinner.values[int(shape)] + "\n"
	inputValues += "Density: " + self.density.text + "\n"
	inputValues += "Dimention1: " + self.dimension1.text + "\n"
	inputValues += "Dimention2: " + self.dimension2.text + "\n"
	inputValues += "Dimention3: " + self.dimension3.text + "\n"
	if sc == '2':	             
            inputValues +=' c11:' + c11.text + "\n" + ' c44:' + c44.text + "\n"			
        elif sc == '3':
            inputValues +=' c11:' + c11.text + "\n" +  ' c12:' + c12.text + "\n" + ' c44:' + c44.text + "\n"
        elif sc == '5' and hextype == '1':
            inputValues +=' c33:' + c33.text + "\n" +  ' c23:' + c23.text + "\n" + ' c12:' + c12.text + "\n" + ' c44:' + c44.text + "\n" + ' c66:' + c66.text + "\n" + ' hextype:' + hextype + "\n"
        elif sc == '5' and hextype == '2':
            inputValues +=' c11:' + c33.text + "\n" +  ' c33:' + c23.text + "\n" + ' c12:' + c12.text + "\n" + ' c44:' + c44.text + "\n" + ' c66:' + c66.text + "\n" + ' hextype:' + hextype + "\n"
        elif sc == '6':
            inputValues +=' c11:' + c11.text + "\n" +  ' c33:' + c33.text + "\n" + ' c23:' + c23.text + "\n" + ' c12:' + c12.text + "\n" +  ' c44:' + c44.text + "\n" + ' c66:' + c66.text + "\n"
        elif sc == '9':
            inputValues +=' c11:' + c11.text + "\n" +  ' c22:' + c22.text + "\n"+ ' c33:' + c33.text + "\n" + ' c23:' + c23.text + "\n" +  ' c13:' + c13.text + "\n" + ' c12:' + c12.text + "\n" + ' c44:' + c44.text + "\n" +  ' c55:' + c55.text + "\n" + ' c66:' + c66.text + "\n"
	

	labelText = inputValues + labelText

        label = Label(text = labelText, size_hint_x=None, width=200)
        layout.add_widget(label)
	
        RUS.graphOutput()
	'''Window.size = (1366, 768)'''
	
	

 
       
        
# run app
if __name__ == "__main__":
    RUS().run()

 

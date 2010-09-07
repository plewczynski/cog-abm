import sys
sys.path.append('../')
import os
import pygtk
pygtk.require("2.0")
import gtk
import pango
import copy
import grapefruit
from cog_abm.extras.parser import *
from cog_abm.core.result import *
from steels.steels_experiment import *
#from steels.analyzer import *
from time import time, sleep


from itertools import imap, izip
argmax = lambda funct, items: max(izip(imap(funct, items), items))
argmin = lambda funct, items: min(izip(imap(funct, items), items))


class WCSPalette(object):
	def __init__(self):
		self.source = "../cog_abm/extras/330WCS.xml"
		self.wcs_environment = Parser().parse_environment(self.source)
	
	def get_colors(self):
		return self.wcs_environment.get_all_stimuli()

class AgentData(object):
	def __init__(self, cielab):
		self.cielab = cielab
		self.painted = []
		self.focals = []
		
	def handle_categories(self, iter, category_set):
		self.painted.append(range(330))
		self.focals.append({})
		dictionary = {}
		for i in xrange(len(category_set)):
			if category_set[i] not in dictionary:
				dictionary[category_set[i]] = []
			dictionary[category_set[i]].append(i)
		
		focals = self.focals[iter]
		for key in dictionary.keys():
			focal = self.find_focal_point(dictionary[key])
			focals[focal] = True
			self.set_focal(iter, dictionary[key], focal)
			
	def set_focal(self, iter, category, focal):
		painted = self.painted[iter]
		for i in xrange(len(category)):
			painted[category[i]] = focal
			
	def find_focal_point(self, category):
		focal = category[0]
		f_sum = float('inf')
		
		for i in xrange(len(category)):

			c = self.cielab[i]
			sum = math.fsum(
				[c.distance(self.cielab[j]) for j in xrange(len(category))])

			if sum < f_sum:
				f_sum = sum
				focal = category[i]
		
		return focal
		
	def get_number_of_categories(self, iter):
		return len(self.focals[iter])
			
class WCSTable(object):
	def __init__(self, colors):
		self.colors = copy.copy(colors)
		self.CELLAR_SPACE = 1
		self.CELLAR_SIZE = 15
		self.area = gtk.DrawingArea()
		self.pangolayout = self.area.create_pango_layout("")
		self.pangolayout.set_font_description(pango.FontDescription("normal 7"))
		#self.pangolayout.set_alignment(pango.ALIGN_RIGHT)
		
		self.area.set_size_request(42 * (self.CELLAR_SIZE + self.CELLAR_SPACE),
								10 * (self.CELLAR_SIZE + self.CELLAR_SPACE))
		self.area.connect("expose-event", self.area_expose)
		self.current_iteration = 0
		self.agent_data = None

	def get_number_of_categories(self, iter):
		if self.agent_data is None:
			return 0
		return self.agent_data.get_number_of_categories(iter)
		
	def area_expose(self, area, event):
		#self.style = self.area.get_style()
		#self.gc = self.style.fg_gc[gtk.STATE_NORMAL]

		self.gc = self.area.window.new_gc()
		self.create_palette_labels()
		self.paint_cellars(self.current_iteration)
		
	def show(self):
			self.area.show()
	
	def set_agent_data(self, agent_data):
		self.agent_data = agent_data
		
	def paint_cellars(self, iter):
		self.current_iteration = iter
		self.gc = self.area.window.new_gc()
		
		if self.agent_data is None:
			paintable = range(330)
			focals = {}
		else:	
			paintable = self.agent_data.painted[iter]
			focals = self.agent_data.focals[iter]
			
		for i in xrange(320):
			col = (2+i%40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)
			row = (1+i/40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)
			
			self.gc.set_rgb_fg_color(self.colors[paintable[i]])
			self.area.window.draw_rectangle(self.gc, True, col, row, 
			                           self.CELLAR_SIZE, self.CELLAR_SIZE)
			#if i in focals:
			#	self.gc.set_rgb_fg_color(self.colors[320])
			#	self.area.window.draw_arc(self.gc, True, col, row, 
			#						self.CELLAR_SIZE, self.CELLAR_SIZE, 0, 23040)#360*64)

		for i in xrange(10):
			self.gc.set_rgb_fg_color(self.colors[paintable[320+i]])
			self.area.window.draw_rectangle(self.gc, True, 0, i*(self.CELLAR_SIZE + 
					self.CELLAR_SPACE), self.CELLAR_SIZE, self.CELLAR_SIZE)
			#if (320 + i) in focals:
			#	self.gc.set_rgb_fg_color(self.colors[320])
			#	self.area.window.draw_arc(self.gc, True, 0, i*(self.CELLAR_SIZE + 
			#			self.CELLAR_SPACE), self.CELLAR_SIZE, self.CELLAR_SIZE, 0, 23040)
		#sleep(0.01)
		self.paint_focals(focals)
									
	def paint_focals(self, focals):
		for i in focals:
			if i < 320:
				col = (2+i%40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)
				row = (1+i/40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)
				
				self.gc.set_rgb_fg_color(self.colors[320])
				self.area.window.draw_arc(self.gc, True, col, row, 
									self.CELLAR_SIZE, self.CELLAR_SIZE, 0, 23040)#360*64)
								

			else:
				self.gc.set_rgb_fg_color(self.colors[320])
				self.area.window.draw_arc(self.gc, True, 0, (i-320)*(self.CELLAR_SIZE + 
						self.CELLAR_SPACE), self.CELLAR_SIZE, self.CELLAR_SIZE, 0, 23040)
						
	def create_palette_labels(self):
		space = self.CELLAR_SIZE + self.CELLAR_SPACE
		for i in xrange(1, 41):
			col = (1 + i) * space
			row = 0
			self.pangolayout.set_text(str(i)) 
			self.area.window.draw_layout(self.gc, col+2, row+3, 
			                             self.pangolayout)
			
		for i in xrange(10):
			self.pangolayout.set_text(chr(65 + i)) 
			self.area.window.draw_layout(self.gc, space+2, i*space+2, 
			                             self.pangolayout)
			
class MunsellPaletteInterface(object):
	def __init__(self, path, agents_viewed):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Agent colour categories map")
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_default_size(1280,-1)
		self.iterations = []
		self.stimuli = []
		self.colors = []
		self.agents_data = []
		start_time = time()
		self.init_wcs_template()
		self.agent_WCSTable = []
	
		self.get_results_from_folder(path)
		print "Processing data..."
		self.set_agents_palettes()
		print 'Done in:', time() - start_time,'s'
		
		self.main_vbox = gtk.VBox(False, 3)
		self.template = WCSTable(self.colors)
	
		self.main_vbox.add(self.template.area)

		self.create_agents_container(agents_viewed)
		
		self.main_vbox.add(self.scrolled_window)
		
		self.init_WCSTable_to_agent_data()

		self.panel = self.create_panel()
		
		self.main_vbox.add(self.panel)
		self.window.add(self.main_vbox)
		
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)

		self.window.show_all()		
		self.set_current_iteration_widgets(0)
		
	def set_agents_palettes(self):
		
		for i in xrange(self.agents_size):
			self.agents_data.append(AgentData(self.stimuli))
			
		for j in xrange(len(self.iterations)):
			iter = self.result_set[j]
			for i in xrange(len(iter)):
				self.agents_data[i].handle_categories(j, iter[i])
	
	def get_results_from_folder(self, path):
		print "From: ", path
		self.result_set = []
		list = os.listdir(path)
		for file in list:
			(root, ext) = os.path.splitext(file)
			if (ext == ".pout"):
				print "Reading:", file
				self.result_set.append(self.get_iteration_from_file(os.path.join(path, file)))
		
		zipped = zip(self.iterations, self.result_set)
		zipped.sort()
		(self.iterations, self.result_set) = zip(*zipped)
		
	def get_iteration_from_file(self, source):
#		result = ResultHandler()
#		result.unpickle(source)
#		tuple = result.get_results()
		with open(source, 'r') as file:
			tuple = cPickle.load(file)
		
		self.iterations.append(tuple[0]) 
		agents_result = []
		for agent in tuple[1]:
			agent_result = []
			for stimuli in self.stimuli:
				agent_result.append(agent.state.classify(stimuli))
			agents_result.append(agent_result)
		
		#constant number of agents for every iteration
		self.agents_size = len(agents_result)
		return agents_result
		
	def init_wcs_template(self):
			template = WCSPalette()
			self.stimuli = template.get_colors()
			for color in self.stimuli:
				r, g, b, a = self.convert_to_RGB(color)
				self.colors.append(gtk.gdk.Color(r, g, b))
	
	def create_agents_container(self, agent_viewed):
		self.cat_size_labels = []
		row = (agent_viewed-1)/2 +1
		col = 2 
		self.container = gtk.Table(row, col, True)
		self.container.set_row_spacings(6)
		self.container.set_col_spacings(6)
			
		for i in xrange(agent_viewed):
			r = i / col
			c = i % col
			self.container.attach(self.create_agent_panel(i), c, c+1, r, r+1)
		
		#self.container.show()
		self.scrolled_window = gtk.ScrolledWindow()
		self.scrolled_window.add_with_viewport(self.container)
		self.scrolled_window.set_size_request(1200, 400)
		#self.scrolled_window.show()
		
	def create_agent_panel(self, number):
		combo = gtk.combo_box_new_text()
		for i in xrange(self.agents_size):
			combo.append_text("Agent " + str(i))
		combo.set_active(number)
		combo.connect('changed', self.changed_cb, number)
		combo.set_size_request(50, 30)
		
		wcs_table = WCSTable(self.colors)
		self.agent_WCSTable.append(wcs_table)
		
		cat_size_label = gtk.Label()
		self.cat_size_labels.append(cat_size_label)
		hbox = gtk.HBox(True, 3)
		hbox.pack_start(combo)
		hbox.pack_start(cat_size_label)
		panel = gtk.VPaned()
		panel.pack1(hbox)
		panel.pack2(wcs_table.area)
		#panel.show()
		return panel
		
	def create_panel(self):
		self.close_button = gtk.Button("Close")
		self.close_button.connect("clicked", gtk.main_quit)
		self.close_button.set_size_request(150, 40)
		#self.close_button.show()
		self.scroll = gtk.HScrollbar()
		self.scroll.set_size_request(150, 40)
		self.scroll.set_update_policy(gtk.UPDATE_CONTINUOUS)
		self.scroll.set_adjustment(gtk.Adjustment(0, 0, len(self.iterations)-1, 1, 1, 0))
		self.scroll.connect("value-changed", self.scroll_value_changed)
		self.iteration_label = gtk.Label()
		#self.scroll.show()
		
		vbox = gtk.VBox(True, 2)
		vbox.pack_start(self.iteration_label)
		vbox.pack_start(self.scroll)
		panel = gtk.Table(1, 3, True)
		panel.set_col_spacings(15)
		panel.attach(self.close_button, 2, 3, 0, 1)
		panel.attach(vbox, 1, 2, 0, 1)

		return panel
	
	def changed_cb(self, combobox, cb_number):
		index = combobox.get_active()
		self.agent_WCSTable[cb_number].set_agent_data(self.agents_data[index])
		self.agent_WCSTable[cb_number].paint_cellars(self.current_iteration)
		
		self.cat_size_labels[cb_number].set_text("Number of categories: " + 
				str(self.agent_WCSTable[cb_number].get_number_of_categories
				    (self.current_iteration)))
				
	def scroll_value_changed(self, scroll):
		if (self.current_iteration is int(scroll.get_value())):
			return
		self.set_current_iteration_widgets(int(scroll.get_value()))
		
		for i in xrange(len(self.agent_WCSTable)):
			self.agent_WCSTable[i].paint_cellars(self.current_iteration)
	
	def set_current_iteration_widgets(self, iter):
		self.current_iteration = iter
		self.scroll.set_value(iter)
		self.iteration_label.set_text("Population iterations: "+ str(self.iterations[iter]))
		for i in xrange(len(self.agent_WCSTable)):
			self.cat_size_labels[i].set_text("Number of categories: " + 
				str(self.agent_WCSTable[i].get_number_of_categories(iter)))
		
	def init_WCSTable_to_agent_data(self):
		for tuple in zip(self.agents_data, self.agent_WCSTable):
			tuple[1].set_agent_data(tuple[0])
		
	def convert_to_RGB(self, color):
		#c1 = grapefruit.Color.NewFromLab(color.L, color.a/100, color.b/100, wref=grapefruit.Color.WHITE_REFERENCE['std_D50'])
		#c2 = grapefruit.Color.NewFromLab(color.L, color.a/100, color.b/100, wref=grapefruit.Color.WHITE_REFERENCE['std_D65'])
		#if c1 is  c2:
		#	print c1, c2
		return grapefruit.Color.NewFromLab(color.L, color.a/100, color.b/100, wref=grapefruit.Color.WHITE_REFERENCE['std_D50'])

	def main(self):
		gtk.main()

if __name__ == "__main__":
	if len(sys.argv) is not 3:
		print "You should specify directory of result set and number of agents viewed simultaneously"
	else:	
		mpi = MunsellPaletteInterface(sys.argv[1], int(sys.argv[2]))
		mpi.main()

#TODO:
#ladne parametry w mainie!! Konrad
#try dla wczytywania plikow
#legendy do gry w zgadywanie
#dopasowanie do wielkosci okna !!
#konwersja do rgb

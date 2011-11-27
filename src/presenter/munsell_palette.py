import sys
sys.path.append('../')
import os
import pygtk
pygtk.require("2.0")
import gtk
import pango
import copy
from presenter import grapefruit
from cog_abm.extras.color import *
from cog_abm.core.result import *
from steels.steels_experiment import *
#from steels.analyzer import *
from time import time


argmax = lambda funct, items: max(izip(imap(funct, items), items))
argmin = lambda funct, items: min(izip(imap(funct, items), items))

def str2bool(v):
    return v.lower() in ["yes", "true", "t", "y", "1"]

CELLAR_SPACE = 1
CELLAR_SIZE = 15
PANGO_FONT = "normal 7"
AGENTS_CONTAINERS_IN_ROW = 2
MAIN_CONTAINER_REQUESTED_HEIGHT = 600
MAIN_CONTAINER_REQUESTED_WIDTH = 1200

class AgentData(object):
	def __init__(self, cielab, find_focal):
		self.cielab = cielab
		self.painted = []
		self.focals = []
		self.ff = find_focal

	def handle_categories(self, iter, agent):
		#start_time = time()
		self.painted.append(range(330))
		self.focals.append({})

		if (iter == 0):
			return

		dictionary = {}
		category_set = [agent.state.classify(stimuli) 
		                for stimuli in self.cielab]
		#print category_set

		for i in xrange(len(category_set)):
			if category_set[i] not in dictionary:
				dictionary[category_set[i]] = []
			dictionary[category_set[i]].append(i)

		#focal_time = time()
		focals = self.focals[iter]
		#print dictionary
		for key, set in dictionary.iteritems():
			if (self.ff == "normal"):
				#print "normal"
				focal = self.find_focal_point(set)
			#elif (key <> None):
			else:
				focal = self.strength_find_focal_point(agent, key, 
				                                       category_set, set)

			focals[focal] = None
			self.set_focal(iter, set, focal)

		#print "Focal handling lasts %f - %f percent of handling category time." % (float(time() - focal_time), float((time() - focal_time)/(time() - start_time)))

	def set_focal(self, iter, category_set, focal):
		painted = self.painted[iter]
		for i in xrange(len(category_set)):
			painted[category_set[i]] = focal

	def find_focal_point(self, index_set):
		focal = index_set[0]
		f_sum = float('inf')

		for i in index_set:

			c = self.cielab[i]
			sum = math.fsum(
				[c.distance(self.cielab[j]) for j in index_set])

			if sum < f_sum:
				f_sum = sum
				focal = i

		return focal

	def strength_find_focal_point(self, agent, key, category_set, values):
		max = - float('inf')
		focal = category_set[0]
		#print key, category_set, values
		for val in values:
			strength = agent.state.sample_strength(key, 
			                                       self.cielab[val])
			if strength > max:
				max = strength
				focal = val

		return focal

	def get_number_of_categories(self, iter):
		return len(self.focals[iter])

class AgentDataWithLanguage(AgentData):
	def __init__(self, cielab, find_focal = "normal"):
		super(AgentDataWithLanguage, self).__init__(cielab, find_focal)
		self.names = []
		self.focal_names = []

	def handle_categories(self, iter, agent):
		#start_time = time()
		self.painted.append(range(330))
		self.focals.append({})
		self.focal_names.append({})
		self.names.append(range(330))

		if (iter == 0):
			return
		dictionary = {}
		category_set = [agent.state.classify(stimuli) 
		                for stimuli in self.cielab]
		#print category_set

		for i in xrange(len(category_set)):
			if category_set[i] not in dictionary:
				dictionary[category_set[i]] = []
			dictionary[category_set[i]].append(i)

		#focal_time = time()
		focals = self.focals[iter]
		focal_names = self.focal_names[iter]
		for key, set in dictionary.iteritems():
			if (self.ff == "normal"):
				#print "normal"
				focal = self.find_focal_point(set)
			#elif key <> None:
			else:
				focal = self.strength_find_focal_point(agent, key, 
				                                       category_set, set)

			name = str(agent.state.word_for(key))
			#two dictionaries for better performance
			focals[focal] = name
			focal_names[name] = focal
			self.set_focal(iter, set, focal, name)

	def set_focal(self, iter, category, focal, name):
		#self.names.append(range(330))
		names = self.names[iter]
		painted = self.painted[iter]
		for i in xrange(len(category)):
			painted[category[i]] = focal
			names[category[i]] = name

class Population(AgentDataWithLanguage):	
	def handle_categories(self, iter, agents_data):
		#self.focals[iter] -> {focal} = name
		#self.names[iter] -> {color} = name
		#self.focal_names[iter] -> {name} = focal

		#print "Iter: ", iter
		names_iter = range(330)	
		self.names.append(names_iter)

		focals_names_iter = {}
		self.focal_names.append(focals_names_iter)
		focals_iter = {}
		self.focals.append(focals_iter)

		self.painted.append(range(330))
		painted = self.painted[iter]

		if (iter == 0):
			return
		#all agents focals in category: key: category_name, value: list_of_focals
		category_set = {}

		#setting name for each color_square
		for color_nr in xrange(len(names_iter)):
			name_counter = {}	#counts names for color for each name
			for agent in agents_data:
				iter_names = agent.names[iter]

				name = iter_names[color_nr]
				if name <> str(None):
					if name in name_counter:
						name_counter[name] += 1
					else:
						name_counter[name] = 1

			best_name = 'None'
			temp_sum  = -1
			for name, sum in name_counter.iteritems():
				if sum > temp_sum:
					best_name = name
					temp_sum = sum

			names_iter[color_nr] = best_name
			if best_name not in category_set:
				category_set[best_name] = []
			category_set[best_name].append(color_nr) 

		#print category_set
		#print names_iter

		focal_counter = {}
		#setting focals data in each category
		for name in category_set:
			counter = {}
			for agent in agents_data:
				iter_focal_names = agent.focal_names[iter]
				if name in iter_focal_names:
					focal = iter_focal_names[name]
					#if focal of this agent appear in right population category
					if names_iter[focal] == name:
						if focal in focal_counter:
							counter[focal] += 1
						else:
							counter[focal] = 1
						#print names_iter[focal], name
						#focals 
						#category_set[name].append(focal)
			focal_counter[name] = counter

		#print focal_counter
		#print names_dic_iter
		#setting nearest focal (to other focals) in each category
		for name, counter in focal_counter.iteritems():
			#focals =category_set?[name]
			#counter = focal_counter[name]
			min = float('inf')
			if len(counter.keys()) == 0:
				for color in category_set[name]:
					c = self.cielab[color]
					sum = math.fsum([c.distance(self.cielab[col]) 
											for col in category_set[name]])
					if sum < min:
						min = sum
						foc = color
			else:
				for focal in counter:
					c = self.cielab[focal]
					sum = math.fsum([c.distance(self.cielab[foc])*counter[foc] 
													for foc in counter])
					if sum < min:
						min = sum
						foc = focal

			focals_names_iter[name] = foc
			focals_iter[foc] = name

		#print "Names_iter:", names_iter, "/n"
		#print "focals_iter:", focals_iter, "/n"
		#setting colors
		for i in xrange(len(painted)):
			painted[i] = focals_names_iter[names_iter[i]]

class WCSPalette(object):
	def __init__(self, colors):
		self.colors = copy.copy(colors)
		self.CELLAR_SPACE = CELLAR_SPACE
		self.CELLAR_SIZE = CELLAR_SIZE
		self.area = gtk.DrawingArea()

		self.area.set_size_request(42 * (self.CELLAR_SIZE + self.CELLAR_SPACE),
								10 * (self.CELLAR_SIZE + self.CELLAR_SPACE))
		self.area.connect("expose-event", self.area_expose)

		self.pangolayout = self.area.create_pango_layout("")
		self.pangolayout.set_font_description(pango.
		                                      FontDescription(PANGO_FONT))

	def area_expose(self, area, event):
		#self.style = self.area.get_style()
		#self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
		#self.gc = self.area.window.new_gc()
		self.paint_cellars()

	def show(self):
		self.area.show()

	def paint_cellars(self, iter=0, paintable=range(330)):
		self.current_iteration = iter
		self.gc = self.area.window.new_gc(line_width=2)
		self.area.window.clear()

		for i in xrange(320):
			col = (2+i%40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)
			row = (1+i/40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)

			self.gc.set_rgb_fg_color(self.colors[paintable[i]])
			self.area.window.draw_rectangle(self.gc, True, col, row, 
			                           self.CELLAR_SIZE, self.CELLAR_SIZE)

		for i in xrange(10):
			self.gc.set_rgb_fg_color(self.colors[paintable[320+i]])
			self.area.window.draw_rectangle(self.gc, True, 1, i*
				(self.CELLAR_SIZE + self.CELLAR_SPACE)+1, self.CELLAR_SIZE, 
				self.CELLAR_SIZE)

		self.paint_category_borders(paintable)
		self.create_palette_labels()

	def paint_category_borders(self, paintable):
		self.gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
		space = self.CELLAR_SIZE + self.CELLAR_SPACE
		self.area.window.draw_rectangle(self.gc, False, 1, 1, 
				self.CELLAR_SIZE, 10*(self.CELLAR_SIZE) + 9*self.CELLAR_SPACE)

		self.area.window.draw_rectangle(self.gc, False, 2*space, space, 
				40*self.CELLAR_SIZE +39*self.CELLAR_SPACE, 8*self.CELLAR_SIZE
				+ 7*self.CELLAR_SPACE)

		#paint column lines
		for i in xrange(8):
			index =i*40
			for j in xrange(39):
				if (paintable[index] is not paintable[index+1]):
					self.area.window.draw_line(self.gc, (3+j)*space-1, 
								(1+i)*space-1, (3+j)*space-1, (2+i)*space-1)
				index += 1

		#paint row lines
		for i in xrange(7):	
			index = i*40
			for j in xrange(40):
				if (paintable[index] is not paintable[index+40]):
					self.area.window.draw_line(self.gc, (2+j)*space-1, 
								(2+i)*space-1, (3+j)*space-1, (2+i)*space-1)
				index += 1

		#paint row lines in side box			
		index = 319
		for i in xrange(9):
			index += 1
			if (paintable[index] is not paintable[index+1]):
				self.area.window.draw_line(self.gc, 0, (1+i)*space, 
											space-1, (1+i)*space)

	def create_palette_labels(self):
		space = self.CELLAR_SIZE + self.CELLAR_SPACE
		self.gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
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

class WCSAgent(WCSPalette):
	def __init__(self, colors):
		super(WCSAgent, self).__init__(colors)
		self.current_iteration = 0
		self.agent_data = None

	def get_number_of_categories(self, iter):
		if self.agent_data is None:
			return 0
		return self.agent_data.get_number_of_categories(iter)

	def set_agent_data(self, agent_data):
		self.agent_data = agent_data

	def area_expose(self, area, event):
		#self.gc = self.area.window.new_gc()
		self.paint_cellars(self.current_iteration)	

	def paint_cellars(self, iter=0):
		super(WCSAgent, self).paint_cellars(iter, self.agent_data.painted[iter])
		self.paint_focals(self.agent_data.focals[iter])

	def paint_focals(self, focals):
		#print "paint focals", focals
		circle_size = self.CELLAR_SIZE-1
		wheel_size = self.CELLAR_SIZE-1
		for i, name in focals.iteritems():
			if i < 320:
				col = (2+i%40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)
				row = (1+i/40)*(self.CELLAR_SIZE + self.CELLAR_SPACE)
				self.gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
				self.area.window.draw_arc(self.gc, False, col, row, 
									circle_size, circle_size, 0, 23040)#360*64)
				self.gc.set_rgb_fg_color(gtk.gdk.color_parse("white"))
				self.area.window.draw_arc(self.gc, True, col, row, 
									wheel_size, wheel_size, 0, 23040)#360*64)

			else:
				self.gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
				self.area.window.draw_arc(self.gc, False, 1, (i-320)*(self.
					CELLAR_SIZE + self.CELLAR_SPACE)+1, circle_size, 
					circle_size, 0, 23040)
				self.gc.set_rgb_fg_color(gtk.gdk.color_parse("white"))
				self.area.window.draw_arc(self.gc, True, 1, (i-320)*(self.
					CELLAR_SIZE + self.CELLAR_SPACE)+1, wheel_size, 
					wheel_size, 0, 23040)

class WCSAgentWithLegend(WCSAgent):
	def __init__(self, colors):
		super(WCSAgentWithLegend, self).__init__(colors)
		self.legend = gtk.DrawingArea()
		self.legend.connect("expose-event", self.legend_expose)

	def area_expose(self, area, event):
		#self.gc = self.area.window.new_gc()
		self.paint_cellars(self.current_iteration)	

	def paint_cellars(self, iter=0):
		super(WCSAgentWithLegend, self).paint_cellars(iter)
		self.paint_legend(iter, self.agent_data.focals[iter])

	def legend_expose(self, area, event):
		self.gc = self.legend.window.new_gc()
		self.paint_legend(self.current_iteration, 
		                  self.agent_data.focals[self.current_iteration])

	def paint_legend(self, iter, focals = {}):
		self.current_iteration = iter
		self.gc = self.legend.window.new_gc()
		self.legend.window.clear()
		column = 0
		row = self.CELLAR_SPACE
		counter = 0

		#focals = self.agent_data.focals[iter]
		for nr, name in focals.iteritems():
			counter += 1
			if (counter == 22):
				row += 2*self.CELLAR_SIZE
				counter = 0
				column = 0

			self.gc.set_rgb_fg_color(self.colors[nr])
			column += 2*self.CELLAR_SIZE
			self.legend.window.draw_rectangle(self.gc, True, column, row, 
						self.CELLAR_SIZE, self.CELLAR_SIZE)
			self.gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
			self.pangolayout.set_text(name) 
			self.legend.window.draw_layout(self.gc, column, row + 
					self.CELLAR_SIZE, self.pangolayout)

class MunsellPaletteInterface(object):
	def __init__(self, path, agents_viewed, find_focal):
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
		self.set_agents_data(find_focal)
		print 'Done in:', time() - start_time,'s'

		self.main_vbox = gtk.VBox(False, 2)
		#self.template = WCSPalette(self.colors)

		#self.main_vbox.add(self.template.area)

		self.create_containers(agents_viewed)

		self.main_vbox.add(self.scrolled_window)

		self.init_WCSTable_to_agent_data()

		self.panel = self.create_panel()

		self.main_vbox.add(self.panel)
		self.window.add(self.main_vbox)

		if (self.window):
			self.window.connect("destroy", gtk.main_quit)

		self.window.show_all()		
		self.set_current_iteration_widgets(0)

	def set_agents_data(self, find_focal):
		for i in xrange(self.agents_size):
			self.agents_data.append(AgentData(self.stimuli, find_focal))

		for j in xrange(len(self.iterations)):
			agent = self.result_set[j]
			for i in xrange(len(agent)):
				self.agents_data[i].handle_categories(j, agent[i])

	def get_results_from_folder(self, path):
		print "From: ", path
		self.result_set = []
		list = os.listdir(path)
		for file in list:
			(root, ext) = os.path.splitext(file)
			if (ext == ".pout"):
				print "Reading:", file
				self.result_set.append(self.get_iteration_from_file
				                       (os.path.join(path, file)))

		zipped = zip(self.iterations, self.result_set)
		zipped.sort()
		(self.iterations, self.result_set) = zip(*zipped)

	def get_iteration_from_file(self, source):
		with open(source, 'r') as file:
			tuple = cPickle.load(file)

		self.iterations.append(tuple[0]) 
		agents = tuple[1]

		#constant number of agents for every iteration
		self.agents_size = len(agents)
		return agents

	def init_wcs_template(self):
		self.stimuli = get_WCS_colors()
		for color in self.stimuli:
			r, g, b, _ = self.convert_to_RGB(color)
			self.colors.append(gtk.gdk.Color(r, g, b))

		#print [self.stimuli[j].distance(self.stimuli[j+1]) for j in xrange(len(self.stimuli)-2)]

	def create_containers(self, agent_viewed):
		self.cat_size_labels = []
		row = (agent_viewed-1)/2 +2

		self.container = gtk.Table(row, AGENTS_CONTAINERS_IN_ROW, True)
		self.container.set_row_spacings(6)
		self.container.set_col_spacings(6)

		wcs_palette = WCSPalette(self.colors)
		self.container.attach(wcs_palette.area, 0, 1, 0, 1)

		for i in xrange(agent_viewed):
			r = i / AGENTS_CONTAINERS_IN_ROW + 1
			c = i % AGENTS_CONTAINERS_IN_ROW
			self.container.attach(self.create_agent_panel(i), c, c+1, r, r+1)

		self.scrolled_window = gtk.ScrolledWindow()
		self.scrolled_window.add_with_viewport(self.container)
		self.scrolled_window.set_size_request(MAIN_CONTAINER_REQUESTED_WIDTH, 
		                                      MAIN_CONTAINER_REQUESTED_HEIGHT)

	def create_agent_panel(self, number):
		combo = gtk.combo_box_new_text()
		for i in xrange(self.agents_size):
			combo.append_text("Agent " + str(i))

		combo.set_active(number)
		combo.connect('changed', self.changed_cb, number)
		combo.set_size_request(50, 30)

		cat_size_label = gtk.Label()
		self.cat_size_labels.append(cat_size_label)

		table = gtk.Table(2, 2, False)
		table.attach(combo, 0, 1, 0, 1)
		table.attach(cat_size_label, 1, 2, 0, 1)

		wcs_table = WCSAgent(self.colors)

		self.agent_WCSTable.append(wcs_table)

		panel = gtk.VPaned()
		panel.pack1(table)
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
		self.scroll.set_adjustment(gtk.Adjustment(0, 0, 
										len(self.iterations)-1, 1, 1, 0))
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
		self.iteration_label.set_text("Population iterations: "+ 
								str(self.iterations[iter]))
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
		return grapefruit.Color.NewFromLab(color.L, 
			color.a/100, color.b/100, wref=grapefruit.Color.
			WHITE_REFERENCE['std_D65'])

	def main(self):
		gtk.main()

class MunsellPaletteInterfaceWithLanguage(MunsellPaletteInterface):
	def set_agents_data(self, find_focal):
		for i in xrange(self.agents_size):
			self.agents_data.append(AgentDataWithLanguage(self.stimuli, 
													find_focal))

		self.population = Population(self.stimuli)
		for j in xrange(len(self.iterations)):
			agent = self.result_set[j]
			for i in xrange(len(agent)):
				try:  
					self.agents_data[i].handle_categories(j, agent[i])
				except:
					print "Could not handle agent categories:", 
					sys.exc_info()[0]
					#sys.exit()
			self.population.handle_categories(j, self.agents_data)

	def create_containers(self, agent_viewed):
		super(MunsellPaletteInterfaceWithLanguage, 
		      self).create_containers(agent_viewed)
		self.container.attach(self.create_population_view(), 1, 2, 0, 1)

	def create_agent_panel(self, number):
		combo = gtk.combo_box_new_text()
		for i in xrange(self.agents_size):
			combo.append_text("Agent " + str(i))

		combo.set_active(number)
		combo.connect('changed', self.changed_cb, number)
		combo.set_size_request(50, 30)

		cat_size_label = gtk.Label()
		self.cat_size_labels.append(cat_size_label)

		table = gtk.Table(2, 2, False)
		table.attach(combo, 0, 1, 0, 1)
		table.attach(cat_size_label, 1, 2, 0, 1)

		wcs_table = WCSAgentWithLegend(self.colors)
		window = gtk.ScrolledWindow()
		window.add_with_viewport(wcs_table.legend)
		window.set_size_request(-1, 50)
		window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		table.attach(window, 0, 2, 1, 2)

		self.agent_WCSTable.append(wcs_table)

		panel = gtk.VPaned()
		panel.pack1(table)
		panel.pack2(wcs_table.area)
		#panel.show()
		return panel

	def create_population_view(self):

		self.population_cat_label = gtk.Label()
		name_label = gtk.Label("Population")

		table = gtk.Table(2, 2, False)
		table.attach(self.population_cat_label, 1, 2, 0, 1)		
		table.attach(name_label, 0, 1, 0, 1)

		wcs_table = WCSAgentWithLegend(self.colors)
		window = gtk.ScrolledWindow()
		window.add_with_viewport(wcs_table.legend)
		window.set_size_request(-1, 50)
		window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		table.attach(window, 0, 2, 1, 2)

		self.population_view = wcs_table

		panel = gtk.VPaned()
		panel.pack1(table)
		panel.pack2(wcs_table.area)
		#panel.show()
		return panel

	def scroll_value_changed(self, scroll):
		if (self.current_iteration is int(scroll.get_value())):
			return
		super(MunsellPaletteInterfaceWithLanguage, 
		      self).scroll_value_changed(scroll)
		self.population_view.paint_cellars(self.current_iteration)

	def set_current_iteration_widgets(self, iter):
		super(MunsellPaletteInterfaceWithLanguage, 
		      self).set_current_iteration_widgets(iter)
		self.population_cat_label.set_text("Number of categories: " + str(self.
			population.get_number_of_categories(self.current_iteration)))

	def init_WCSTable_to_agent_data(self):
		super(MunsellPaletteInterfaceWithLanguage, self). \
						init_WCSTable_to_agent_data()
		self.population_view.set_agent_data(self.population)

if __name__ == "__main__":
	import optparse

	optp = optparse.OptionParser()

	optp.add_option('-a','--agents', action="store", dest='agents', type="int",
			help="Number of agents viewed", default=10)

	optp.add_option('-d','--directory', action="store", dest='directory', 
			type="string", help="Directory with input data")

	optp.add_option('-f','--findfocal', action="store", type="string", 
		dest="find_focal", help="Determines which 'find_focal' algorithm will \
		be used ('normal' as default or 'strength_based')", default="normal")

	optp.add_option('-l', '--legend', action="store", type="string", dest=
		"legend", help="Type true to show language sharing", default="false")

	# Parse the arguments (defaults to parsing sys.argv).
	opts, args = optp.parse_args()

	if (str2bool(opts.legend) == 1):
		mpi = MunsellPaletteInterfaceWithLanguage(opts.directory, opts.agents, 
		                                          opts.find_focal)

	else:
		mpi = MunsellPaletteInterface(opts.directory, opts.agents, 
		                              opts.find_focal)

	mpi.main()

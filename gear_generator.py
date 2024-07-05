import math
import json
import os, sys
import platform
import time
import datetime
import pathlib
from pathvalidate import sanitize_filename
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkFont
from PIL import ImageFont
import Pmw

textmode = False

def get_config_dir():
	if sys.platform == 'win32':
		# Use AppData on Windows
		appdata = os.getenv('APPDATA')
		config_dir = os.path.join(appdata, 'PB3 Gear Generator')
	elif sys.platform == 'darwin':
		# Use macOS specific path
		config_dir = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'PB3GearGenerator')
	else:
		# Use Linux specific path
		config_dir = os.path.join(os.path.expanduser('~'), '.config', 'pb3_gear_generator')

	return config_dir

def save_to_config(key, value):
	config_dir = get_config_dir()
	os.makedirs(config_dir, exist_ok=True)
	config_path = os.path.join(config_dir, 'pb3_gear_generator_config.json')

	if os.path.exists(config_path):
		with open(config_path, 'r') as f:
			config = json.load(f)
	else:
		config = {}

	config[key] = value
	with open(config_path, 'w') as f:
		json.dump(config, f)

def load_from_config(key):
	config_dir = get_config_dir()
	config_path = os.path.join(config_dir, 'pb3_gear_generator_config.json')

	if os.path.exists(config_path):
		with open(config_path, 'r') as f:
			config = json.load(f)
			return config.get(key)
	else:
		print(f"Configuration file '{config_path}' does not exist.")
		return None

#print(load_from_config("custom_shapes_dir"))
if load_from_config("custom_shapes_dir") is None:
	if platform.system() == "Windows":
		dir = os.path.join(pathlib.Path.home(), "AppData", "LocalLow", "Dry Cactus", "Poly Bridge 3", "CustomShapeLibrary")
		save_to_config("custom_shapes_dir", dir)
	else:
		dir = None
else:
	dir = load_from_config("custom_shapes_dir")
	#print(dir)

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

pb3_font = ImageFont.truetype(resource_path("Fredoka-SemiBold.ttf"))
alert_image = resource_path("alert.png")
check_y = resource_path("check_y.png")
check_n = resource_path("check_n.png")
icon = resource_path("iconv2.ico")

gear_type_options = ['1: Triangle Tooth Spur Gear',
					'2: Trapezoidal Tooth Spur Gear',
					'3: Triangle Tooth Ring Gear',
					'4: Trapezoidal Tooth Ring Gear',
					'5: Triangle Tooth Rack Gear',
					'6: Trapezoidal Tooth Rack Gear'
					]

def verifyVerticesAbove100():
	print("Warning, the number of vertices that will be generated for this gear exceeds the max amount of manually editable vertices (100), continue anyways? (Y/N)")
	while True:
		y_n = input(">").lower()
		if y_n in ['y', 'n']:
			if y_n == 'y': print("Continuing anyways.")
			return y_n == 'y'
		
def is_number(num):
	if not num: return True
	try:
		float(num)
		return True
	except ValueError:
		return False
	
def is_number_gui(num, name):
	if not num: return True
	try:
		float(num)
		if '-' not in num:
			return True
		else:
			return False
		#if (name == "radius" and float(num) < 10000 and float(num) >= 0.1):
		#	return True 
		#else:
		#	return False
		return True
	except ValueError:
		return False
	
def is_int(num):
	try:
		int(num)
	except ValueError:
		return False
	
def is_int_gui(num, name):
	if not num: return True
	try:
		int(num)
		if '-' not in num:
			return True
		else:
			return False
		#if (name == "teeth" and int(num) < 10000 and int(num) >= min_teeth.get()):
		#	return True 
		#else:
		#	return False
	except ValueError:
		return False
	
def is_filename_sanitary(filename):
	print([filename, sanitize_filename(filename)])
	return (sanitize_filename(filename) == filename) or filename[-1] == ' '

root = Tk()
root.title("PB3 Gear Generator")
root.resizable(width=False, height=False)
Pmw.initialise(root)
	
teeth_wrapper = (root.register(is_int_gui), '%P', 'teeth')
radius_wrapper = (root.register(is_number_gui), '%P', 'radius')
filename_wrapper = (root.register(is_filename_sanitary), '%P')

def updateGearType(_):
	num = gear_type_picker.current() + 1
	setValuesForRingType() if num in [3, 4] else setValuesForRackType() if num in [5, 6] else setValuesNormal()

def setValuesForRingType():
	#min_teeth.set(4)
	fixFormatting(num_teeth_entry, "teeth")
	#num_teeth_entry['from_'] = 4
	#teeth_text.set("Number of Teeth (min 4)")
	reference_gear_label.grid_remove()
	rack_gear_label.grid_remove()
	outer_radius_entry.grid(column=4, row=5, sticky=(W, E))
	outer_radius_label.grid(column=2, row=5, columnspan=2, sticky=(E))
	editable_entry.grid()
	true_num_teeth_entry.grid_remove()
	true_num_teeth_label.grid_remove()
	#editable_label.grid()
	num_teeth_entry.grid(row=2)
	num_teeth_label.grid(row=2)
	gear_radius_entry.grid(row=3)
	gear_radius_label.grid(row=3)
	tooth_height_entry.grid(row=4)
	tooth_height_label.grid(row=4)
	tooth_height_alert.grid(row=4)
	clearance_entry.grid(row=7)
	clearance_label.grid(row=7)

def setValuesForRackType():
	#min_teeth.set(2)
	#num_teeth_entry['from_'] = 2
	#teeth_text.set("Number of Teeth (min 2)")
	outer_radius_entry.grid_remove()
	outer_radius_label.grid_remove()
	editable_entry.grid_remove()
	clearance_entry.grid(row=8)
	clearance_label.grid(row=8)
	clearance_alert.grid(row=8)
	true_num_teeth_entry.grid(column=4, row=7, sticky=(W, E))
	true_num_teeth_label.grid(column=2, row=7, columnspan=2, sticky=(E), padx=5)
	rack_gear_label.grid(column=2, row=6, columnspan=3)
	tooth_height_entry.grid(row=5)
	tooth_height_label.grid(row=5)
	tooth_height_alert.grid(row=5)
	gear_radius_entry.grid(row=4)
	gear_radius_label.grid(row=4)
	num_teeth_entry.grid(row=3)
	num_teeth_label.grid(row=3)
	reference_gear_label.grid(column=2, row=2, columnspan=3)

def setValuesNormal():
	#min_teeth.set(4)
	fixFormatting(num_teeth_entry, "teeth")
	#num_teeth_entry['from_'] = 4
	#teeth_text.set("Number of Teeth (min 4)")
	outer_radius_entry.grid_remove()
	outer_radius_label.grid_remove()
	editable_entry.grid_remove()
	reference_gear_label.grid_remove()
	rack_gear_label.grid_remove()
	true_num_teeth_entry.grid_remove()
	true_num_teeth_label.grid_remove()
	#editable_label.grid_remove()
	num_teeth_entry.grid(row=2)
	num_teeth_label.grid(row=2)
	gear_radius_entry.grid(row=3)
	gear_radius_label.grid(row=3)
	tooth_height_entry.grid(row=4)
	tooth_height_label.grid(row=4)
	tooth_height_alert.grid(row=4)
	clearance_entry.grid(row=5)
	clearance_label.grid(row=5)
	clearance_alert.grid(row=5)

def fixFormatting(widget, name):
	#print(widget)
	val = widget.get()
	#print([name, val])
	if not val: val = 0
	else:
		if "." in val:
			val = float(val)
		else:
			val = int(val)
	#print(val)
	if name == "teeth":
		widget.set(min(max(4, val), 9999))
	elif name == "radius":
		widget.set(min(max(0.1, val), 9999))
	elif name == "height":
		widget.set(min(max(0.1, val), 9999))
	elif name == "clearance":
		widget.set(min(max(0, val), 9999))
	elif name == "true_teeth":
		widget.set(min(max(2, val), 9999))

def checkConflicts(_):
	if tooth_height_var.get() / 2 >= gear_radius_var.get():
		tooth_height_alert.grid()
		tooth_height_alert['image'] = alert
		tooltip.bind(tooth_height_alert, f"Tooth height is too high, keep tooth height less than double the radius. (Max {gear_radius_var.get() * 2}m)")
		tooth_height_entry.grid(padx=[0, 35])
		return False
	else:
		tooth_height_alert.grid_remove()
		tooth_height_entry.grid(padx=0)

	if gear_type_picker.current() + 1 in [3, 4] and outer_radius_var.get() <= gear_radius_var.get() + tooth_height_var.get() / 2:
		outer_radius_alert.grid()
		outer_radius_alert['image'] = alert
		tooltip.bind(outer_radius_alert, f"Outer radius is too small, must be at least the gear radius plus half the tooth height. (Min >{gear_radius_var.get() + tooth_height_var.get() / 2}m)")
		outer_radius_entry.grid(padx=[0, 35])
		return False
	elif gear_type_picker.current() + 1 in [3, 4]:
		outer_radius_alert.grid_remove()
		outer_radius_entry.grid(padx=0)

	if clearance_var.get() >= tooth_height_var.get():
		clearance_alert.grid()
		clearance_alert['image'] = alert
		tooltip.bind(clearance_alert, f"Clearance is too high, must be less than the tooth height. (Max {tooth_height_var.get()}m)")
		clearance_entry.grid(padx=[0, 35])
		return False
	else:
		clearance_alert.grid_remove()
		clearance_entry.grid(padx=0)

	return True

def updateGear(_, __, ___):
	global values_changed
	values_changed = True
	if generate_with_value_change_var.get():
		#print("yes")
		for i in [num_teeth_var, gear_radius_var, tooth_height_var, clearance_var, outer_radius_var]:
			try:
				#print(i.get())
				if i.get() == "":
					#print("invalid  " + str(i.get()))
					return
			except TclError:
				#print("invalid")
				return
		if (num_teeth_var.get() < 4):
			return
		generateGear()

gear1 = None
gear2 = None
gear_vertices = None
generated_gear_type = None
values_changed = False

def generateGear():
	if not checkConflicts(None):
		return
	display.delete("all")

	farthest_point = 0
	
	avg_x = 0
	x_offset = 0

	gear_type = (0 if gear_type_picker.current() == -1 else gear_type_picker.current()) + 1
	global generated_gear_type
	generated_gear_type = gear_type
	num_teeth = num_teeth_var.get()
	inner_size = gear_radius_var.get()
	tooth_height = tooth_height_var.get() / 2
	outer_radius = outer_radius_var.get()
	editable = editable_var.get()
	clearance = clearance_var.get()
	true_num_teeth = true_num_teeth_var.get()
	
	if gear_type == 1:
		points = []
		max_vertices = (num_teeth * 2)
		for i in range(0, max_vertices):
			r = inner_size - tooth_height
			if i%2 == 0: r += tooth_height*2 - clearance
			#print(math.pow(-1 ,i))
			x = r * math.cos(math.radians(i * (360 / max_vertices)))
			y = r * math.sin(math.radians(i * (360 / max_vertices)))
			points.append([x, y])
		farthest_point = inner_size + tooth_height - clearance
	elif gear_type == 2:
		points = []
		max_vertices = (num_teeth * 4)
		for i in range(0, max_vertices):
			r = inner_size - tooth_height
			if i%4 < 2: r += tooth_height*2 - clearance
			x = r * math.cos(math.radians((i-0.5) * (360 / max_vertices)))
			y = r * math.sin(math.radians((i-0.5) * (360 / max_vertices)))
			points.append([x, y])
		farthest_point = inner_size + tooth_height - clearance
	elif gear_type == 3:
		points = []
		max_vertices = (num_teeth * 2)
		for i in range(0, max_vertices):
			r = inner_size - tooth_height + clearance
			if i%2 == 0: r += tooth_height*2
			x = r * math.cos(math.radians(i * (360 / max_vertices)))
			y = r * math.sin(math.radians(i * (360 / max_vertices)))
			points.append([x, y])
		if editable:
			points.append([r + tooth_height*2, -0.025])
		else:
			points.append([r + tooth_height*2, -0.00001])
		for i in range(0, 16):
			r2 = outer_radius
			x2 = r2 * math.cos(-math.radians(i * (360 / 16)))
			y2 = r2 * math.sin(-math.radians(i * (360 / 16)))
			points.append([x2, y2])
		farthest_point = outer_radius
		if editable:
			points.append([r2, 0.025])
		else:
			points.append([r2, 0.00001])
	elif gear_type == 4:
		points = []
		max_vertices = (num_teeth * 4)
		for i in range(0, max_vertices):
			r = inner_size - tooth_height + clearance
			if i%4 < 2: r += tooth_height*2
			x = r * math.cos(math.radians((i-0.5) * (360 / max_vertices)))
			y = r * math.sin(math.radians((i-0.5) * (360 / max_vertices)))
			points.append([x, y])
		if editable:
			points.append([(r + tooth_height*2) * math.cos(math.radians(-0.55 * (360 / max_vertices))), (r + tooth_height*2) * math.sin(math.radians(-0.55 * (360 / max_vertices))) -0.0001])
		else:
			points.append([(r + tooth_height*2) * math.cos(math.radians(-0.5 * (360 / max_vertices))), (r + tooth_height*2) * math.sin(math.radians(-0.5 * (360 / max_vertices))) -0.0001])
		for i in range(0, 16):
			r2 = outer_radius
			x2 = r2 * math.cos(-math.radians(i * (360 / 16)))
			y2 = r2 * math.sin(-math.radians(i * (360 / 16)))
			points.append([x2, y2])
		farthest_point = outer_radius
		if editable:
			points.append([r2 * math.cos(math.radians(0.05 * (360 / max_vertices))), r2 * math.sin(math.radians(0.05 * (360 / max_vertices)))])
		else:
			points.append([r2, 0.0001])
	elif gear_type == 5:
		inner_size *= 1000000
		num_teeth *= 1000000
		points = []
		max_vertices = (num_teeth * 2)
		offset = -(inner_size - tooth_height) * math.cos(math.radians((360 / max_vertices) + 90))
		for i in range(-1, true_num_teeth * 2):
			r = inner_size - tooth_height
			if i%2 == 0: r += tooth_height*2 - clearance
			x = r * math.cos(math.radians(i * (360 / max_vertices) + 90)) + offset
			y = r * math.sin(math.radians(i * (360 / max_vertices) + 90)) - (inner_size - tooth_height*2)
			points.append([x, y])
			avg_x += x
		points.append([r * math.cos(math.radians(i * (360 / max_vertices) + 90)) + offset, -0.5])
		points.append([r * math.cos(math.radians(-1 * (360 / max_vertices) + 90)) + offset, -0.5])
		x_offset = (-avg_x / ((true_num_teeth * 2) + 1))
		farthest_point = x_offset + offset + (r * math.cos(math.radians(-1 * (360 / max_vertices) + 90)))
	elif gear_type == 6:
		inner_size *= 1000000
		num_teeth *= 1000000
		points = []
		max_vertices = (num_teeth * 4)
		offset = -(inner_size - tooth_height) * math.cos(math.radians((2) * (360 / max_vertices) + 90))
		for i in range(-1, true_num_teeth * 4 - 1):
			r = inner_size - tooth_height
			if i%4 < 2: r += tooth_height*2 - clearance
			if i%4 in [1, 2]: i -= 0.075
			#if i%4 == 2: i -= 0.075
			if i%4 in [3, 0]: i += 0.075
			#if i%4 == 0: i += 0.075
			x = r * math.cos(math.radians((i-0.5) * (360 / max_vertices) + 90)) + offset
			y = r * math.sin(math.radians((i-0.5) * (360 / max_vertices) + 90)) - (inner_size - tooth_height*2)
			points.append([x, y])
			avg_x += x
		points.append([r * math.cos(math.radians((i-0.5) * (360 / max_vertices) + 90)) + offset, -0.5])
		points.append([r * math.cos(math.radians(-1.425 * (360 / max_vertices) + 90)) + offset, -0.5])
		x_offset = (-avg_x / (true_num_teeth * 4))
		farthest_point = x_offset + offset + (r * math.cos(math.radians(-1.425 * (360 / max_vertices) + 90)))
		#print(x_offset)

	global gear_vertices
	gear_vertices = points

	display_points = []
	scale_factor = 175/farthest_point
	#print(farthest_point)
	#print(scale_factor)
	
	for i in range(0, math.floor(200/(scale_factor/4)) + 1):
		#if i%20 == 0:
		#	color = "#203f57"
		#elif i%4 == 0:
		#	color = "#2d5475"
		#else:
		color = "#345f84"
		display.create_line(i * (scale_factor/4) + 200, 0, i * (scale_factor/4) + 200, 400, fill=color, width=2.5)
		display.create_line(0, i * (scale_factor/4) + 200, 400, i * (scale_factor/4) + 200, fill=color, width=2.5)
		display.create_line(-i * (scale_factor/4) + 200, 0, -i * (scale_factor/4) + 200, 400, fill=color, width=2.5)
		display.create_line(0, -i * (scale_factor/4) + 200, 400, -i * (scale_factor/4) + 200, fill=color, width=2.5)
		#print(str(i) + "  " + str(i * (scale_factor/4)) + "  " + color)
	for i in range(0, math.floor(200/(scale_factor)) + 1):
		color = "#2d5475"
		display.create_line(i * (scale_factor) + 200, 0, i * (scale_factor) + 200, 400, fill=color, width=2.5)
		display.create_line(0, i * (scale_factor) + 200, 400, i * (scale_factor) + 200, fill=color, width=2.5)
		display.create_line(-i * (scale_factor) + 200, 0, -i * (scale_factor) + 200, 400, fill=color, width=2.5)
		display.create_line(0, -i * (scale_factor) + 200, 400, -i * (scale_factor) + 200, fill=color, width=2.5)
	for i in range(0, math.floor(200/(scale_factor*4)) + 1):
		color = "#203f57"
		display.create_line(i * (scale_factor*4) + 200, 0, i * (scale_factor*4) + 200, 400, fill=color, width=2.5)
		display.create_line(0, i * (scale_factor*4) + 200, 400, i * (scale_factor*4) + 200, fill=color, width=2.5)
		display.create_line(-i * (scale_factor*4) + 200, 0, -i * (scale_factor*4) + 200, 400, fill=color, width=2.5)
		display.create_line(0, -i * (scale_factor*4) + 200, 400, -i * (scale_factor*4) + 200, fill=color, width=2.5)

	for i in points:
		#print(i)
		display_points.append([((i[0] + x_offset) * scale_factor) + 200, 200 - (i[1] * scale_factor)])
	
	linewidth = (7 if stylized_var.get() else 1)

	global gear1, gear2
	gear1 = display.create_polygon(display_points, outline='#a1acbc', width=(linewidth + 0.5), fill=('' if stylized_var.get() else 'black'))
	gear2 = display.create_polygon(display_points, outline='white', width=linewidth, fill='')

	stylized_entry = display.create_image(10, 394, image=(check_y if stylized_var.get() else check_n), anchor='sw')
	stylized_entry_label = display.create_text(30, 396, text="Stylize", anchor='sw', font=('Fredoka SemiBold', 13), fill='white')
	display.tag_bind(stylized_entry, "<Button-1>", lambda e: toggleStyle(stylized_entry))
	display.tag_bind(stylized_entry_label, "<Button-1>", lambda e: toggleStyle(stylized_entry))

	global values_changed
	values_changed = False

def clickedOff(_):
	root.focus()
	
def toggleStyle(widget):
	stylized_var.set(not stylized_var.get())
	if stylized_var.get():
		display.itemconfig(widget, image=check_y)
		display.itemconfig(gear1, fill='', width=7.5)
		display.itemconfig(gear2, width=7)
	else:
		display.itemconfig(widget, image=check_n)
		display.itemconfig(gear1, fill='black', width=1.5)
		display.itemconfig(gear2, width=1)

def chooseFilepath():
	global dir
	dir = filedialog.askdirectory()
	save_to_config("custom_shapes_dir", dir)
	filepath_var.set(dir)
	tooltip.bind(filepath_select, dir)
	
def newOrOverwrite():
	if gear_vertices is None:
		messagebox.showerror(message="No gear generated!", icon='error', title="Error")
	else:
		if values_changed:
			if not messagebox.askokcancel(message="Some parameters have been modified since last gear generation. Save anyways?", title="Unapplied Changes"):
				return
		def saveGearAsNew():
			save_or_overwrite_menu.grab_release()
			save_or_overwrite_menu.destroy()
			save_as_new_menu = Toplevel(root)
			save_as_new_menu.focus_force()
			save_as_new_menu.title("Save as New")
			ttk.Label(save_as_new_menu, text="What would you like to name the new file?", justify='center').grid(column=1, row=1, padx=20)
			filename_var = StringVar()
			filename_entry = ttk.Entry(save_as_new_menu, textvariable=filename_var, validate='key', validatecommand=filename_wrapper)
			filename_entry.grid(column=1, row=2)
			Button(save_as_new_menu, text="Save", command=lambda : saveGear(True, filename_var.get(), save_as_new_menu), font=('Fredoka SemiBold', 13)).grid(column=1, row=3, pady=[10, 20])
			
			positionWindowCenterOfRoot(save_as_new_menu, root)
			save_as_new_menu.transient(root)   # dialog window is related to main
			save_as_new_menu.wait_visibility() # can't grab until window appears, so we wait
			save_as_new_menu.focus_force()
			save_as_new_menu.grab_set()        # ensure all input goes to our window
			save_as_new_menu.wait_window()     # block until window is destroyed
		
		def overwriteGear():
			overwrite_menu = Toplevel(root)
			overwrite_menu.focus_force()
			overwrite_menu.title("Overwrite")

			ttk.Label(overwrite_menu, text="Select a file to overwrite.", justify='center').grid(column=1, row=1, padx=20)

			folder_list = os.walk(dir)

			for i in folder_list:
				#print(folder_list)
				#for sub_dir in main_dir:
				#print(main_dir)
				subfolders = [x[0] for x in folder_list]
				#print(subfolders)
				shape_displaynames = []
				shape_names = []
				shape_paths = []
				for i in subfolders:
					#print(i[2:])
					if not os.path.isfile(os.path.join(i, "cs-1.shape")):
						continue
					with open(os.path.join(i, "propstub")) as propstub:
						try:
							shapename = json.load(propstub)['m_DisplayNamLocID']
						except:
							#print("\n ## Error reading custom shape's name, repairing.")
							shapename = i[2:]
							with open(os.path.join(i, "propstub"), "w") as propstub_edit:
								json.dump({"$id": 0, "$type": "0|CustomShapesLibrarySlotProxy, Assembly-CSharp", "m_DisplayNamLocID": shapename, "m_IconFilename": "", "m_PrefabAddress": ""}, propstub_edit, indent = "")
						
						last_edited = time.localtime(os.path.getmtime(os.path.join(i, "cs-1.shape")))
						shape_display = f"{shapename} - Last edited {last_edited[1]}/{last_edited[2]}/{last_edited[0]}, {datetime.datetime.strptime(f"{last_edited[3]}:{last_edited[4]}:{last_edited[5]}", "%H:%M:%S").strftime("%I:%M:%S %p")}"
						shape_displaynames.append(shape_display)
						shape_names.append(shapename)
						shape_paths.append(i)
					#print(f"{shapename} - Last edited {last_edited[1]}/{last_edited[2]}/{last_edited[0]}, {datetime.datetime.strptime(f"{last_edited[3]}:{last_edited[4]}:{last_edited[5]}", "%H:%M:%S").strftime("%I:%M:%S %p")}")
				#print(shape_paths)
			if not shape_names:
				messagebox.showerror(message="No saved custom shapes exist. Please save as new.", title="Error")
				overwrite_menu.destroy()
				return
			else:
				save_or_overwrite_menu.grab_release()
				save_or_overwrite_menu.destroy()

			file_list = StringVar(value=shape_names)
			filename_var = StringVar()
			filename_entry = Listbox(overwrite_menu, listvariable=file_list, height=min(10, len(shape_names)))
			filename_entry.grid(column=1, row=2)

			scrollbar = ttk.Scrollbar(overwrite_menu, orient=VERTICAL) 
			scrollbar.grid(column=1, row=2, sticky=(E, N, S))
			
			filename_entry.configure(yscrollcommand=scrollbar.set)
			scrollbar.configure(command=filename_entry.yview)

			Button(overwrite_menu, text="Save", command=lambda : saveGear(False, filename_var.get(), overwrite_menu, shape_names[filename_entry.curselection()[0]], shape_paths[filename_entry.curselection()[0]]), font=('Fredoka SemiBold', 13)).grid(column=1, row=3, pady=[10, 20])
			
			positionWindowCenterOfRoot(overwrite_menu, root)
			overwrite_menu.transient(root)   # dialog window is related to main
			overwrite_menu.wait_visibility() # can't grab until window appears, so we wait
			overwrite_menu.focus_force()
			overwrite_menu.grab_set()        # ensure all input goes to our window
			overwrite_menu.wait_window()     # block until window is destroyed

		save_or_overwrite_menu = Toplevel(root)
		save_or_overwrite_menu.title("Save as New or Overwrite?")

		ttk.Label(save_or_overwrite_menu, text="Would you like to save this gear to a new file,\nor overwrite an existing one?", justify='center').grid(column=1, row=1, columnspan=2, padx=20)
		Button(save_or_overwrite_menu, text="Save as New (needs game restart)", command=saveGearAsNew, font=('Fredoka SemiBold', 13)).grid(column=1, row=2, pady=[10, 20])
		Button(save_or_overwrite_menu, text="Overwrite", command=overwriteGear, font=('Fredoka SemiBold', 13)).grid(column=2, row=2, pady=[10, 20])
		
		#print([math.floor(center_x - (save_or_overwrite_menu.winfo_width() / 2)), math.floor(center_y - (save_or_overwrite_menu.winfo_height() / 2))])
		positionWindowCenterOfRoot(save_or_overwrite_menu, root)
		#save_or_overwrite_menu.protocol("WM_DELETE_WINDOW", saveGearAsNew) # intercept close button
		save_or_overwrite_menu.transient(root)   # dialog window is related to main
		save_or_overwrite_menu.wait_visibility() # can't grab until window appears, so we wait
		save_or_overwrite_menu.focus_force()
		save_or_overwrite_menu.grab_set()        # ensure all input goes to our window
		save_or_overwrite_menu.wait_window()     # block until window is destroyed
		
def saveGear(save_as_new, filename, popup_to_kill, filename_to_overwrite, filepath_to_overwrite):
	if save_as_new:
		filename = filename.rstrip()
		filepath = os.path.join(dir, filename)
		print([filename, filepath])
		if not os.path.exists(filepath):
			os.makedirs(filepath)
			with open(os.path.join(filepath, 'cs-1.shape'), 'w') as shape:
				converted_points = ''
				point_num = 0
				for i in gear_vertices:
					if point_num == 0:
						converted_points += '\n\t\t\t{\n\t\t\t\t"$type": "5|UnityEngine.Vector2, UnityEngine.CoreModule",\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
					else:
						converted_points += ',\n\t\t\t{\n\t\t\t\t"$type": 5,\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
					point_num += 1
				if generated_gear_type in [5, 6]:
					shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(gear_vertices)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
				else:
					shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(gear_vertices)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 1,\n\t\t"$rcontent": [\n\t\t\t{\n\t\t\t\t"$type": 1,\n\t\t\t\t0,\n\t\t\t\t0,\n\t\t\t\t-2\n\t\t\t}\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
				shape.write(shape_data)
			with open(os.path.join(filepath, 'propstub'), 'w') as propstub:
				json.dump({"$id": 0, "$type": "0|CustomShapesLibrarySlotProxy, Assembly-CSharp", "m_DisplayNamLocID": filename, "m_IconFilename": "", "m_PrefabAddress": ""}, propstub, indent = "")
			messagebox.showinfo(message=f"Shape saved as {filename}.")
			popup_to_kill.grab_release()
			popup_to_kill.destroy()
			root.focus_force()
		else:
			messagebox.showwarning(message="Error: a folder with this name already exists. Please try a different name.", icon='error')
	else:
		filepath = filepath_to_overwrite
		with open(os.path.join(filepath, 'cs-1.shape'), 'w') as shape:
			converted_points = ''
			point_num = 0
			for i in gear_vertices:
				if point_num == 0:
					converted_points += '\n\t\t\t{\n\t\t\t\t"$type": "5|UnityEngine.Vector2, UnityEngine.CoreModule",\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
				else:
					converted_points += ',\n\t\t\t{\n\t\t\t\t"$type": 5,\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
				point_num += 1
			if generated_gear_type in [5, 6]:
				shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(gear_vertices)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
			else:
				shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(gear_vertices)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 1,\n\t\t"$rcontent": [\n\t\t\t{\n\t\t\t\t"$type": 1,\n\t\t\t\t0,\n\t\t\t\t0,\n\t\t\t\t-2\n\t\t\t}\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
			shape.write(shape_data)
		messagebox.showinfo(message=f"\"{filename_to_overwrite}\" saved.")
		popup_to_kill.grab_release()
		popup_to_kill.destroy()
		root.focus_force()

def positionWindowCenterOfRoot(new_window, root_window):
	x = root_window.winfo_x()
	y = root_window.winfo_y()
	width = root_window.winfo_width()
	height = root_window.winfo_height()
	center_x = x + width // 2
	center_y = y + height // 2
	#print([center_x, center_y])
	new_window.update()
	new_window.geometry(f"+{math.floor(center_x - (new_window.winfo_width() / 2))}+{math.floor(center_y - (new_window.winfo_height() / 2))}")

#def find_nth(s, x, n):
#	i = -1
#	for _ in range(n):
#		i = s.find(x, i + len(x))
#		if i == -1:
#			break
#	return i

if __name__ == '__main__':
	if not textmode:
	
		#debugtext = StringVar()
		min_teeth = IntVar(value=4)
		teeth_text = StringVar(value="Number of Teeth (min 4)")
		alert = PhotoImage(file=alert_image)
		check_y = PhotoImage(file=check_y)
		check_n = PhotoImage(file=check_n)

		#shiftdown = BooleanVar(value=False)
		#ctrldown = BooleanVar(value=False)

		#root.option_add('*TCombobox*Listbox.font', ('Fredoka SemiBold', 15))
		#root.option_add('*TLabel*Listbox.font', ('Fredoka SemiBold', 15))
		root.option_add("*Font", ('Fredoka SemiBold', 13))
		#root.option_add('*TButton.font', ('Fredoka SemiBold', 15))

		mainframe = ttk.Frame(root, padding="12 12 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.bind('<Button-1>', clickedOff)
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		root.iconbitmap(icon)
		
		tooltip = Pmw.Balloon(mainframe)

		generate_with_value_change_var = BooleanVar(value=False)
		generate_with_value_change_entry = Checkbutton(mainframe, text="Re-generate gear every time a value is changed", variable=generate_with_value_change_var, onvalue=True, offvalue=False)
		generate_with_value_change_entry.grid(column=1, row=12, sticky=(W, S))

		if dir:
			display_dir = dir
		else:
			display_dir = "Filepath could not be found automatically for your OS. Please set it manually."

		filepath_var = StringVar(value=display_dir)
		filepath_select = Button(mainframe, text="Select Custom Shape Folder (hover for filepath)", font=('Fredoka SemiBold', 11), command=chooseFilepath)
		filepath_select.grid(column=1, row=1, sticky=(W))
		tooltip.bind(filepath_select, filepath_var.get())

		#filepath_label = ttk.Label(mainframe, textvariable=filepath_var, font=('Fredoka SemiBold', 10))
		#filepath_label.grid(column=1, row=1, sticky=(W), padx=[173, 0])

		gear_type_label = ttk.Label(mainframe, text='Gear Type')
		gear_type_label.grid(column=2, row=1, sticky=(E), padx=5)

		gear_type_var = StringVar()
		gear_type_var.trace_add("write", updateGear)
		gear_type_picker = ttk.Combobox(mainframe, width=24, textvariable=gear_type_var)
		gear_type_picker['values'] = ('Triangular Tooth Spur Gear', 'Trapezoidal Tooth Spur Gear', 'Triangular Tooth Ring Gear', 'Trapezoidal Tooth Ring Gear', 'Triangular Tooth Rack Gear', 'Trapezoidal Tooth Rack Gear')
		gear_type_picker.state(['readonly'])
		gear_type_picker.grid(column=3, row=1, columnspan=2, sticky=(W, E))
		gear_type_picker.set('Triangular Tooth Spur Gear')
		gear_type_picker.bind('<<ComboboxSelected>>', updateGearType)
		#debugtext.set(gear_type_picker.current(newindex=None))

		reference_gear_label = ttk.Label(mainframe, text="-------- Reference Gear: --------")
		
		num_teeth_label = ttk.Label(mainframe, text="Number of Teeth (min 4)")
		num_teeth_label.grid(column=2, row=2, columnspan=2, sticky=(E), padx=5)

		num_teeth_var = IntVar(value=8)
		num_teeth_var.trace_add("write", updateGear)
		num_teeth_entry = ttk.Spinbox(mainframe, width=7, from_=4, to=9999, textvariable=num_teeth_var, validate='key', validatecommand=teeth_wrapper)
		num_teeth_entry.grid(column=4, row=2, sticky=(W, E))
		num_teeth_entry.bind("<Return>", lambda event, widget=num_teeth_entry, name="teeth": fixFormatting(widget, name))
		num_teeth_entry.bind("<FocusOut>", lambda event, widget=num_teeth_entry, name="teeth": fixFormatting(widget, name))
		
		gear_radius_label = ttk.Label(mainframe, text='Gear Radius')
		gear_radius_label.grid(column=2, row=3, columnspan=2, sticky=(E), padx=5)

		gear_radius_var = DoubleVar(value=1.5)
		gear_radius_var.trace_add("write", updateGear)
		gear_radius_entry = ttk.Spinbox(mainframe, width=7, from_=0.1, to=9999, increment=0.1, textvariable=gear_radius_var, validate='key', validatecommand=radius_wrapper)
		gear_radius_entry.grid(column=4, row=3, sticky=(W, E))
		gear_radius_entry.bind("<Return>", lambda event, widget=gear_radius_entry, name="radius": fixFormatting(widget, name))
		gear_radius_entry.bind("<Return>", checkConflicts, add="+")
		gear_radius_entry.bind("<FocusOut>", lambda event, widget=gear_radius_entry, name="radius": fixFormatting(widget, name))
		gear_radius_entry.bind("<FocusOut>", checkConflicts, add="+")
		
		tooth_height_label = ttk.Label(mainframe, text='Tooth Height')
		tooth_height_label.grid(column=2, row=4, columnspan=2, sticky=(E), padx=5)

		tooth_height_var = DoubleVar(value=0.5)
		tooth_height_var.trace_add("write", updateGear)
		tooth_height_entry = ttk.Spinbox(mainframe, width=7, from_=0.1, to=9999, increment=0.1, textvariable=tooth_height_var, validate='key', validatecommand=radius_wrapper)
		tooth_height_entry.grid(column=4, row=4, sticky=(W, E))
		tooth_height_entry.bind("<Return>", lambda event, widget=tooth_height_entry, name="height": fixFormatting(widget, name))
		tooth_height_entry.bind("<Return>", checkConflicts, add="+")
		tooth_height_entry.bind("<FocusOut>", lambda event, widget=tooth_height_entry, name="height": fixFormatting(widget, name))
		tooth_height_entry.bind("<FocusOut>", checkConflicts, add="+")

		tooth_height_alert = ttk.Label(mainframe, image="")
		tooth_height_alert.grid(column=4, row=4, sticky=(E))

		tooltip.bind(tooth_height_alert, "Tooth height is too high, keep tooth height less than double the radius.")

		rack_gear_label = ttk.Label(mainframe, text="-------- Rack Gear: --------")
		
		outer_radius_label = ttk.Label(mainframe, text='Outer Radius')
		outer_radius_label.grid(column=2, row=5, columnspan=2, sticky=(E), padx=5)

		outer_radius_var = DoubleVar(value=2)
		outer_radius_var.trace_add("write", updateGear)
		outer_radius_entry = ttk.Spinbox(mainframe, width=7, from_=0, to=9999, increment=0.01, textvariable=outer_radius_var, validate='key', validatecommand=radius_wrapper)
		outer_radius_entry.bind("<Return>", lambda event, widget=outer_radius_entry, name="outer_radius": fixFormatting(widget, name))
		outer_radius_entry.bind("<Return>", checkConflicts, add="+")
		outer_radius_entry.bind("<FocusOut>", lambda event, widget=outer_radius_entry, name="outer_radius": fixFormatting(widget, name))
		outer_radius_entry.bind("<FocusOut>", checkConflicts, add="+")

		outer_radius_alert = ttk.Label(mainframe, image="")
		outer_radius_alert.grid(column=4, row=5, sticky=(E))
		
		tooltip.bind(outer_radius_alert, "Outer radius is too small, must be at least the gear radius plus half the tooth height.")
		
		#editable_label = ttk.Label(mainframe, text='Editable')
		#editable_label.grid(column=2, row=6, sticky=(E))

		editable_var = BooleanVar(value=False)
		editable_var.trace_add("write", updateGear)
		editable_entry = Checkbutton(mainframe, text="Make gear editable?", variable=editable_var, onvalue=True, offvalue=False)
		editable_entry.grid(column=3, row=6, columnspan=2, sticky=(W, E))
		
		true_num_teeth_label = ttk.Label(mainframe, text="Number of Teeth (min 2)")

		true_num_teeth_var = IntVar(value=8)
		true_num_teeth_var.trace_add("write", updateGear)
		true_num_teeth_entry = ttk.Spinbox(mainframe, width=7, from_=4, to=9999, textvariable=true_num_teeth_var, validate='key', validatecommand=teeth_wrapper)
		true_num_teeth_entry.bind("<Return>", lambda event, widget=true_num_teeth_entry, name="true_teeth": fixFormatting(widget, name))
		true_num_teeth_entry.bind("<FocusOut>", lambda event, widget=true_num_teeth_entry, name="true_teeth": fixFormatting(widget, name))
		
		clearance_label = ttk.Label(mainframe, text='Clearance')
		clearance_label.grid(column=2, row=7, columnspan=2, sticky=(E), padx=5)

		clearance_var = DoubleVar(value=0)
		clearance_var.trace_add("write", updateGear)
		clearance_entry = ttk.Spinbox(mainframe, width=7, from_=0, to=9999, increment=0.01, textvariable=clearance_var, validate='key', validatecommand=radius_wrapper)
		clearance_entry.grid(column=4, row=7, sticky=(W, E))
		clearance_entry.bind("<Return>", lambda event, widget=clearance_entry, name="clearance": fixFormatting(widget, name))
		clearance_entry.bind("<Return>", checkConflicts, add="+")
		clearance_entry.bind("<FocusOut>", lambda event, widget=clearance_entry, name="clearance": fixFormatting(widget, name))
		clearance_entry.bind("<FocusOut>", checkConflicts, add="+")

		clearance_alert = ttk.Label(mainframe, image="")
		clearance_alert.grid(column=4, row=7, sticky=(E))
		
		tooltip.bind(clearance_alert, "Clearance is too high, must not be greater than the tooth height.")

		generate = Button(mainframe, text="Generate", font=('Fredoka SemiBold', 13), command=generateGear)
		generate.grid(column=4, row=12, sticky=(E), padx=[0, 60])

		save = Button(mainframe, text="Save", font=('Fredoka SemiBold', 13), command=newOrOverwrite)
		save.grid(column=4, row=12, sticky=(E))

		display = Canvas(mainframe, width=400, height=400, background='#36638a')
		display.grid(column=1, row=2, columnspan=1, rowspan=10, sticky=(N, W))

		stylized_var = BooleanVar(value=True)
		#stylized_entry = Checkbutton(display, variable=stylized_var, onvalue=True, offvalue=False)

		stylized_entry = display.create_image(10, 394, image=check_y, anchor='sw')
		stylized_entry_label = display.create_text(30, 396, text="Stylize", anchor='sw', font=('Fredoka SemiBold', 13), fill='white')
		display.tag_bind(stylized_entry, "<Button-1>", lambda e: toggleStyle(stylized_entry))
		display.tag_bind(stylized_entry_label, "<Button-1>", lambda e: toggleStyle(stylized_entry))

		#stylized_entry_window = display.create_window(0, 400, anchor=S+W, window=stylized_entry)
		#stylized_entry.grid(column=1, row=10, sticky=(W, S))

		#ttk.Label(mainframe, textvariable=debugtext).grid(column=2, row=4, sticky=(W))
		#ttk.Label(mainframe, textvariable=gear_type_var).grid(column=2, row=5, sticky=(W))

		setValuesNormal()

		root.focus_force()
		root.mainloop()
	else: 
		if os_has_filepath:
			print("Gear generator by Masonator")
			print(f"PB3 custom shapes folder located at {dir}")
			while True:
				print("\nSelect a gear type using the corresponding number.")
				for i in range(0, len(gear_type_options)):
					print(gear_type_options[i])

				while True:
					gear_type = input("\nGear type: ")
					if gear_type.isdigit() and int(gear_type) in range(1, len(gear_type_options)+1):
						gear_type = int(gear_type)
						if gear_type in [5, 6]:
							print("\nTo generate a rack gear, you will have to create a reference gear. Input the values of the reference gear here:\n")
						break
					else:
						print("\n ## Invalid selection, please try again.")

				while True:
					num_teeth = input("(Reference gear) Number of teeth: " if gear_type in [5, 6] else "Number of teeth: ")
					if num_teeth.isdigit() and int(num_teeth) >= 4:
						num_teeth = int(num_teeth)
						if (gear_type == 1 and num_teeth > 50) or (gear_type == 2 and num_teeth > 25) or (gear_type == 3 and num_teeth > 41) or (gear_type == 4 and num_teeth > 20): 
							if verifyVerticesAbove100():
								break
						else:
							break
					else:
						if num_teeth.isdigit():
							print("\n ## Invalid input, number of teeth must be at least 4.")
						else:
							print("\n ## Invalid input, must be an integer (whole number).")
						
				while True:
					inner_size = input("(Reference gear) Gear radius (aka pitch circle radius): " if gear_type in [5, 6] else "Gear radius (aka pitch circle radius): ")
					if is_number(inner_size) and float(inner_size) > 0:
						inner_size = float(inner_size)
						break
					else:
						if is_number(inner_size):
							print("\n ## Invalid input, gear radius must be greater than 0.")
						else:
							print("\n ## Invalid input, must be a number.")
						
				while True:
					tooth_height = input("(Reference gear) Tooth height: " if gear_type in [5, 6] else "Tooth height: ")
					if is_number(tooth_height) and float(tooth_height) > 0:
						tooth_height = float(tooth_height)/2
						break
					else:
						if is_number(tooth_height):
							print("\n ## Invalid input, tooth height must be greater than 0.")
						else:
							print("\n ## Invalid input, must be a number.")

				if gear_type in [5, 6]:
					print("\nReference gear done. These next few parameters will directly control the resulting rack gear.\n")

					while True:
						true_num_teeth = input("Number of teeth: ")
						if true_num_teeth.isdigit() and int(true_num_teeth) >= 2:
							true_num_teeth = int(true_num_teeth)
							if (gear_type == 5 and true_num_teeth > 49) or (gear_type == 6 and true_num_teeth > 24): 
								if verifyVerticesAbove100():
									break
							else:
								break
						else:
							if true_num_teeth.isdigit():
								print("\n ## Invalid input, number of teeth must be at least 2.")
							else:
								print("\n ## Invalid input, must be an integer (whole number).")

				if gear_type in [3, 4]:
					while True:
						outer_radius = input("Outer radius of ring: ")
						if is_number(outer_radius) and float(outer_radius) > inner_size + tooth_height:
							outer_radius = float(outer_radius)
							break
						else:
							if is_number(outer_radius):
								print(f"\n ## Invalid input, tooth height must be greater than the gear radius plus half the tooth height ({inner_size + tooth_height}m).")
							else:
								print("\n ## Invalid input, must be a number.")
					
					print("Make gear editable? (This will make the seam in the ring wide enough to be visible) (Y/N)")
					while True:
						editable = input(">").lower()
						if editable in ['y', 'n']:
							if editable == 'y': print("Gear will be editable.")
							else: print("Seam hidden.")
							editable = (editable == 'y')
							break

						
				while True:
					clearance = input("Clearance (the teeth will be shortened by this amount in meters to prevent locking up): ")
					if is_number(clearance) and float(clearance) >= 0:
						clearance = float(clearance)
						break
					else:
						if is_number(clearance):
							print("\n ## Invalid input, clearance must be at least 0.")
						else:
							print("\n ## Invalid input, must be a number.")

				if gear_type == 1:
					points = []
					max_vertices = (num_teeth * 2)
					for i in range(0, max_vertices):
						r = inner_size - tooth_height
						if i%2 == 0: r += tooth_height*2 - clearance
						#print(math.pow(-1 ,i))
						points.append([r * math.cos(math.radians(i * (360 / max_vertices))), r * math.sin(math.radians(i * (360 / max_vertices)))])
				elif gear_type == 2:
					points = []
					max_vertices = (num_teeth * 4)
					for i in range(0, max_vertices):
						r = inner_size - tooth_height
						if i%4 < 2: r += tooth_height*2 - clearance
						points.append([r * math.cos(math.radians((i-0.5) * (360 / max_vertices))), r * math.sin(math.radians((i-0.5) * (360 / max_vertices)))])
				elif gear_type == 3:
					points = []
					max_vertices = (num_teeth * 2)
					for i in range(0, max_vertices):
						r = inner_size - tooth_height + clearance
						if i%2 == 0: r += tooth_height*2
						points.append([r * math.cos(math.radians(i * (360 / max_vertices))), r * math.sin(math.radians(i * (360 / max_vertices)))])
					if editable:
						points.append([r + tooth_height*2, -0.025])
					else:
						points.append([r + tooth_height*2, -0.00001])
					for i in range(0, 16):
						r2 = outer_radius
						points.append([r2 * math.cos(-math.radians(i * (360 / 16))), r2 * math.sin(-math.radians(i * (360 / 16)))])
					if editable:
						points.append([r2, 0.025])
					else:
						points.append([r2, 0.00001])
				elif gear_type == 4:
					points = []
					max_vertices = (num_teeth * 4)
					for i in range(0, max_vertices):
						r = inner_size - tooth_height + clearance
						if i%4 < 2: r += tooth_height*2
						points.append([r * math.cos(math.radians((i-0.5) * (360 / max_vertices))), r * math.sin(math.radians((i-0.5) * (360 / max_vertices)))])
					if editable:
						points.append([(r + tooth_height*2) * math.cos(math.radians(-0.55 * (360 / max_vertices))), (r + tooth_height*2) * math.sin(math.radians(-0.55 * (360 / max_vertices))) -0.0001])
					else:
						points.append([(r + tooth_height*2) * math.cos(math.radians(-0.5 * (360 / max_vertices))), (r + tooth_height*2) * math.sin(math.radians(-0.5 * (360 / max_vertices))) -0.0001])
					for i in range(0, 16):
						r2 = outer_radius
						points.append([r2 * math.cos(-math.radians(i * (360 / 16))), r2 * math.sin(-math.radians(i * (360 / 16)))])
					if editable:
						points.append([r2 * math.cos(math.radians(0.05 * (360 / max_vertices))), r2 * math.sin(math.radians(0.05 * (360 / max_vertices)))])
					else:
						points.append([r2, 0.0001])
				elif gear_type == 5:
					inner_size *= 1000000
					num_teeth *= 1000000
					points = []
					max_vertices = (num_teeth * 2)
					for i in range(0, true_num_teeth * 2):
						r = inner_size - tooth_height
						if i%2 == 0: r += tooth_height*2 - clearance
						points.append([r * math.cos(math.radians(i * (360 / max_vertices) + 90)), (r * math.sin(math.radians((i-0.5) * (360 / max_vertices) + 90)) - (inner_size - tooth_height*2))])
					points.append([r * math.cos(math.radians(i * (360 / max_vertices) + 90)), -0.5])
					points.append([0, -0.5])
				elif gear_type == 6:
					inner_size *= 1000000
					num_teeth *= 1000000
					points = []
					max_vertices = (num_teeth * 4)
					for i in range(-1, true_num_teeth * 4 - 1):
						r = inner_size - tooth_height
						if i%4 < 2: r += tooth_height*2 - clearance
						if i%4 == 1: i -= 0.075
						if i%4 == 2: i -= 0.075
						if i%4 == 3: i += 0.075
						if i%4 == 0: i += 0.075
						points.append([r * math.cos(math.radians((i-0.5) * (360 / max_vertices) + 90)), (r * math.sin(math.radians((i-0.5) * (360 / max_vertices) + 90)) - (inner_size - tooth_height*2))])
					points.append([r * math.cos(math.radians((i-0.5) * (360 / max_vertices) + 90)), -0.5])
					points.append([r * math.cos(math.radians(-1.45 * (360 / max_vertices) + 90)), -0.5])


				#print('\n'.join(map(str, points)))
						
				print("\nGear generation done! Would you like to save it as a new custom shape (requires game reopen) or overwrite an existing shape?\n")
				while True:
					save_as_new = input("New or Overwrite? ").lower()
					if save_as_new in ['new', 'overwrite']:
						save_as_new = (save_as_new == 'new')
						#print(save_as_new)
						break
					else:
						print("\n ## Invalid input, please respond with 'New' or 'Overwrite'.")

				while True:
					print("\n")
					if save_as_new:
						filename = sanitize_filename(input("What would you like to name the shape? "))
						filepath = os.path.join(dir,filename)
						#print(filename)
						#print(filepath)
						if not os.path.exists(filepath):
							os.makedirs(filepath)
							with open(os.path.join(filepath, 'cs-1.shape'), 'w') as shape:
								converted_points = ''
								point_num = 0
								for i in points:
									if point_num == 0:
										converted_points += '\n\t\t\t{\n\t\t\t\t"$type": "5|UnityEngine.Vector2, UnityEngine.CoreModule",\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
									else:
										converted_points += ',\n\t\t\t{\n\t\t\t\t"$type": 5,\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
									point_num += 1
								if gear_type in [5, 6]:
									shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(points)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
								else:
									shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(points)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 1,\n\t\t"$rcontent": [\n\t\t\t{\n\t\t\t\t"$type": 1,\n\t\t\t\t0,\n\t\t\t\t0,\n\t\t\t\t-2\n\t\t\t}\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
								shape.write(shape_data)
							with open(os.path.join(filepath, 'propstub'), 'w') as propstub:
								json.dump({"$id": 0, "$type": "0|CustomShapesLibrarySlotProxy, Assembly-CSharp", "m_DisplayNamLocID": filename, "m_IconFilename": "", "m_PrefabAddress": ""}, propstub, indent = "")
							print("File saved.")
							break
						else:
							print("\n ## Error: a folder with this name already exists. Please try a different name.")
					else:
						folder_list = os.walk(dir)

						for i in folder_list:
							#print(folder_list)
							#for sub_dir in main_dir:
							#print(main_dir)
							subfolders = [x[0] for x in folder_list]
							#print(subfolders)
							shape_names = []
							shape_paths = {}
							for i in subfolders:
								#print(i[2:])
								if not os.path.isfile(os.path.join(i, "cs-1.shape")):
									continue
								with open(os.path.join(i, "propstub")) as propstub:
									try:
										shapename = json.load(propstub)['m_DisplayNamLocID']
									except:
										print("\n ## Error reading custom shape's name, repairing.")
										shapename = i[2:]
										with open(os.path.join(i, "propstub"), "w") as propstub_edit:
											json.dump({"$id": 0, "$type": "0|CustomShapesLibrarySlotProxy, Assembly-CSharp", "m_DisplayNamLocID": shapename, "m_IconFilename": "", "m_PrefabAddress": ""}, propstub_edit, indent = "")
									shape_names.append(shapename)
									shape_paths.update([(shapename, i)])
								last_edited = time.localtime(os.path.getmtime(os.path.join(i, "cs-1.shape")))
								print(f"{shapename} - Last edited {last_edited[1]}/{last_edited[2]}/{last_edited[0]}, {datetime.datetime.strptime(f"{last_edited[3]}:{last_edited[4]}:{last_edited[5]}", "%H:%M:%S").strftime("%I:%M:%S %p")}")
							#print(shape_paths)
						if not shape_names:
							print("No saved custom shapes found. Saving as new instead.")
							save_as_new = True
							continue

						while True:
							file_to_overwrite = input("\nWhich file would you like to overwrite? ")
							if file_to_overwrite in shape_names:
								filepath = shape_paths[file_to_overwrite]
								with open(os.path.join(filepath, 'cs-1.shape'), 'w') as shape:
									converted_points = ''
									point_num = 0
									for i in points:
										if point_num == 0:
											converted_points += '\n\t\t\t{\n\t\t\t\t"$type": "5|UnityEngine.Vector2, UnityEngine.CoreModule",\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
										else:
											converted_points += ',\n\t\t\t{\n\t\t\t\t"$type": 5,\n\t\t\t\t' + str(i[0]) + ',\n\t\t\t\t' + str(i[1]) + '\n\t\t\t}'
										point_num += 1
									if gear_type in [5, 6]:
										shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(points)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
									else:
										shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": true,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(points)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 1,\n\t\t"$rcontent": [\n\t\t\t{\n\t\t\t\t"$type": 1,\n\t\t\t\t0,\n\t\t\t\t0,\n\t\t\t\t-2\n\t\t\t}\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
									shape.write(shape_data)
								with open(os.path.join(filepath, 'propstub'), 'w') as propstub:
									json.dump({"$id": 0, "$type": "0|CustomShapesLibrarySlotProxy, Assembly-CSharp", "m_DisplayNamLocID": file_to_overwrite, "m_IconFilename": "", "m_PrefabAddress": ""}, propstub, indent = "")
								print("File overwritten.")
								break
							else:
								print("\n ## Error: File does not exist. Please try again.")
						break

				print("\nType 'new' to generate a new gear, or type 'exit' to close this program.")
				while True:
					continue_program = input(">").lower()
					if continue_program in ['new', 'exit']:
						continue_program = (continue_program == 'new')
						if not continue_program:
							quit()
						break
		else:
			print("You are using an OS that doesn't have its custom shape folder filepath set up in this program, which it needs in order to know where to read/write from.\nPlease let @Masonator on Discord know about this, and ideally provide the filepath.")
			input = input("Press Enter to close this program. ")
			quit()

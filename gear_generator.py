import math
import json
import os
import platform
import time
import datetime
import pathlib
from pathvalidate import sanitize_filename

if platform.system() == "Windows":
	dir = os.path.join(pathlib.Path.home(), "AppData", "LocalLow", "Dry Cactus", "Poly Bridge 3", "CustomShapeLibrary")
	os_has_filepath = True
else:
	os_has_filepath = False

gear_type_options = ['1: Triangle Tooth Spur Gear',
					'2: Trapezoidal Tooth Spur Gear',
					'3: Triangle Tooth Ring Gear',
					'4: Trapezoidal Tooth Ring Gear'
					]
def verifyVerticesAbove100():
	print("Warning, the number of vertices that will be generated for this gear exceeds the max amount of manually editable vertices (100), continue anyways? (Y/N)")
	while True:
		y_n = input(">").lower()
		if y_n in ['y', 'n']:
			if y_n == 'y': print("Continuing anyways.")
			return y_n == 'y'
		
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

if __name__ == '__main__':
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
					break
				else:
					print("\n ## Invalid selection, please try again.")

			while True:
				num_teeth = input("Number of teeth: ")
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
				inner_size = input("Gear radius (aka pitch circle radius): ")
				if is_number(inner_size) and float(inner_size) > 0:
					inner_size = float(inner_size)
					break
				else:
					if is_number(inner_size):
						print("\n ## Invalid input, gear radius must be greater than 0.")
					else:
						print("\n ## Invalid input, must be a number.")
					
			while True:
				tooth_height = input("Tooth height: ")
				if is_number(tooth_height) and float(tooth_height) > 0:
					tooth_height = float(tooth_height)/2
					break
				else:
					if is_number(tooth_height):
						print("\n ## Invalid input, tooth height must be greater than 0.")
					else:
						print("\n ## Invalid input, must be a number.")

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
							shape_data = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": false,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(points)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 1,\n\t\t"$rcontent": [\n\t\t\t{\n\t\t\t\t"$type": 1,\n\t\t\t\t0,\n\t\t\t\t0,\n\t\t\t\t-2\n\t\t\t}\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
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
								shape_data =  '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": false,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": ' + str(len(points)) + ',\n\t\t"$rcontent": [' + converted_points + '\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 1,\n\t\t"$rcontent": [\n\t\t\t{\n\t\t\t\t"$type": 1,\n\t\t\t\t0,\n\t\t\t\t0,\n\t\t\t\t-2\n\t\t\t}\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": ""\n}'
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

#file_template = '{\n\t"$id": 0,\n\t"$type": "0|CustomShapeProxy, Assembly-CSharp",\n\t"m_Version": 1,\n\t"m_Pos": {\n\t\t"$type": "1|UnityEngine.Vector3, UnityEngine.CoreModule",\n\t\t-29.25,\n\t\t16.75,\n\t\t0\n\t},\n\t"m_Rot": {\n\t\t"$type": "2|UnityEngine.Quaternion, UnityEngine.CoreModule",\n\t\t0,\n\t\t0,\n\t\t0,\n\t\t1\n\t},\n\t"m_Scale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_MeshScale": {\n\t\t"$type": 1,\n\t\t1,\n\t\t1,\n\t\t1\n\t},\n\t"m_CollidesWithRoad": false,\n\t"m_CollidesWithNodes": false,\n\t"m_CollidesWithRamps": false,\n\t"m_CollidesWithVehicles": true,\n\t"m_CollidesWithSplitNodes": false,\n\t"m_Flipped": false,\n\t"m_LowFriction": false,\n\t"m_RotationDegrees": 0,\n\t"m_Mass": 40,\n\t"m_Bounciness": 0.5,\n\t"m_PinMotorStrength": 0,\n\t"m_PinTargetVelocity": 0,\n\t"m_PinTargetAcceleration": 0,\n\t"m_Thickness": 4,\n\t"m_Color": {\n\t\t"$type": "3|UnityEngine.Color, UnityEngine.CoreModule",\n\t\t0,\n\t\t1,\n\t\t1,\n\t\t0\n\t},\n\t"m_PointsLocalSpace": {\n\t\t"$id": 1,\n\t\t"$type": "4|System.Collections.Generic.List`1[[UnityEngine.Vector2, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 4,\n\t\t"$rcontent": [\n\t\t\t{\n\t\t\t\t"$type": "5|UnityEngine.Vector2, UnityEngine.CoreModule",\n\t\t\t\t-1,\n\t\t\t\t1\n\t\t\t},\n\t\t\t{\n\t\t\t\t"$type": 5,\n\t\t\t\t-1,\n\t\t\t\t-1\n\t\t\t},\n\t\t\t{\n\t\t\t\t"$type": 5,\n\t\t\t\t1,\n\t\t\t\t-1\n\t\t\t},\n\t\t\t{\n\t\t\t\t"$type": 5,\n\t\t\t\t1,\n\t\t\t\t1\n\t\t\t}\n\t\t]\n\t},\n\t"m_StaticPins": {\n\t\t"$id": 2,\n\t\t"$type": "6|System.Collections.Generic.List`1[[UnityEngine.Vector3, UnityEngine.CoreModule]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchors": {\n\t\t"$id": 3,\n\t\t"$type": 6,\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_DynamicAnchorGuids": {\n\t\t"$id": 4,\n\t\t"$type": "7|System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib",\n\t\t"$rlength": 0,\n\t\t"$rcontent": [\n\t\t]\n\t},\n\t"m_TextureId": "",\n\t"m_TextureTiling": 10,\n\t"m_Behavior": 0,\n\t"m_MeshId": "AUTOGEN",\n\t"m_MeshLocalPos": {\n\t\t"$type": 1,\n\t\t0,\n\t\t0,\n\t\t-2\n\t},\n\t"m_UndoGuid": "20lerZ86v0CtO06uBO97gw"\n}'
		

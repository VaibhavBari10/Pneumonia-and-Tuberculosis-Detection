import os

def print_tree(startpath , max_depth=2):
	with open("folder_structure.txt" ,"w") as f:
		for root , dirs, files in os.walk(startpath): 
			depth= root.replace(startpath , '' ).count(os.sep) 
			if depth < max_depth :
				indent = ' ' * 4 * depth
				f.write(f"{indent}{os.path.basename(root)}/\n")
				subindent = ' ' * 4 *(depth + 1)
				for file in files:
					f.write(f"{subindent}{file}\n")
print_tree('.',max_depth = 2)

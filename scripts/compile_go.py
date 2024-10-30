import os
import json
import shutil
from subprocess import PIPE,run
import sys

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go","build"]

def make_json_meta_data(path,game_dir):
	data = {
	"gameNames": game_dir,
	"numberOfFiles": len(game_dir)
	}

	with open(path,"w") as f:
		json.dump(data,f)

def compileGameCode(path):
	code_file_name = None
	for root,dirs,files in os.walk(path):
		for file in files:
			if file.endswith(GAME_CODE_EXTENSION):
				code_file_name = file
				break
		break
	if code_file_name is None:
		return
	command = GAME_COMPILE_COMMAND 
	print(command)
	run_command(command,path)

def run_command(command,path):
	cwd = os.getcwd()
	os.chdir(path)
	result = run(command,stdout=PIPE, stdin=PIPE,universal_newlines=True)
	print("compile result",result)
	os.chdir(cwd)
def find_all_game_paths(source):
	game_paths = []
	for root,dirs,files in os.walk(source):
		print(root)
		print(dirs)
		print(files)
		for directory in dirs:
			if GAME_DIR_PATTERN in directory.lower():
				path = os.path.join(source,directory)
				game_paths.append(path)

		break
	return game_paths

def copy_and_overwrite(source,dest):
	if os.path.exists(dest):
		shutil.rmtree(dest)
	shutil.copytree(source,dest)

def get_name_from_paths(paths,to_strip):
	new_names = []
	for path in paths:
		_,dir_name = os.path.split(path)
		new_dir_name = dir_name.replace(to_strip,"")
		new_names.append(new_dir_name)
	return new_names
def create_dir(path):
	if not os.path.exists(path):
		os.mkdir(path)

def main(source,target):
	cwd = os.getcwd()
	source_path = os.path.join(cwd,source)
	target_path = os.path.join(cwd,target)
#	print(source_path)
#	print(target_path)
	game_paths = find_all_game_paths(source_path)
	game_names = get_name_from_paths(game_paths,"game")
#	print(game_names)	
#	print(game_paths)
	create_dir(target_path)
	for src,dest in zip(game_paths, game_names):
		dest_path = os.path.join(target_path,dest)
		copy_and_overwrite(src,dest_path)
		compileGameCode(dest_path)
	json_path = os.path.join(target_path,"metadata.json")
	make_json_meta_data(json_path,game_paths)	

	



if __name__ == "__main__":
	args = sys.argv
	print(args)
	if len(args) != 3:
		raise Exception("You must pass a source and target dir")

	source,target = args[1:]
	main(source,target)


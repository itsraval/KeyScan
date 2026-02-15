from utils import *
import sys
from colorama import Fore, Back, Style, init

def main():
	if len(sys.argv) == 1:
		print("Error! No input path found...")
		return
	else:
		matching_files = []
		for path in sys.argv[1:]:
			files, unscanned_folders = getFilesContent(path)
			print("=============INFO=============")
			print(f"Files found: {len(files)}")
			print(f"Folders not scanned: {len(unscanned_folders)}")
			for unscanned_folder in unscanned_folders:
				print(f"\t-{unscanned_folder}")

			print("\n===========SCANNING===========")
			if files != None:
				for index, file in enumerate(files, start=1):
					print(f"{file['path']}\t-\t{index}/{len(files)}")
					file = scanFile(file)
					if file['scanned']:
						matching_files.append(file)
		print("\n===========RESULTS============")
		for i, file in enumerate(matching_files, start=1):
			if file['regex_matches_found'] == [] and file['tag_matches_found'] == []:
				print(f"No matches found for: {file['path']}")
			else:
				print(Fore.CYAN + f"Matches found for: {file['path']}")
				print(Fore.CYAN + f"FILENAME: {file['name']}")
				printMatches(file)

			if i != len(matching_files):
				print("\n------------------")

if __name__ == '__main__':
	main()

from utils import *
import sys

def main():
	# maybe add from github or gitlab...
	...
	
	if len(sys.argv) == 1:
		print("Error! No input path found...")
		return
	else:
		matchesFiles = []
		for path in sys.argv[1:]:
			files, notScannedFolders = getFilesContent(path)
			print(f"Files found: {len(files)}")
			print(f"Folders not scanned: {len(notScannedFolders)}")
			print(f"\t{notScannedFolders}")

			print("\n===========SCANNING===========")
			if files != None:
				for index, f in enumerate(files, start=1):
					print(f"{f['path']}\t-\t{index}/{len(files)}")
					f = scanFile(f)
					if f['found_matches']:
						matchesFiles.append(f)
		print("\n\n==============================")
		print("Scan Completed!")
		print("==============================")
		for f in matchesFiles:
			print(f"Match found in: {f['path']}")
			print(f"File: {f['name']}")
			for m in f['matches']:
				print(f"At line: {m[0]}")
				for mr in m[1]:
					print(f"\tRegex found:\t{mr['match_type']} - {mr['match']}")
				for mt in m[2]:
					print(f"\tTag found:\t{mt['match']}")
			print("=====")

if __name__ == '__main__':
	main()
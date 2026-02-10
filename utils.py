import re
import json
from pathlib import Path


with open('config.json', 'r') as f:
	config = json.load(f)

raw_tags = config.get("assign_after_operators", [])
raw_ignore_folders  = config.get("ignore_folders", [])
IGNORE_FOLDERS = {folder.strip("/\\").lower() for folder in raw_ignore_folders}
IGNORE_FILES = config.get("ignore_files", [])
IGNORE_EXTENSIONS = config.get("ignore_extensions", [])

CHECK_REGEXP = config.get("check_regex", [])
CHECK_TAGS = config.get("check_tags", [])
ASSIGN_BEFORE_OPERATORS = config.get("assign_before_operators", [])
ASSIGN_AFTER_OPERATORS = [t.lower() for t in raw_tags]
POSSIBLE_QUOTES = config.get("possible_quotes", [])

def readFile(path):
	try:
		content = path.read_text(encoding="utf-8")
	except Exception as e:
		content = ""
		print(e)
	return {"path":path, "folder":path.parent, "name":path.name, "extention":path.suffix, "content":content}

def ignoreFolder(path):
	for part in path.parts:
		if part.lower() in IGNORE_FOLDERS:
			return True
	return False

def getFilesContent(path):
	fileContents = []
	notScannedFolders = []
	p = Path(path)

	if p.is_file():
		fileContents.append(readFile(p))
	elif p.is_dir():
		if not ignoreFolder(p):
			for f in p.iterdir():
				x,y = getFilesContent(f)
				fileContents.extend(x)
				notScannedFolders.extend(y)
		else:
			notScannedFolders.append(str(p))

	else:
		print("Error! Path incorrect...")
		return None
	return fileContents, notScannedFolders


def scanFile(file):
	if file['content'] == "":
		file['scanned'] = False
		return file
	else:
		if file['name'] in IGNORE_FILES or file['extention'] in IGNORE_EXTENSIONS:
			file['scanned'] = False
			return file
		ln = 1
		lines = file['content'].split('\n')
		matches = []
		for line in lines:
			print(f'Line: {ln}/{len(lines)}', end='\r')
			matchesR, matchesT = scanLine(line, ln)
			if matchesR != [] or matchesT != []:
				matches.append((ln, matchesR, matchesT))
			ln += 1
		file['scanned'] = True
		if matches != []:
			file['found_matches'] = True
		else:
			file['found_matches'] = False
		file['matches'] = matches
	return file

def scanReg(text, lineNumer):
	matches = []
	for r in CHECK_REGEXP:
		match = re.search(r['reg'], text)
		if match != None:
			if match.group()[0]*len(match.group()) != match.group():
				matches.append({"line": lineNumer, "match_type": r['name'], "match": match.group()})
	return matches

def scanTags(text, lineNumer):
	text = text.lower()
	matches = []
	for tag in CHECK_TAGS:
		for b in ASSIGN_BEFORE_OPERATORS:
			match = re.search(f'{b}\\s*{tag}', text)
			if match != None:
				matches.append({"line": lineNumer, "match_type": f'{b}\\s*{tag}', 'match_tag': tag, "match": match.group()})
		for a in ASSIGN_AFTER_OPERATORS:
			for q in POSSIBLE_QUOTES:
				match = re.search(f'{tag}\\s*{a}\\s*{q}', text)
				if match != None:
					matches.append({"line": lineNumer, "match_type": f'{tag}\\s*{a}\\s*{q}', 'match_tag': tag, "match": match.group()})
	return matches

def scanLine(text, lineNumer):
	matchesR = scanReg(text, lineNumer)
	matchesT = scanTags(text, lineNumer)
	found = False
	for match in matchesR:
		if not found:
			print()
			found = True
		print(f'\t{match}')
	for match in matchesT:
		if not found:
			print()
			found = True
		print(f'\t{match}')
	return (matchesR, matchesT)



# Check if it contains a tag
# Check if it contains a valid assignment operator
# Check if a quoted value exists
# Extract the value
# Run heuristics (length, entropy)
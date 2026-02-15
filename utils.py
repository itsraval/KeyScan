import re
import json
from pathlib import Path
from colorama import Fore,	 init
from collections import Counter, defaultdict

with open('config.json', 'r') as f:
	config = json.load(f)

init(autoreset=True)

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

before_operator_regex = f'(?:{"|".join(ASSIGN_BEFORE_OPERATORS)})'
after_operator_regex = f'(?:{"|".join(ASSIGN_AFTER_OPERATORS)})'
quote_regex = f'(?:{"|".join(POSSIBLE_QUOTES)})'

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
	file_contents = []
	unscanned_folders = []
	p = Path(path)

	if p.is_file():
		file_contents.append(readFile(p))
	elif p.is_dir():
		if not ignoreFolder(p):
			for f in p.iterdir():
				fc,usf = getFilesContent(f)
				file_contents.extend(fc)
				unscanned_folders.extend(usf)
		else:
			unscanned_folders.append(str(p))
	else:
		print("Error! Path incorrect...")
		return None
	return file_contents, unscanned_folders

def printMatches(file):
	matches = sorted(file['regex_matches_found'] + file['tag_matches_found'], key=lambda x: x['line'])

	for index, match in enumerate(matches):
		if index != 0:
			if match['line'] != matches[index-1]['line']:
				print(Fore.YELLOW + f"\n  Line: {match['line']}")
		else:
			print(Fore.YELLOW + f"  Line: {match['line']}")
 
		if len(match['match_type']) < 30:
			print(Fore.MAGENTA + f"     Regex: {match['match_type']}")
		print(Fore.GREEN + f"     Matched:", end=" ")
		print(Fore.RED + f"{match['match']}")
		print(f"     Text: {match['full_string']}")
		if index < len(matches)-1:
			print(f"\t-------")
	return

def scanFile(file):
	if file['content'] == "":
		file['scanned'] = False
		return file
	else:
		if file['name'] in IGNORE_FILES or file['extention'] in IGNORE_EXTENSIONS:
			file['scanned'] = False
			return file

		file['scanned'] = True
		regex_matches_found = scanReg(file['content'])
		regex_matches_found = sorted(regex_matches_found, key=lambda x: x['line'])

		tag_matches_found = scanTags(file['content'])		
		tag_matches_found = sorted(tag_matches_found, key=lambda x: x['line'])

		file['regex_matches_found'] = regex_matches_found
		file['tag_matches_found'] = tag_matches_found
	return file

def appendMatch(regex_name, matches, lines):
	found_matches = []
	if matches != []:
		counts = Counter(matches)
		matches = list(counts.keys())

		for match in matches:
			for line_number, line in enumerate(lines, start=1):
				if match in line:
					found_matches.append({"line": line_number, "match_type": regex_name, "match": match, "full_string": line})
					counts[match] -= 1
				if counts[match] == 0:
					break
	return found_matches


def filterGenericAPI(found_matches):
	line_groups = defaultdict(list)
	for match in found_matches:
		line_groups[match['line']].append(match)

	filtered_matches = []

	for matches in line_groups.values():
		if len(matches) > 1:
			non_generic = [match for match in matches if match['match_type'] != 'Generic API']
			filtered_matches.extend(non_generic if non_generic else matches)
		else:
			filtered_matches.extend(matches)
	return filtered_matches

def scanReg(content):
	lines = content.split('\n')
	found_matches = []

	for regex in CHECK_REGEXP:
		matches = re.findall(regex['reg'], content)
		found_matches.extend(appendMatch(regex['name'], matches, lines))
	found_matches = filterGenericAPI(found_matches)
	return found_matches

def scanTags(content):
	lines = content.split('\n')
	found_matches = []

	for tag in CHECK_TAGS:
		tag_regex = f'{before_operator_regex}\\s*{tag}'
		matches = re.findall(tag_regex, content, re.IGNORECASE)
		found_matches.extend(appendMatch(tag_regex, matches, lines))

		tag_regex = f'{tag}\\s*{after_operator_regex}\\s*{quote_regex}'
		matches = re.findall(tag_regex, content, re.IGNORECASE)
		found_matches.extend(appendMatch(tag_regex, matches, lines))	
	return found_matches
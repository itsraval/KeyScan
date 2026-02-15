# 🔐 KeyScan

KeyScan is a lightweight Python tool that scans files and folders for **potentially sensitive information** such as API keys, secrets, tokens, passwords, and credentials that should **not** be uploaded to public repositories.

It is designed as a **pre-upload / pre-commit safety check** to help you avoid accidental secret leaks on GitHub, GitLab, or anywhere else online.

---

## ✨ Features

* 📂 Recursively scans files and directories
* 🚫 Skips common build, dependency, and virtual environment folders
* 🔎 Detects secrets using:

  * Regular expressions (AWS keys, GitHub tokens, OpenAI keys, Stripe keys, JWTs, etc.)
  * Heuristic tag-based detection (`password`, `api_key`, `secret`, etc.)
* ⚙️ Fully configurable via `config.json`
* 🧠 Language-agnostic (works on any text-based file)

---

## 📦 Project Structure

```text
.
├── KeyScan.py      # Main entry point
├── utils.py        # Scanning logic and helpers
├── config.json     # Rules, regexes, ignore lists
└── README.md
```

---

## 🚀 Usage

### Requirements

* Python **3.8+**
* No external dependencies (standard library only 🎉)

### Run a scan

```bash
python KeyScan.py <path1> <path2> ...
```

Examples:

```bash
# Scan a single file
python KeyScan.py app.py

# Scan a directory recursively
python KeyScan.py ./my_project

# Scan multiple paths
python KeyScan.py backend frontend .env
```

---

## 🖨️ Output

During scanning, KeyScan will:

* Print progress per file
* List folders that were skipped
* Report any detected matches with:

  * File path
  * Line number
  * Match type (regex or tag)
  * The matched value

Example output:

```text
=============INFO=============
Files found: 3
Folders not scanned: 0

===========SCANNING===========
C:\test\index.php   -       1/3
C:\test\main.rs     -       2/3
C:\test\script.py   -       3/3

===========RESULTS============
Matches found for: C:\test\script.py
FILENAME: script.py
  Line: 5
     Regex: Stripe API Token sk
     Matched: sk_live_51NQpQwH8xYF3mZ7d9QkL2A6
     Text: API_TOKEN = "sk_live_51NQpQwH8xYF3mZ7d9QkL2A6bEJpR0s"
        -------
     Matched: TOKEN = "
     Text: API_TOKEN = "sk_live_51NQpQwH8xYF3mZ7d9QkL2A6bEJpR0s"
        -------

  Line: 18
     Matched: #define pass
     Text: #define pass 1234
        -------

  Line: 30
     Regex: Stripe API Token sk
     Matched: sk_live_51NQpQwH8xYF3mZ7d9QkL2A6
     Text: quis nostrud exercitation sk_live_51NQpQwH8xYF3mZ7d9QkL2A6bEJpR0s ullamco laboris nisi ut aliquip ex ea commodo

------------------
=====
```

---

## ⚙️ Configuration (`config.json`)

All detection logic is driven by `config.json`.

### Ignore rules

* `ignore_folders` – folders that will not be scanned
* `ignore_files` – specific files to skip
* `ignore_extensions` – binary or irrelevant file types

### Secret detection

* `check_regex` – list of named regular expressions
* `check_tags` – keywords like `password`, `token`, `secret`
* `assign_before_operators` / `assign_after_operators` – assignment patterns
* `possible_quotes` – supported quoting styles

You can easily extend or tune the rules without touching the Python code.

---

## ⚠️ Disclaimer

KeyScan is a **best-effort detection tool**.

* It may produce **false positives**
* It may **miss obfuscated or encrypted secrets**

Always review results manually and rotate any exposed credentials immediately.

---

## 🤝 Contributing

Contributions are welcome!

* Add new regex patterns
* Improve heuristics
* Refactor performance
* Improve documentation

Feel free to open an issue or submit a PR.

---

## 📜 License

MIT License — do whatever you want, just don’t leak secrets 😉

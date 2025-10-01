# Zenpo

A simple, interactive sorta control panel? idk use it for school hehe

---

## Features

### Run

```bash
zenpo
```

Displays:

- **ASCII Banner:** `a00137`
- **Creator:** Zenpo
- **GitHub Repo:** https://github.com/ZC-RS/zenpo
- **Version:** 1.0.0
- **Help text:**
  - `-p` → Show panel with apps to open
  - `zenpo` → Show this text

**Colors:**

- Banner: **Green**
- Creator/GitHub: **Green**
- Version: **Dark Blue**
- Help section: **Bright**

---

### 2. Panel Mode

Run:

```bash
zenpo -p
```


- **ASCII Banner:** `PANEL` in green  
- **Description:** “A general control panel for apps” (light blue)  
- **Interactive menu:** Press keys to launch apps

**Hotkeys & Functions:**

| Key | Action | Notes |
|-----|--------|------|
| X   | Exit the panel | Quit panel |
| T   | Open Task Manager | `taskmgr` |
| C   | Open CMD | Opens Command Prompt |
| P   | Open PowerShell | `powershell` |
| Q   | Open Control Panel | `control` |
| N   | Open Notepad | `notepad` |
| B   | Open default Browser | `start ""` (shell=True) |
| E   | Open Explorer | `explorer` |
| M   | Open Microsoft Store | `start ms-windows-store:` (shell=True) |
| S   | Open Settings | `start ms-settings:` (shell=True) |
| H   | Open Hosts file in Notepad | `C:\Windows\System32\drivers\etc\hosts` |
| L   | Lock Workstation | `rundll32.exe user32.dll,LockWorkStation` |
| R   | Run custom script | `C:\path\to\yourscript.bat` |

- Hotkeys are **green**, descriptions in default or light blue.
- The panel automatically displays all available hotkeys.

---

### 3. Additional Features

- Editable install (`pip install -e .`) – changes are live immediately
- Easily extendable: add new hotkeys by updating the `hotkeys` dictionary
- Subprocess handling: opens apps, runs scripts, executes commands

---

## Installation

```bash
git clone https://github.com/ZC-RS/zenpo.git
cd zenpo
pip install -e .
```
<img width="413" height="316" alt="image" src="https://github.com/user-attachments/assets/9f292d64-950c-479a-a0a9-150c389eb55e" />

| When run 'zenpo' in terminal


<img width="1699" height="102" alt="image" src="https://github.com/user-attachments/assets/c6b497bd-6d5a-401d-9b87-85716142f2e5" />



<img width="339" height="497" alt="image" src="https://github.com/user-attachments/assets/3680e0d8-451a-4881-b296-26eaf72fc1e5" />

| When run 'zenpo -p' in terminal - panel


> ⚠️ Make sure your Python Scripts directory is in your PATH to use `zenpo` globally:
>
> ```
> C:\Users\YourUser\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts
> ```

---

## Usage

```bash
# Show info
zenpo

# Open interactive panel
zenpo -p
```


## License
MIT License

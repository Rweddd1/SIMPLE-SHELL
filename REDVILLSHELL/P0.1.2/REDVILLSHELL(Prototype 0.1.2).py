import os
import shutil
import sys
import ctypes
import time
import datetime
import pathlib
import pandas as pd ####
import csv as cs ####
import sklearn ####
import matplotlib####

#------- infos and stuff
version = '0.1.2'

Build_in_commands = ['info', 'sysinfo', 'version', 'calculator', 'time', 'open', 'crate', 'delete',
                  'rename', 'copy', 'Fcreate' 'change', 'check', 'say']

def cmd_info():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Information
    ────────────────────────────────────────────
    Creator                              | Villena, Red L.
    Creation Timeline                    | 10/29/25 - 10/30/25
    Version                              | Prototype 0.1.2
Version Date                         | 10/31/25####
    
    ────────────────────────────────────────────
    Notes by me:
      >> THIS IS THE SECOND UPDATE YEYEEYGHDSGFH
      now dinagdagan ko ng administration privilage
      toh so wala lang mas madami ka pwedeng gawin and
      stuff like deleting some stuff so more freedom 
      heheh
    ────────────────────────────────────────────
          ''')
    
def Version():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Version
    ────────────────────────────────────────────
    >> 10/30/25 - Prototype 0.1.2 - Python 
    - admin command
    - administration access 
    - head and tail for view file             
    ''')

def help():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Information
    ────────────────────────────────────────────
    exit               | exit help
    1                  | Build in command          
    2                  | File type
    3                  | Boolean
    4                  | Command example
    clear              | clear
    
    ────────────────────────────────────────────
          ''')
    global Build_in_commands
    while True:
        try:
            cmd = input("help/REDVILLSHELL >> ").strip()
            if cmd == 'exit':
                return 0
            elif cmd == 'clear':
                clear_screen()
            elif cmd == Build_in_commands:
                print(f"ERROR: {cmd}. Type 'exit' to do commands")
            elif cmd == '1':
                build_in_command()
            elif cmd == '2':
                File_type()
            elif cmd == '3':
                Boolean()
            elif cmd == '4':
                Command_example()
            else:
                print(f'Unknown command: {cmd}. r u stupid or something')
        except Exception as e:
            print(f'ERROR {e}')
        except ValueError:
            print("Integers only")
            
def build_in_command():
     print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Built in Command List
    ────────────────────────────────────────────
    info                                 | Red's Information
    version                              | Version's info
    sysinfo                              | Show the every info possible ###
    caclculator <T/F>                    | Calculator mode ####
    time                                 | show time
    open <filename> or <path/file>       | Open a file
    create <filename>                    | Create a new file
    delete <filename> or <path/file>     | Delete a file
    rename <oldname> / <newname>         | Rename a file
    copy <path/filename> / <newpath>     | Move file #####
    change <path>                        | Change directory
    check                                | List files in current directory
    clear                                | Clear the screen
    sysinfo                              | Show your system####
    say >"word">                         | print your word####
    exit                                 | Exit REDVILLSHELL
    help                                 | Show this help message
    ---------------------------future update hehe-----------------------
    head <filename> ---| extra open      | view the first 10 line
    tail <filename> ---| args            | view the last 10 line
    Finfo <filename> or <path/filename>  | file info
    Ffind <filename> or <path/filename>  | lahat ng file with the key######
    Kfind <filename> <line>              | Find where the keyword is

    ────────────────────────────────────────────''')
     
def File_type():
     print('''
    ────────────────────────────────────────────
               REDVILLSHELL — File Type######
    ────────────────────────────────────────────
    F+                                    | file
    F++                                   | folder
    +f++                                  | Whole folder
    py                                    | Python File
    cpp                                   | Cpp file
    c                                     | C file
    ────────────────────────────────────────────''')
     
def Boolean():
     print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Booelan/Others
    ────────────────────────────────────────────
    Y                                    | Yes
    N                                    | No
    T                                    | True      
    F                                    | False  
    ────────────────────────────────────────────''')
     
def Command_example():
     print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Example commands
    ────────────────────────────────────────────
     Example Commands:
      >> open f+ notes.txt 
      >> create f+ test.txt 
      >> rename f+ test.txt / final.txt
      >> delete f+ folder/data.csv 
      >> delete f++ Redred #delete folder
      >> cd Documents
      >> admin T  -   #Administration enable 
    ────────────────────────────────────────────''')
#-----------admin launch 
def is_elevated():#check if 'NOW' is admin or nah
    if os.name != 'nt':
        return True
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def relaunch_as_admin():#UAC prompt
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        return True
    except Exception:
        return False
    
#-----------admin
admin_mode = False

def admin_privilage():#Windows
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

process_elevated = admin_privilage()

def admin(Boolean):#admin main
    global admin_mode
    s = str(Boolean).strip().upper()
    
    if s in ['T', 'Y', 'TRUE', 'YES']:
        if is_elevated():
            admin_mode = True
            print("ADMINISTRATION TRUE — Already running with elevated privileges.")
        else:
            print("Requesting admin privilege (UAC prompt)...")
            success = relaunch_as_admin()
            if success:
                print("Launching REDVILLSHELL as administrator...")
                sys.exit(0)
            else:
                print("ERROR! Failed to request administrator privilege.")
    elif s in ['F', 'N', 'FALSE', 'NO']:
        admin_mode = False
        print("ADMINISTRATION FALSE")
    else:
        print(f"ERROR: '{Boolean}' is not recognized. Use 'T' or 'F'")
        
#----------built in function-------------------
def open_file(filename):#open
    try:
        if os.path.exists(filename):
            os.startfile(filename)
            print(f"Opened '{filename}'.")
        else:
            print(f"ERROR File '{filename}' not found.")
    except PermissionError:
        print("ACCESS DENIED! Enable the 'admin' command")
    except OSError as e:
        print(f'ERROR: {e}')

def create_item(command):#create <c> <file>
    """Create files or folders based on data type notation"""
    try:
        parts = command.strip().split(None, 1)
        if len(parts) < 2:
            print("ERROR: Use format 'create <type> <name>'")
            print("Types: F+ (file), F++ (folder), py, cpp, c, txt")
            return
        
        item_type = parts[0].strip().lower()
        name = parts[1].strip()
        
        file_extensions = {
            'py': '.py',
            'cpp': '.cpp',
            'c': '.c',
        }
        
        if item_type in file_extensions:
        
            if not name.endswith(file_extensions[item_type]):
                name += file_extensions[item_type]
            with open(name, 'w') as file:
                pass
            print(f"SUCCESS! Created {item_type.upper()} file '{name}'.")

        elif item_type == 'f+':#file
            with open(name, 'w') as file:
                pass
            print(f"SUCCESS! Created file '{name}'.")
        elif item_type == 'f++':#folder
            os.makedirs(name, exist_ok=True)
            print(f"SUCCESS! Created folder '{name}'.")
        else:
            print(f"ERROR: Unknown type '{item_type}'.")
            print("Valid types: F+, F++, py, cpp, c, txt")
    except PermissionError:
        print("ACCESS DENIED! Enable the 'admin' command")
    except Exception as e:
        print(f"ERROR: Creation failed: {e}")

#----- 

def delete_item(command):
    """Delete files or folders based on data type notation"""
    try:
        parts = command.strip().split(None, 1)
        if len(parts) < 2:
            print("ERROR: Use format 'delete <type> <name>'")
            print("Types: F+ (file), F++ (empty folder), +f++ (folder with contents)")
            return
        
        item_type = parts[0].strip().lower()
        name = parts[1].strip()
        
        if not os.path.exists(name):
            print(f"ERROR: '{name}' not found.")
            return
        
        if item_type == 'f+': #file
            if not os.path.isfile(name):
                print(f"ERROR: '{name}' is not a file. Use 'F++' or '+f++' for folders.")
                return
            try:
                os.remove(name)
                print(f"SUCCESS! Deleted file '{name}'.")
            except PermissionError:
                if admin_mode:
                    pathlib.Path(name).unlink()
                    print(f"SUCCESS! Deleted file '{name}' with admin privileges.")
                else:
                    print("ACCESS DENIED! Enable the 'admin' command to 'T'")
                    
        elif item_type == 'f++':#empty folder
            if not os.path.isdir(name):
                print(f"ERROR: '{name}' is not a folder. Use 'F+' for files.")
                return
            try:
                os.rmdir(name)
                print(f"SUCCESS! Deleted empty folder '{name}'.")
            except OSError:
                print(f"ERROR: Folder '{name}' is not empty. Use 'delete +f++' to delete with contents.")
            except PermissionError:
                print("ACCESS DENIED! Enable the 'admin' command to 'T'")
                
        elif item_type == '+f++':#folder with content
            if not os.path.isdir(name):
                print(f"ERROR: '{name}' is not a folder. Use 'F+' for files.")
                return
            try:
                shutil.rmtree(name)
                print(f"SUCCESS! Deleted folder '{name}' and all its contents.")
            except PermissionError:
                print("ACCESS DENIED! Enable the 'admin' command to 'T'")
        else:
            print(f"ERROR: Unknown type '{item_type}'.")
            print("Valid types: F+ (file), F++ (empty folder), +f++ (whole folder)")    
    except PermissionError:
        print("ACCESS DENIED! Enable the 'admin' command to 'T'")
    except Exception as e:
        print(f"ERROR: Deletion failed: {e}")

#--------

def rename_file(command):#rename 
    try:
        if '/' not in command:
            print("ERROR: Use format 'oldname / newname'")
            return
        old, new = command.split('/', 1)
        old, new = old.strip(), new.strip()
        if not os.path.exists(old):
            print(f"ERROR: '{old}' not found.")
            return
        os.rename(old, new)
        print(f"SUCCESS! Renamed '{old}' TO '{new}'.")
    except PermissionError:
        print("ACCESS DENIED! Enable the 'admin' command")
    except Exception as e:
        print(f"ERROR: Rename failed: {e}")

#------

def list_dir():
    try:
        print("\nCurrent directory:", os.getcwd())
        for item in os.listdir():
            if os.path.isdir(item):
                item_type = "[F++]"
            else:
                ext = os.path.splitext(item)[1].lower()
                type_map = {
                    '.py': '[PY]',
                    '.cpp': '[CPP]',
                    '.c': '[C]',
                }
                item_type = type_map.get(ext, '[F+]')
            print(f"    {item_type} {item}")
        print()
    except PermissionError:
        print("ACCESS DENIED! Enable the 'admin' command")
    except OSError:
        print("ERROR! Cannot view the current directory")
        
#-----

def change_dir(path):
    try:
        os.chdir(path)
        print(f"SUCCESS! Changed directory to '{path}'.")
    except PermissionError:
        print("ACCESS DENIED! Enable the 'admin' command")
    except Exception as e:
        print(f"ERROR: {e}")
        
#-----

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
#-----

def time(): 
    now = datetime.datetime.now()
    print(now)
    
def main():
    print("Welcome to REDVILLSHELL. Type 'help' for commands.")
    while True:
        try:
            cmd = input("red_pogi_cmdline >> ").strip()

            if not cmd:
                continue
            elif cmd == 'help':
                help()
            elif cmd.startswith('open '):
                open_file(cmd[5:].strip())
            elif cmd.startswith('create '):
                create_item(cmd[7:].strip())
            elif cmd.startswith('delete '):
                delete_item(cmd[7:].strip())
            elif cmd.startswith('rename '):
                rename_file(cmd[7:].strip())
            elif cmd.startswith('change '):
                change_dir(cmd[7:].strip())
            elif cmd.startswith('admin '):
                admin(cmd[6:].strip())
            elif cmd == 'check':
                list_dir()
            elif cmd == 'clear':
                clear_screen()
            elif cmd == 'exit':
                print("Goodbye, Pahinga na ako.")
                break
            elif cmd == 'info':
                cmd_info()
            elif cmd == 'version':
                Version()
            elif cmd == 'time':
                time()
            else:
                print(f"ERROR: Unknown command: '{cmd}'. Type 'help' for commands.")
        except KeyboardInterrupt:
            print("\nUse 'exit' to close REDVILLSHELL.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
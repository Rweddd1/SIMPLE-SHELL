import os
import shutil

def cmd_info():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Information
    ────────────────────────────────────────────
    Creator                              | Villena, Red L.
    Creation Timeline                    | 10/29/25 - 10/30/25
    Version                              | Prototype 0.1
    Version Date                         | 10/30/25
    
    ────────────────────────────────────────────
    Notes by me:
      >> HI! ginawa ko to kasi wala ako magawa at
      gusto ko talaga matuto ng file handling kaso
      sa python ko toh ginawa which is ang bagal!! 
      originally 200 lines toh pero naging 167 li
      -nes nalang kasi ang tagal magbukas nung 
      interpreter so yeah, in the future gagawa ako
      ng cpp version para mas mabilis and more
      built in function! Na enjoy ko naman yung 
      pagawa ko sa simple system na toh although
      prototype lang madami ako gusto gawin
    ────────────────────────────────────────────
          ''')
    
def Patch():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Patch
    ────────────────────────────────────────────
    >> 10/30/25 - Prototype 0.1 - Python
    -Creation REDVILLSHELL
    -open <filename> or <path/file>      
    -create <filename>                    
    -delete <filename> or <path/file>     
    -rename <oldname> / <newname>         
    -mkdir <foldername>                   
    -cd <path>                            
    -change                               
    -clear                                
    -exit                                 
    -help
    -patch
    -info                               
    ''')

def help():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Command List
    ────────────────────────────────────────────
    info                                 | Red's Information
    patch                                | Version patch
    open <filename> or <path/file>       | Open a file
    create <filename>                    | Create a new file
    delete <filename> or <path/file>     | Delete a file
    rename <oldname> / <newname>         | Rename a file
    mkdir <foldername>                   | Create a folder
    cd <path>                            | Change directory
    change                               | List files in current directory
    clear                                | Clear the screen
    exit                                 | Exit RedShell
    help                                 | Show this help message
    ────────────────────────────────────────────
    Example Commands:
      >> open notes.txt
      >> create test.txt
      >> rename test.txt / final.txt
      >> delete folder/data.csv
      >> cd Documents
    ────────────────────────────────────────────
    ''')

def open_file(filename):
    if os.path.exists(filename):
        os.startfile(filename)
        print(f"Opened '{filename}'.")
    else:
        print(f"ERROR File '{filename}' not found.")

def create_file(filename):
    with open(filename, 'w') as f:
        pass
    print(f"SUCCESS! Created file '{filename}'.")

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"SUCCESS! Deleted '{filename}'.")
    else:
        print(f"ERROR File '{filename}' not found.")

def rename_file(command):
    try:
        old, new = command.split('/')
        old, new = old.strip(), new.strip()
        os.rename(old, new)
        print(f"SUCCESS! Renamed '{old}' TO '{new}'.")
    except Exception as e:
        print(f"ERROR Rename failed: {e}")

def make_folder(foldername):
    os.makedirs(foldername, exist_ok=True)
    print(f"SUCCESS! Folder '{foldername}' created.")

def list_dir():
    print("\nCurrent directory:", os.getcwd())
    for item in os.listdir():
        print("   ", item)
    print()

def change_dir(path):
    try:
        os.chdir(path)
        print(f"SUCCESS! Changed directory to '{path}'.")
    except Exception as e:
        print(f"ERROR {e}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    

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
                create_file(cmd[7:].strip())
            elif cmd.startswith('delete '):
                delete_file(cmd[7:].strip())
            elif cmd.startswith('rename '):
                rename_file(cmd[7:].strip())
            elif cmd.startswith('mkdir '):
                make_folder(cmd[6:].strip())
            elif cmd.startswith('cd '):
                change_dir(cmd[3:].strip())
            elif cmd == 'change':
                list_dir()
            elif cmd == 'clear':
                clear_screen()
            elif cmd == 'exit':
                print("Goodbye, Pahinga na ako.")
                break
            elif cmd == 'info':
                cmd_info()
            elif cmd == 'patch':
                Patch()
            else:
                print(f"ERROR Unknown command: '{cmd}'. AYOD BOI!")
        except KeyboardInterrupt:
            print("Use 'exit' to close REDVILLSHELL.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
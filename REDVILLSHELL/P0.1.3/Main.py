import os
import sys
import tkinter as tk
from Utility import Admin, FileHandling, ReaderHandling, Timer, Network

#------- infos and stuff
version = '0.1.3'

def cmd_info():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Information
    ────────────────────────────────────────────
    Creator                              | Villena, Red L.
    Creation Timeline                    | 10/5/25 - 11/10/25
    Version                              | Prototype 0.1.3
    Version Date                         | 11/08/25
    
    ────────────────────────────────────────────
    Notes by me:
      >> Saya gawin kasi madami ako natutunan, 
      dati puro function nd call lang ngayon naka
      class architecture, and nagdagdag din ako 
      ng ibang commands for networks and stuff.
      next update ilalagay ko sa cyhton lahat
      para mas mabilis hehehe
    ────────────────────────────────────────────
    ''')

def Version():
    print(f'''
    ────────────────────────────────────────────
               REDVILLSHELL — Version {version}
    ────────────────────────────────────────────
    >> 11/08/25 - Prototype 0.1.3 - Python 
    - Class-based architecture
    - Separated utilities
    - Better admin handling
    - Improved file operations
    ────────────────────────────────────────────
    ''')

def help():
    print('''
    ────────────────────────────────────────────
               REDVILLSHELL — Command List
    ────────────────────────────────────────────
    GENERAL:
      info                   | Shell information
      version                | Version info
      help                   | Show this help
      clear                  | Clear screen
      exit                   | Exit shell
    
    ADMIN:
      admin <T/F>            | Enable/disable admin mode
      sysinfo                | Show system information
      hardware               | Show hardware information
      
    FILES:
      open <file>            | Open a file
      create <type> <name>   | Create file/folder
      delete <type> <name>   | Delete file/folder
      rename <old> / <new>   | Rename file
      check                  | List directory
      change <path>          | Change directory
      finfo <file>           | File information
    
    READER:
      read <file>            | Read file content
      find <file> <keyword>  | Find keyword in file
    
    TIME:
      time                   | Show current time
      timer <seconds>        | Start countdown timer
    
    NETWORK:
      ipconfig               | Show network info
      ssids                  | Show available ssids
    ────────────────────────────────────────────
    ''')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    admin = Admin()
    file_handler = FileHandling(admin)
    reader = ReaderHandling()
    timer = Timer()
    network = Network()
    
    print(f"Welcome to REDVILLSHELL v{version}. Type 'help' for commands.")
    
    while True:
        try:
            directory = os.getcwd().split(os.sep)[-1]
            prompt = f"{directory} >> "
            cmd = input(prompt).strip()
            
            if not cmd:
                continue
            
            parts = cmd.split(None, 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ''

            #basta info
            if command == 'help':
                help()
            elif command == 'info':
                cmd_info()
            elif command == 'version':
                Version()
            elif command == 'clear':
                clear_screen()
            elif command == 'exit':
                print("Goodbye! Pahinga na ako.")
                break
            
            #admin
            elif command == 'admin':
                admin.toggle_admin_mode(args)
            elif command == 'sysinfo':
                admin.get_system_info()
            elif command == 'hardware':
                admin.get_hardware_info()
            
            #file handling
            elif command == 'open':
                file_handler.open_file(args)
            elif command == 'create':
                file_handler.create_item(args)
            elif command == 'delete':
                file_handler.delete_item(args)
            elif command == 'rename':
                file_handler.rename_file(args)
            elif command == 'check':
                file_handler.list_dir()
            elif command == 'change':
                file_handler.change_dir(args)
            elif command == 'finfo':
                file_handler.file_info(args)
            
            #read
            elif command == 'read':
                reader.read_file(args)
            elif command == 'find':
                if ' ' in args:
                    filename, keyword = args.split(None, 1)
                    reader.find_in_file(filename, keyword)
                else:
                    print("ERROR: Use format 'find <file> <keyword>'")
            
            #time
            elif command == 'time':
                timer.show_current_time()
            elif command == 'timer':
                try:
                    seconds = int(args)
                    timer.start_timer(seconds)
                except ValueError:
                    print("ERROR: Timer needs a number (seconds)")
            
            #Network 
            elif command == 'ipconfig':
                network.show_ipconfig()
            elif command == 'ssids':
                network.ssids()
                 
            else:
                print(f"ERROR: Unknown command '{command}'. Type 'help' for commands.")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to close REDVILLSHELL.")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
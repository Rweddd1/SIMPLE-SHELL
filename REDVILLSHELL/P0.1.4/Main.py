import os
import re
import sys
import tkinter as tk
from tkinter import scrolledtext
from Utility import Admin, FileHandling, ReaderHandling, Timer, Network
from Arithmetic import Arithmetic

version = '0.1.4'

class RedvillShellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"REDVILLSHELL v{version}")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Redirect stdout to capture print statements
        sys.stdout = self
        
        # Initialize utility classes
        self.admin = Admin()
        self.file_handler = FileHandling(self.admin)
        self.reader = ReaderHandling()
        self.timer = Timer()
        self.network = Network()
        self.calc = Arithmetic()  
        
        # Command history
        self.history = []
        self.history_index = -1
        
        # Create output area (looks like CMD)
        self.output_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            bg='black',
            fg='#00FF00',  # Green text like CMD
            font=('Consolas', 10),
            insertbackground='#00FF00',
            selectbackground='#404040',
            selectforeground='#00FF00',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        #frame
        input_frame = tk.Frame(root, bg='black')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        #label
        self.prompt_label = tk.Label(
            input_frame,
            text=f"{os.getcwd().split(os.sep)[-1]} >> ",
            bg='black',
            fg='#00FF00',
            font=('Consolas', 10)
        )
        self.prompt_label.pack(side=tk.LEFT)
        
        # Input entry
        self.input_entry = tk.Entry(
            input_frame,
            bg='black',
            fg='#00FF00',
            font=('Consolas', 10),
            insertbackground='#00FF00',
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind('<Return>', self.process_command)
        self.input_entry.bind('<Up>', self.history_up)
        self.input_entry.bind('<Down>', self.history_down)
        self.input_entry.focus()
        
        #Welcome
        self.write_output(f"Welcome to REDVILLSHELL v{version}. Type 'help' for commands.\n")
    
    def write(self, text):#std.out write redirection
        if text.strip():  # Only write non-empty text
            self.write_output(text)
        return len(text)
    
    def flush(self):#stdout flash
        pass
    
    def write_output(self, text, color='#00FF00'):#ourput area
        self.output_area.config(state=tk.NORMAL)
        
        #tag color
        tag_name = f"color_{color}"
        self.output_area.tag_config(tag_name, foreground=color)
        
        self.output_area.insert(tk.END, text, tag_name)
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)
    
    def update_prompt(self):#directory
        directory = os.getcwd().split(os.sep)[-1]
        self.prompt_label.config(text=f"{directory} >> ")
    
    def history_up(self, event):#command history
        if self.history:
            if self.history_index == -1:
                self.history_index = len(self.history) - 1
            elif self.history_index > 0:
                self.history_index -= 1
            
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.history[self.history_index])
    
    def history_down(self, event):#navigation
        if self.history and self.history_index != -1:
            self.history_index += 1
            
            if self.history_index >= len(self.history):
                self.history_index = -1
                self.input_entry.delete(0, tk.END)
            else:
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, self.history[self.history_index])
    
    def process_command(self, event):#process
        cmd = self.input_entry.get().strip()
        
        if not cmd:
            return
        
        # Add to history
        self.history.append(cmd)
        self.history_index = -1
    
        directory = os.getcwd().split(os.sep)[-1]
        self.write_output(f"{directory} >> {cmd}\n", '#FFFFFF')#write input
        self.input_entry.delete(0, tk.END)#delete input
        self.execute_command(cmd)#execute(bale dito mga arguments and command)
        self.update_prompt()#update command
    
    def execute_command(self, cmd):
        parts = cmd.split(None, 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        
        try:
            #INFO
            if command == 'help':
                self.cmd_help()
            elif command == 'info':
                self.cmd_info()
            elif command == 'version':
                self.cmd_version()
            elif command == 'clear':
                self.clear_screen()
            elif command == 'exit':
                self.write_output("Goodbye! Pahinga na ako.\n")
                self.root.after(1000, self.root.quit)
            
            #ADMIN
            elif command == 'admin':
                self.admin.toggle_admin_mode(args)
            elif command == 'sysinfo':
                self.admin.get_system_info()
            elif command == 'hardware':
                self.admin.get_hardware_info()
            
            #FILE
            elif command == 'open':
                self.file_handler.open_file(args)
            elif command == 'create':
                self.file_handler.create_item(args)
            elif command == 'delete':
                self.file_handler.delete_item(args)
            elif command == 'rename':
                self.file_handler.rename_file(args)
            elif command == 'check':
                self.file_handler.list_dir()
            elif command == 'change':
                self.file_handler.change_dir(args)
            elif command == 'finfo':
                self.file_handler.file_info(args)
            
            #READ
            elif command == 'read':
                self.reader.read_file(args)
            elif command == 'find':
                if ' ' in args:
                    filename, keyword = args.split(None, 1)
                    self.reader.find_in_file(filename, keyword)
                else:
                    self.write_output("ERROR: Use format 'find <file> <keyword>'\n", '#FF0000')
            
            #TIME
            elif command == 'time':
                self.timer.show_current_time()
            elif command == 'timer':
                try:
                    seconds = int(args)
                    self.timer.start_timer(seconds)
                except ValueError:
                    self.write_output("ERROR: Timer needs a number (seconds)\n", '#FF0000')
            
            #NETWORK
            elif command == 'ipconfig':
                self.network.show_ipconfig()
            elif command == 'ssids':
                ssid_list = self.network.ssids()
                if ssid_list:
                    for i, ssid in enumerate(ssid_list, 1):
                        print(f"  {i}. {ssid}")
                else:
                    print("No Wi-Fi networks detected.")
            
            #HISTORY
            elif command == 'history':
                if self.history:
                    self.write_output("Command History:\n")
                    for i, h in enumerate(self.history[:-1], 1):  # Exclude current command
                        self.write_output(f"  {i}. {h}\n")
                else:
                    self.write_output("No command history yet.\n")
            
            #MATH
            elif command == 'calc':
                self.calc.calculate(args)
            elif command == 'add':
                self.calc.add(args)
            elif command == 'sub':
                self.calc.subtract(args)
            elif command == 'mul':
                self.calc.multiply(args)
            elif command == 'div':
                self.calc.divide(args)
            elif command == 'pow':
                self.calc.power(args)
            elif command == 'sqrt':
                self.calc.sqrt(args)
            elif command == 'mod':
                self.calc.mod(args)
            elif command == 'fact':
                self.calc.factorial(args)
            elif command == 'percent':
                self.calc.percentage(args)
            elif command == 'sin':
                self.calc.sin_calc(args)
            elif command == 'cos':
                self.calc.cos_calc(args)
            elif command == 'tan':
                self.calc.tan_calc(args)
            elif command == 'log':
                self.calc.log_calc(args)
            elif command == 'ln':
                self.calc.ln_calc(args)
            elif command == 'abs':
                self.calc.abs_calc(args)
            elif command == 'round':
                self.calc.round_calc(args)
            elif command == 'last':
                self.calc.last()
            elif command == 'mstore':
                self.calc.mem_store()
            elif command == 'mrecall':
                self.calc.mem_recall()
            elif command == 'mclear':
                self.calc.mem_clear()
            elif command == 'constants':
                self.calc.constants()
            
            else:
                if any(op in cmd for op in ['+', '-', '*', '/', '**', '%', '(', ')']):
                    if re.match(r'^[\d\+\-\*\/\%\(\)\.\s\*\*]+$', cmd):
                        self.calc.calculate(cmd)
                    else:
                        self.write_output(f"ERROR: Unknown command '{command}'. Type 'help' for commands.\n", '#FF0000')
                else:
                    self.write_output(f"ERROR: Unknown command '{command}'. Type 'help' for commands.\n", '#FF0000')
        
        except Exception as e:
            self.write_output(f"ERROR: {e}\n", '#FF0000')
    
    def clear_screen(self):#delete every ouput nyheheh
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state=tk.DISABLED)
    
    def cmd_help(self):
        help_text = '''────────────────────────────────────────────
           REDVILLSHELL — Command List
────────────────────────────────────────────
INFORMATION:
  info                   | Shell information
  version                | Version info
  help                   | Show this help
  clear                  | Clear screen
  exit                   | Exit shell
  
GENERAL:
  run <program>          | Run a program
  install <program>      | Install a program/library
  site <website>         | open a website
  setting                | Shell settings
  history                | Command History
  
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
  ping                   | Check your ping
  
MATH:
  calc <expression>      | Calculate expression (2+2*3)
  add <numbers>          | Add numbers
  sub <numbers>          | Subtract numbers
  mul <numbers>          | Multiply numbers
  div <numbers>          | Divide numbers
  pow <base> <exp>       | Power (2^8)
  sqrt <number>          | Square root
  mod <num> <div>        | Modulo operation
  fact <number>          | Factorial
  percent <p> <of>       | Percentage
  sin/cos/tan <angle>    | Trigonometry (degrees)
  log/ln <number>        | Logarithms
  abs <number>           | Absolute value
  round <num> <dec>      | Round number
  last                   | Show last result
  mstore/mrecall/mclear  | Memory operations
  constants              | Math constants
────────────────────────────────────────────
'''
        self.write_output(help_text)
    
    def cmd_info(self):
        info_text = '''────────────────────────────────────────────
           REDVILLSHELL — Information
────────────────────────────────────────────
Creator                              | Villena, Red L.
Creation Timeline                    | 10/5/25 - 11/10/25
Version                              | Prototype 0.1.4
Version Date                         | 11/12/25

────────────────────────────────────────────
Notes by me:
  >> Saya gawin kasi madami ako natutunan, 
  dati puro function nd call lang ngayon naka
  class architecture, and nagdagdag din ako 
  ng ibang commands for networks and stuff.
  next update ilalagay ko sa cyhton lahat
  para mas mabilis hehehe
────────────────────────────────────────────
'''
        self.write_output(info_text)
    
    def cmd_version(self):
        version_text = f'''────────────────────────────────────────────
           REDVILLSHELL — Version {version}
────────────────────────────────────────────
>> 11/12/25 - Prototype 0.1.4 - Python 
- Class-based architecture
- Separated utilities
- Better admin handling
- Improved file operations
- Added arithmetic operations
- Auto-calculate math expressions
- GUI with CMD styling
────────────────────────────────────────────
'''
        self.write_output(version_text)

def main():
    root = tk.Tk()
    app = RedvillShellGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()#nyehehehe
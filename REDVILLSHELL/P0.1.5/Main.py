import os
import re
import sys
import tkinter as tk
from tkinter import scrolledtext
from Utility import Admin, FileHandling, ReaderHandling, Timer, Network
from Arithmetic import Arithmetic

version = '0.1.5'

class RedvillShellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"REDVILLSHELL OS v{version}")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Settings storage
        self.current_settings = {
            'theme': 'matrix',
            'font_size': 10,
            'font_color': '#00FF00',
            'bg_color': 'black',
            'prompt_style': 'directory',
            'autocomplete': True,
            'history_enabled': True
        }
        
        # Redirect stdout to capture print statements
        sys.stdout = self
        
        #OOP NG MGA POGI
        self.admin = Admin()
        self.file_handler = FileHandling(self.admin)
        self.reader = ReaderHandling()
        self.timer = Timer()
        self.network = Network()
        self.calc = Arithmetic()  
        
        #history
        self.history = []
        self.history_index = -1
        
        # output area
        self.output_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            bg='black',
            fg='#00FF00',  
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
        
        #font label(yung sa una)
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
        if text.strip(): #non emp text
            self.write_output(text)
        return len(text)
    
    def flush(self):#stdout flash
        pass
    
    def write_output(self, text, color=None):#ourput area
        if color is None:
            color = self.current_settings['font_color']
            
        self.output_area.config(state=tk.NORMAL)
        
        #tag color
        tag_name = f"color_{color}"
        self.output_area.tag_config(tag_name, foreground=color)
        
        self.output_area.insert(tk.END, text, tag_name)
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)
    
    def update_prompt(self):#directory
        directory = os.getcwd().split(os.sep)[-1]
        if self.current_settings['prompt_style'] == 'detailed':
            self.prompt_label.config(text=f"[{directory}] >> ")
        else:
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
        
        if self.current_settings['history_enabled']:
            self.history.append(cmd)#add history
        self.history_index = -1
    
        directory = os.getcwd().split(os.sep)[-1]
        self.write_output(f"{directory}>> {cmd}\n", '#FFFFFF')#write input
        self.input_entry.delete(0, tk.END)#delete input
        self.execute_command(cmd)#execute(bale dito mga arguments and command)
        self.update_prompt()#update command
        
#------------------------------------------ Settings
    def settings(self, args):
        if not args:
            self._show_current_settings()
            return

        parts = args.split(None, 1)
        if len(parts) < 1:
            self._show_setting_options()
            return
    
        option = parts[0].lower()
        value = parts[1] if len(parts) > 1 else None
        
        # Handle settings without values
        if option in ['show', 'list', 'display']:
            self._show_current_settings()
            return
        elif option == 'reset':
            self._reset_settings()
            return
        elif option == 'export':
            self._export_settings()
            return
        
        # Handle settings that require values
        if value is None:
            self.write_output(f"ERROR: Setting '{option}' requires a value\n", '#FF0000')
            self._show_setting_options()
            return
        
        try:
            if option == 'theme':
                self._change_theme(value)
            elif option in ['fontsize', 'font-size', 'size']:
                self._change_font_size(value)
            elif option in ['fontcolor', 'font-color', 'color', 'textcolor']:
                self._change_font_color(value)
            elif option in ['bgcolor', 'bg-color', 'background']:
                self._change_bg_color(value)
            elif option in ['prompt', 'prompt-style']:
                self._change_prompt_style(value)
            elif option in ['autocomplete', 'auto-complete']:
                self._toggle_autocomplete(value)
            elif option == 'history':
                self._manage_history(value)
            else:
                self.write_output(f"ERROR: Unknown setting '{option}'\n", '#FF0000')
                self._show_setting_options()
            
        except Exception as e:
            self.write_output(f"ERROR: Setting change failed: {e}\n", '#FF0000')
            
    def _show_current_settings(self):
        settings_text = f'''────────────────────────────────────────────
            REDVILLSHELL — Current Settings
────────────────────────────────────────────
Theme                    | {self.current_settings['theme']}
Font Size                | {self.current_settings['font_size']}
Font Color               | {self.current_settings['font_color']}
Background Color         | {self.current_settings['bg_color']}
Prompt Style             | {self.current_settings['prompt_style']}
Auto-complete            | {'Enabled' if self.current_settings['autocomplete'] else 'Disabled'}
History                  | {'Enabled' if self.current_settings['history_enabled'] else 'Disabled'}
────────────────────────────────────────────
Type 'setting help' for available options
────────────────────────────────────────────
'''
        self.write_output(settings_text)

    def _show_setting_options(self):#option
        options_text = '''────────────────────────────────────────────
              Available Settings Options
────────────────────────────────────────────
DISPLAY:
  setting show                |Show current settings
  setting theme <name>        |Change color theme
  setting fontsize <8-20>     |Change font size
  setting fontcolor <color>   |Change text color
  setting bgcolor <color>     |Change background color
  
PROMPT:
    • directory              |Simple directory name
    • detailed               |Detailed with brackets
    
FEATURES:
  setting autocomplete <on/off>  |Toggle auto-complete
  setting history <on/off>       |Toggle command history
  setting history clear          |Clear command history
  
UTILITIES:
  setting reset               |Reset to default settings
  setting export              |Show all settings

────────────────────────────────────────────
AVAILABLE THEMES:
  matrix, dark, light, cmd, blue, hacker,
  ocean, sunset, forest, nord, dracula
  
COLOR FORMATS:
  • Hex: #00FF00, #FF5733
  • Named: red, green, blue, cyan, magenta
  • RGB: Not supported yet
────────────────────────────────────────────
'''
        self.write_output(options_text)

    def _change_theme(self, theme):#pogi theme
        themes = {
            'matrix': {'bg': 'black', 'fg': '#00FF00'},
            'dark': {'bg': 'black', 'fg': 'white'},
            'light': {'bg': 'white', 'fg': 'black'},
            'cmd': {'bg': 'black', 'fg': '#C0C0C0'},
            'blue': {'bg': '#1E1E2E', 'fg': '#89B4FA'},
            'hacker': {'bg': '#0A0A0A', 'fg': '#00FF41'},
            'ocean': {'bg': '#001F3F', 'fg': '#39CCCC'},
            'sunset': {'bg': '#2C1810', 'fg': '#FF6B35'},
            'forest': {'bg': '#1B2E1F', 'fg': '#A8E6A1'},
            'nord': {'bg': '#2E3440', 'fg': '#88C0D0'},
            'dracula': {'bg': '#282A36', 'fg': '#F8F8F2'}
        }
        
        theme_lower = theme.lower()
        if theme_lower in themes:
            colors = themes[theme_lower]
            self._apply_colors(colors['bg'], colors['fg'])
            self.current_settings['theme'] = theme_lower
            self.current_settings['bg_color'] = colors['bg']
            self.current_settings['font_color'] = colors['fg']
            self.write_output(f"Theme changed to '{theme_lower}'\n", '#00FF00')
        else:
            self.write_output(f"Unknown theme '{theme}'\n", '#FF0000')
            self.write_output("Available themes: " + ", ".join(themes.keys()) + "\n")

    def _change_font_size(self, size_str):#font
        try:
            size = int(size_str)
            if 8 <= size <= 20:
                font = ('Consolas', size)
                self.output_area.config(font=font)
                self.input_entry.config(font=font)
                self.prompt_label.config(font=font)
                self.current_settings['font_size'] = size
                self.write_output(f"Font size changed to {size}\n", '#00FF00')
            else:
                self.write_output("Font size must be between 8 and 20\n", '#FF0000')
        except ValueError:
            self.write_output("Font size must be a number\n", '#FF0000')

    def _change_font_color(self, color):#color mappifn
        named_colors = {
            'green': '#00FF00',
            'red': '#FF0000',
            'blue': '#0000FF',
            'yellow': '#FFFF00',
            'cyan': '#00FFFF',
            'magenta': '#FF00FF',
            'white': '#FFFFFF',
            'black': '#000000',
            'orange': '#FF8800',
            'purple': '#9933FF',
            'pink': '#FF69B4',
            'lime': '#00FF00',
            'teal': '#008080',
            'navy': '#000080',
            'gray': '#808080',
            'grey': '#808080'
        }
        
        color_lower = color.lower()
        
        if color_lower in named_colors:
            final_color = named_colors[color_lower]#r colors
        
        elif re.match(r'^#[0-9A-Fa-f]{6}$', color):#hex
            final_color = color.upper()
        else:
            self.write_output(f"✗ Invalid color format '{color}'\n", '#FF0000')
            self.write_output("Use hex (#00FF00) or named colors (green, red, blue, etc.)\n")
            return
        
        # Apply the color
        self.output_area.config(fg=final_color)
        self.input_entry.config(fg=final_color, insertbackground=final_color)
        self.prompt_label.config(fg=final_color)
        self.current_settings['font_color'] = final_color
        self.write_output(f"Font color changed to {final_color}\n", '#00FF00')

    def _change_bg_color(self, color):
        """Change the background color"""
        named_colors = {
            'black': '#000000',
            'white': '#FFFFFF',
            'gray': '#808080',
            'grey': '#808080',
            'darkgray': '#333333',
            'lightgray': '#CCCCCC',
            'navy': '#001F3F',
            'darkblue': '#00008B',
            'darkgreen': '#013220'
        }
        
        color_lower = color.lower()
        
        if color_lower in named_colors:
            final_color = named_colors[color_lower]
        elif re.match(r'^#[0-9A-Fa-f]{6}$', color):
            final_color = color.upper()
        else:
            self.write_output(f"Invalid color format '{color}'\n", '#FF0000')
            self.write_output("Use hex (#000000) or named colors (black, white, gray, etc.)\n")
            return
        
        self.output_area.config(bg=final_color)
        self.input_entry.config(bg=final_color)
        self.prompt_label.config(bg=final_color)
        self.root.configure(bg=final_color)
        self.current_settings['bg_color'] = final_color
        self.write_output(f"Background color changed to {final_color}\n", '#00FF00')

    def _apply_colors(self, bg, fg):
        """Helper to apply both background and foreground colors"""
        self.output_area.config(bg=bg, fg=fg)
        self.input_entry.config(bg=bg, fg=fg, insertbackground=fg)
        self.prompt_label.config(bg=bg, fg=fg)
        self.root.configure(bg=bg)

    def _change_prompt_style(self, style):#prompt desig
        style_lower = style.lower()
        if style_lower in ['directory', 'basic', 'simple']:
            self.current_settings['prompt_style'] = 'directory'
            self.update_prompt()
            self.write_output(f"Prompt style changed to 'directory'\n", '#00FF00')
        elif style_lower in ['detailed', 'full', 'verbose']:
            self.current_settings['prompt_style'] = 'detailed'
            self.update_prompt()
            self.write_output(f"Prompt style changed to 'detailed'\n", '#00FF00')
        else:
            self.write_output("Available styles: directory, detailed\n", '#FF0000')

    def _toggle_autocomplete(self, value):#other usr validsba
        if value.lower() in ['on', 'true', 'yes', '1', 'enable']:
            self.current_settings['autocomplete'] = True
            self.write_output("Auto-complete enabled\n", '#00FF00')
        elif value.lower() in ['off', 'false', 'no', '0', 'disable']:
            self.current_settings['autocomplete'] = False
            self.write_output("Auto-complete disabled\n", '#00FF00')
        else:
            self.write_output("Use 'on' or 'off'\n", '#FF0000')

    def _manage_history(self, action):#more history
        action_lower = action.lower()
        if action_lower == 'clear':
            self.history.clear()
            self.history_index = -1
            self.write_output("Command history cleared\n", '#00FF00')
        elif action_lower in ['on', 'enable', 'true']:
            self.current_settings['history_enabled'] = True
            self.write_output("Command history enabled\n", '#00FF00')
        elif action_lower in ['off', 'disable', 'false']:
            self.current_settings['history_enabled'] = False
            self.write_output("Command history disabled\n", '#00FF00')
        else:
            self.write_output("Use 'history clear', 'history on', or 'history off'\n", '#FF0000')
    
    def _reset_settings(self):
        """Reset all settings to default"""
        self.current_settings = {
            'theme': 'matrix',
            'font_size': 10,
            'font_color': '#00FF00',
            'bg_color': 'black',
            'prompt_style': 'directory',
            'autocomplete': True,
            'history_enabled': True
        }
        self._apply_colors('black', '#00FF00')
        font = ('Consolas', 10)
        self.output_area.config(font=font)
        self.input_entry.config(font=font)
        self.prompt_label.config(font=font)
        self.update_prompt()
        self.write_output("All settings reset to default\n", '#00FF00')
    
    def _export_settings(self):
        """Export all current settings"""
        export_text = f'''────────────────────────────────────────────
            REDVILLSHELL — Settings Export
────────────────────────────────────────────
setting theme {self.current_settings['theme']}
setting fontsize {self.current_settings['font_size']}
setting fontcolor {self.current_settings['font_color']}
setting bgcolor {self.current_settings['bg_color']}
setting prompt {self.current_settings['prompt_style']}
setting autocomplete {'on' if self.current_settings['autocomplete'] else 'off'}
setting history {'on' if self.current_settings['history_enabled'] else 'off'}
────────────────────────────────────────────
Copy these commands to restore your settings
────────────────────────────────────────────
'''
        self.write_output(export_text)
#---------------------------------------------
    
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
            elif command == 'setting':
                self.settings(args)
            
            #FILE
            elif command == 'open':
                self.file_handler.open_file(args)
            elif command == 'run':
                self.file_handler.open_file(args)
            elif command == 'create':
                self.file_handler.create_item(args)
            elif command == 'install':
                self.file_handler.install(args)
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
            elif command == 'connect':
                if ' ' in args:
                    ssid, password = args.split(' ', 1)
                    self.network.connect_wifi(ssid, password)
                else:
                    self.write_output("ERROR: Use format 'connect <SSID> <password>'\n", '#FF0000')
            elif command == 'ping':
                self.network.ping(args)

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
            else:#command calculation handling
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
Creation Timeline                    | 11/15/25 - 11/21/25
Version                              | Prototype 0.1.5
Version Date                         | 11/21/25

────────────────────────────────────────────
Notes by me:
  >> Ang dami ko nilagay like madaming feature
  and na enjoy ko siya gawin and ang dami ko 
  natutunan specially sa socket and os, i uupdate
  ko pa siya and gagawin ko pa siya mas robust
  kasi every feature na dinadagdag ko mas bumabagal
  siya. and also add ko lang di lang siya shell
  I think naging Operating System yung ginawa ko
  nywhwhwh.
────────────────────────────────────────────
'''
        self.write_output(info_text)
    
    def cmd_version(self):
        version_text = f'''────────────────────────────────────────────
           REDVILLSHELL — Version {version}
────────────────────────────────────────────
>> 11/12/25 - Prototype 0.1.5 - Python 
- SSIDS and Network login
- Enhanced Settings with Font Color
- Run program 
- Better handling
- OS settings
- Package simulation 
────────────────────────────────────────────
'''
        self.write_output(version_text)

def main():
    root = tk.Tk()  
    app = RedvillShellGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()#nyehehehe
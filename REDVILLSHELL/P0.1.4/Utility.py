#main imports
import os
import shutil
import sys
import ctypes
import pathlib
import psutil
import GPUtil
import time
import datetime
#basic networking imports########
import socket
import subprocess
import re
import platform
import requests#
import httpx#
import http#



class Admin:#admin mode

    def __init__(self):#always set false
        self.admin_mode = False
    
    def is_elevated(self):#check if current running admin or nah
        
        if os.name == 'nt':  # Windows
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                return False
        else:  # Linux/macOS
            try:
                return os.geteuid() == 0
            except AttributeError:
                return False
    
    def request_elevation_windows(self):#UAC COMMAND
        if os.name != 'nt':
            return False
        
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            return True
        except Exception:
            return False
    
    def request_elevation_unix(self):#SUDO REQUEST
        if os.name == 'nt':
            return False
        try:
            args = ['sudo', sys.executable] + sys.argv
            os.execvp('sudo', args)
            return True
        except Exception:
            return False
    
    def toggle_admin_mode(self, boolean):#ADMIN MODE
        TRUE_VALUES = ['T', 'Y', 'TRUE', 'YES', '1']
        FALSE_VALUES = ['F', 'N', 'FALSE', 'NO', '0']
        
        s = str(boolean).strip().upper()
        
        if s in TRUE_VALUES:
            if self.is_elevated():
                self.admin_mode = True
                print("ADMINISTRATION TRUE — Already running with elevated privileges.")
            else:
                print("Requesting admin privilege...")
                
                if os.name == 'nt':
                    success = self.request_elevation_windows()
                else:
                    success = self.request_elevation_unix()
                
                if success:
                    print("Relaunching REDVILLSHELL as administrator...")
                    sys.exit(0)
                else:
                    print("ERROR! Failed to request administrator privilege.")
                    
        elif s in FALSE_VALUES:
            self.admin_mode = False
            print("ADMINISTRATION FALSE")
        else:
            print(f"ERROR: '{boolean}' is not recognized.")
            print(f"Use: {', '.join(TRUE_VALUES)} or {', '.join(FALSE_VALUES)}")
    
    def get_system_info(self):
        
        print(f"""
SYSTEM INFORMATION:
Operating System: {os.name}
Platform: {sys.platform}
Admin/Root: {'YES' if self.is_elevated() else 'NO'}
Admin Mode: {'ENABLED' if self.admin_mode else 'DISABLED'}
Python Version: {sys.version.split()[0]}
Current Directory: {os.getcwd()}
        """)
        
    def get_hardware_info(self):
        # CPU info
        cpu_model = platform.processor()
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
    
        # GPU info
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            gpu_model = gpu.name
            gpu_driver = gpu.driver
            gpu_vram = f"{round(gpu.memoryTotal / 1024, 2)} GB"
            gpu_id = gpu.id
        else:
            gpu_model = "N/A"
            gpu_driver = "N/A"
            gpu_vram = "N/A"
            gpu_id = "N/A"

        # RAM info
        ram = psutil.virtual_memory()
        total_ram = round(ram.total / (1024 ** 3), 2)

        # Storage info
        disk = psutil.disk_usage('/')
        total_storage = round(disk.total / (1024 ** 3), 2)
        used_storage = round(disk.used / (1024 ** 3), 2)
        free_storage = round(disk.free / (1024 ** 3), 2)

        print(f"""
    CPU
    CPU Model: {cpu_model}
    CPU Physical cores: {physical_cores}
    CPU Logical cores: {logical_cores}
    GPU
    GPU Model: {gpu_model}
    GPU ID: {gpu_id}
    GPU Driver: {gpu_driver}
    GPU VRAM: {gpu_vram}
    RAM
    Total RAM: {total_ram}
    DISK
    Total storage: {total_storage}
    Used storage: {used_storage}
    Free_storage: {free_storage}
            """)
        
        
class FileHandling:#file operation
    
    def __init__(self, admin_instance):
        self.admin = admin_instance
    
    def open_file(self, filename):
        
        try:
            if os.path.exists(filename):
                os.startfile(filename) if os.name == 'nt' else os.system(f'open "{filename}"')
                print(f"Opened '{filename}'.")
            else:
                print(f"ERROR: File '{filename}' not found.\n")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.")
        except OSError as e:
            print(f'ERROR: {e}')
    
    def create_item(self, command):#create
        
        try:
            parts = command.strip().split(None, 1)
            if len(parts) < 2:
                print("ERROR: Use format 'create <type> <name>'")
                print("Types: F+ (file), F++ (folder), py, cpp, c")
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
            elif item_type == 'f+':
                with open(name, 'w') as file:
                    pass
                print(f"SUCCESS! Created file '{name}'.")
            elif item_type == 'f++':
                os.makedirs(name, exist_ok=True)
                print(f"SUCCESS! Created folder '{name}'.")
            else:
                print(f"ERROR: Unknown type '{item_type}'.")
                print("Valid types: F+, F++, py, cpp, c")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.")
        except Exception as e:
            print(f"ERROR: Creation failed: {e}")
    
    def delete_item(self, command):#delete
        
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
            
            if item_type == 'f+':
                if not os.path.isfile(name):
                    print(f"ERROR: '{name}' is not a file. Use 'F++' or '+f++' for folders.")
                    return
                try:
                    os.remove(name)
                    print(f"SUCCESS! Deleted file '{name}'.")
                except PermissionError:
                    if self.admin.admin_mode:
                        pathlib.Path(name).unlink()
                        print(f"SUCCESS! Deleted file '{name}' with admin privileges.")
                    else:
                        print("ACCESS DENIED! Enable admin mode first.")
                        
            elif item_type == 'f++':
                if not os.path.isdir(name):
                    print(f"ERROR: '{name}' is not a folder. Use 'F+' for files.")
                    return
                try:
                    os.rmdir(name)
                    print(f"SUCCESS! Deleted empty folder '{name}'.")
                except OSError:
                    print(f"ERROR: Folder '{name}' is not empty. Use 'delete +f++' to delete with contents.")
                except PermissionError:
                    print("ACCESS DENIED! Enable admin mode first.")
                    
            elif item_type == '+f++':
                if not os.path.isdir(name):
                    print(f"ERROR: '{name}' is not a folder. Use 'F+' for files.")
                    return
                try:
                    shutil.rmtree(name)
                    print(f"SUCCESS! Deleted folder '{name}' and all its contents.")
                except PermissionError:
                    print("ACCESS DENIED! Enable admin mode first.")
            else:
                print(f"ERROR: Unknown type '{item_type}'.")
                print("Valid types: F+ (file), F++ (empty folder), +f++ (whole folder)")
        except Exception as e:
            print(f"ERROR: Deletion failed: {e}")
    
    def rename_file(self, command):#rename
    
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
            print(f"SUCCESS! Renamed '{old}' to '{new}'.")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.")
        except Exception as e:
            print(f"ERROR: Rename failed: {e}")
    
    def list_dir(self):#Currect directory of the OS
        
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
            print("ACCESS DENIED! Enable admin mode first.")
        except OSError:
            print("ERROR! Cannot view the current directory")
    
    def change_dir(self, path):
        
        try:
            os.chdir(path)
            print(f"SUCCESS! Changed directory to '{path}'.")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def file_info(self, filename):

        try:
            if not os.path.exists(filename):
                print(f"ERROR: '{filename}' not found.")
                return
            
            stat = os.stat(filename)
            print(f"""
FILE INFORMATION:
Name: {filename}
Size: {stat.st_size} bytes
Type: {'Directory' if os.path.isdir(filename) else 'File'}
Created: {datetime.datetime.fromtimestamp(stat.st_ctime)}
Modified: {datetime.datetime.fromtimestamp(stat.st_mtime)}
            """)
        except Exception as e:
            print(f"ERROR: {e}")


class ReaderHandling:
    
    def read_file(self, filename, lines=None):#read file
        try:
            with open(filename, 'r') as f:
                if lines:
                    content = [f.readline() for _ in range(lines)]
                else:
                    content = f.readlines()
                
                for line in content:
                    print(line, end='')
        except FileNotFoundError:
            print(f"ERROR: File '{filename}' not found.")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def find_in_file(self, filename, keyword):#find file
        try:
            with open(filename, 'r') as f:
                for i, line in enumerate(f, 1):
                    if keyword in line:
                        print(f"Line {i}: {line.strip()}")
        except FileNotFoundError:
            print(f"ERROR: File '{filename}' not found.")
        except Exception as e:
            print(f"ERROR: {e}")


class Timer:
    
    def show_current_time(self):#current time
        now = datetime.datetime.now()
        print(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def start_timer(self, seconds):
        """Start a countdown timer"""
        print(f"Timer started for {seconds} seconds...")
        time.sleep(seconds)
        print("Time's up!")
    
    def set_alarm(self, target_time):
        """Set an alarm (placeholder)"""
        print(f"Alarm set for {target_time}")
        

class Network:
    
    def show_ipconfig(self):
        """Show IP configuration"""
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            print(f"""
NETWORK INFORMATION:      
Hostname:   {hostname}
Local IP:   {ip}
            """)
        except Exception as e:
            print(f"ERROR: {e}")
#--------------- FIX PA
    def ssids(self):
        system = platform.system()
        ssids = []

        if system == "Windows" or os.name == 'nt':
            command = ["netsh", "wlan", "show", "networks"]
            try:
                results = subprocess.check_output(command, text=True, encoding='utf-8')
                for line in results.splitlines():
                    if "SSID" in line:
                        ssid_name = line.split(":", 1)[-1].strip()
                        if ssid_name and ssid_name not in ssids:
                            ssids.append(ssid_name)
            except FileNotFoundError:
                print("Error: 'netsh' command not found. Make sure you are on Windows.")
            except Exception as e:
                print(f"An error occurred during scan: {e}")
                
        elif system == "Darwin": # macOS
                command = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"]
                try:
                    results = subprocess.check_output(command, text=True, encoding='utf-8')
                    # The output has a header, then SSIDs and BSSIDs
                    lines = results.strip().splitlines()
                    for line in lines[1:]: # Skip the header
                        # Split by whitespace, the first column is the SSID
                        ssid_name = line.strip().split()[0]
                        if ssid_name and ssid_name not in ssids:
                            ssids.append(ssid_name)
                except FileNotFoundError:
                    print("Error: 'airport' command not found or path is incorrect. Make sure you are on macOS.")
                except Exception as e:
                    print(f"An error occurred during scan: {e}")
                    
        elif system == "Linux":
                try:
                    command = ["nmcli", "dev", "wifi", "list"]
                    results = subprocess.check_output(command, text=True, encoding='utf-8')
                    lines = results.strip().splitlines()
                    for line in lines[1:]: # Skip the header
                        parts = line.strip().split()
                        ssid_name = parts[1] # Often the second column
                        if ssid_name and ssid_name not in ssids:
                            ssids.append(ssid_name)

                except FileNotFoundError:
                    print("Error: 'nmcli' command not found. Try installing NetworkManager or use 'iwlist scan'.")
                    try:
                        command = ["iwlist", "scan"]
                        results = subprocess.check_output(command, text=True, encoding='utf-8')
                        for line in results.splitlines():
                            if "ESSID" in line:
                                ssid_name = re.search(r'ESSID:"(.*)"', line).group(1)
                                if ssid_name and ssid_name not in ssids:
                                    ssids.append(ssid_name)
                    except FileNotFoundError:
                        print("Error: 'iwlist' command not found. Make sure wireless tools are installed.")
                except Exception as e:
                    print(f"An error occurred during scan: {e}")
                    
        else:
            print(f"Unsupported operating system: {system}")

        return ssids
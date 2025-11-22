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
import requests
import json
import webbrowser
import httpx
import http

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
                print("ADMINISTRATION TRUE — Already running with elevated privileges.\n")
            else:
                print("Requesting admin privilege...\n")
                
                if os.name == 'nt':
                    success = self.request_elevation_windows()
                else:
                    success = self.request_elevation_unix()
                
                if success:
                    print("Relaunching REDVILLSHELL as administrator...\n")
                    sys.exit(0)
                else:
                    print("ERROR! Failed to request administrator privilege.\n")
                    
        elif s in FALSE_VALUES:
            self.admin_mode = False
            print("ADMINISTRATION FALSE\n")
        else:
            print(f"ERROR: '{boolean}' is not recognized.\n")
            print(f"Use: {', '.join(TRUE_VALUES)} or {', '.join(FALSE_VALUES)}\n")
    
    def get_system_info(self):
        if os.name == 'nt':
            operating_system = 'Windows'
        elif os.name == 'darwins':
            operating_system = 'MacOs'
        else:
            operating_system = 'Unix'
        
        print(f"""
SYSTEM INFORMATION:
Operating System: {operating_system}
Platform: {sys.platform}
Admin/Root: {'YES' if self.is_elevated() else 'NO'}
Admin Mode: {'ENABLED' if self.admin_mode else 'DISABLED'}
Python Version: {sys.version.split()[0]}
Current Directory: {os.getcwd()}
""")
        
    def get_hardware_info(self):
        # CPU 
        cpu_model = platform.processor()
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
        
        # GPU 
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

        # RAM 
        ram = psutil.virtual_memory()
        total_ram = round(ram.total / (1024 ** 3), 2)

        # Storage 
        disk = psutil.disk_usage('/')
        total_storage = round(disk.total / (1024 ** 3), 2)
        used_storage = round(disk.used / (1024 ** 3), 2)
        free_storage = round(disk.free / (1024 ** 3), 2)

        print(f"""
HARDWARE INFO:
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
Total RAM: {total_ram} GB
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
                # Check if it's an application
                if any(filename.lower().endswith(ext) for ext in ['.exe', '.app', '.msi', '.bat', '.cmd']):
                    self._run_application(filename)
                else:
                    os.startfile(filename) if os.name == 'nt' else os.system(f'open "{filename}"')
                print(f"Opened '{filename}'.")
            else:
                print(f"ERROR: File '{filename}' not found.\n")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.\n")
        except OSError as e:
            print(f'ERROR: {e}')
    
    def run_application(self, app_path):#Direct run depends on OS
        try:
            if os.name == 'nt':  
                os.startfile(app_path)
            else:  # Linux/macOS
                if platform.system() == 'Darwin':  #
                    os.system(f'open "{app_path}"')
                else:  
                    os.system(f'"{app_path}" &')
        except Exception as e:
            print(f"ERROR running application: {e}\n")
    
    def run_program(self, program_name):#hanap path
        try:
            if os.path.exists(program_name):
                subprocess.Popen([program_name])
                print(f"Started '{program_name}'")
                return
            #---- search path para sa program
            if os.name == 'nt':  # Windows
                executable = shutil.which(program_name) or shutil.which(program_name + '.exe')
            else:  # Linux/macOS
                executable = shutil.which(program_name)
            if executable:
                subprocess.Popen([executable])
                print(f"Started '{program_name}'")
            else:
                print(f"ERROR: Program '{program_name}' not found\n")
                
        except Exception as e:
            print(f"ERROR running program: {e}\n")
    
    def create_item(self, command):#create
        try:
            parts = command.strip().split(None, 1)
            if len(parts) < 2:
                print("ERROR: Use format 'create <type> <name>'\n")
                print("Types: F+ (file), F++ (folder), py, cpp, c\n")
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
                print(f"SUCCESS! Created {item_type.upper()} file '{name}'.\n")
            elif item_type == 'f+':
                with open(name, 'w') as file:
                    pass
                print(f"SUCCESS! Created file '{name}'.\n")
            elif item_type == 'f++':
                os.makedirs(name, exist_ok=True)
                print(f"SUCCESS! Created folder '{name}'.\n")
            else:
                print(f"ERROR: Unknown type '{item_type}'.\n")
                print("Valid types: F+, F++, py, cpp, c\n")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.\n")
        except Exception as e:
            print(f"ERROR: Creation failed: {e}\n")
            
    def install(self, args):
        if not args:
            self.write_output("ERROR: Use format 'install <program/library>'\n", '#FF0000')
            return
        
        try:
            if self.admin.admin_mode:#py lib
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', args], 
                                    capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.write_output(f"SUCCESS! Installed '{args}'\n")
                    if result.stdout:
                        self.write_output(result.stdout + '\n')
                else:#if fail
                    self.write_output(f"Trying system package manager for '{args}'...\n")
                    self._install_system_package(args)
            else:
                self.write_output("ACCESS DENIED! Enable admin mode first for installation.\n", '#FF0000')
                
        except Exception as e:
            self.write_output(f"ERROR: Installation failed: {e}\n", '#FF0000')

    def _install_system_package(self, package_name):#check what platform package
            try:
                if os.name == 'nt':  # Windows
                    try:
                        result = subprocess.run(['winget', 'install', package_name], capture_output=True, text=True)
                        if result.returncode == 0:
                            self.write_output(f"SUCCESS! Installed '{package_name}' via winget\n")
                        else:
                            self.write_output(f"ERROR: Could not install '{package_name}'\n", '#FF0000')
                    except FileNotFoundError:
                        self.write_output("ERROR: winget not available. Install Windows Package Manager.\n", '#FF0000')
                        
                elif platform.system() == 'Darwin':  # macOS
                    result = subprocess.run(['brew', 'install', package_name], capture_output=True, text=True)
                    if result.returncode == 0:
                        self.write_output(f"SUCCESS! Installed '{package_name}' via Homebrew\n")
                    else:
                        self.write_output("ERROR: Homebrew not available or package not found.\n", '#FF0000')
                        
                else:  # Linux
                    for manager in ['apt', 'yum', 'pacman']:
                        try:
                            if manager == 'apt':
                                cmd = ['sudo', 'apt', 'install', '-y', package_name]
                            elif manager == 'yum':
                                cmd = ['sudo', 'yum', 'install', '-y', package_name]
                            else:  # pacman
                                cmd = ['sudo', 'pacman', '-S', '--noconfirm', package_name]
                            
                            result = subprocess.run(cmd, capture_output=True, text=True)
                            if result.returncode == 0:
                                self.write_output(f"SUCCESS! Installed '{package_name}' via {manager}\n")
                                return
                        except FileNotFoundError:
                            continue
                    
                    self.write_output("ERROR: No supported package manager found.\n", '#FF0000')
                    
            except Exception as e:
                self.write_output(f"ERROR: System installation failed: {e}\n", '#FF0000')
            
    def delete_item(self, command):#delete
        try:
            parts = command.strip().split(None, 1)
            if len(parts) < 2:
                print("ERROR: Use format 'delete <type> <name>'\n")
                print("Types: F+ (file), F++ (empty folder), +f++ (folder with contents)\n")
                return
            
            item_type = parts[0].strip().lower()
            name = parts[1].strip()
            
            if not os.path.exists(name):
                print(f"ERROR: '{name}' not found.\n")
                return
            
            if item_type == 'f+':
                if not os.path.isfile(name):
                    print(f"ERROR: '{name}' is not a file. Use 'F++' or '+f++' for folders.\n")
                    return
                try:
                    os.remove(name)
                    print(f"SUCCESS! Deleted file '{name}'.\n")
                except PermissionError:
                    if self.admin.admin_mode:
                        pathlib.Path(name).unlink()
                        print(f"SUCCESS! Deleted file '{name}' with admin privileges.\n")
                    else:
                        print("ACCESS DENIED! Enable admin mode first.\n")
                        
            elif item_type == 'f++':
                if not os.path.isdir(name):
                    print(f"ERROR: '{name}' is not a folder. Use 'F+' for files.\n")
                    return
                try:
                    os.rmdir(name)
                    print(f"SUCCESS! Deleted empty folder '{name}'.\n")
                except OSError:
                    print(f"ERROR: Folder '{name}' is not empty. Use 'delete +f++' to delete with contents.\n")
                except PermissionError:
                    print("ACCESS DENIED! Enable admin mode first.\n")
                    
            elif item_type == '+f++':
                if not os.path.isdir(name):
                    print(f"ERROR: '{name}' is not a folder. Use 'F+' for files.\n")
                    return
                try:
                    shutil.rmtree(name)
                    print(f"SUCCESS! Deleted folder '{name}' and all its contents.\n")
                except PermissionError:
                    print("ACCESS DENIED! Enable admin mode first.\n")
            else:
                print(f"ERROR: Unknown type '{item_type}'.")
                print("Valid types: F+ (file), F++ (empty folder), +f++ (whole folder)\n")
        except Exception as e:
            print(f"ERROR: Deletion failed: {e}")
    
    def rename_file(self, command):#rename
        try:
            if '/' not in command:
                print("ERROR: Use format 'oldname / newname'\n")
                return
            old, new = command.split('/', 1)
            old, new = old.strip(), new.strip()
            if not os.path.exists(old):
                print(f"ERROR: '{old}' not found.")
                return
            os.rename(old, new)
            print(f"SUCCESS! Renamed '{old}' to '{new}'.\n")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.\n")
        except Exception as e:
            print(f"ERROR: Rename failed: {e}\n")
    
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
            print("ACCESS DENIED! Enable admin mode first.\n")
        except OSError:
            print("ERROR! Cannot view the current directory\n")
    
    def change_dir(self, path):
        
        try:
            os.chdir(path)
            print(f"SUCCESS! Changed directory to '{path}'.\n")
        except PermissionError:
            print("ACCESS DENIED! Enable admin mode first.\n")
        except Exception as e:
            print(f"ERROR: {e}\n")
    
    def file_info(self, filename):
        try:
            if not os.path.exists(filename):
                print(f"ERROR: '{filename}' not found.\n")
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
            print(f"ERROR: {e}\n")

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
            print(f"ERROR: File '{filename}' not found.\n")
        except Exception as e:
            print(f"ERROR: {e}\n")


class Timer:
    def show_current_time(self):#current time
        now = datetime.datetime.now()
        print(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def start_timer(self, seconds):#start
        print(f"Timer started for {seconds} seconds...\n")
        time.sleep(seconds)
        print("Time's up!\n")
    
    def set_alarm(self, target_time):#set
        print(f"Alarm set for {target_time}\n")
        

class Network:
    
    def show_ipconfig(self):
        try:
            hostname = socket.gethostname()
            ip4 = socket.gethostbyname(hostname)
            if ip4 == '127.0.0.1':
                media = 'Media disconnected'
            else:
                media = 'Media connected'

            print(f"""
NETWORK INFORMATION:      
Hostname:   {hostname}
IP4:        {ip4}
Media stat: {media}
""")
        except Exception as e:
            print(f"ERROR: {e}")
#------
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
                print("Error: 'netsh' command not found. Make sure you are on Windows.\n")
            except Exception as e:
                print(f"An error occurred during scan: {e}\n")
                
        elif system == "Darwin": # macOS
                command = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"]
                try:
                    results = subprocess.check_output(command, text=True, encoding='utf-8')
                    lines = results.strip().splitlines()
                    for line in lines[1:]: 
                        ssid_name = line.strip().split()[0]
                        if ssid_name and ssid_name not in ssids:
                            ssids.append(ssid_name)#header shit
                except FileNotFoundError:
                    print("Error: 'airport' command not found or path is incorrect. Make sure you are on macOS.\n")
                except Exception as e:
                    print(f"An error occurred during scan: {e}\n")
                    
        elif system == "Linux":
                try:
                    command = ["nmcli", "dev", "wifi", "list"]
                    results = subprocess.check_output(command, text=True, encoding='utf-8')
                    lines = results.strip().splitlines()
                    for line in lines[1:]: 
                        parts = line.strip().split()
                        ssid_name = parts[1] 
                        if ssid_name and ssid_name not in ssids:
                            ssids.append(ssid_name)

                except FileNotFoundError:
                    print("Error: 'nmcli' command not found. Try installing NetworkManager or use 'iwlist scan'.\n")
                    try:
                        command = ["iwlist", "scan"]
                        results = subprocess.check_output(command, text=True, encoding='utf-8')
                        for line in results.splitlines():
                            if "ESSID" in line:
                                ssid_name = re.search(r'ESSID:"(.*)"', line).group(1)
                                if ssid_name and ssid_name not in ssids:
                                    ssids.append(ssid_name)
                    except FileNotFoundError:
                        print("Error: 'iwlist' command not found. Make sure wireless tools are installed.\n")
                except Exception as e:
                    print(f"An error occurred during scan: {e}\n")
                    
        else:
            print(f"Unsupported operating system: {system}\n")

        return ssids
    
    def connect_wifi(self, ssid, password): 
        system = platform.system()
        
        if not ssid:
            print("ERROR: SSID is required\n")
            return False
        #platform
        if system == "Windows" or os.name == 'nt':
            return self._connect_windows(ssid, password)
        elif system == "Darwin":  
            return self._connect_macos(ssid, password)
        elif system == "Linux":
            return self._connect_linux(ssid, password)
        else:
            print(f"Unsupported operating system: {system}")
            return False
    
    def _connect_windows(self, ssid, password):#windows
        try:
            check_cmd = ['netsh', 'wlan', 'show', 'profile', f'name={ssid}']
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                profile_xml = f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>'''
                
                temp_file = f"temp_{ssid}.xml"
                with open(temp_file, 'w') as f:
                    f.write(profile_xml)
                
                add_cmd = ['netsh', 'wlan', 'add', 'profile', f'filename={temp_file}']
                add_result = subprocess.run(add_cmd, capture_output=True, text=True)
                
                # tangal temp file
                os.remove(temp_file)
                
                if add_result.returncode != 0:
                    print(f"ERROR: Failed to add profile: {add_result.stderr}")
                    return False
            
            # Connect 
            connect_cmd = ['netsh', 'wlan', 'connect', f'name={ssid}']
            connect_result = subprocess.run(connect_cmd, capture_output=True, text=True)
            
            if connect_result.returncode == 0:
                print(f"SUCCESS! Connecting to '{ssid}'...\n")
                # wait establush
                time.sleep(3)
                self._check_connection_status(ssid)
                return True
            else:
                print(f"ERROR: Failed to connect: {connect_result.stderr}\n")
                return False
                
        except Exception as e:
            print(f"ERROR: {e}\n")
            return False
    
    def _connect_macos(self, ssid, password):
        try:
            # Use networksetup to connect
            interface_cmd = ['networksetup', '-listallhardwareports']
            interface_result = subprocess.run(interface_cmd, capture_output=True, text=True)
            wifi_interface = None
            for line in interface_result.stdout.splitlines():
                if 'Wi-Fi' in line or 'AirPort' in line:
                    next_line = interface_result.stdout.splitlines()[
                        interface_result.stdout.splitlines().index(line) + 1
                    ]
                    if 'Device' in next_line:
                        wifi_interface = next_line.split(':')[-1].strip()
                        break
            
            if not wifi_interface:
                print("ERROR: Could not find Wi-Fi interface\n")
                return False
            
            # Connect 
            connect_cmd = [
                'networksetup', 
                '-setairportnetwork', 
                wifi_interface, 
                ssid, 
                password
            ]
            connect_result = subprocess.run(connect_cmd, capture_output=True, text=True)
            
            if connect_result.returncode == 0:
                print(f"SUCCESS! Connecting to '{ssid}'...")
                time.sleep(3)
                self._check_connection_status(ssid)
                return True
            else:
                print(f"ERROR: Failed to connect: {connect_result.stderr}\n")
                return False
                
        except Exception as e:
            print(f"ERROR: {e}\n")
            return False
    
    def _connect_linux(self, ssid, password):
        try:
            check_cmd = ['which', 'nmcli']
            check_result = subprocess.run(check_cmd, capture_output=True)
            
            if check_result.returncode != 0:
                print("ERROR: 'nmcli' not found. Install NetworkManager.\n")
                return False
            
            # nmcli
            connect_cmd = [
                'nmcli', 
                'dev', 
                'wifi', 
                'connect', 
                ssid, 
                'password', 
                password
            ]
            connect_result = subprocess.run(connect_cmd, capture_output=True, text=True)
            if connect_result.returncode == 0:
                print(f"SUCCESS! Connecting to '{ssid}'...")
                time.sleep(3)
                self._check_connection_status(ssid)
                return True
            else:
                print(f"ERROR: Failed to connect: {connect_result.stderr}\n")
                return False
                
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    def _check_connection_status(self, ssid):
        try:
            time.sleep(5)  # Wait for connection blha
            try:
                response = requests.get('http://httpbin.org/ip', timeout=10)
                if response.status_code == 200:
                    print(f"SUCCESS! Connected to '{ssid}' and have internet access!\n")
                    ip_info = response.json()
                    print(f"Your IP: {ip_info.get('origin', 'Unknown')}\n")
                else:
                    print(f"Connected to '{ssid}' but no internet access\n")
            except:
                print(f"Connected to '{ssid}' but cannot verify internet access\n")
                
        except Exception as e:
            print(f"Note: Could not verify connection status: {e}\n")
            
    def ping(self, target):
        try:
            if not target:
                print("ERROR: Use format 'ping <hostname/IP>'\n")
                return
            
            target = target.replace('http://', '').replace('https://', '')#protocol
            
            param = '-n' if os.name == 'nt' else '-c'
            command = ['ping', param, '4', target]
            
            print(f"Pinging {target}...")
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"SUCCESS! {target} is reachable\n")
            else:
                print(f"FAILED! {target} is not reachable\n")
                
            lines = result.stdout.split('\n')
            for line in lines[-6:-1]:  # 5 lines and shi
                if line.strip():
                    print(line)
                    
        except Exception as e:
            print(f"ERROR: Ping failed: {e}")
        
# installer.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import sys
import os
import platform
from threading import Thread
import time

class REDVILLSHELLInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("REDVILLSHELL OS - Installer")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Installation status
        self.installation_complete = False
        self.current_module = ""
        
        # Required modules
        self.required_modules = [
            'psutil',           
            'gputil',           
            'requests',        
            'httpx',            
            'numpy',            
        ]
        
        self.setup_gui()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_gui(self):
        """Setup the installer GUI"""
        # Header
        header_frame = tk.Frame(self.root, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title_label = tk.Label(
            header_frame,
            text="REDVILLSHELL OS Installer",
            font=('Consolas', 24, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Complete Installation Package",
            font=('Consolas', 12),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        subtitle_label.pack()
        
        # System info frame
        info_frame = tk.Frame(self.root, bg='#2a2a2a', relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Python version
        python_version = f"Python {sys.version.split()[0]}"
        python_label = tk.Label(
            info_frame,
            text=f"Python Version: {python_version}",
            font=('Consolas', 10),
            fg='#00ff00',
            bg='#2a2a2a'
        )
        python_label.pack(anchor='w', padx=10, pady=5)
        
        # Platform info
        platform_info = f"{platform.system()} {platform.release()}"
        platform_label = tk.Label(
            info_frame,
            text=f"Platform: {platform_info}",
            font=('Consolas', 10),
            fg='#00ff00',
            bg='#2a2a2a'
        )
        platform_label.pack(anchor='w', padx=10, pady=5)
        
        # Progress frame
        progress_frame = tk.Frame(self.root, bg='#1a1a1a')
        progress_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to install...",
            font=('Consolas', 11),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        self.progress_label.pack(anchor='w', pady=5)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient=tk.HORIZONTAL,
            length=760,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Log frame
        log_frame = tk.Frame(self.root, bg='#1a1a1a')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        log_label = tk.Label(
            log_frame,
            text="Installation Log:",
            font=('Consolas', 10, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        log_label.pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 9),
            insertbackground='#00ff00',
            selectbackground='#404040',
            relief=tk.FLAT
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.install_button = tk.Button(
            button_frame,
            text="Start Installation",
            command=self.start_installation,
            font=('Consolas', 12, 'bold'),
            bg='#00aa00',
            fg='white',
            activebackground='#00ff00',
            activeforeground='black',
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.install_button.pack(side=tk.LEFT, padx=5)
        
        self.exit_button = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            font=('Consolas', 12),
            bg='#aa0000',
            fg='white',
            activebackground='#ff0000',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.exit_button.pack(side=tk.RIGHT, padx=5)
        
        self.launch_button = tk.Button(
            button_frame,
            text="Launch REDVILLSHELL",
            command=self.launch_shell,
            font=('Consolas', 12),
            bg='#0055aa',
            fg='white',
            activebackground='#0088ff',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.launch_button.pack(side=tk.RIGHT, padx=5)
    
    def log_message(self, message, color='#00ff00'):
        """Add message to log with specified color"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n", color)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def update_progress(self, value, text):
        """Update progress bar and label"""
        self.progress_bar['value'] = value
        self.progress_label.config(text=text)
        self.root.update()
    
    def check_python_version(self):
        """Check if Python version is supported"""
        version = sys.version_info
        self.log_message(f"Checking Python version: {version.major}.{version.minor}.{version.micro}")
        
        # Check if Python version is between 3.10 and 3.14
        if version.major == 3 and version.minor >= 10:
            self.log_message("✓ Python version is supported", '#00ff00')
            return True
        else:
            self.log_message(f"✗ Python {version.major}.{version.minor} is not supported", '#ff0000')
            self.log_message("REDVILLSHELL requires Python 3.10 - 3.14", '#ff0000')
            return False
    
    def install_module(self, module):
        self.current_module = module
        self.log_message(f"Installing {module}...")
        
        try:
            # Use subprocess to run pip install
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', module, '--quiet'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.log_message(f"✓ Successfully installed {module}", '#00ff00')
                return True
            else:
                self.log_message(f"✗ Failed to install {module}", '#ff0000')
                self.log_message(f"Error: {result.stderr}", '#ff0000')
                return False
                
        except subprocess.TimeoutExpired:
            self.log_message(f"✗ Timeout installing {module}", '#ff0000')
            return False
        except Exception as e:
            self.log_message(f"✗ Error installing {module}: {str(e)}", '#ff0000')
            return False
    
    def check_module(self, module):
        try:
            __import__(module)
            self.log_message(f"✓ {module} is already installed", '#00ff00')
            return True
        except ImportError:
            return False
    
    def start_installation(self):
        self.install_button.config(state=tk.DISABLED)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Start installation in thread
        thread = Thread(target=self.installation_thread)
        thread.daemon = True
        thread.start()
    
    def installation_thread(self):
        try:
            if not self.check_python_version():
                messagebox.showerror("Error", "Unsupported Python version!\nPlease use Python 3.10 - 3.14")
                self.install_button.config(state=tk.NORMAL)
                return
            
            total_modules = len(self.required_modules)
            installed_count = 0
            failed_modules = []
            
            self.update_progress(0, "Starting installation...")
            
            # Install each module
            for i, module in enumerate(self.required_modules):
                progress = (i / total_modules) * 100
                self.update_progress(progress, f"Installing {module}...")
                
                # Check if module is already installed
                if self.check_module(module):
                    installed_count += 1
                    continue
                
                # Install module
                if self.install_module(module):
                    installed_count += 1
                else:
                    failed_modules.append(module)
                
                time.sleep(1)  
            
            self.update_progress(100, "Installation complete!")
            
            self.log_message("\n" + "="*50, '#00ff00')
            self.log_message("INSTALLATION SUMMARY", '#00ff00')
            self.log_message("="*50, '#00ff00')
            self.log_message(f"Total modules: {total_modules}", '#00ff00')
            self.log_message(f"Successfully installed: {installed_count}", '#00ff00')
            
            if failed_modules:
                self.log_message(f"Failed modules: {len(failed_modules)}", '#ff0000')
                for failed in failed_modules:
                    self.log_message(f"  - {failed}", '#ff0000')
                self.log_message("\nYou can try installing failed modules manually:", '#ffff00')
                self.log_message("pip install " + " ".join(failed_modules), '#ffff00')
            else:
                self.log_message("✓ All modules installed successfully!", '#00ff00')
                self.installation_complete = True
            
            if self.check_required_files():
                self.launch_button.config(state=tk.NORMAL)
                self.log_message("\n✓ REDVILLSHELL is ready to launch!", '#00ff00')
            else:
                self.log_message("\n✗ Required files missing. Cannot launch REDVILLSHELL.", '#ff0000')
            
            self.install_button.config(state=tk.NORMAL)
            
        except Exception as e:
            self.log_message(f"✗ Installation failed: {str(e)}", '#ff0000')
            self.install_button.config(state=tk.NORMAL)
    
    def check_required_files(self):
        required_files = ['Main.py', 'Utility.py', 'Arithmetic.py']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            self.log_message(f"Missing files: {', '.join(missing_files)}", '#ff0000')
            return False
        return True
    
    def launch_shell(self):
        if not self.check_required_files():
            messagebox.showerror("Error", "Required files are missing!\nPlease make sure Main.py, Utility.py, and Arithmetic.py are in the same directory.")
            return
        
        try:
            self.log_message("Launching REDVILLSHELL OS...", '#00ff00')
            self.root.destroy()
            from Main import main
            main()
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch REDVILLSHELL:\n{str(e)}")

def main():
    """Main function to run the installer"""
    root = tk.Tk()
    app = REDVILLSHELLInstaller(root)
    root.mainloop()

if __name__ == "__main__":
    main()
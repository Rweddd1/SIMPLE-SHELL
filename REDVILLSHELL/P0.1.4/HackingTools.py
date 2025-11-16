import subprocess
import os
class NetworkH:
    def __init__(self, ssids, password):
        self.ssids
        self.password
        
    def BruteForce(self):
        command = subprocess.run(["netsh", "wlan", "export", "profile",
        "key=Clear"], capture_output = True).stdout.decode()
        
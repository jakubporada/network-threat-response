import json
import time
import re
from netmiko import ConnectHandler

raspberry_pi = {
    'device_type': 'linux',
    'host': '10.0.0.14',
    'username': 'pi',
    'password': 'vaTECH-pi5',
    'port': 22,
}

R0 = {
    'device_type': 'cisco_ios',
    'host': '10.0.0.100',
    'username': 'cisco',
    'password': 'cisco',
}

R1 = {
    'device_type': 'cisco_ios',
    'host': '10.0.0.101',
    'username': 'cisco',
    'password': 'cisco',
}

blocked_ips = set()

def getAlerts(ssh):

    output = ssh.send_command("sudo strings /var/log/suricata/eve.json | grep '\"event_type\":\"alert\"' | head -1")
    alerts = []

    for line in output.strip().split('/n'):
        if not line:
            continue
        try:
            alert = json.load(line)
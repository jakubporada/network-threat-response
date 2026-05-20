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

    output = ssh.send_command("sudo strings /var/log/suricata/eve.json | grep '\"event_type\":\"alert\"' | tail -20")
    alerts = []

    for line in output.strip().split('\n'):
        if not line:
            continue
        try:
            alert = json.loads(line)
            alerts.append(alert)
        except json.JSONDecodeError:
            continue
    return alerts

def block_ip(ip):
    print(f"Blocking {ip} on both Routers")
    for router_config in [R0, R1]:
        try:
            with ConnectHandler(**router_config) as conn:
                commands = [
                    'ip access-list extended BLOCK_THREATS',
                    f'deny ip host {ip} any',
                    'permit ip any any',
                ]
                conn.send_config_set(commands)
                print(f" ACL pushed to {router_config['host']}")

        except Exception as e:
            print(f"[-] Failed to push ACL to {router_config['host']}: {e}")

def run():

    print(" Orchestrator started and will poll every 10 seconds")
    with ConnectHandler(**raspberry_pi) as pi_ssh:
        while True:
            alerts = getAlerts(pi_ssh)
            for alert in alerts:
                src_ip = alert.get('src_ip')
                signature = alert.get('alert', {}).get('signature', '')

                if src_ip not in blocked_ips:
                    print(f" Alert: {signature} from {src_ip}")
                    block_ip(src_ip)
                    blocked_ips.add(src_ip)

            time.sleep(10)

if __name__ == "__main__":
    run()
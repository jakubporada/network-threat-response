from netmiko import ConnectHandler

r0 = {
    "device_type": "cisco_ios",
    "host": "10.0.0.100",
    "username": "cisco",
    "password": "cisco",
}

routers = [("R0", r0)]

for name, config in routers:
    print(f"\n=== {name} Routing Table ===")
    conn = ConnectHandler(**config)
    output = conn.send_command("show ip route")
    print(output)
    conn.disconnect()
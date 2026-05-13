from netmiko import ConnectHandler

router = {
    "device_type": "cisco_ios",
    "host": "10.0.0.100",
    "username": "cisco",
    "password": "cisco",
}

connection = ConnectHandler(**router)
output = connection.send_command("show ip route")
output += connection.send_command('show ip interface brief')
print(output)
connection.disconnect()
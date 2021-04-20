#!/usr/bin/env python3 
import os
from itertools import product, chain

# Tutaj należy wypisać wszystkie interfejsy sieciowe komputera, na których ma być uruchomiona zapora.
# (oprócz interfejsu loopback, on jest przez skrypt traktowany odrębnie)
INTERFACES = [
    "enp3s0",
    "wlp2s0"
]

# Czy zezwalać na pingowanie do tej maszyny?
ALLOW_PINGING = True

# Tryb Dockera, dodający dodatkowe reguły do obsługi kontenerów.
# Ustaw na False, jeżeli nie będziesz używał Dockera.
DOCKER_MODE = True

# Grupy adresów IP do wykorzystania w regułach poniżej.
# Oprócz grup, które wpiszesz poniżej, istnieje jeszcze jedna grupa domyślna - grupa "public".
# Grupa "public" oznacza "wszystkie możliwe adresy IP".
IP_GROUPS = {
    "trusted": [
        "192.168.0.160"
    ]
}

# Domyślnie, firewall blokuje cały ruch przychodzący (oprócz ruchu niezbędnego do działania Internetu).
# W polu poniżej możesz skonfigurować które porty mają być otwarte dla których grup IP. 
OPEN_PORTS = [
    # ("nazwa", "port", "grupa ip", "protokół (tcp, udp lub both)")
    ("minidlna", "8200", "public", "tcp"),

    ("ftp", "20:21", "trusted", "tcp"),
    ("ftp passive", "10090:10100", "trusted", "tcp"),

    ("vnc", "5900", "trusted", "tcp"),

    ("samba", "137:138", "trusted", "udp"),
    ("samba", "139", "trusted", "tcp"),
    ("samba", "445", "trusted", "tcp"),

    ("ssh", "22", "trusted", "tcp")
]

# Otwarte porty dla kontenerów Dockera.
OPEN_PORTS_DOCKER = [
    # ("nazwa", "port kontenera", "port komputera-hosta", "grupa ip", "protokół (tcp, udp lub both)")
    ("apache", "80", "8080", "trusted", "tcp"),
    ("mysql", "3306", "9075", "trusted", "both"),
    ("phpmyadmin", "80", "5000", "trusted", "tcp")
]

# Własne linijki, które zostaną dodane na końcu pliku /etc/iptables/iptables.rules
OWN_RULES = [
]

if not os.geteuid() == 0:
    print("Musisz uruchomić ten skrypt jako root.")
    exit(1)

with open("/etc/iptables/iptables.rules", "w") as rules:
    fw = lambda msg: rules.write(msg + "\n")

    fw("*filter")
    fw(":INPUT DROP [0:0]")
    fw(":FORWARD DROP [0:0]")
    fw(":OUTPUT ACCEPT [0:0]")

    if DOCKER_MODE:
        fw("-N DOCKER-USER")

    if ALLOW_PINGING:
        fw("\n# Allow ICMP (allow pinging this device)")
        fw("-A INPUT -p icmp --icmp-type 8 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT")

    fw("\n# Allow loopback traffic")
    fw("-A FORWARD -i lo -j ACCEPT")
    fw("-A INPUT -i lo -j ACCEPT")

    fw("\n# Allow DHCP incoming data")
    fw("-I INPUT -p udp --dport 67:68 --sport 67:68 -j ACCEPT")

    fw("\n# Allow established and related connections")
    fw("-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT")
    fw("-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")

    if DOCKER_MODE:
        fw("\n# Drop connections from network interfaces by default")
        for interface in INTERFACES:
            fw(f"-I DOCKER-USER -i {interface} -j DROP")

        fw("\n# Allow Docker loopback connections")
        fw("-A DOCKER-USER -i lo -j ACCEPT")
        fw("-I DOCKER-USER -i lo -j ACCEPT")

        fw("\n# Access rules for specific containers")
        for name, container_port, host_port, ip_group, protocol in OPEN_PORTS_DOCKER:
            instruction_scheme = [["-I DOCKER-USER"]]

            if ip_group != "public":
                instruction_scheme.append(["-s"])
                instruction_scheme.append(IP_GROUPS[ip_group])

            prot = ["udp", "tcp"] if protocol == "both" else [protocol]
            instruction_scheme.append(["-p"])
            instruction_scheme.append(prot)

            instruction_scheme.append([f"--dport {container_port}"])
            instruction_scheme.append([f"-m conntrack --ctorigdstport {host_port}"])
            instruction_scheme.append(["-j ACCEPT"])

            instructions = [" ".join(instr) for instr in product(*instruction_scheme)]
            for instruction in instructions:
                fw(instruction)

        fw("\n# Allow internet for Docker")
        fw("-I DOCKER-USER -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT")
        fw("-I DOCKER-USER -m state --state ESTABLISHED,RELATED -j ACCEPT")

    fw("\n# Allow input traffic to specific ports")
    for name, port, ip_group, protocol in OPEN_PORTS:
        instruction_scheme = [["-A INPUT"]]

        if ip_group != "public":
            instruction_scheme.append(["-s"])
            instruction_scheme.append(IP_GROUPS[ip_group])

        prot = ["udp", "tcp"] if protocol == "both" else [protocol]
        instruction_scheme.append(["-p"])
        instruction_scheme.append(prot)

        instruction_scheme.append(["--dport"])
        instruction_scheme.append([port])

        instruction_scheme.append(["-j ACCEPT"])

        instructions = [" ".join(instr) for instr in product(*instruction_scheme)]
        for instruction in instructions:
            fw(instruction)

    if len(OWN_RULES) != 0:
        fw("\n# Custom rules (from firewall.py)")
        for rule in OWN_RULES:
            fw(rule)

    fw("\nCOMMIT")

print("Zmodyfikowano plik /etc/iptables/iptables.rules")
if DOCKER_MODE:
    print("Użyj systemctl restart iptables && systemctl restart docker, aby zmiany weszły w życie.")
else:
    print("Użyj systemctl restart iptables, aby zmiany weszły w życie.")

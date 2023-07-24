#!/bin/bash

# Set IP address for vboxnet0 interface
VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1

# Set iptables rules
sudo iptables -t nat -A POSTROUTING -o enp7s0 -s 192.168.56.0/24 -j MASQUERADE
sudo iptables -P FORWARD DROP
sudo iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -s 192.168.56.0/24 -j ACCEPT
sudo iptables -A FORWARD -s 192.168.56.0/24 -d 192.168.56.0/24 -j ACCEPT
sudo iptables -A FORWARD -j LOG

# Enable IP forwarding
echo 1 | sudo tee -a /proc/sys/net/ipv4/ip_forward
sudo sysctl -w net.ipv4.ip_forward=1

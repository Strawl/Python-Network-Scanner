from scanner import PortScanner, NetworkScanner
import asyncio
import threading

network = {}


def network_scan(string):
    global network
    n_scanner = NetworkScanner()
    splitted = string.split()
    ip_str = splitted[2].split(".")
    ip_end = splitted[3].split(".")
    n_scanner.set_range([range(int(ip_str[0]), int(ip_end[0]) + 1),
                         range(int(ip_str[1]), int(ip_end[1]) + 1),
                         range(int(ip_str[2]), int(ip_end[2]) + 1),
                         range(int(ip_str[3]), int(ip_end[3]) + 1)])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(n_scanner.scan(loop))
    print("the network scan is completed")
    if len(results) != 0:
        for ip in results:
            if ip not in network:
                network[ip] = []
    else:
        print("no adresses were found")


def port_scan(string):
    global network
    p_scanner = PortScanner()
    splitted = string.split(" ")
    p_scanner.set_ip_address(splitted[2])
    p_scanner.set_port_range(range(int(splitted[3]), int(splitted[4]) + 1))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(p_scanner.scan(loop))
    print("port scan completed")
    if len(results) != 0:
        network[splitted[2]] = results
    else:
        print("no ports were found")


def program():
    global network
    print("Welcome to the Portscanner")
    print()
    help_commands = [
        "",
        "Here are the possible commands:",
        "",
        "\tscan network <start_ip> <end_ip>",
        "\texample:",
        "\t\tscan network 192.168.0.10 192.168.0.30",
        "",
        "\tscan ports <ipaddress> <startport> <endport>",
        "\texample:",
        "\t\tscan ports 192.168.0.1 0 6500",
        "",
        "\tview network",
        "",
        "\tclear network",
        "",
        "\thelp",
        "",
        "\texit"
    ]
    [print(x) for x in help_commands]
    while True:
        i = input()
        if i == "help":
            [print(x) for x in help_commands]
        if i == "exit":
            break
        if i == "view network":
            if len(network) == 0: print("the netowork is empty")
            for key in network.keys():
                print(key)
                for ports in network[key]:
                    print("\t", ports)
        if i == "clear network":
            network = {}
            print("network cleared")
        if "scan ports" in i:
            threading.Thread(target=port_scan, args=[i]).start()
        if "scan network" in i:
            threading.Thread(target=network_scan, args=[i]).start()


if __name__ == '__main__':
    program()

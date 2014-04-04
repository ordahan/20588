from server.server import RTSPServer
from netifaces import interfaces, ifaddresses, AF_INET

if __name__ == '__main__':

    choose_ip_dict = {}

    print "Available IPs:"
    ip_index = 0
    for ifaceName in interfaces():

        for address_list in [address
                        for type_, address in ifaddresses(ifaceName).items()
                        if type_ == AF_INET ]:

            for ip_address in address_list:
                choose_ip_dict[ip_index] = ip_address['addr']
                print str(ip_index) + ": " + choose_ip_dict[ip_index]
                ip_index += 1

    while(True):
        user_chosen_ip_index = int(raw_input("Choose an IP index from the list above: "))

        if (user_chosen_ip_index not in choose_ip_dict.keys()):
            print "Chosen an invalid index, try again."
        else:
            RTSPServer(choose_ip_dict[user_chosen_ip_index]).run()
            break

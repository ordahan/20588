
from server.server import RTSPServer
from netifaces import interfaces, ifaddresses, AF_INET

class Main (object):
    '''
    RTSP Server startup.

    Displays the user a list of valid IP's on this machine.

    The server is initialized with the chosen IP, and port 8554.
    '''

    def get_valid_ips(self):
        '''
        Get all valid IP's that we can listen to
        '''
        choose_ip_dict = {}
        print "Available IPs:"
        ip_index = 0
        for ifaceName in interfaces():
            for address_list in [address for type_, address in ifaddresses(ifaceName).items() if
                type_ == AF_INET]:
                for ip_address in address_list:
                    choose_ip_dict[ip_index] = ip_address['addr']
                    print str(ip_index) + ": " + choose_ip_dict[ip_index]
                    ip_index += 1

        return choose_ip_dict

    def user_selects_ip(self):
        '''
        User selects a valid IP
        '''
        choose_ip_dict = self.get_valid_ips()

        while True:
            user_chosen_ip_index = int(raw_input("Choose an IP index from the list above: "))
            if (user_chosen_ip_index not in choose_ip_dict.keys()):
                print "Chosen an invalid index, try again."
            else:
                selected_ip = choose_ip_dict[user_chosen_ip_index]
                break

        return selected_ip

    def run(self):
        '''
        Let's get this show on the road!
        '''
        selected_ip = self.user_selects_ip()

        RTSPServer(selected_ip).run()
if __name__ == '__main__':
    Main().run()

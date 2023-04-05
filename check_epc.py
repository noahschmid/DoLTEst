import subprocess, os
#print(subprocess.check_output(['tshark', '-r', 'epc.pcap']))


def parse_file(filename):
    os.system(f"tshark -r {filename} > tmp.txt")

    current_state = 0
    highest_msg = ''

    states = ['No_SC', 'N-SC', 'NR-SC', 'REGI']
    no_sc_msgs = ['InitialUEMessage, Attach request', 'Identity request', 'Identity response', 'Authentication request', 'Authentication response']
    valid_test_msgs = ['Identity request', 'Security mode command', 'GUTI reallocation command', 'Service request', 'EMM information', 'Downlink NAS transport(DTAP)', 'Attach reject', 'Attach accept']

    file = open("tmp.txt", "r")
    lines = file.readlines()
    line_no = 0
    file.close()
    os.remove("tmp.txt")

    bugs_found = 0
    test_msg = ''

    def parse_line(line):
        return line[::-1].split('  ')[0][::-1][:-1]

    for line in lines:
        line_no += 1
        msg = parse_line(line)

        if line.find('S1AP/NAS-EPS') == -1: # not interesting
            continue

        if msg.find('DownlinkNASTransport') != -1:
            test_msg = msg

        if msg.find('InitialUEMessage, Attach request') != -1:
            highest_msg = 'InitialUEMessage'
            current_state = 0

        #
        # Establishing NAS security context (No_SC -> N-SC)
        #
        elif msg.find('Authentication request') != -1 and states[current_state] == 'No_SC':
            highest_msg = 'Authentication request'

        elif msg.find('Authentication response') != -1 and highest_msg == 'Authentication request' and states[current_state] == 'No_SC':
            highest_msg = 'Authentication response'

        elif msg.find('Security mode command') != -1 and highest_msg == 'Authentication response' and states[current_state] == 'No_SC':
            highest_msg = 'Security mode command'

        elif msg.find('Security mode complete') != -1 and highest_msg == 'Security mode command' and states[current_state] == 'No_SC':
            highest_msg = 'Security mode complete'
            current_state += 1
            
        #
        # Establishing RRC security context (N_SC -> NR-SC)
        #
        elif msg.find('RRC security mode command') != -1 and states[current_state] == 'N-SC':
            highest_msg = 'RRC security mode command'

        elif msg.find('RRC security mode complete') != -1 and highest_msg == 'RRC security mode command' and states[current_state] == 'N-SC':
            highest_msg = 'RRC security mode complete'
            current_state += 1

        #
        # Finishing registration (NR_SC -> REGI)
        #
        elif msg.find('NAS attach accept') != -1 and states[current_state] == 'NR-SC':
            highest_msg = 'NAS attach accept'

        elif msg.find('NAS attach complete') != -1 and highest_msg == 'NAS attach accept' and states[current_state] == 'NR-SC':
            highest_msg = 'NAS attach complete'
            current_state += 1

        #
        # Releasing UE
        #
        elif msg.find('UEContextReleaseRequest') != -1:
            if highest_msg == 'RRC security mode complete':
                print("")
                print("[!] Bug found [!]")
                print("State: " + states[current_state-1])
                print("Message number: " + str(line_no))
                print("Test message: " + test_msg)
                print('Response: ' + msg)

            bugs_found += 1
            highest_msg = ''
            current_state = 0

        #
        # Everything else on the uplink could be a bug
        #
        elif msg.find('UplinkNASTransport') != -1:
            # UE sending an error message is not a bug
            if msg.find('Security mode reject') != -1 or msg.find('Detach request') != -1 or msg.find('EMM status') != -1 or msg.find('Authentication failure') != -1:
                continue

            # UE sending identity response in state No_SC is not a bug
            if msg.find('Identity response') != -1 and states[current_state] == 'No_SC':
                continue

            # Test if response responds to a valid test msg
            #test_msg = parse_line(lines[line_no-2])
            valid_test_msg = False
            for tmsg in valid_test_msgs:    
                if test_msg.find(tmsg) != -1:
                    valid_test_msg = True

            if not valid_test_msg:
                continue

            # UE sending RRC ConnectionReconfigurationComplete 

            print("")
            print("[!] Bug found [!]")
            print("State: " + states[current_state])
            print("Message number: " + str(line_no))
            print("Test message: " + test_msg)
            print('Response: ' + msg)

            bugs_found += 1

    print("\n-------------------")
    print(f"Bugs found: {bugs_found}")


import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 parse.py [PCAP_FILENAME]")
        exit()
    parse_file(sys.argv[1])   
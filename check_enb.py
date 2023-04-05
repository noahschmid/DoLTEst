import subprocess, os
#print(subprocess.check_output(['tshark', '-r', 'epc.pcap']))


def parse_file(filename):
    target_state = 'No_SC'
    target_msg = ''
    target_mac = ''
    meas_config = False
    highest_line = ''
    ie = ''

    no_sc_lines = ['InitialUEMessage, Attach request', 'Identity request', 'Identity response', 'Authentication request', 'Authentication response']

    test_active = False
    test_msg_sent = False
    try:
        file = open(filename, "r")
    except:
        print("File not found")
        exit(-1)
    lines = file.readlines()
    line_no = 0
    file.close()

    bugs_found = 0

    def parse_line(line):
        return line[::-1].split('  ')[0][::-1][:-1]

    for line in lines:
        line_no += 1
        

        if line.find('------- [DoLTEst] Preparing next test message.. -------') != -1:
            test_active = True
            test_msg_sent = False
            ie = ''
            continue

        if line.find('<--- RRC Connection Request') != -1:
            test_active = False
            continue

        if line.find('---> Target State : ') != -1 and test_active == True:
            target_state = line.split(': ')[1].split(' ')[0]
            continue

        if line.find('---> Target Msg   : ') != -1 and test_active == True:
            target_msg = line.split(': ')[1].split(' ')[0]
            continue

        if line.find('---> Target MAC   : ') != -1 and test_active == True:
            target_mac = line.split(': ')[1].split(' ---')[0]
            test_msg_sent = True
            continue

        if line.find("---> Sent test message with IE,") != -1 and test_active == True:
            test_msg_sent = True
            meas_config = line.find('measConfig')  != -1
            ie = line.split('IE,')[1].split(' --->')[0]
            continue

        if line.find('==== [DoLTEst] No RRC response from UE ====') != -1 and test_active == True and test_msg_sent == True:
            test_msg_sent = False
            test_active = False
            
            continue

        elif line.find('<---') != -1 and test_active == True and test_msg_sent == True:
            if line.find('ULInformationTransfer') != -1 or line.find('RRC Connection Setup Complete') != -1:
                continue

            # Response to UECapabilityEnquiry is not a bug
            if line.find('(RRC)UECapabilityInformation') != -1:
                continue

            # UE sending an error message is not a bug
            if line.find('RRC Security Mode Failure') != -1 or line.find('RRC Connection Reestablishment Request') != -1:
                continue

            # UE sending RRC ConnectionReconfigurationComplete with measConfig is not a bug
            if (line.find("RRC Connection Reconfiguration Complete") != -1 or line.find("RRCConnectionReconfigurationComplete") != -1) and target_state in ["No-SC", "N-SC"] and target_msg == "RRCConnectionReconfiguration" and meas_config == True:
                continue

            print("")
            print("[!] Bug found [!]")
            print(f"Line number: {line_no}")
            print("Target state: " + target_state)
            print("Target msg: " + target_msg)
            print("Target MAC: " + target_mac)
            
            if target_msg == "RRCConnectionReconfiguration":
                #print("measConfig: " + str(meas_config))
                print('IE: ' + ie)
            print('Response: ' + line)

            bugs_found += 1

            test_msg_sent = False
            test_active = False

    print("\n-------------------")
    print(f"Bugs found: {bugs_found}")


import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 parse.py [PCAP_FILENAME]")
        exit()
    parse_file(sys.argv[1])   
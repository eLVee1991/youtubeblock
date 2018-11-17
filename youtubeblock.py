#!/bin/env/python

import os
import re
try:
    import pexpect as p
except ImportError:
    print("[+] Pexpect not installed. Please run: 'pip install pexpect' in command line.")
    exit()

raw_addlist = "youtube_raw_addlist.log"
all_queries = "all_queries.log"
blocklist = "blocklist.txt"
logfile = "/var/log/pihole.log"
    
# Regex used to match relevant loglines (in this case, a specific IP address)
prefix = [
"r1---sn-",
"r2---sn-",
"r3---sn-",
"r4---sn-",
"r5---sn-",
"r6---sn-",
"r7---sn-",
"r8---sn-",
"r9---sn-",
"r10---sn-",
"r11---sn-",
"r12---sn-",
"r13---sn-",
"r14---sn-",
"r15---sn-",
"r16---sn-",
"r17---sn-",
"r18---sn-",
"r19---sn-",
"r20---sn-",
".sn-"
]

class colors:
    """
    Class specifically for message fuction below.
    Contains colors and fonts.
    """
    UNDERLINE = '\033[4m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    END = '\033[0m'

def message(state, msg):
    """
    Function that creates print statements with fonts and colors.
    """
    if state == "underline":
        print(colors.UNDERLINE + msg + colors.END)
    elif state == "green":
        print(colors.GREEN + msg + colors.END)
    elif state == "red":
        print(colors.RED + msg + colors.END)
    elif state == "bold":
        print(colors.BOLD + msg + colors.END)
    else:
        print("Wrong state. Please try: 'underline', 'green', 'red'")


def text():
    message("red", """
Yb  dP .d88b. 8    8 88888 8    8 888b. 8888 
 YbdP  8P  Y8 8    8   8   8    8 8wwwP 8www 
  YP   8b  d8 8b..d8   8   8b..d8 8   b 8    
  88   `Y88P' `Y88P'   8   `Y88P' 888P' 8888 
                                             
    8    8            8    8 w       w        
    88b. 8 .d8b. .d8b 8.dP 8 w d88b w8ww      
    8  8 8 8' .8 8    88b  8 8 `Yb.  8        
    88P' 8 `Y8P' `Y8P 8 Yb 8 8 Y88P  Y8P      
""")
    message("underline", "Pihole unique YouTube advertisement url checker")
    message("underline", "Created by eLVee")
    print("")

def check_raw():
    """
    Checks the pihole logs for the prefix var above. 
    Saves the raw data that needs to be sorting to 'youtube_raw_addlist.log'
    """
    output_filename = os.path.normpath(raw_addlist)
    message("green", "[+] Checking for youtube fingerprint..")
    for url in prefix:
        line_regex = re.compile(r".*"+url+".*$")
        with open(output_filename, "a+") as out_file:
            with open(logfile, "r") as in_file:
                for line in in_file:
                    if (line_regex.search(line)):
                        #print line
                        out_file.write(line)
                    else:
                        #print(url+" not found trying again")
                        continue
            in_file.close()
        out_file.close()

def query_list():
    """
    Checks 'youtube_raw_addlist.log' for the word 'query', so we know for sure it's outgoing.
    Then saves that data to 'all_queries.log' for further sorting.
    """
    output_filename = os.path.normpath(all_queries)
    line_regex = re.compile(r".*"+"query"+".*$")
    with open(output_filename, "a+") as out_file:
        with open(raw_addlist, "r") as in_file:
            for line in in_file:
                if (line_regex.search(line)) and "googlevideo.com" in line:
                    words = line.split(" ")
                    #print words[8]
                    out_file.write(words[8]+"\n")
                else:
                    #print(url+" not found trying again")
                    continue
        in_file.close()
    out_file.close()



def blocklist():
    """
    Check the the file 'all_queries.log' for unique urls and sorts them.
    Then check the blocklist.txt if the urls is already present. If not, adds it. 
    """
    uniquelines = set(open(all_queries).readlines())
    for line in uniquelines:
        with open(blocklist, "r") as in_file:
            if line in in_file:
                #print("> "+line+" Already in 'blocklist.txt'.")
                pass
            else:
                with open(str(blocklist), "a") as out_file:
                    out_file.write(line.rstrip()+" ")
                out_file.close()
        in_file.close()
    

def add_to_pihole():
    """
    Uploads the contents of 'blocklist.txt' to the pihole with the command pihole -b
    """
    with open(blocklist, 'r') as in_file:
        line = in_file.read()
        #print("[+] Adding "+line+" to pihole.")
        command = p.spawnu("pihole -b "+line)
        command.interact()
        #print("[+] Done.")
        command.close()
        command = p.spawnu("pihole restartdns")
        command.interact()
        command.close()
    in_file.close()

def delete_logs():
    """
    Delete the files 
    - youtube_raw_addlist.log
    - all_queries.log

    to keep it nice and clean.
    """
    command = p.spawnu("rm -rf youtube_raw_addlist.log all_queries.log")
    command.interact()
    command.close()



text()
message("green", "[+] Checking all dns requests for YouTube queries.")
check_raw()
message("bold", "[+] Done checking requests.")
message("green", "[+] Sorting urls..")
query_list()
message("bold", "[+] Done sorting urls for queries.")
message("green", "[+] Sorting for unique urls and adding to list 'blocklist.txt'..")
blocklist()
message("bold", "[+] Done adding to blocklist.")
message("green", "[+] Adding contents of blocklist to pihole.")
add_to_pihole()
message("bold", "[+] Done adding to pihole.")
message("bold", "[+] Finished.")
delete_logs()

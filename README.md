# youtubeblock.py
This python file will search the pihole logs for youtube advertisement urls and adds them to the blocklist.
Run this script once a day or after seeing advertisement. 

For now it searches the logs for:
- r1---sn-
- r2---sn-
- r3---sn-
- r4---sn-
- r5---sn-
- r6---sn-
- r7---sn-
- r8---sn-
- r9---sn-
- r10---sn-
- r11---sn-
- r12---sn-
- r13---sn-
- r14---sn-
- r15---sn-
- r16---sn-
- r17---sn-
- r18---sn-
- r19---sn-
- r20---sn-
- .sn-

as described in https://discourse.pi-hole.net/t/how-do-i-block-ads-on-youtube/253/237

run this command on pihole (over ssh):
- git clone https://github.com/eLVee1991/youtubeblock.git
- sudo apt-get install python-pip (If python2 is not pre-installed)
- pip install pexpect
- cd youtubeblock
- python youtubeblock.py

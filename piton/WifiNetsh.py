# this import file is for CMD
import subprocess
#this for make us of regular expression
import re

#declare ke cmd dengan menggunakan string
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
#mendapatkan semua profile wifi yang terjangkau
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
#empty list untuk daftar wifi yg ditemukan
wifi_list = list()

#check apakah bisa ditemukan tidaknya koneksi ke wifi dan paswortnya 
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        #ngecek sekuriti wifi present tidaknya (openport)
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            #capture group dari password wifi yang tersedia
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile)

for x in range(len(wifi_list)):
    print(wifi_list[x])


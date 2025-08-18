#!/usr/bin/env python3
import os
import sys
import subprocess
import getpass
import time
import shutil
from typing import List, Optional

print("""
⠀⠀⠀⠀⣄⠀⠀⢰⡆⠀⠀⢠⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⢀⢀⢠⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⢠⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⡄⠀⣾⡇⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⢒⣭⠉⠥⢌⡋⠐⠀⠠⠦⠍⢉⡃⢴⠂⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⢸⡇⠀⢀⡆⠀⠀⠀
⠈⣦⠀⠀⢻⡇⠀⣿⡇⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢤⠈⠔⠀⣉⣥⣶⣶⣬⣭⣼⣿⣿⣶⣤⣄⠰⠶⠐⠀⢁⡀⠀⠀⠀⠀⠆⡀⢀⣀⡀⠀⣶⣒⡀⠀⠀⠀⠀⠀⠀⡀⠀⠀⣿⡀⠀⢸⡇⠀⣸⡇⠀⠀⠀
⠀⠸⣇⠀⢸⣧⠀⣿⡇⠀⣿⠇⠀⠀⣀⣀⣀⣀⣀⣀⣚⣒⣒⣋⣛⣚⣡⡤⠁⠴⠠⠗⣸⣿⣿⣿⡟⣻⣿⣿⣿⣿⣿⡿⣿⣿⣿⣶⣿⣷⣄⠁⢀⢼⡴⢰⣾⣷⣿⣿⣿⣶⣶⣶⣿⣭⣿⣿⣿⣿⣤⣤⣙⣀⢹⣇⠀⢸⡇⠀⣿⠁⠂⣰⠃
⠀⠀⢻⣆⣸⣿⣶⣿⣷⣾⣿⠀⣴⡞⢋⣨⡍⢻⣿⣿⣿⣿⣿⣿⣿⣿⠟⣠⠃⣰⣿⣿⡟⣻⣿⣿⢡⣿⣿⣿⣿⣿⣿⡇⢻⣿⣿⣿⣿⣏⢻⣿⠰⠖⠀⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⡛⠻⣿⣿⢸⣿⣄⣼⣇⣸⣿⠘⢰⡏⣸
⠀⠀⠈⣿⣿⠿⢛⣋⣵⡿⢛⡀⠊⣰⡿⢃⣴⣿⣿⣿⣿⣿⣿⣿⡿⠏⣰⡟⣰⣿⣿⡟⣰⣿⣿⡏⣼⣿⣿⣿⣿⣿⣿⡇⡌⠿⢿⣇⢻⡿⠂⢿⣷⠖⠀⠰⠀⠀⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠹⣷⡌⠻⢸⣿⣛⠻⢿⣿⣿⣦⡙⢰⣿
⠀⠀⡆⣾⣷⣾⣿⣿⢋⣴⣿⣿⣿⡟⢁⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⣰⣿⠁⡁⡌⢻⢃⡿⡀⣿⡇⣿⣿⣿⣿⣿⣿⣿⡇⣿⣄⢠⡤⠀⠀⠺⠘⣿⠀⠀⠀⠀⠀⡄⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡘⣿⣦⣶⣭⠻⣿⣶⣬⣝⣿⡇⣿⣿
⢸⢹⡇⠸⣿⣿⣿⣯⣾⣿⣿⣿⠟⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢰⡏⣤⣃⣴⣾⢸⣷⣶⣿⢰⣿⣿⣿⣿⡇⣿⣿⢇⣿⣿⣆⠀⣴⢸⣶⡆⣿⠀⠈⠀⠀⠈⠁⢁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⣿⣿⣿⣷⠸⣿⣿⣿⣿⢀⣿⣿
⢸⢻⣿⡀⢻⣿⣿⣿⣿⣿⡿⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡄⣿⠃⣿⣿⣿⣿⢸⡇⣿⣿⢸⣿⣿⣿⣿⡇⣿⣿⢠⣴⣶⣮⣤⠹⡌⣿⡇⣿⡏⠀⡆⠀⠐⠄⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡘⢿⣿⣿⣷⣿⣿⣿⡏⣸⣿⣿
⢸⢿⣿⣷⠠⢉⣩⣽⣿⡷⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⠁⣿⠀⣿⣿⡏⣿⢸⡇⣿⣿⢸⢿⣿⣿⣿⠇⣿⡇⣜⣩⠽⠻⠿⣷⡀⣿⡇⣿⡧⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠙⣉⣽⣟⠻⠏⣰⣿⣿⣿
⣾⡿⠟⣋⠀⣿⣿⣿⡿⠇⣀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⠀⣿⡇⣿⣿⡇⣿⢸⣷⢸⣿⡘⡘⣿⣿⣿⢰⣿⢱⢃⡀⠀⠀⠀⠈⠃⢹⠇⣿⠇⠆⡆⢰⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣀⠀⢿⣿⣿⣿⠀⠿⣿⣿⣿
⣩⣴⠾⠛⣀⣭⡥⠶⠖⠋⠁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⠀⢻⡇⢸⡟⣿⢸⡌⣿⡈⣿⡇⠇⣿⣿⣿⢸⠇⣾⣿⡇⢀⠀⠀⡷⢰⠸⢰⡿⠈⠀⡇⠘⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠈⠙⠒⠦⣭⡛⠸⣶⣬⡙⠿
⣭⠴⠚⠋⠉⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠰⠘⣇⠈⢧⠹⡄⠳⣘⣃⣹⣃⣀⣹⣿⣟⣘⣸⣿⣿⣿⣦⣭⣼⣷⡏⠂⠁⠠⠘⢰⠃⢀⡄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠉⠓⠦⣍⡛⢷
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠹⡐⡈⢆⠱⠸⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣷⢄⣀⠔⡀⡜⠀⢈⡇⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⡀⠈⢦⣀⠀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣬⠁⠌⠀⣰⠀⣼⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡈⠍⢣⡈⢿⣿⣿⣿⣿⣝⣛⣿⣿⣻⣿⣿⣿⣿⡿⢋⡼⠃⠘⣠⣾⣿⠀⢿⣷⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣦⣀⡑⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠛⣡⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠
⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣴⣷⣦⡙⢿⣿⣿⣿⣿⣿⡆⢀⡀⣌⡉⠛⠿⠛⣋⣥⡆⡨⠐⢶⣿⣿⣿⣿⣿⣿⠟⣋⣥⣦⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣄⢛⠛⢿⣿⣿⡆⢆⢡⣬⡙⠗⣒⠻⢋⣥⡅⠔⠁⣾⣿⣿⡿⠿⠟⣡⣾⣿⣿⣿⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿
⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⠿⠿⣿⣿⣿⣿⣿⠟⡉⢡⡌⣿⣿⣿⣿⡇⣾⣿⡆⢨⣄⠲⢮⡀⢿⣿⣆⣿⣠⣿⠟⠁⣢⣶⣶⡌⡅⣶⣿⡆⣿⣿⣿⠿⡏⣼⢙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿
⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⢡⡞⠡⢤⣆⢈⠍⣷⣬⡁⠙⢿⡇⡜⣿⣿⡦⠉⠀⡁⠀⠀⠀⢀⠈⠛⢿⣿⣿⢃⢣⣿⠟⠐⣋⣿⠀⢄⣤⣙⣀⠳⣌⣛⡛⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿
⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⢿⣿⣿⣿⡶⢸⡆⢼⣿⣿⡟⠀⣿⣷⡐⡘⢿⡀⠰⠟⠀⠀⣆⠀⠈⠻⠆⢀⡿⢃⢂⣾⣿⠀⢺⣿⣿⣷⠸⣿⠩⣥⣶⣾⣦⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿
⢸⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣯⣅⠰⣿⣇⠘⣿⣿⡇⠀⢨⠍⣿⣬⡊⠑⠄⢠⠆⢠⣿⠀⢣⡀⠀⡊⢔⣡⣟⢛⡁⠀⢸⣿⣿⠃⣾⣿⣷⠌⣩⣿⡙⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
⢸⣿⣿⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢛⠿⠝⢋⡬⠵⣷⠌⡃⠁⠀⣿⣷⣌⣛⡛⢶⣬⣤⠀⣀⣀⡀⢐⣢⣥⡖⠿⠿⢋⣼⣧⠀⢈⣬⠠⣄⣛⣛⠰⠾⠿⠟⢛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿
⢸⣿⢿⣿⣿⣿⣷⣤⣶⣶⣴⣦⣤⣄⣀⣀⣀⣀⣊⡙⢷⡌⢭⣭⣤⡈⢰⣿⠀⣸⣿⣿⣿⣿⣿⣦⣭⡅⠀⣈⣋⡀⠨⣙⣩⣴⣾⣿⣿⣿⣿⡄⠸⣿⠆⠛⣛⣛⣛⠂⣴⡾⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣾⣿⣿⣿⣿⣿
⠠⠉⠉⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣶⣤⣼⣿⣿⣿⡄⠛⠀⣡⣬⣉⣴⣌⢛⣛⠻⣷⣴⠻⡟⣡⣶⡿⠿⠻⢛⣩⡙⣋⣍⠃⠀⡋⠐⣀⣿⣿⣇⣚⣡⣴⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠑⠂⠈⠹⢻⣿⣿⣿⣿⣿⣿⣻⣿⣾⣿⣻⣿⣿⣿⣿⣿⣿⣷⠀⣴⣿⣿⣿⣿⣿⣿⣿⣧⣉⣍⠃⠁⣫⣭⣰⣿⣿⣿⣿⣿⣿⣿⣿⡀⡔⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠈⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⡿⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠃⠈⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⡿⣿⠿⠿⠿⠟⠛⠋⠉⠈
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠉⠉⠛⠛⠋⠛⢻⡿⢻⠻⠆⠰⣨⠻⡏⣿⣿⣿⣿⣿⣿⣿⣀⡄⢦⣴⣿⣿⣿⣿⣿⣿⣿⢻⣿⠟⡀⢸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠉⠙⠋⠙⠂⠐⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣈⡁⠀⠀⢀⣀⣉⣁⡂⠨⢉⣩⣭⣁⢶⠆⢈⣠⣤⣁⠉⡙⣛⢛⣛⣋⡉⣈⢡⠞⢀⡈⠉⣉⣉⣉⣉⠉⢉⣉⣉⣉⠙⠙⠉⠉⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⢹⡀⠀⢸⣇⣀⣀⠗⠀⢺⣄⣂⠙⠀⢰⡏⠀⠀⠘⣇⠀⣻⠈⠛⠋⠃⣿⠈⠀⢸⡇⠀⠀⢸⡇⠀⠀⢸⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠤⠬⣧⠀⢸⡏⠉⠉⣷⠀⣀⠈⠉⢹⡆⠸⣇⠂⠠⢢⡏⠀⢿⠀⠀⠀⠀⣿⠀⠀⢸⡇⠀⠀⢸⡇⠀⠀⢸⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠘⠂⠘⠛⠛⠛⠁⠀⠈⠛⠒⠋⠀⠀⠈⠓⠚⠋⠀⠀⠘⠛⠛⠛⠀⠈⠓⠒⠋⠀⠀⠀⠘⠃⠀⠀⠘⠛⠛⠛⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣶⣦⣄⠀⠀⠀⢰⣶⣶⡆⠀⠀⣶⣶⣶⣄⠀⠀⠀⠀⠀⣶⣶⡆⠀⠀⢰⣶⣶⣶⣶⣶⣶⣶⣶⣶⡆⠀⠀⣶⣶⣶⣶⡄⠀⠀⠀⠀⢰⣶⣶⣶⣶⠀⠀⠀⠀⠀⠀⢀⣶⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣼⣿⡿⠉⠀⠀⠈⠙⢿⣿⣧⠀⠀⢸⣿⣿⡇⠀⠀⣿⣿⣿⣿⣆⠀⠀⠀⠀⣿⣿⠀⠀⠀⢸⣿⣿⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⣿⣿⡟⣿⣷⠀⠀⠀⠀⣾⣿⢻⣿⣿⠀⠀⠀⠀⠀⠀⣼⣿⠏⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⠀⠀⠀⠀⠀⠀⠘⠛⠛⠃⠀⢸⣿⣿⡇⠀⠀⣿⣿⡇⠹⣿⣦⠀⠀⠀⣿⣿⡇⠀⠀⣸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⢹⣿⡆⠀⠀⢰⣿⡏⢸⣿⣿⠀⠀⠀⠀⠀⣸⣿⡟⠀⢹⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⣿⣿⣧⠀⠹⣿⣧⡀⠀⣿⣿⡇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⣿⣿⡇⠀⣿⣿⠀⠀⣾⣿⠁⢸⣿⣿⠀⠀⠀⠀⢠⣿⣿⠃⠀⠈⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢿⣿⣷⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⢸⣿⣿⡇⠀⠀⣿⣿⡟⠀⠀⠘⣿⣷⡀⣿⣿⡇⢀⣤⢸⣿⣿⠠⣴⡀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠸⣿⡇⢠⣿⡏⠀⢸⣿⣿⠀⠀⠀⠀⣾⣿⣯⣤⣤⣤⣼⣿⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⢿⣿⣧⣀⠀⠀⠀⣀⣼⣿⡟⠀⠀⢸⣿⣿⡇⠀⠀⢿⣿⣿⠀⠀⠀⠘⢿⣿⣿⣿⡇⡃⣿⢸⣿⣿⣈⣘⣡⣀⣀⣀⣀⡀⠀⠀⣿⣿⡇⠀⠀⢿⣷⣾⣿⠁⠀⢸⣿⣿⠀⠀⠀⣸⣿⡿⠻⠿⠿⠿⠿⢿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⢸⣿⣿⠇⠀⠀⢼⣿⡿⠀⠀⠀⠀⠈⢿⣿⣿⡇⠃⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⡇⠀⠀⠘⣿⣿⡏⠀⠀⢸⣿⣿⠀⠀⢰⣿⣿⠇⠀⠀⠀⠀⠀⠘⣿⣿⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠂⠀⠀⠀⠀⠀⠀⠀⠀⠒⠒⠀⠘⠛⠛⠒⠒⠒⠒⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")

def run_command(cmd: List[str], check: bool = True) -> None:
    """Выполнить команду с проверкой результата"""
    print(f"⌛ Выполняю: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=check)
    except subprocess.CalledProcessError as e:
        print(f"✖ Ошибка при выполнении команды: {' '.join(cmd)}", file=sys.stderr)
        sys.exit(1)

def check_root() -> None:
    """Проверка прав root"""
    if os.geteuid() != 0:
        print("✖ Скрипт должен быть запущен от имени root!", file=sys.stderr)
        sys.exit(1)

def check_internet() -> None:
    """Проверка интернет-соединения"""
    try:
        subprocess.run(["ping", "-c", "1", "archlinux.org"],
                      check=True,
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("✖ Нет интернет-соединения!", file=sys.stderr)
        sys.exit(1)

def select_disk() -> str:
    """Выбор диска для установки"""
    print("Доступные диски:")
    run_command(["lsblk", "-d", "-e", "7,11", "-o", "NAME,SIZE,MODEL"])
    print()

    while True:
        disk = input("Введите диск для установки (например: sda или nvme0n1): ").strip()
        if not disk:
            continue

        disk_path = f"/dev/{disk}"
        if os.path.exists(disk_path):
            confirm = input(f"⚠ ВСЕ ДАННЫЕ НА ДИСКЕ {disk_path} БУДУТ УДАЛЕНЫ! Продолжить? (y/N): ").strip().lower()
            if confirm == "y":
                return disk
            else:
                print("Отмена установки.")
                sys.exit(0)
        else:
            print(f"Указанный диск {disk_path} не найден!", file=sys.stderr)

def get_partitions(disk: str) -> tuple:
    """Определение разделов"""
    if disk.startswith("sd"):
        return (f"/dev/{disk}1", f"/dev/{disk}2", f"/dev/{disk}3")
    else:
        return (f"/dev/{disk}p1", f"/dev/{disk}p2", f"/dev/{disk}p3")

def partition_disk(disk: str) -> None:
    """Ручная разметка диска"""
    print("⌛ Запуск cfdisk для ручной разметки...")
    run_command(["cfdisk", f"/dev/{disk}"])

def format_partitions(boot_part: str, swap_part: str, root_part: str) -> None:
    """Форматирование разделов"""
    print("⌛ Форматирование разделов...")
    run_command(["mkfs.fat", "-F32", boot_part])
    run_command(["mkswap", swap_part])
    run_command(["mkfs.ext4", root_part])

def mount_partitions(boot_part: str, swap_part: str, root_part: str) -> None:
    """Монтирование разделов"""
    print("⌛ Монтирование разделов...")
    run_command(["mount", root_part, "/mnt"])
    os.makedirs("/mnt/boot/efi", exist_ok=True)
    run_command(["mount", boot_part, "/mnt/boot/efi"])
    run_command(["swapon", swap_part])

def update_mirrors() -> None:
    """Обновление зеркал"""
    print("⌛ Обновление зеркал через reflector...")
    run_command(["reflector", "--country", "Kazakhstan,Russia", "--latest", "10",
                "--sort", "rate", "--save", "/etc/pacman.d/mirrorlist"])

def install_base_system() -> None:
    """Установка базовой системы"""
    print("⌛ Установка базовой системы...")
    packages = [
        "base", "linux", "linux-firmware", "sof-firmware", "base-devel", "grub",
        "efibootmgr", "nano", "networkmanager", "git", "cmake", "sassc",
        "reflector"
    ]
    run_command(["pacstrap", "/mnt"] + packages)

def generate_fstab() -> None:
    """Генерация fstab"""
    print("⌛ Генерация fstab...")
    with open("/mnt/etc/fstab", "w") as f:
        subprocess.run(["genfstab", "-U", "/mnt"], stdout=f, check=True)

def copy_user_files() -> None:
    """Копирование пользовательских файлов"""
    print("⌛ Копирование пользовательских файлов...")
    setup_dir = "/mnt/root/setup"
    os.makedirs(setup_dir, exist_ok=True)

    files_to_copy = [
        "hypr", "fish", "waybar", "wofi", "yay", "customize.service",
        "CyberGRUB-2077-base", "sddm-astronaut-theme", "Graphite-gtk-theme",
        "wallpaper.jpg"
    ]

    for item in files_to_copy:
        try:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.copytree(item, f"{setup_dir}/{item}")
                else:
                    shutil.copy2(item, setup_dir)
        except Exception as e:
            print(f"⚠ Не удалось скопировать {item}: {e}")

def get_user_input() -> tuple:
    """Получение пользовательского ввода"""
    while True:
        username = input("Введите имя пользователя (латинские буквы, без пробелов): ").strip()
        if username and username.isalnum():
            break
        print("✖ Имя пользователя содержит недопустимые символы!", file=sys.stderr)

    while True:
        userpass = getpass.getpass(f"Введите пароль для пользователя {username}: ")
        if userpass:
            break
        print("✖ Пароль не может быть пустым!", file=sys.stderr)

    while True:
        rootpass = getpass.getpass("Введите пароль для root: ")
        if rootpass:
            break
        print("✖ Пароль не может быть пустым!", file=sys.stderr)

    timezone_input = input("Введите часовой пояс (например: Almaty или Tomsk): ").strip()

    return username, userpass, rootpass, timezone_input

def save_user_data(username: str, userpass: str, rootpass: str, timezone: str) -> None:
    """Сохранение пользовательских данных"""
    with open("/mnt/root/setup/username", "w") as f:
        f.write(username)
    with open("/mnt/root/setup/userpass", "w") as f:
        f.write(userpass)
    with open("/mnt/root/setup/rootpass", "w") as f:
        f.write(rootpass)
    with open("/mnt/root/setup/timezone", "w") as f:
        f.write(timezone)

def select_de() -> str:
    """Выбор окружения рабочего стола"""
    print("Выберите DE:")
    print("1) KDE Plasma")
    print("2) Hyprland")

    while True:
        choice = input("Введите 1 или 2: ").strip()
        if choice == "1":
            with open("/mnt/root/setup/.de-choice", "w") as f:
                f.write("kde")
            return "kde"
        elif choice == "2":
            with open("/mnt/root/setup/.de-choice", "w") as f:
                f.write("hyprland")
            return "hyprland"
        else:
            print("✖ Неверный выбор окружения!", file=sys.stderr)

def mount_system_dirs() -> None:
    """Монтирование системных директорий"""
    run_command(["mount", "--bind", "/dev", "/mnt/dev"])
    run_command(["mount", "--bind", "/dev/pts", "/mnt/dev/pts"])
    run_command(["mount", "--bind", "/proc", "/mnt/proc"])
    run_command(["mount", "--bind", "/sys", "/mnt/sys"])

def chroot_configure() -> None:
    """Настройка системы в chroot"""
    print("⌛ Настройка системы в chroot...")
    chroot_script = """
#!/bin/bash
set -eu

# Чтение сохраненных данных
USERNAME=$(cat /root/setup/username)
USERPASS=$(cat /root/setup/userpass)
ROOTPASS=$(cat /root/setup/rootpass)
TIMEZONE_INPUT=$(cat /root/setup/timezone)

# Настройка часового пояса
case "$TIMEZONE_INPUT" in
  [Aa]lmaty) TIMEZONE="Asia/Almaty" ;;
  [Tt]omsk) TIMEZONE="Asia/Tomsk" ;;
  *) TIMEZONE="Asia/Almaty" ;;
esac

ln -sf "/usr/share/zoneinfo/$TIMEZONE" /etc/localtime
hwclock --systohc

# Локализация
sed -i 's/^#\(ru_RU\.UTF-8\)/\1/' /etc/locale.gen
sed -i 's/^#\(en_US\.UTF-8\)/\1/' /etc/locale.gen
locale-gen
reflector --country Kazakhstan --latest 5 --sort rate --save /etc/pacman.d/mirrorlist

echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "KEYMAP=ru" > /etc/vconsole.conf
echo "FONT=cyr-sun16" >> /etc/vconsole.conf
echo "Arch" > /etc/hostname

# Пользователи и пароли
printf "root:%s\n" "$ROOTPASS" | chpasswd
useradd -m -G wheel -s /bin/bash "$USERNAME"
printf "%s:%s\n" "$USERNAME" "$USERPASS" | chpasswd
echo "%wheel ALL=(ALL:ALL) ALL" >> /etc/sudoers

# Службы
systemctl enable NetworkManager
loginctl enable-linger "$USERNAME"

# Установка окружения
DE_CHOICE=$(cat /root/setup/.de-choice)

if [[ "$DE_CHOICE" == "kde" ]]; then
  echo "⌛ Установка KDE Plasma..."
  pacman -Syu --noconfirm
  pacman -Sy --noconfirm plasma sddm konsole kate firefox pipewire dolphin \\
    pipewire-pulse pipewire-jack fish ark gwenview spectacle

  # Настройка обоев по умолчанию
  mkdir -p /usr/share/wallpapers/MyWallpaper/contents/images/
  cp /root/setup/wallpaper.jpg /usr/share/wallpapers/MyWallpaper/contents/images/
  chmod 644 /usr/share/wallpapers/MyWallpaper/contents/images/wallpaper.jpg

  mkdir -p /etc/skel/.config
  cat > /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc <<EOL
[Containments][1][Wallpaper][org.kde.image][General]
Image=file:///usr/share/wallpapers/MyWallpaper/contents/images/wallpaper.jpg
EOL

  mkdir -p "/home/$USERNAME/.config"
  cp /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc "/home/$USERNAME/.config/"
  chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/.config"

  systemctl enable sddm
  chsh -s /bin/fish "$USERNAME"

elif [[ "$DE_CHOICE" == "hyprland" ]]; then
  echo "⌛ Установка Hyprland..."
  pacman -Syu --noconfirm
  pacman -Sy --noconfirm meson git wofi fastfetch fish pkgfile ttf-dejavu \\
    powerline-fonts inetutils ttf-font-awesome otf-font-awesome \\
    ttf-jetbrains-mono hyprpaper hyprlock sddm kitty kate firefox pipewire \\
    thunar pipewire-pulse pipewire-jack waybar nwg-look papirus-icon-theme dbus

  systemctl enable sddm
  systemctl enable dbus
  chsh -s /bin/fish "$USERNAME"

  # Копирование конфигураций
  mkdir -p "/home/$USERNAME/.config"
  cp -r /root/setup/{hypr,fish,waybar,wofi} "/home/$USERNAME/.config/"
  chown -R "$USERNAME:$USERNAME" "/home/$USERNAME"

  # Установка yay
  if [ ! -d "/home/$USERNAME/yay" ]; then
    sudo -u "$USERNAME" git clone https://aur.archlinux.org/yay.git "/home/$USERNAME/yay"
    cd "/home/$USERNAME/yay" && sudo -u "$USERNAME" makepkg -si --noconfirm
    cd ..
    cd ..
    cd ..
  fi
fi

# Установка тем
if [ -f "/root/setup/sddm-astronaut-theme/install.sh" ]; then
  chmod +x /root/setup/sddm-astronaut-theme/install.sh
  cd /root/setup/sddm-astronaut-theme
  ./install.sh
  cd ..
fi

if [ -f "/root/setup/Graphite-gtk-theme/install.sh" ]; then
  chmod +x /root/setup/Graphite-gtk-theme/install.sh
  cd /root/setup/Graphite-gtk-theme
  ./install.sh
  cd ..
fi

# Настройка темы SDDM
mkdir -p /etc/sddm.conf.d
echo '[Theme]' > /etc/sddm.conf.d/theme.conf
echo 'Current=astronaut' >> /etc/sddm.conf.d/theme.conf

if [ ! -d /sys/firmware/efi ]; then
  echo "✖ Не найден /sys/firmware/efi — установка возможна только в UEFI!" >&2
  exit 1
fi

# Загрузчик
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --recheck

# Установка темы GRUB вручную
echo "⌛ Установка темы GRUB CyberGRUB-2077..."
cd /root/setup/CyberGRUB-2077-base
./install.sh

# Настройка GRUB
grub-mkconfig -o /boot/grub/grub.cfg

# Очистка
shred -u /root/setup/username /root/setup/userpass /root/setup/rootpass /root/setup/timezone
"""

    with open("/mnt/chroot_script.sh", "w") as f:
        f.write(chroot_script)

    run_command(["chmod", "+x", "/mnt/chroot_script.sh"])
    run_command(["arch-chroot", "/mnt", "/bin/bash", "/chroot_script.sh"])
    os.remove("/mnt/chroot_script.sh")

def unmount_system() -> None:
    """Размонтирование системы"""
    print("⌛ Завершение установки...")
    run_command(["umount", "-R", "/mnt/dev/pts"], False)
    run_command(["umount", "-R", "/mnt/dev"], False)
    run_command(["umount", "-R", "/mnt/proc"], False)
    run_command(["umount", "-R", "/mnt/sys"], False)
    run_command(["umount", "-R", "/mnt"], False)
    run_command(["swapoff", "-a"], False)

def reboot_system() -> None:
    """Перезагрузка системы"""
    print("✅ Установка завершена! Перезагрузка через 5 секунд...")
    time.sleep(5)
    run_command(["reboot"])

def main() -> None:
    """Основная функция"""
    try:
        check_root()
        check_internet()
        disk = select_disk()
        boot_part, swap_part, root_part = get_partitions(disk)

        partition_disk(disk)
        format_partitions(boot_part, swap_part, root_part)
        mount_partitions(boot_part, swap_part, root_part)
        update_mirrors()
        install_base_system()
        generate_fstab()
        copy_user_files()

        username, userpass, rootpass, timezone = get_user_input()
        save_user_data(username, userpass, rootpass, timezone)
        select_de()
        mount_system_dirs()
        chroot_configure()
        unmount_system()
        reboot_system()
    except KeyboardInterrupt:
        print("\nУстановка прервана пользователем.")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

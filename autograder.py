# autograder --- Student Version to grade all the files
#
# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import autochecker
import os
print("What's the directory where the files (index.html, academics.html, etc.) reside? ")
directory = input()



try:
    os.chdir(directory)
    ret = autochecker.automain()
except OSError as e:
    ret = [0 for i in range(0,12)]

print("results are in result.txt")

text_file = open("result.txt", "w")

text_file.write("UCR ID: your UCR ID \n")
text_file.write("Part 1: Text style modification through inline CSS changes.  45pts\n" )
text_file.write("1. Correct <header>  {0}/5pts\n".format(ret[0]) )
text_file.write("2. Text-shadow added correctly {0}/5pts\n".format(ret[1]) )
text_file.write("3. Correct <h1> heading (text-shadow, background-color, text-align)  {0}/15pts\n".format(ret[2]) )
text_file.write("4. <h1> heading color added  {0}/5pts\n".format(ret[3]) )
text_file.write("5. <br> added  {0}/5pts\n".format(ret[4]) )
text_file.write("6. <nav> style  {0}/5pts\n".format(ret[5]) )
text_file.write("7. <footer> style  {0}/5pts\n".format(ret[6]) )
text_file.write("\n" )
text_file.write("Part 2: Headings of various levels (<h1>, <h2>, <h3>, ...) modified via Internal style\n" )
text_file.write("rules..  25pts\n" )
text_file.write("1. Font, text color, alignment and background of heading styles {0}/25\n".format(ret[7]) )
text_file.write("" )
text_file.write("Part 3: External Style Sheet   30pts\n" )
text_file.write("1. External Style Sheet exists and is named properly.  {0}/5pts\n".format(ret[8]) )
text_file.write("2. External Style Sheet has two selectors.  {0}/10pts\n".format(ret[9]) )
text_file.write("   Each selector has two properties.  {0}/10pts\n".format(ret[10]) )
text_file.write("   External Style Sheets are properly linked to the HTML file.  {0}/5pts\n".format(ret[11]) )
sum = 0
for i in ret:
    sum = sum + i
text_file.write("total points:{0}/100\n".format(sum))
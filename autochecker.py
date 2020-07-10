# autochecker.py --- Do grading for specific folder selected by autodirfinder.py
#
# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import tinycss
from html.parser import HTMLParser
from html.entities import name2codepoint
import re


class MyHeaderFinder(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag in ["h1", "h2", "h3", "h4", "h5"]:
            for attr in attrs:
                x,y = attr
                if x == "style":
                    self.cssdata[tag] = y

    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

    def read(self, data):
        self.cssdata = {}
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self.cssdata
def fdh(html):
    s = MyHeaderFinder()
    return s.read(html)

class GetTextShadown(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

    def read(self, data):
        self.textshadow = []
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self.textshadow
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        for attr in attrs:
            x, y = attr
            if x == 'style' and ('text-shadow' in y):
                self.textshadow.append((tag,x,y))
def textshadower(html):
    s = GetTextShadown()
    return s.read(html)

class GetH1tage(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

    def read(self, data):
        self.textshadow = []
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self.textshadow
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        added = False
        if tag == 'h1':
            added = True
        for attr in attrs:
            x, y = attr
            if added:
                self.textshadow.append((tag,x,y))
def h1tagfinder(html):
    s = GetH1tage()
    return s.read(html)

class FindBR(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

    def read(self, data):
        self.textshadow = []
        self.result = False
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self.result
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        if tag == 'br':
            if self.textshadow[-1] == 'h1':
                self.result = True
        self.textshadow.append(tag)
def findbr(html):
    s = FindBR()
    return s.read(html)

class Findstyle(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

    def read(self, data):
        self.textshadow = []
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self.textshadow
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        for attr in attrs:
            x, y = attr
            if x == 'style' and y != '':
                self.textshadow.append(tag)
def fdstyle(html):
    s = Findstyle()
    return s.read(html)

class FindLink(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

    def read(self, data):
        self.textshadow = {}
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self.textshadow
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        if tag == 'link':
            for attr in attrs:
                x, y = attr
                self.textshadow[x] = y
def fdlink(html):
    s = FindLink()
    return s.read(html)

class FindHeader(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

    def read(self, data):
        self.getpoints = False
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self.getpoints
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        if tag == "header" and len(attrs) == 0:
            self.getpoints = True
def fdheader(html):
    s = FindHeader()
    return s.read(html)
def automain():
    ret = []
    try: 
        f = open("index.html", "r")
        html = f.read()
    except OSError as e:
        html = ""
    tmp = textshadower(html)
    points1 = 5 if fdheader(html) else 0

    print(points1)
    ret.append(points1)

    points1 = 0
    for x,y,z in tmp:
        p = re.compile(r'\s*text-shadow\s*:\s*\d+px\s+\d+px\s+\d+px\s')
        result = re.findall(p,z)
        if len(result) != 0:
            points1 = points1 + 2.5
    print(points1)
    ret.append(points1)
    tmp1 = h1tagfinder(html) 
    points = 0
    for x,y,z in tmp1:
        p = re.compile(r'text-shadow')
        result = re.findall(p,z)
        if len(result) != 0:
            points = points + 5
        p = re.compile(r'background-color')
        result = re.findall(p,z)
        if len(result) != 0:
            points = points + 5
        p = re.compile(r'center')
        result = re.findall(p,z)
        if len(result) != 0:
            points = points + 5
    print(points)
    ret.append(points)
    points = 0
    for x,y,z in tmp1:
        p = re.compile(r'-*color')
        lists = re.findall(p,z)
        if 'color' in lists:
            points = 5
    print(points)
    ret.append(points)
    points = (5 if findbr(html) else 0)
    print(points)
    ret.append(points)
    points = (5 if 'nav' in fdstyle(html) else 0)
    print(points)
    ret.append(points)
    points = (5 if 'footer' in fdstyle(html) else 0)
    print(points)
    ret.append(points)

    class MyCSSFinder(HTMLParser):
        def handle_starttag(self, tag, attrs):
            self.currentag = tag

        def __init__(self):
            # initialize the base class
            HTMLParser.__init__(self)

        def read(self, data):
            self.currentag = ""
            self.cssdata = ""
            # re-set the parser's state before re-use
            self.reset()
            self.feed(data)
            return self.cssdata

        def handle_data(self, data):
            if self.currentag == 'style':
                self.cssdata = data
            self.currentag = ""

    def fdcss(html):
        s = MyCSSFinder()
        return s.read(html)
    try: 
        f = open("academics.html", "r", encoding="utf8")
        html = f.read()
    except OSError as e:
        html = ""
    stylexi = (str(fdcss(html)))
    cssparser = tinycss.make_parser()

    st = cssparser.parse_stylesheet(stylexi)
    hashma = {}
    hashma['font'] = 0
    hashma['color'] = 0
    hashma['text-align'] = 0
    hashma['background-color'] = 0

    totalrule = 0

    for x in st.rules:
        if x.selector[0].value in ['h1', 'h2', 'h3', 'h4', 'h5']:
            totalrule = totalrule + 1
            for decl in x.declarations:
                if 'font' in decl.name or 'word' in decl.name:
                    hashma['font'] = hashma['font'] + 1
                elif decl.name == 'text-align' and decl.value[0].value == 'center':
                    hashma['text-align'] = hashma['text-align'] + 1
                else:
                    hashma[decl.name] = hashma[decl.name] + 1 
    pointspossible = totalrule * 4
    pointsactual = 0
    for x in hashma:
        pointsactual = pointsactual  + hashma[x]
    rett = 0
    if pointspossible != 0:
        rett = 25 * (float(pointsactual)/float(pointspossible))
    else:
        stylexi = ""
        hd = fdh(html)
        for x in hd:
            stylexi = stylexi + x
            stylexi = stylexi + "{"
            stylexi = stylexi + hd[x]
            stylexi = stylexi + ";}"
            st = cssparser.parse_stylesheet(stylexi)
            hashma = {}
            hashma['font'] = 0
            hashma['color'] = 0
            hashma['text-align'] = 0
            hashma['background-color'] = 0

            totalrule = 0

            for x in st.rules:
                totalrule = totalrule + 1
                for decl in st.rules[0].declarations:
                    if 'font' in decl.name:
                        hashma['font'] = hashma['font'] + 1
                    elif decl.name == 'text-align' and decl.value[0].value == 'center':
                        hashma['text-align'] = hashma['text-align'] + 1
                    elif decl.name in hashma:
                        hashma[decl.name] = hashma[decl.name] + 1 
            pointspossible = totalrule * 4
            pointsactual = 0
            for x in hashma:
                pointsactual = pointsactual  + hashma[x]
            rett = 12.5 * (pointsactual/pointspossible)
    print(rett)
    ret.append(rett)

    filefound = True
    try: 
        f = open("lab3-style.css", "r")
        css = f.read()
    except OSError as e:
        filefound = False
    if filefound == True:
        cssparser = tinycss.make_parser()
        st = cssparser.parse_stylesheet(css)
        totalrule = len(st.rules)
        actualdeclare = 0
        possibledeclare = 2 * totalrule
        for x in st.rules:
            actualdeclare = actualdeclare + (2 if len(x.declarations) >= 2 else len(x.declarations))
        if totalrule > 2:
            totalrule = 2
        print(5)
        ret.append(5)
        print(float(totalrule)/2.0*10.0)
        ret.append(float(totalrule)/2.0*10.0)
        rett = 0
        if possibledeclare != 0:
            rett = float(actualdeclare)/float(possibledeclare)*10
        print(rett)
        ret.append(rett)
    else:
        print( "lab3-style.css is not found!")
        print(0)
        ret.append(0)
        ret.append(0)
        ret.append(0)
        print(0)
        print(0)
    correctnum = 0
    possible = 4
    for x in ["index.html", "professional.html", "personal.html", "academics.html"]:
        try: 
            f = open(x, "r", encoding="utf8")
            html = f.read()
            h1 = fdlink(html)
            if 'rel' not in h1 or 'type' not in h1 or 'href' not in h1:
                continue
            if h1['rel'] == 'stylesheet' and h1['type'] == 'text/css' and h1['href'] == 'lab3-style.css':
                correctnum = correctnum + 1
        except OSError as e:
            print( x + " is not found!")
        
    print(5.0 * float(correctnum) / float(possible))
    ret.append(5.0 * float(correctnum) / float(possible))
    return ret
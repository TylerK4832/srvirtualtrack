import os

from flask import redirect, render_template, request

def bubbleSortTimes(list):
    n = len(list)
    for i in range(n-1):
        for j in range(0, n-i-1):
            a = (60*int(list[j][1])) + int(list[j][2]) + (int(list[j][3])/10)
            b = (60*int(list[j+1][1])) + int(list[j+1][2]) + (int(list[j+1][3])/10)
            if a > b :
                list[j], list[j+1] = list[j+1], list[j]

def bubbleSortDates(list):
    n = len(list)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if list[j][5] < list[j+1][5] :
                list[j], list[j+1] = list[j+1], list[j]

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

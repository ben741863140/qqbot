import re
s = "购2333"

r = re.compile(r'购买(\d*)')

if len(r.findall(s)):
    print(233)
else:
    print(r.fullmatch(s))
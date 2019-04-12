import re
import math
a='3.0+16.0%2'
place=a.rfind("%")
s=re.search(r'(?:\d+(?:\.\d+)?|\.\d+)',a[place::-1])
print(str(s[0]))
print(str(math.log(800)))
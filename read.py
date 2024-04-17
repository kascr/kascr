import re

with open('hosts', 'r') as f:
    lines = f.readlines()
    domains = []
    for line in lines:
        match = re.search(r'^(\s*#*\s*127\.0\.0\.1\s+)([\w\.-]+)(.*)', line)
        if match:
            domain = match.group(2)
            comment = match.group(3)
            domains.append((domain, comment))

with open('hosts.txt', 'w') as f:
    for domain, comment in domains:
        f.write(  domain + comment + '\n')

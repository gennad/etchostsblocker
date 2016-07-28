import re


# TODO use some API
SOCIAL_WEBSITES = set([
        'vk.com',
        'rambler.ru',
        'yandex.ru',
        'facebook.com',
        'dom2',
        'rbc',        
        'linkedin.com'
])
TOGGLE_LINE = '# toggle:'


def is_host_record(line):
    pattern = re.compile("#*.*?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s+(\w+\.\w+.*).*$")
    res = pattern.match(line)
    return res

def is_toggle_line(line):
    pattern = '.*(' + TOGGLE_LINE + ')\s*(\w+)'
    pattern = re.compile(pattern)
    res = pattern.match(line)
    return res


#with open('/etc/hosts') as f:
with open('hosts') as f:
    lines = f.readlines()
    

# unblock

def unblock(lines):
    new_lines = []
    toggle_seen = False
    
    for line in lines:
        res = is_toggle_line(line)
        if res:
            line = res.group(1) + ' unblock\n'
            toggle_seen = True
        else:
            res = is_host_record(line)
            if res:
                ip = res.group(1)
                host = res.group(2)
                line = ip + ' ' + host + '\n'
                        
        new_lines.append(line)

    if not toggle_seen:
        new_lines.insert(0, TOGGLE_LINE + ' unblock\n')

    with open('hosts', 'w') as f:
        f.writelines(new_lines)


# block
def block(lines):
    new_lines = []
    toggle_seen = False
    blocked = set()
    
    for line in lines:
        res = is_toggle_line(line)
        if res:
            line = res.group(1) + ' block\n'
            toggle_seen = True
        else:
            res = is_host_record(line)
            if res:
                ip = res.group(1)
                host = res.group(2)

                for social_site in SOCIAL_WEBSITES:
                    if social_site in host:
                        line = '# ' + ip + ' ' + host + '\n'
                        if host == social_site:
                            blocked.add(social_site)

                        break

        new_lines.append(line)

    if not toggle_seen:
        new_lines.insert(0, TOGGLE_LINE + ' block\n')

    for host in SOCIAL_WEBSITES - blocked:
        if '.' in host:
            new_lines.append('127.0.0.1 ' + host + '\n')

    with open('hosts', 'w') as f:
        f.writelines(new_lines)


if __name__ == '__main__':
    action = None

    for line in lines:
        if TOGGLE_LINE in line:
            action = line[line.find(TOGGLE_LINE) + len(TOGGLE_LINE):].strip()
            break

    if action is None or action == 'unblock':
        print (block(lines) )
    else:
        print (unblock(lines) )
    

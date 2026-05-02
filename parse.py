import re;

def getSections(definition_file):
    sections={} 
    content=[] 
    in_section=0

    with open(definition_file, 'r') as f:
        for line in f.readlines():
            #for getting rid of everithing that comes after a comment
            if '//' in line:
                line = line.split('//')[0]
            
            line = line.strip()
            if not line:
                continue

            #regex accepting only if section has a name
            if re.search('[a-zA-Z]+\\{', line):
                if in_section: 
                    return -1
                in_section=1
                #saving the name of the section(without '}') as a dictionary key
                length=len(line)
                name=line[:length-1]
                sections[name]=[]
            elif '{'==line:
                return -1
            elif '}'==line:
                if not in_section: 
                    return -1
                in_section=0
                sections[name]=content
                content=[]
            elif in_section:
                content.append(line)

    return sections
    
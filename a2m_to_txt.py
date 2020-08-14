# Ce fichier sert a convertir les fichiers de séquences générées sous format a2m au fichier txt se trouvant dans le dossier data/

import os
files = os.listdir('./data_a2m/')

for filename in files:
    file = open('./data_a2m/'+filename,'r')
    if filename.split('.')[0]+'.txt' in files :
        continue
    output = ''
    out_line = ''
    lines = [line.replace('\n','') for line in file]
    for line in lines[1:] :
        if line[0] in ['>','\n']:
            output += out_line+'\n' 
            out_line = ''
            continue
        out_line +=  line
    file.close()
    file = open('./data/'+filename.split('.')[0]+'.txt','w')
    file.write(output)

import os
import sys
from fuzzywuzzy import fuzz
import subprocess

def generate_requirements_file():
    file_path = os.path.dirname(os.path.realpath(__file__))
    abs_root = os.path.split(file_path)[0]
    dir_path = abs_root.split("\source")[0]
    path = dir_path


    files = os.listdir(path)
    pyfiles = []
    for root, dirs, files in os.walk(path):
          for file in files:
            if file.endswith('.py'):
                  pyfiles.append(os.path.join(root, file))

    stopWords = ['from', 'import',',','.']

    importables = []
    importing_files = []

    for file in pyfiles:
        with open(file) as f:
            content = f.readlines()

            for line in content:
                if "import" in line:
                    for sw in stopWords:
                        line = ' '.join(line.split(sw))

                    importables.append(line.strip().split(' ')[0])


    subprocess.call(f"pip freeze > {path}/requirements.txt", shell=True)

    with open(path+'/requirements.txt') as req:
        modules = req.readlines()
        modules = {m.split('=')[0].lower() : m for m in modules}


    notList = [''.join(i.split('_')) for i in sys.builtin_module_names]+['os']

    new_requirements = []
    for req_module in importables:
        try :
            new_requirements.append(modules[req_module])

        except KeyError:
            for k,v in modules.items():
                if len(req_module)>1 and req_module not in notList:
                    if fuzz.partial_ratio(req_module,k) > 90:
                        new_requirements.append(modules[k])

    new_requirements = [i for i in set(new_requirements)]



    with open(path+'/requirements.txt','w') as req:
        req.write(''.join(new_requirements))


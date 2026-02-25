import os, tempfile, urllib.request, shutil, traceback

REPO_FOLDER = 'docs'
REPOSITORY = 'repository.cache-sk'

PLUGINS = [ REPOSITORY,
           'https://github.com/cache-sk/repohub/#main:repository.cache-hub',
           'https://github.com/cache-sk/plugin.program.cache-sk.kodi.tools.git',
           # archived 'https://github.com/cache-sk/plugin.video.dokumenty.tv.git#uni',
           # archived 'https://github.com/cache-sk/YABoP.git#master:plugin.video.yabop',
           'https://github.com/cache-sk/SkTonline.git#master:plugin.video.sktonline',
           'https://github.com/cache-sk/plugin.video.freeview.sk',
           # archived 'https://github.com/cache-sk/plugin.video.rebit.tv',
           'https://github.com/cache-sk/plugin.video.yawsp',
           'https://github.com/xbmc-kodi-cz/script.module.urlresolver',
           #'https://github.com/tvaddonsco/script.module.urlresolver',
           # abandoned 'https://github.com/jsergio123/script.module.resolveurl',
           'https://github.com/Gujal00/ResolveURL.git#master:script.module.resolveurl'
           #too big!'https://github.com/CastagnaIT/repository.castagnait.git#kodi:repository.castagnait'
           ]

EXTERNAL = [{'name':'speedtest','url':'https://github.com/add-ons/script.speedtester/releases/download/v1.1.3/script.speedtester-1.1.3+matrix.1.zip'}
            ]

#UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
UA = " Kodi/21.1 (Windows NT 10.0.19045.2965; Win64; x64) App_Bitness/64 Version/21.1-(21.1.0)-Git:20240817-183eb85f10"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', UA)]
urllib.request.install_opener(opener)

def delete_all_files(folder,skip):
    print('Cleaning '+folder)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        #print(file_path)
        if not file_path in skip:
            try:
                if os.path.isfile(file_path):
                    print('unlinking '+file_path)
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    delete_all_files(file_path,skip)
                    print('removing '+file_path)
                    os.rmdir(file_path)
            except Exception as e:
                print(e)
        else:
            print('skipping '+file_path)

delete_all_files(REPO_FOLDER,[])

externals = []
try:
    for ext in EXTERNAL:
        tmpf = tempfile.NamedTemporaryFile()
        tempname = tmpf.name + '_' + ext['name'] + '.zip'
        tmpf.close
        print("Downloading "+ext['url'])
        urllib.request.urlretrieve(ext['url'],tempname) 
        externals.append(tempname)

    os.system(f"python create_repository.py --no-parallel --datadir {REPO_FOLDER} {' '.join(PLUGINS)} {' '.join(externals)}")
except:
    traceback.print_exc()
    for tempname in externals:
        os.unlink(tempname)
    quit()

print("Creating index with listing")
with open(os.path.join(REPO_FOLDER,"index.html"), "w") as index:
    index.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<html>\n<body>\n')
    repofolder = os.path.join(REPO_FOLDER,REPOSITORY)
    files = [f for f in os.listdir(repofolder) if os.path.isfile(os.path.join(repofolder,f)) and f.endswith(".zip")]
    for f in files:
        index.write(f'<a href="{f}">{f}</a>\n')
        shutil.copy(os.path.join(repofolder,f),REPO_FOLDER)
        print("Processed file "+f)
    index.write("</body>\n</html>\n")

print("Copying announcements.json")
shutil.copy("announcements.json","docs")

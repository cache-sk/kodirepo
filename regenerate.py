import os, tempfile, urllib.request, shutil

REPO_FOLDER = 'docs'
REPOSITORY = 'repository.cache-sk'

PLUGINS = [ REPOSITORY,
           'https://github.com/cache-sk/plugin.program.cache-sk.kodi.tools.git',
           'https://github.com/cache-sk/plugin.video.dokumenty.tv.git#uni',
           # archived 'https://github.com/cache-sk/YABoP.git#master:plugin.video.yabop',
           ##'https://github.com/cache-sk/SkTonline.git#master:plugin.video.sktonline',
           ##'https://github.com/cache-sk/plugin.video.freeview.sk',
           # archived 'https://github.com/cache-sk/plugin.video.rebit.tv',
           ##'https://github.com/cache-sk/plugin.video.yawsp',
           'https://github.com/xbmc-kodi-cz/repository.xbmc-kodi.cz',
           'https://github.com/xbmc-kodi-cz/script.module.urlresolver',
           #'https://github.com/tvaddonsco/script.module.urlresolver',
           # abandoned 'https://github.com/jsergio123/script.module.resolveurl',
           'https://github.com/Gujal00/ResolveURL.git#master:script.module.resolveurl'
           #too big!'https://github.com/CastagnaIT/repository.castagnait.git#kodi:repository.castagnait'
           ]

EXTERNAL = [#{'name':'repository_jsergio','url':'https://github.com/jsergio123/zips/raw/master/repository.jsergio/repository.jsergio-1.0.4.zip'},
            #{'name':'repository_kodi_czsk','url':'https://kodi-czsk.github.io/repository/repo/repository.kodi-czsk/repository.kodi-czsk-1.0.2.zip'},
            ##{'name':'repository_cder','url':'https://cder.sk/repository.cder.sk-1.0.4.zip'},
            #{'name':'repository_hacky','url':'http://repo.sc2.zone/hacky/repository.hacky.zip'},
            {'name':'repository_saros','url':'https://github.com/Saros72/kodirepo/raw/main/repo-19/repository.saros/repository.saros-1.4.0.zip'}, #old - http://saros.wz.cz/repo/repository.saros-1.1.0.zip
            {'name':'repository_zdenci22','url':'http://repoczsk.wz.sk/repository.repoczsk-1.0.7.zip'},
            #{'name':'repository_skinbase','url':'https://github.com/kaffepausse71/Guidos-SKINBASE/raw/master/repository.skinbase.nexus/repository.skinbase.nexus-3.0.06.zip'},
            #https://downloads.guidos-skinbase.de/repos/repository.master.skinbase/repository.master.skinbase-3.3.50.zip
            #https://github.com/kaffepausse71/Guidos-SKINBASE/raw/master/repository.skinbase.18/repository.skinbase.18-1.1.16.zip
            #https://github.com/kaffepausse71/Guidos-SKINBASE/raw/master/repository.master.skinbase/repository.master.skinbase-3.3.44.zip
            {'name':'repository_zachmorris','url':'https://github.com/zach-morris/repository.zachmorris/raw/master/repository.zachmorris/repository.zachmorris-1.0.4.zip'},
            {'name':'repository_resolveurl','url':'https://raw.githubusercontent.com/Gujal00/smrzips/master/zips/repository.resolveurl/repository.resolveurl-1.0.0.zip'},
            {'name':'repository_parrot','url':'http://p.wz.sk/repository.Parrot-1.3.1.zip'},
            {'name':'speedtest','url':'https://github.com/add-ons/script.speedtester/releases/download/v1.1.3/script.speedtester-1.1.3+matrix.1.zip'},
            {'name':'jurialmunkey','url':'https://github.com/jurialmunkey/repository.jurialmunkey/raw/master/repository.jurialmunkey-3.4.zip'},
            #{'name':'castagnait','url':'https://github.com/CastagnaIT/repository.castagnait/raw/kodi/repository.castagnait-2.0.1.zip'}
            #{'name':'netflix','url':'https://github.com/CastagnaIT/plugin.video.netflix/releases/download/v1.22.0/plugin.video.netflix-1.22.0+matrix.1.zip'}
            ]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
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
    for tempname in externals:
        os.unlink(tempname)

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

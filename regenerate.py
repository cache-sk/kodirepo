import os, tempfile, urllib.request

try:
    from urllib import FancyURLopener
except ImportError:
    from urllib.request import FancyURLopener


PLUGINS = ['repository.cache-sk',
           'https://github.com/cache-sk/plugin.program.cache-sk.kodi.tools.git',
           'https://github.com/cache-sk/plugin.video.dokumenty.tv.git#uni',
           'https://github.com/cache-sk/YABoP.git#master:plugin.video.yabop',
           'https://github.com/cache-sk/SkTonline.git#master:plugin.video.sktonline',
           'https://github.com/cache-sk/plugin.video.freeview.sk',
           'https://github.com/cache-sk/plugin.video.rebit.tv',
           'https://github.com/cache-sk/plugin.video.yawsp',
           'https://github.com/xbmc-kodi-cz/repository.xbmc-kodi.cz',
           'https://github.com/xbmc-kodi-cz/script.module.urlresolver',
           #'https://github.com/tvaddonsco/script.module.urlresolver',
           # abandoned 'https://github.com/jsergio123/script.module.resolveurl',
           'https://github.com/Gujal00/ResolveURL.git#master:script.module.resolveurl']

EXTERNAL = [{'name':'repository_jsergio','url':'https://github.com/jsergio123/zips/raw/master/repository.jsergio/repository.jsergio-1.0.4.zip'},
            {'name':'repository_kodi_czsk','url':'https://kodi-czsk.github.io/repository/repo/repository.kodi-czsk/repository.kodi-czsk-1.0.2.zip'},
            {'name':'repository_cder','url':'https://cder.sk/repository.cder.sk-1.0.2.zip'},
            {'name':'repository_hacky','url':'http://repo.sc2.zone/hacky/repository.hacky.zip'},
            {'name':'repository_saros','url':'http://saros.wz.cz/repo/repository.saros-1.0.0.zip'},
            {'name':'repository_zdenci22','url':'http://repoczsk.wz.sk/repository.repoczsk-1.0.2.zip'},
            {'name':'repository_skinbase','url':'https://github.com/kaffepausse71/Guidos-SKINBASE/raw/master/repository.skinbase.19/repository.skinbase.19-3.1.34.zip'},
            #https://downloads.guidos-skinbase.de/repos/repository.master.skinbase/repository.master.skinbase-3.3.50.zip
            #https://github.com/kaffepausse71/Guidos-SKINBASE/raw/master/repository.skinbase.18/repository.skinbase.18-1.1.16.zip
            #https://github.com/kaffepausse71/Guidos-SKINBASE/raw/master/repository.master.skinbase/repository.master.skinbase-3.3.44.zip
            {'name':'repository_zachmorris','url':'https://github.com/zach-morris/repository.zachmorris/raw/master/repository.zachmorris/repository.zachmorris-1.0.0.zip'}]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
class MyOpener(FancyURLopener):
    version = UA
urlretrieve = MyOpener().retrieve

def delete_all_files(folder,skip):
    print('processing '+folder)
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

delete_all_files('repository',[])
externals = []
for ext in EXTERNAL:
    tmpf = tempfile.NamedTemporaryFile()
    tempname = tmpf.name + '_' + ext['name'] + '.zip'
    tmpf.close
    print("Downloading "+ext['url'])
    urlretrieve(ext['url'],tempname) 
    externals.append(tempname)

os.system("python create_repository.py --no-parallel --datadir repository " + " ".join(PLUGINS) + " " + " ".join(externals))

for tempname in externals:
    os.unlink(tempname)
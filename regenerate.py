import os, tempfile, urllib

PLUGINS = ['repository.cache-sk',
           'https://github.com/cache-sk/plugin.video.dokumenty.tv.git',
           'https://github.com/cache-sk/YABoP.git#master:plugin.video.yabop', #fixed 1.2.1 release //master to 495c6f66807360b915da025cf409b46c3f1178ed
           'https://github.com/cache-sk/SkTonline.git#master:plugin.video.sktonline',
           #'https://github.com/cache-sk/plugin.video.topserialy.to',
           'https://github.com/cache-sk/plugin.video.freeview.sk',
           'https://github.com/cache-sk/plugin.video.rebit.tv',
           'https://github.com/cache-sk/plugin.video.yawsp',
           'https://github.com/tvaddonsco/script.module.urlresolver',
           'https://github.com/jsergio123/script.module.resolveurl']

EXTERNAL = [#{'name':'repository_tva_common','url':'https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/zips/repository.tva.common/repository.tva.common-2.0.0.zip'},
            {'name':'repository_jsergio','url':'https://github.com/jsergio123/zips/raw/master/repository.jsergio/repository.jsergio-1.0.4.zip'},
            {'name':'repository_xbmc_kodi_cz','url':'https://repo.xbmc-kodi.cz/posledni.php'},
            {'name':'repository_kodi_czsk','url':'https://kodi-czsk.github.io/repository/repo/repository.kodi-czsk/repository.kodi-czsk-1.0.2.zip'},
            {'name':'repository_cder','url':'https://cder.sk/repository.cder.sk-1.0.2.zip'}]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
class MyOpener(urllib.FancyURLopener):
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
    print "Downloading "+ext['url']
    urlretrieve(ext['url'],tempname) 
    externals.append(tempname)

os.system("python create_repository.py --no-parallel --datadir repository " + " ".join(PLUGINS) + " " + " ".join(externals))

for tempname in externals:
    os.unlink(tempname)
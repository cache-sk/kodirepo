import os, tempfile, urllib, create_repository

PLUGINS = ['repository.cache-sk',
           'https://github.com/cache-sk/plugin.video.dokumenty.tv.git',
           'https://github.com/cache-sk/YABoP.git#master:plugin.video.yabop']

EXTERNAL = ['https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/zips/repository.tva.common/repository.tva.common-2.0.0.zip']

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
for path in EXTERNAL:
    tmpf = tempfile.NamedTemporaryFile()
    tempname = tmpf.name + '.zip'
    tmpf.close
    urllib.urlretrieve(path,tempname) 
    externals.append(tempname)

os.system("python create_repository.py --no-parallel --datadir repository " + " ".join(PLUGINS) + " " + " ".join(externals))

for tempname in externals:
    os.unlink(tempname)
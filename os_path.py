import os
for dir_path,subpaths,files in os.walk("",False):
        for file in files:
            file_path=os.path.join(dir_path,file)
            print "delete file:%s"  %file_path
            os.remove(file_path)
        print "delete dir:%s" %dir_path
        os.rmdir(dir_path)
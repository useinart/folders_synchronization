import os 
import hashlib
import time

LOG = 'log.txt'

def log(message):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(LOG, 'a') as f:
        f.write('['+now+']'+ message+ '\n')


def compare2file(file1, file2):
    #compare 2 files
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False


def compareHashFolder(folder1, folder2):
    files = os.listdir(folder1)
    other_folder = os.listdir(folder2)

    if len(files) != len(other_folder):
        return False

    for file in files:
        if file in other_folder:
            if not compare2file(folder1+'/'+file, folder2+'/'+file):
                return False
        else: 
            return False
    
    return True


log("Begin")

if os.path.isfile('config.txt'):
    print("config file: OK")
    log ('config file: OK')
    # get variable from config
    with open('config.txt', 'r') as f:
        lines = f.readlines()
        folder1 = lines[0].split(':')[1].strip()
        folder2 = lines[1].split(':')[1].strip()

else:
    log('config file: NOT FOUND')
    print("config file: NOT FOUND")
    # register folder
    folder1 = input('put your path in the computer:')
    folder2 = input('put your second folder path:')
    # check if folder is exist
    if not os.path.isdir(folder1):
        log('folder: NOT FOUND')
        print('folder is not exist')
        exit()
    # check if folder2 is exist
    if not os.path.isdir(folder2):
        log('folder2: NOT FOUND')
        print('folder2 is not exist')
        exit()
    # write config
    with open('config.txt', 'w') as f:
        f.write('folder:'+folder1)
        f.write('\n')
        f.write('folder2:'+folder2)
    print('config file: CREATED')
    log('config file: CREATED')

# run loop every 5 minutes

while True:
    # check if folder is same with second folder
    if compareHashFolder(folder1, folder2):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'[{now}] file is up to date')
        log('file is up to date')
        # sleep for 5 minutes
        time.sleep(300)
        continue    

    # check folder
    if os.path.isdir(folder1):
        print('folder: ACTIVE')
        log('folder: ACTIVE')
    else:
        print('folder is not exist')
        log('folder is not exist')
        print('please check your config file')
        break

    # check second folder
    if os.path.isdir(folder2):
        print('second folder: ACTIVE')
        log('second folder: ACTIVE')
    else:
        print('second folder is not exist')
        log('second folder is not exist')
        print('second folder check your config file')
        break

    # check file hash in folder and compare with second folder
    countSync = 0
    updateFile = 0
    deleteFile = 0

    # get all file in folder
    files = os.listdir(folder1)
    # get all file in second folder
    files_folder2 = os.listdir(folder2)
    # compare 2 list
    for file in files_folder2:
        if file in files:
            if compare2file(folder1+'/'+file, folder2+'/'+file):
                log(f'{file} is up to date')
                countSync += 1
            else:
                # copy file from folder to second folder
                updateFile += 1
                os.remove(folder2+'/'+file)
                os.system('copy '+folder1+'/'+file+' '+folder2)
                log(f'{file} is updated')
        if file not in files:
            # delete file in second folder
            log(f'{file} is deleted')
            deleteFile += 1
            os.remove(folder2+'/'+file)

    for file in files:
        if file not in files_folder2:
            # copy file from folder to second folder
            updateFile += 1
            log(f'{file} is copied')
            os.system('copy '+folder1+'/'+file+' '+folder2)



    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f'[{now}] sync: {countSync}; update: {updateFile}; delete: {deleteFile};')

    time.sleep(100)

tpath = input('Table: ')

if not tpath == '':
    savefile = open('ptrscan.cfg', 'w', encoding = 'utf-8')
    savefile.write(tpath)
    savefile.close()
else:
    savefile = open('ptrscan.cfg', 'r', encoding = 'utf-8')
    tpath = str(savefile.read())
    savefile.close()

table = open(tpath, 'r', encoding = 'utf-8')

def nullifyFile(file_path):
    import os
    tfile = open(os.getcwd() + '\\' + file_path, 'w')
    tfile.close()

def textPointerScan(file_path, address):
    import os

    sfaddr = findsubfileaddr(file_path, 4)[0]
    
    sfile = open(os.getcwd() + '\\' + file_path, 'rb')
    sfile.seek(sfaddr+address-1)
    sbytes = sfile.read(2)
    if sbytes[0] == 0 and not sbytes[1] == 0:
        return True
    else:
        return False

def findsubfileaddr(file_path, subfile_num):
    import os
    ret_list = list()
    wad = open(file_path, 'rb')
    wad.seek((subfile_num-1)*8)
    bytes0 = wad.read(4)
    ret_list.append(bytes0[0] + bytes0[1]*256 + bytes0[2]*65536 + bytes0[3]*16777216)
    wad.seek((subfile_num-1)*8+4)
    bytes0 = wad.read(4)
    ret_list.append(ret_list[0] + bytes0[0] + bytes0[1]*256 + bytes0[2]*65536 + bytes0[3]*16777216)
    wad.close()
    return ret_list

def checkAddr(num, alist):
    ##print(alist)
    ctrigger = True
    for e in alist:
        if e == num:
            print('catch')
            ctrigger = False
    return ctrigger

def searchAddr(filepath, txt, addr_list):
    import os
    
    subfile = findsubfileaddr(os.getcwd() + '\\' + filepath, 4)
    ##print(txt)
    wad = open(os.getcwd() + '\\' + filepath, 'rb')
    wad.seek(subfile[0])
    flength = subfile[1] - subfile[0]
    llength = len(txt.encode())
    ##print(llength)
    addr = 0
    ptr_l = list()

    ##print(llength)
    
    for x in range(flength):
        wad.seek(subfile[0] + x)
        line0 = (wad.read(llength)).decode('cp1251', errors = 'ignore')
        if line0 == txt:
            if checkAddr(x, addr_list):
                addr = x
                break
        
    ptr_l.append(addr)
    
    if not addr == 0:
        for x in range(int(flength/4)):
            wad.seek(subfile[0] + x*4)
            bytes0 = wad.read(4)
            ptr0 = bytes0[0] + bytes0[1]*256 + bytes0[2]*65536 + bytes0[3]*16777216
            if ptr0 >= addr - 16 and ptr0 <= addr:
                ptr_l.append(ptr0)

    wad.close()
    return ptr_l

#------------------------------------------------

canRead = False

##nullifyFile('ptr.txt')

addr_list = list()
for line in table.readlines():
    ##print('.', end='')
    if canRead:
        rtrigger = True
        ccount = 0
        txtline = ''
        sf_num = ''
        for symbol in line:
            if symbol == '"':
                if rtrigger:
                    rtrigger = False
                else:
                    rtrigger = True
            if rtrigger:
                if symbol == ',':
                    ccount += 1
            if ccount == 4:
                if not symbol == '"':
                    txtline += symbol
            elif ccount == 1:
                if not symbol == ',':
                    sf_num += symbol

        txtline = txtline[1:len(txtline)]
        ofile = open('text.txt', 'a')
        ofile.write(txtline + '\n')
        ofile.close()
        
    canRead = True

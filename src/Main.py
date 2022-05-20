# return img, nested list
import sys


def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


filename = input()
operation = int(input())


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
(nl, old_max) = read_ppm_file(filename)

row = len(nl)
col = len(nl[0])
cha = len(nl[0][0])


def op1(nnll):  #min-max normalisation

    new_min = int(input())
    new_max = int(input())
    old_min = 0

    for i in range(row):
        for j in range(col):
            for k in range(cha):
                old_val = nl[i][j][k]
                new_val = (old_val-old_min)*(new_max-new_min)/(old_max-old_min)+new_min
                new_val = (round(new_val, 4))
                nl[i][j][k] = new_val
    img_printer(nl)

def op2(nnll):  #z-score normalization
    for k in range(cha):
        channel_mean = 0
        for i in range(row):
            for j in range(col):
                channel_mean += nl[i][j][k]
        channel_mean = channel_mean/ (row*col)          #channel mean buluyorum
        variable = 0

        for i in range(row):
            for j in range(col):
                channel_value = nl[i][j][k]
                variable = variable + (channel_value-channel_mean)**2           #channel sd buluyorum
        channel_sd = (variable/(row*col))**0.5 + 1e-6

        for i in range(row):
            for j in range(col):
                channel_value = nl[i][j][k]
                nl[i][j][k] = round(((channel_value-channel_mean)/channel_sd),4)           #değeri eşitliyorum
    img_printer(nl)
def op3(nnll):  #black and white
    for i in range(row):
        for j in range(col):
            sum = 0
            for k in range(cha):
                sum = sum + nl[i][j][k]         #değerleri topluyorum
            average = sum//cha          #ortalamayı buluyorum
            for k in range(cha):
                nl[i][j][k] = average           #değere eşitliyorum
    img_printer(nl)

def op4(nl):    #convolution
    filter = input()
    stride = int(input())
    fp2 = open(filter)
    fltr_lst = fp2.read().split()
    fltr_arr = []
    rows_cols = int(len(fltr_lst)**0.5)
    hs = 0
    for c in range(rows_cols):
        rowe=[]
        for i in range(rows_cols):
            rowe.append(float(fltr_lst[hs]))        #filtreyi listeye çevirdim
            hs+=1
        fltr_arr.append(rowe)
    new_img_lst = []
    for sy in range(0, row-rows_cols+1, stride):
        new_row = []
        for df in range(0, col-rows_cols+1, stride):            #doğru sayıda boş listeye sahip boş liste hazırladım
            new_row.append([])
        new_img_lst.append(new_row)
    for k in range(cha):            #her renk için loop
        for i in range(0, row-rows_cols+1, stride):         #satır loop'u
            bhmlm = i//stride
            hmlm = i
            for j in range(0, col-rows_cols+1, stride):         #sütun loop'u
                bmlm = j//stride
                mlm = j
                victo = 0
                i = hmlm
                for a in range(rows_cols):          #çarpım için loop
                    j = mlm
                    for d in range(rows_cols):
                        victo += (float(nl[i][j][k]) * float(fltr_arr[a][d]))           #filtreye denk gelen sayıyla çarpıyorum
                        j += 1
                    i += 1
                if victo<0:         #çarpımı elde ettim bir değişkene eşitledim
                    victo = 0
                if victo>255:
                    victo = 255
                if type(victo) == float:
                    victo = int(victo)
                new_img_lst[bhmlm][bmlm].append(victo)          #değeri boş listeye atıyorum
    img_printer(new_img_lst)


def op5(nl):    #convolution with same dimensions with the input
    row = len(nl)
    col = len(nl[0])
    cha = len(nl[0][0])
    filter = input()
    stride = int(input())
    fp2 = open(filter)
    fltr_lst = fp2.read().split()
    fltr_arr = []
    rows_cols = int(len(fltr_lst) ** 0.5)
    nl = (rows_cols//2)*[row*[[0,0,0]]] + nl + (rows_cols//2)*[row*[[0,0,0]]]           #satır sayısını arttırdım
    for rw in range(len(nl)):
        nl[rw] = (rows_cols//2)*[[0,0,0]] + nl[rw] + (rows_cols//2)*[[0,0,0]]           #sütun sayısını artırdım
    hs = 0
    row = len(nl)
    col = len(nl[0])
    cha = len(nl[0][0])
    for c in range(rows_cols):          #op4 ile aynı
        rowe=[]
        for i in range(rows_cols):
            rowe.append(fltr_lst[hs])
            hs+=1
        fltr_arr.append(rowe)
    new_img_lst = []
    for sy in range(0, row-rows_cols+1, stride):
        new_row = []
        for df in range(0, col-rows_cols+1, stride):
            new_row.append([])
        new_img_lst.append(new_row)
    for k in range(cha):
        for i in range(0, row-rows_cols+1, stride):
            bhmlm = i//stride
            hmlm = i
            for j in range(0, col-rows_cols+1, stride):
                bmlm = j//stride
                mlm = j
                victo = 0
                i = hmlm
                for a in range(rows_cols):
                    j = mlm
                    for d in range(rows_cols):
                        victo += (float(nl[i][j][k]) * float(fltr_arr[a][d]))
                        j += 1
                    i += 1
                if victo<0:
                    victo = 0
                if victo>255:
                    victo = 255
                if type(victo) == float:
                    victo = int(victo)
                new_img_lst[bhmlm][bmlm].append(victo)
    img_printer(new_img_lst)


def quantization(frst, scnd, rango, nl, a, b, down_ch):             #op6 için karşılaştırma fonksiyonu
    it_is_ok = True
    for val in range(3):            #üç renk için de baktım
        if it_is_ok == False:
            break
        try:
            if float(abs(frst[val] - scnd[val])) >= rango:
                it_is_ok = False
        except:
            continue
    if it_is_ok:        #tamamsa eşitledim
        scnd = frst
    if down_ch:         #tekrar listeye geçirmem gerekti
        if a + 1 < row:
            nl[a + 1][b] = scnd
        elif a + 1 == row:
            if b + 1 <= col:
                nl[a][b + 1] = scnd
    elif down_ch == False:
        if a-1 >= 0:
            nl[a-1][b] = scnd
        elif a == 0:
            if b+1 <= col:
                nl[a][b+1] = scnd
def up_and_down(rango, nl, a=0, b=0, down_ch = True):       #piksel değiştirme fonksiyonu
    if down_ch:         #aşağı doğru gitmek için boolean tanımladım ve arada değiştiriyorum
        if a+1 < row:           #aşağıda satır kaldıysa
            frst = nl[a][b]                 #iki piksel için farklı değişkenler atadım
            scnd = nl[a+1][b]
            quantization(frst, scnd, rango, nl, a, b, down_ch)                #karşılaştırdım
            a+=1            #aşağı indim
            up_and_down(rango, nl, a, b, down_ch)           #baştan bakıyorum
        elif a+1 == row:            #aşağıda satır kalmadıysa
            if b+1 < col:           #sağda yer kaldıysa
                frst = nl[a][b]
                scnd = nl[a][b+1]
                quantization(frst, scnd, rango, nl, a, b, down_ch)
                b+=1            #sağa gittim
                down_ch = False         #şimdi yukarıya doğru gitcek
                up_and_down(rango, nl, a, b, down_ch)
            else:           #sağda yer kalmadıysa bitiryorum
                return
    else:           #yön yukarıysa
        if a-1 >= 0:            #yukarıda satır kaldıysa
            frst = nl[a][b]
            scnd = nl[a-1][b]
            quantization(frst, scnd, rango, nl, a, b, down_ch)
            a-=1
            up_and_down(rango, nl, a, b, down_ch)
        elif a == 0:            #yukarıda satır kalmadıysa
            if b+1 < col:           ##sağda yer kaldıysa
                frst = nl[a][b]
                scnd = nl[a][b+1]
                quantization(frst, scnd, rango, nl, a, b, down_ch)
                b+=1        #sağa gittim
                down_ch = True
                up_and_down(rango, nl, a, b, down_ch)
            else:               #sağda yer kalmadıysa bitiriyorum
                return

def op6(nl):        #color quantization
    rango = float(input())
    up_and_down(rango, nl)
    img_printer(nl)


def quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch):        #op6 ile aynı şeyler fakat bu sefer sağa sola gitme boolean'ı var
    if float(abs(frst - scnd)) < rango:
        scnd = frst                 #op6'dan diğer farkı değişkenler piksellere değil renklerin değerlerine eşit
    if right_ch:
        if down_ch:
            if a + 1 < row:
                nl[a + 1][b][c] = scnd
            elif a + 1 == row:
                if b + 1 < col:
                    nl[a][b + 1][c] = scnd
                else:
                    if c < 2:
                        nl[a][b][c+1] = scnd
        else:
            if a - 1 >= 0:
                nl[a - 1][b][c] = scnd
            elif a == 0:
                if b + 1 < col:
                    nl[a][b + 1][c] = scnd
                else:
                    if c < 2:
                        nl[a][b][c+1] = scnd
    else:                   # bu if-elselerin hepsi listeye geçirmek için
        if down_ch:
            if a + 1 < row:
                nl[a + 1][b][c] = scnd
            elif a + 1 == row:
                if b - 1 >= 0:
                    nl[a][b - 1][c] = scnd
                else:
                    if c < 2:
                        nl[a][b][c+1] = scnd
        else:
            if a - 1 >= 0:
                nl[a - 1][b][c] = scnd
            elif a == 0:
                if b - 1 >= 0:
                    nl[a][b - 1][c] = scnd
                else:
                    if c < 2:
                        nl[a][b][c+1] = scnd


def up_and_down_for_op7(rango, nl, a=0, b=0, c=0, down_ch = True, right_ch = True):
    if right_ch:        #sağa gidiliyorsa
        if down_ch:         #aşağı gidiliyorsa
            if a + 1 < row:         #aşağıda yer var mı?
                frst = nl[a][b][c]
                scnd = nl[a + 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a += 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a + 1 == row:          #yoksa
                if b + 1 < col:         #sağda yer var mı?
                    frst = nl[a][b][c]
                    scnd = nl[a][b + 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b += 1
                    down_ch = False
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:       #yoksa
                    if c < 2:           #renk kaldı mı?
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = False         #artık yön yukarı
                        right_ch = False           #artık yön sola
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:           #kalmadıysa bitir
                        return
        else:           #yukarı gidiliyorsa
            if a - 1 >= 0:          #yukarıda yer var mı
                frst = nl[a][b][c]
                scnd = nl[a - 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a -= 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a == 0:            #yoksa
                if b + 1 < col:         #sağda yer var mı
                    frst = nl[a][b][c]
                    scnd = nl[a][b + 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b += 1
                    down_ch = True      #artık yön aşağı
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:           #yoksa
                    if c < 2:           #renk kaldı mı?
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = True      #artık yön aşağı
                        right_ch = False        #artık yön sola
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:           #kalmamışsa bitir
                        return

    else:           #sola gidiliyorsa
        if down_ch:         #aşağı gidiliyorsa
            if a + 1 < row:             #aşağıda yer var mı
                frst = nl[a][b][c]
                scnd = nl[a + 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a += 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a + 1 == row:              #yoksa
                if b - 1 >= 0:              #solda yer var mı
                    frst = nl[a][b][c]
                    scnd = nl[a][b - 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b -= 1
                    down_ch = False
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:               #yoksa
                    if c < 2:           #renk kaldı mı?
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = False
                        right_ch = True
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:               #kalmamışsa bitir
                        return
        else:           #yukarı gidiliyorsa
            if a - 1 >= 0:              #yukarıda yer var mı?
                frst = nl[a][b][c]
                scnd = nl[a - 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a -= 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a == 0:            #yoksa
                if b - 1 >= 0:          #solda yer var mı?
                    frst = nl[a][b][c]
                    scnd = nl[a][b - 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b -= 1
                    down_ch = True
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:               #yoksa
                    if c < 2:           #renk kaldı mı?
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = True
                        right_ch = True
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:           #kalmadıysa bitir
                        return


def op7(nl):    #3d color quantization
    rango = float(input())
    up_and_down_for_op7(rango, nl)
    img_printer(nl)




if operation==1:
    op1(nl)
if operation==2:
    op2(nl)
if operation==3:
    op3(nl)
if operation==4:
    op4(nl)
if operation==5:
    op5(nl)
if operation==6:
    op6(nl)
if operation==7:
    op7(nl)
# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE



# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE


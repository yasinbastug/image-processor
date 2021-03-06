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
                nl[i][j][k] = round(((channel_value-channel_mean)/channel_sd),4)           #de??eri e??itliyorum
    img_printer(nl)
def op3(nnll):  #black and white
    for i in range(row):
        for j in range(col):
            sum = 0
            for k in range(cha):
                sum = sum + nl[i][j][k]         #de??erleri topluyorum
            average = sum//cha          #ortalamay?? buluyorum
            for k in range(cha):
                nl[i][j][k] = average           #de??ere e??itliyorum
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
            rowe.append(float(fltr_lst[hs]))        #filtreyi listeye ??evirdim
            hs+=1
        fltr_arr.append(rowe)
    new_img_lst = []
    for sy in range(0, row-rows_cols+1, stride):
        new_row = []
        for df in range(0, col-rows_cols+1, stride):            #do??ru say??da bo?? listeye sahip bo?? liste haz??rlad??m
            new_row.append([])
        new_img_lst.append(new_row)
    for k in range(cha):            #her renk i??in loop
        for i in range(0, row-rows_cols+1, stride):         #sat??r loop'u
            bhmlm = i//stride
            hmlm = i
            for j in range(0, col-rows_cols+1, stride):         #s??tun loop'u
                bmlm = j//stride
                mlm = j
                victo = 0
                i = hmlm
                for a in range(rows_cols):          #??arp??m i??in loop
                    j = mlm
                    for d in range(rows_cols):
                        victo += (float(nl[i][j][k]) * float(fltr_arr[a][d]))           #filtreye denk gelen say??yla ??arp??yorum
                        j += 1
                    i += 1
                if victo<0:         #??arp??m?? elde ettim bir de??i??kene e??itledim
                    victo = 0
                if victo>255:
                    victo = 255
                if type(victo) == float:
                    victo = int(victo)
                new_img_lst[bhmlm][bmlm].append(victo)          #de??eri bo?? listeye at??yorum
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
    nl = (rows_cols//2)*[row*[[0,0,0]]] + nl + (rows_cols//2)*[row*[[0,0,0]]]           #sat??r say??s??n?? artt??rd??m
    for rw in range(len(nl)):
        nl[rw] = (rows_cols//2)*[[0,0,0]] + nl[rw] + (rows_cols//2)*[[0,0,0]]           #s??tun say??s??n?? art??rd??m
    hs = 0
    row = len(nl)
    col = len(nl[0])
    cha = len(nl[0][0])
    for c in range(rows_cols):          #op4 ile ayn??
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


def quantization(frst, scnd, rango, nl, a, b, down_ch):             #op6 i??in kar????la??t??rma fonksiyonu
    it_is_ok = True
    for val in range(3):            #???? renk i??in de bakt??m
        if it_is_ok == False:
            break
        try:
            if float(abs(frst[val] - scnd[val])) >= rango:
                it_is_ok = False
        except:
            continue
    if it_is_ok:        #tamamsa e??itledim
        scnd = frst
    if down_ch:         #tekrar listeye ge??irmem gerekti
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
def up_and_down(rango, nl, a=0, b=0, down_ch = True):       #piksel de??i??tirme fonksiyonu
    if down_ch:         #a??a???? do??ru gitmek i??in boolean tan??mlad??m ve arada de??i??tiriyorum
        if a+1 < row:           #a??a????da sat??r kald??ysa
            frst = nl[a][b]                 #iki piksel i??in farkl?? de??i??kenler atad??m
            scnd = nl[a+1][b]
            quantization(frst, scnd, rango, nl, a, b, down_ch)                #kar????la??t??rd??m
            a+=1            #a??a???? indim
            up_and_down(rango, nl, a, b, down_ch)           #ba??tan bak??yorum
        elif a+1 == row:            #a??a????da sat??r kalmad??ysa
            if b+1 < col:           #sa??da yer kald??ysa
                frst = nl[a][b]
                scnd = nl[a][b+1]
                quantization(frst, scnd, rango, nl, a, b, down_ch)
                b+=1            #sa??a gittim
                down_ch = False         #??imdi yukar??ya do??ru gitcek
                up_and_down(rango, nl, a, b, down_ch)
            else:           #sa??da yer kalmad??ysa bitiryorum
                return
    else:           #y??n yukar??ysa
        if a-1 >= 0:            #yukar??da sat??r kald??ysa
            frst = nl[a][b]
            scnd = nl[a-1][b]
            quantization(frst, scnd, rango, nl, a, b, down_ch)
            a-=1
            up_and_down(rango, nl, a, b, down_ch)
        elif a == 0:            #yukar??da sat??r kalmad??ysa
            if b+1 < col:           ##sa??da yer kald??ysa
                frst = nl[a][b]
                scnd = nl[a][b+1]
                quantization(frst, scnd, rango, nl, a, b, down_ch)
                b+=1        #sa??a gittim
                down_ch = True
                up_and_down(rango, nl, a, b, down_ch)
            else:               #sa??da yer kalmad??ysa bitiriyorum
                return

def op6(nl):        #color quantization
    rango = float(input())
    up_and_down(rango, nl)
    img_printer(nl)


def quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch):        #op6 ile ayn?? ??eyler fakat bu sefer sa??a sola gitme boolean'?? var
    if float(abs(frst - scnd)) < rango:
        scnd = frst                 #op6'dan di??er fark?? de??i??kenler piksellere de??il renklerin de??erlerine e??it
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
    else:                   # bu if-elselerin hepsi listeye ge??irmek i??in
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
    if right_ch:        #sa??a gidiliyorsa
        if down_ch:         #a??a???? gidiliyorsa
            if a + 1 < row:         #a??a????da yer var m???
                frst = nl[a][b][c]
                scnd = nl[a + 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a += 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a + 1 == row:          #yoksa
                if b + 1 < col:         #sa??da yer var m???
                    frst = nl[a][b][c]
                    scnd = nl[a][b + 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b += 1
                    down_ch = False
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:       #yoksa
                    if c < 2:           #renk kald?? m???
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = False         #art??k y??n yukar??
                        right_ch = False           #art??k y??n sola
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:           #kalmad??ysa bitir
                        return
        else:           #yukar?? gidiliyorsa
            if a - 1 >= 0:          #yukar??da yer var m??
                frst = nl[a][b][c]
                scnd = nl[a - 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a -= 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a == 0:            #yoksa
                if b + 1 < col:         #sa??da yer var m??
                    frst = nl[a][b][c]
                    scnd = nl[a][b + 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b += 1
                    down_ch = True      #art??k y??n a??a????
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:           #yoksa
                    if c < 2:           #renk kald?? m???
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = True      #art??k y??n a??a????
                        right_ch = False        #art??k y??n sola
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:           #kalmam????sa bitir
                        return

    else:           #sola gidiliyorsa
        if down_ch:         #a??a???? gidiliyorsa
            if a + 1 < row:             #a??a????da yer var m??
                frst = nl[a][b][c]
                scnd = nl[a + 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a += 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a + 1 == row:              #yoksa
                if b - 1 >= 0:              #solda yer var m??
                    frst = nl[a][b][c]
                    scnd = nl[a][b - 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b -= 1
                    down_ch = False
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:               #yoksa
                    if c < 2:           #renk kald?? m???
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = False
                        right_ch = True
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:               #kalmam????sa bitir
                        return
        else:           #yukar?? gidiliyorsa
            if a - 1 >= 0:              #yukar??da yer var m???
                frst = nl[a][b][c]
                scnd = nl[a - 1][b][c]
                quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                a -= 1
                up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
            elif a == 0:            #yoksa
                if b - 1 >= 0:          #solda yer var m???
                    frst = nl[a][b][c]
                    scnd = nl[a][b - 1][c]
                    quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                    b -= 1
                    down_ch = True
                    up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                else:               #yoksa
                    if c < 2:           #renk kald?? m???
                        frst = nl[a][b][c]
                        scnd = nl[a][b][c+1]
                        quantization_for_op7(frst, scnd, rango, nl, a, b, c, down_ch, right_ch)
                        c += 1
                        down_ch = True
                        right_ch = True
                        up_and_down_for_op7(rango, nl, a, b, c, down_ch, right_ch)
                    else:           #kalmad??ysa bitir
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


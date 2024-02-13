import time 
import random

class Token :
    def __init__(self,data,koor) :
        self.data = data
        self.koor = koor

    def __str__(self):
        return f"{self.data}"
    
class Sequence :
    def __init__(self, data, poin) :
        self.sequence = data
        self.poin = poin
    
    def __str__(self) :
        return f"{self.sequence}"
    
class pohon :
    def __init__(self, data, koor) :
        self.value = Token(data, koor)
        self.children = []
        self.parent = None
    
    def add_child(self, child) :
        child.parent = self
        self.children.append(child)

    def get_level(self) : 
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    
    def display_tree(self) :
        space = " " * self.get_level() * 2
        print(space + str(self.value.data)) 
        if self.children :
            for child in self.children :
                child.display_tree()

    def isTaken(self, ortu) :
        taken = False
        p = ortu
        while not taken and p :
            if self.value.koor == p.value.koor:
                taken = True
                break
            else :
                p = p.parent
        return taken
    
    def cari_seq(self, idx_brs, idx_kol, vertikal, ctr, matrix) : 
        if ctr > 0 :
            if vertikal :
                for i in range(0,len(matrix)) :
                    child = pohon(matrix[i][idx_kol].data,(i,idx_kol))
                    if not child.isTaken(self) : 
                        self.add_child(child)
                        vertikal = False
                        child.cari_seq(i, idx_kol, vertikal, ctr-1, matrix)                     
            else :
                for i in range(0,len(matrix[0])) :
                    child = pohon(matrix[idx_brs][i].data,(idx_brs,i))
                    if not child.isTaken(self) :
                        self.add_child(child)
                        vertikal = True
                        child.cari_seq(idx_brs,i, vertikal, ctr-1, matrix)

def bacaData(namaFile) : 
    try :
        with open(namaFile, 'r') as file:
            lines = file.readlines()

        matrix = []
        for line in lines:
            row = [str(num) for num in line.strip().split()]
            matrix.append(row)
    
        buffer = int(matrix[0][0])-1
        nbrs = int(matrix[1][0])
        nkol = int(matrix[1][1])
        mtrx = []
        for i in range(2,nbrs+2) :
            baris = matrix[i]
            mtrx.append(baris)
        nseq = int(matrix[nbrs+2][0])
        seq = []
        for i in range(nbrs+3,nbrs+3+nseq+nseq) :
            baris = matrix[i]
            seq.append(baris)

        lseq = makeListSequence(seq)
        return buffer, nbrs, nkol, mtrx, nseq, lseq 
    except FileNotFoundError :
        print("File tidak ditemukan") 
        nama = input("Masukkan Path File yang benar : ")
        buffer, nbrs, nkol, mtrx, nseq, lseq = bacaData(nama)
        return buffer, nbrs, nkol, mtrx, nseq, lseq  

def makeMatrixToken(matriks) :
    matrixToken = []
    for i in range(0,len(matriks)) :
        mcol = []
        for j in range(0,len(matriks[0])) :
            col = Token(matriks[i][j],(i,j))
            mcol.append(col)
        matrixToken.append(mcol)
    return matrixToken

def printMatrixToken(matriks) :
    for i in range(0,len(matriks)) :
        for j in range(0,len(matriks[0])) :
            print(matriks[i][j].data, end=" ")
        print()

def makeListSequence(seq) :
    listSequence = []
    for i in range(0,len(seq),2) :
        poin = seq[i+1][0]
        s = Sequence(seq[i], poin)
        listSequence.append(s)
    return listSequence
 
def printListSequence(seq) : 
    for data in seq :
        print(data.sequence)
        print(data.poin)
    
        
def poinBuffer(buffer, lseq):
    total_poin = 0
    for seq in lseq :
        if cocokin_seq(seq,buffer) :
            total_poin = total_poin + int(seq.poin)
    return total_poin

def maks_poin(lbuffer, lseq) :
    maks = 0
    buff_maks = []
    for buffer in lbuffer :
        poin_buffer = poinBuffer(buffer, lseq)
        if poin_buffer > maks :
            maks = poin_buffer
            buff_maks = buffer    
    return maks, buff_maks

def cocokin_seq(sequence, token) :
    if len(token) >= len(sequence.sequence) :
        for i in range(0, (len(token)-len(sequence.sequence)+1)) :
            j = 0
            while j < len(sequence.sequence) and sequence.sequence[j] == token[i+j].data :
                j = j + 1
            if j == len(sequence.sequence) :
                return True    
        return False 
    else :
        return False  

def tree_to_array(root, path=[]):
    if not root:
        return []
    path = path + [root.value]
    if not root.children:
        return [path]
    paths = []
    for child in root.children:
        paths.extend(tree_to_array(child, path))

    return paths
    
def bacaCLI() :
    jumlah_token_unik = int(input("Masukkan Jumlah Token Unik = "))
    token = input("Masukkan Token Unik = ").split(" ")
    ukuran_buffer = int(input("Masukkan Ukuran Buffer = "))
    ukuran_matriks = input("Masukkan Ukuran Matrix = ").split(" ")
    mbaris = int(ukuran_matriks[0])
    mkolom = int(ukuran_matriks[1])
    jumlah_sekuens = int(input("Masukkan Jumlah Sekuens = "))
    ukuran_maksimal_sekuens = int(input("Masukkan Ukuran Maksimal Sekuens = "))

    matrix = [["" for i in range(mkolom)] for j in range(mkolom)]

    for i in range(mbaris) :
        for j in range(mkolom) :
            random_int = random.randint(0,jumlah_token_unik-1)
            matrix[i][j] = token[random_int]

    list_sekuens = []
    for i in range(jumlah_sekuens) :
        random_poin = 5*random.randint(0,20)
        random_nseq = random.randint(2,ukuran_maksimal_sekuens)
        lseq = []
        for j in range(random_nseq) :
            random_int = random.randint(0,jumlah_token_unik-1)
            lseq.append(token[random_int])
        sekuens = Sequence(lseq, random_poin)
        list_sekuens.append(sekuens)

    return ukuran_buffer, mbaris, mkolom, matrix, jumlah_sekuens, list_sekuens

def simpantxt(namaFile, nilai, sekuens, waktu) :
    token = str('')
    for i in sekuens :
        token = token + str(i.data) + ' '
    koordinat = str('')
    for i in sekuens :
        koordinat = koordinat + str((i.koor[1]+1)) + ' ' + str(i.koor[0]+1) + '\n'

    with open(namaFile, 'w') as file :
        file.write(str(nilai) + '\n')
        file.write(token + '\n')
        file.write(koordinat + '\n')
        file.write(str(f"{(waktu)*10**3:.03f} ms"))

def mulai() :
    print("Selamat datang di Cyberpunk 2077 Breach Protokol\n")

    print("Pilihan yang tersedia")
    print("1. Menggunakan File txt")
    print("2. Menggunakan Command Line Interface\n")

    pilih = input("Masukkan nomor yang diinginkan\n")
    while pilih != '1' and pilih != '2' :
        print("Masukkan tidak valid")
        pilih = input("Masukkan nomor yang diinginkan\n")

    ukuran_buffer, mbaris, mkolom, matrix, jumlah_sekuens, list_sekuens = int, int, int, [], int, []
    if pilih == '1' :
        nama = input("Masukkan path menuju file : ")
        ukuran_buffer, mbaris, mkolom, matrix, jumlah_sekuens, list_sekuens = bacaData(nama)
    elif pilih == '2' : 
        ukuran_buffer, mbaris, mkolom, matrix, jumlah_sekuens, list_sekuens = bacaCLI()

    start = time.time()
    mtoken = makeMatrixToken(matrix)
    print()
    printMatrixToken(mtoken)
    print()
    printListSequence(list_sekuens)
    print()

    hasil_akhir = []
    for i in range (1,ukuran_buffer+1):
        for j in range(0,len(mtoken[0])) :
            seq2 = pohon(mtoken[0][j].data,(0,j))
            seq2.cari_seq(0,j,True,i,mtoken)
            result_array = tree_to_array(seq2)
            for k in result_array :
                hasil_akhir.append(k)
    maks, buffer_maks = maks_poin(hasil_akhir,list_sekuens)
    print(maks)
    for i in buffer_maks :
        print(i.data, end=" ")
    print()
    for i in buffer_maks :
        print((i.koor[1]+1), (i.koor[0]+1))
    end  = time.time()
    print(f"\nTime taken: {(end-start)*10**3:.03f} ms\n")

    simpan = input("Apakah ingin menyimpan solusi? (y/n)\n")
    while simpan != 'y' and simpan != 'n' and simpan != 'Y' and simpan != 'N' :
        print('Masukkan tidak valid')
        simpan = input("Apakah ingin menyimpan solusi? (y/n)\n")

    if simpan == 'y' or simpan == 'Y' :
        nama_simpan = input("Masukkan nama file yang ingin disimpan : ")
        simpantxt(nama_simpan, maks, buffer_maks, end-start)
     
mulai()
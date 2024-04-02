import cv2 as cv
import numpy as np
from skimage.segmentation import clear_border

def comparar(ref, imagem):
    n_label, label = cv.connectedComponents(imagem)
    label = np.uint8(label)

    val = np.zeros((0,1))

     # - Laco para comparar 
    for n in range(1, n_label):
        elemento = np.uint8(label.copy() == n) * 255

        cont1, _ = cv.findContours(ref, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cont2, _ = cv.findContours(elemento, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Verifica Aproximidade 
        aprox = [cv.matchShapes(cont1[0], cont2[0], cv.CONTOURS_MATCH_I3, 0)]
        val = np.append(val, [aprox], axis=0)
    
    # Quanto menor, menos diferentes
    placa = np.argmin(val) + 1
    regiao = np.uint8(label.copy() == placa) * 255
    return regiao

def canny_2(imagem, ll, lh):
    # - Filtro Gaussiano
    kernel = (3,3)
    gauss = cv.GaussianBlur(imagem, kernel, 0)

    # - Kernel: Leitura Horizontal
    ku = np.array([[-1, 0, 1], 
                   [-2, 0, 2], 
                   [-1, 0, 1]])

    # - Kernel: Leitura Vertical
    kv = np.transpose(ku.copy())

    # - Filtro Horizontal
    bu = cv.filter2D(gauss.astype(np.float64), -1, ku, borderType=cv.BORDER_REPLICATE)

    # - Filtro Vertical
    bv = cv.filter2D(gauss.astype(np.float64), -1, kv, borderType=cv.BORDER_REPLICATE)

    # Magnitude
    mi = np.sqrt(np.add(np.power(bu, 2), np.power(bv, 2)))

    # Gradiente
    gi = np.degrees(np.arctan2(bv, bu)) # Escala em Graus

    linha, coluna = gauss.shape
    gn = np.zeros((linha, coluna))

    for v in range(1, linha-1):
        for u in range(1, coluna-1):
            theta = gi[v,u]

            # Comparar: Esquerda e Direita
            if (theta >= -22.5 and theta < 22.5) or (theta < -157.5 or theta >= 157.5):
                if mi[v,u] > mi[v, (u+1)] and mi[v, u] > mi[v, (u-1)]:
                    gn[v,u] = mi[v,u]

            # Comparar: Diagonal Superior Direito
            if (theta < -22.5 and theta >= -67.5) or (theta >= 122.5 and theta < 157.5):
                if mi[v,u] > mi[(v-1), (u+1)] and mi[v,u] > mi[(v+1),(u-1)]:
                    gn[v,u] = mi[v,u]

            # Comparar: Em Cima e Em Baixo
            if (theta < -67.5 and theta >= -112.5) or (theta < 122.5 and theta >= 67.5):
                 if mi[v,u] > mi[(v-1), u] and mi[v,u] > mi[(v+1), u]:
                     gn[v,u] = mi[v,u]

            # Comparar: Diagonal Superior Esquerdo
            if (theta < -122.5 and theta >= -157.5) or (theta < 67.5 and theta >= 22.5):
                if mi[v,u] > mi[(v-1), (u-1)] and mi[v,u] > mi[(v+1),(u+1)]:
                    gn[v,u] = mi[v,u]

    gn = np.clip(gn, 0, 255).astype(np.uint8)   # Escala: uint8

    # Gnh
    _, gnh = cv.threshold(gn, lh, 255, cv.THRESH_BINARY)

    # Gnl
    _, gnl = cv.threshold(gn, ll, 255, cv.THRESH_BINARY)

    gnl = gnh - gnl

    gnl2 = np.zeros((linha, coluna))

    for v in range(1, linha-1):
        for u in range(1, coluna-1):
            if (gnh[v, u] != 0):
                gnl2[v-1:v+1, u-1:u+1] = gnl[v-1:v+1, u-1:u+1]

    borda = gnh + gnl2
    borda = np.clip(borda, 0, 255).astype(np.uint8)   # Escala: uint8
    #cv.imshow('Borda', borda)

    return borda

def placa(imagem, flag):
    gray = cv.cvtColor(imagem.copy(), cv.COLOR_BGR2GRAY)

    # - Borrar Imagem
    if (flag == 1):
        blur = cv.bilateralFilter(gray.copy(), 5, 19, 125)

    else:
        blur = cv.bilateralFilter(gray.copy(), 5, 123, 55)

    # Limiar OTSU
    thresh, _ = cv.threshold(blur.copy(), 55, 255, cv.THRESH_OTSU)

    # Detectar Borda
    borda = canny_2(blur.copy(), thresh, 200)

    # Limpeza de Borda
    borda = clear_border(borda)

    mascara = np.zeros_like(borda)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    morph = cv.morphologyEx(borda, cv.MORPH_DILATE, kernel)

    # Flag: 1 - Placas Proximas
    if (flag == 1):
        # Primeiro Rotulamento 
        n_label, label = cv.connectedComponents(morph)
        label = np.uint8(label)

        # - Limpeza de Pequenos Ruidos
        altura_max = 0

        for n in range(1, n_label):
            elemento = np.uint8(label.copy() == n) * 255
            ind = np.where(elemento == 255)
            min_y = np.min(ind[0])
            max_y = np.max(ind[0])
            altura = max_y - min_y

            if altura > altura_max:
                altura_max = altura

        limite = 0.6

        for n in range(1, n_label):
            elemento = np.uint8(label.copy() == n) * 255
            ind = np.where(elemento == 255)
            min_y = np.min(ind[0])
            max_y = np.max(ind[0])
            altura = max_y - min_y

            if altura > (altura_max * limite):
                mascara = cv.bitwise_or(mascara, elemento)

    # Flag: Placas Longes
    else:
        # Busca por formas fechadas
        contour, _ = cv.findContours(morph, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour = sorted(contour, key=cv.contourArea, reverse=True)[:5]
        cv.drawContours(mascara, contour, -1, 255)

    # - Retangulo de referencia
    ref = np.zeros((500, 800))
    cv.rectangle(ref, (200, 200), (450, 300), 255, 1)
    ref = np.uint8(ref)

    # Buscar pelo elemento mais proximo da referencia
    regiao = comparar(ref, mascara)

    # Contorno do elemento
    countours, _ = cv.findContours(regiao, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Ponto inicial e final do retangulo
    for contour in countours:
        x, y, w, h = cv.boundingRect(contour)

    new = imagem.copy()
    cv.rectangle(new, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # - Corte de regiao de interesse
    corte = imagem[y:y+h, x:x+w, :].copy()
    
    return (corte, new) 









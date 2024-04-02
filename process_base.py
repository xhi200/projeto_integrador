import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from scipy.interpolate import interp1d
import pickle


def calcular_momentos(imagem, ordem_q, ordem_p, tipo):
    linhas, colunas = imagem.shape

    # Inicializa os momentos Q, P e o momento como zero
    momento_q = 0
    momento_p = 0
    momento = 0

    if tipo == "m00":
        for i in range(linhas):
            for j in range(colunas):
                # Calcula o momento Q
                momento += (i ** ordem_q) * (j ** ordem_q) * imagem[i, j]



        return momento

    if tipo == "m01":
        for i in range(linhas):
            for j in range(colunas):
                # Calcula o momento
                momento += j * imagem[i, j]

        return momento

    if tipo == "m10":
        for i in range(linhas):
            for j in range(colunas):
                # Calcula o momento
                momento += i * imagem[i, j]

        return momento

def encontrar_bordas(I):
    v, u = np.where(I)
    umin = np.min(u)
    umax = np.max(u)
    vmin = np.min(v)
    vmax = np.max(v)
    _, u2 = np.where(I[vmin:vmin + 1, :])
    u2min = np.min(u2)

    uo = u2min
    vo = vmin
    uBorda = [uo]
    vBorda = [vo]
    vc = vo
    uc = uo
    pos = 1
    fim = False

    while not fim:
        if pos == 1:
            if I[vc, uc - 1] == 1:
                vBorda.append(vc)
                uBorda.append(uc - 1)
                pos = 7
                uc -= 1
            elif pos == 1:
                pos = 2

        if pos == 2:
            if I[vc - 1, uc - 1] == 1:
                vBorda.append(vc - 1)
                uBorda.append(uc - 1)
                pos = 7
                vc -= 1
                uc -= 1
            elif pos == 2:
                pos = 3

        if pos == 3:
            if I[vc - 1, uc] == 1:
                vBorda.append(vc - 1)
                uBorda.append(uc)
                pos = 1
                vc -= 1
            elif pos == 3:
                pos = 4

        if pos == 4:
            if I[vc - 1, uc + 1] == 1:
                vBorda.append(vc - 1)
                uBorda.append(uc + 1)
                pos = 1
                vc -= 1
                uc += 1
            elif pos == 4:
                pos = 5

        if pos == 5:
            if I[vc, uc + 1] == 1:
                vBorda.append(vc)
                uBorda.append(uc + 1)
                pos = 3
                uc += 1
            elif pos == 5:
                pos = 6

        if pos == 6:
            if I[vc + 1, uc + 1] == 1:
                vBorda.append(vc + 1)
                uBorda.append(uc + 1)
                pos = 3
                vc += 1
                uc += 1
            elif pos == 6:
                pos = 7

        if pos == 7:
            if I[vc + 1, uc] == 1:
                vBorda.append(vc + 1)
                uBorda.append(uc)
                pos = 5
                vc += 1
            elif pos == 7:
                pos = 8

        if pos == 8:
            if I[vc + 1, uc - 1] == 1:
                vBorda.append(vc + 1)
                uBorda.append(uc - 1)
                pos = 5
                vc += 1
                uc -= 1

            elif pos == 8:
                pos = 1

        if vc == vo and uc == uo and len(uBorda) > 1:
            fim = True

    return uBorda,vBorda


def limiarizar_imagem(imagem, limiar):


    # imagem_limiarizada= imagem <limiar

    imagem_limiarizada = imagem

    height = imagem.shape[0]
    width = imagem.shape[1]
    # print(imagem.shape)

    for y in range(height):
        for x in range(width):
            if imagem[y][x]< limiar:
                imagem_limiarizada[y][x]= 1
            else:
                imagem_limiarizada[y][x] = 0

    # print(type(imagem_limiarizada))

    # # # Exibe a imagem limiarizada
    # plt.imshow(imagem_limiarizada)
    # plt.title('mimiar')
    # plt.show()

    #  # Converte a imagem para o tipo logical
    #  imagem_limiarizada = imagem_limiarizada.astype(bool)
    #
    # # Converte a imagem para o tipo uint8 (0 para False, 255 para True)
    # imagem_limiarizada = imagem_limiarizada.astype('uint8') * 255




    return imagem_limiarizada

def f_norm_cc(crv_dist, crv_dist_comp):
    # Normalização das curvas
    x1 = crv_dist - np.mean(crv_dist)
    x2 = crv_dist_comp - np.mean(crv_dist_comp)

    y1 = x1 / np.sqrt(np.sum(x1 ** 2))
    y2 = x2 / np.sqrt(np.sum(x2 ** 2))

    plo1 = y1
    plo2 = y2

    correlacao = np.zeros(500)

    for k in range(500):
        y2 = np.roll(y2, 1)
        correlacao[k] = np.sum(y1 * y2)

        # plt.clf()
        # plt.subplot(1, 2, 1)
        # plt.plot(y1, color='r', linestyle='-')
        # plt.plot(y2, color='k', linestyle='-')
        # plt.title('Ilustração da operação de correlação circular')
        # plt.legend(['Img. Referência', 'Img. Atual'])
        #
        # plt.subplot(1, 2, 2)
        # plt.plot(correlacao[:k + 1])
        # plt.ylim([-0.65, 1])
        # plt.xlim([1, 500])
        # plt.title('Curva de Correlação')
        #
        # plt.pause(0.0001)



    ret = np.max(correlacao)

    return ret


def f_interpolation(x, y, num):
    x_vals = np.arange(1, len(x) + 1)
    xi = np.linspace(1, len(x), num)

    f_rows = interp1d(x_vals, y, kind='linear', fill_value="extrapolate")
    f_cols = interp1d(x_vals, x, kind='linear', fill_value="extrapolate")

    new_rows = f_rows(xi)
    new_cols = f_cols(xi)

    return new_cols, new_rows

def curvas_distancia(imagem1):


    # Define o valor de limiar
    limiar1 = 200

    # Aplica a limiarização na primeira imagem

    imagem_limiarizada1 = limiarizar_imagem(imagem1, limiar1)
    # plt.imshow(imagem_limiarizada1)
    # plt.show()


    # Chamada da função para encontrar as bordas
    bordas_x, bordas_y = encontrar_bordas(imagem_limiarizada1)

    bordas_x.pop()
    bordas_y.pop()
    # print(len(bordas_y),len(bordas_x))

    # for b in range(pp):
    #     print(bordas_x[b],bordas_y[b])

    # print(len(bordas_yi))

    # plt.scatter(bordas_x, bordas_y, color='blue', marker='+')



    # # Configurar os eixos
    # plt.axis('off')
    #
    # # Exibir o gráfico
    # plt.show()
    #



    #
    # # Imprime as posições dos pixels de borda
    # for linha, coluna in zip(bordas_y, bordas_x):
    #     # print((linha,coluna))
    #     imagem_limiarizada1[linha, coluna] = 0.5
    #
    # # print(imagem_limiarizada1[linha, coluna])
    # # plt.imshow(imagem_limiarizada1)
    # # plt.show()
    #
    #
    # # exit(1)
    #




    ordem_q1 = 0
    ordem_p1 = 0

    # Cálculo dos momentos de Inércia
    momento_m00_1 = calcular_momentos(imagem_limiarizada1, ordem_q1, ordem_p1, "m00")
    momento_m10_1 = calcular_momentos(imagem_limiarizada1, ordem_q1, ordem_p1, "m10")
    momento_m01_1 = calcular_momentos(imagem_limiarizada1, ordem_q1, ordem_p1, "m01")

    # centroide
    Centroide_vertical1 = int(momento_m10_1 / momento_m00_1)
    Centroide_horizontal1 = int(momento_m01_1 / momento_m00_1)
    #
    # imagem_limiarizada1[Centroide_vertical1, Centroide_horizontal1] = 0.5
    # print([Centroide_vertical1, Centroide_horizontal1])
    #
    # plt.imshow(imagem_limiarizada1)
    # plt.show()
    #
    #
    # exit(1)

    # teste=len(bordas_x)/2

    bordas_xi,bordas_yi = f_interpolation(bordas_x, bordas_y, 500)

    # pp= len(bordas_yi)
    #
    # for b in range(pp):
    #     print(bordas_xi[b],bordas_yi[b])
    #
    # print(len(bordas_yi))
    # #
    # plt.scatter(bordas_xi, bordas_yi, color='red', marker='+')
    #
    # # Configurar os eixos
    # plt.axis('off')
    #
    # # Exibir o gráfico
    # plt.show()
    #
    # exit(1)

    # for xi, yi in zip(bordas_xi,bordas_yi):
    #     print((xi,yi))
    #     imagem_limiarizada1[ int(yi)][int(xi)] = 0.5
    #     # print(imagem_limiarizada1[linha, coluna])
    #
    # plt.imshow(imagem_limiarizada1)
    # plt.show()
    # exit(1)



    # print(len(bordas_xi))

    # Vetor de distâncias d1
    distancias1 = []

    for i in range(len(bordas_xi)):
        distancia = np.sqrt(((bordas_yi[i] - Centroide_vertical1) ** 2)+((bordas_xi[i] - Centroide_horizontal1) ** 2))
        distancias1.append(distancia)



    # plt.plot(distancias1)
    #
    # print(distancia)
    #
    # # Configurações do gráfico
    # plt.xlabel('Índice')
    # plt.ylabel('Distância')
    # plt.title('Vetor de Distâncias')
    # plt.grid(True)
    #
    # # Exibição do gráfico
    # plt.show()

    # exit(1)
    return distancias1


def template_comp(diretorio):

    # Obtém a lista de arquivos no diretório
    arquivos = os.listdir(diretorio)


    similaridades = []  # Lista para armazenar as tuplas de similaridade e nome do arquivo

    # Itera sobre os arquivos
    for arquivo in arquivos:
        if arquivo.endswith(".png"):
            caminho_completo = os.path.join(diretorio, arquivo)

            nome_arquivo = os.path.splitext(arquivo)[0]  # Remove a extensão ".png"

            imagem1 = cv2.imread(arquivo,0)
            imagem1 = imagem1.astype(np.float64)
            # print(imagem1.dtype)


            similaridade = curvas_distancia(imagem1)

        # Adiciona a tupla (similaridade, nome do arquivo) à lista de similaridades
            similaridades.append((similaridade, nome_arquivo))

        with open("tupla.base", "wb") as auxi:
            pickle.dump(similaridades, auxi)







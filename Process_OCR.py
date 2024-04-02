
import cv2
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt
from skimage.segmentation import clear_border
from scipy.interpolate import interp1d


def calcular_momentos(imagem, ordem_q, ordem_p, tipo):
    # calcula momentos de inércia de uma imagem, dependendo do valor do parâmetro

    # Complexidade:
    # o pior caso ocorre quando o código executa o tipo de momento "m00",
    # e a complexidade seria O(linhas * colunas).


    # obter as dimensões da imagem.
    linhas, colunas = imagem.shape


    # Inicializa os momentos Q, P e o momento como zero
    momento_q = 0
    momento_p = 0
    momento = 0

    # Condição para o momento m00
    #     momento é calculado somando-se o produto do valor do pixel ao quadrado pela ordem do momento Q.
    if tipo == "m00":
        for i in range(linhas):
            for j in range(colunas):
                # Calcula o momento Q
                momento += (i ** ordem_q) * (j ** ordem_q) * imagem[i, j]

        return momento


    # Condição para o momento m01
    #    o momento é calculado somando-se o produto da coluna do pixel pelo valor do pixel.
    if tipo == "m01":
        for i in range(linhas):
            for j in range(colunas):
                # Calcula o momento
                momento += j * imagem[i, j]

        return momento

    # Condição para o momento m10
    #     o momento é calculado somando-se o produto da linha do pixel pelo valor do pixel.
    if tipo == "m10":
        for i in range(linhas):
            for j in range(colunas):
                # Calcula o momento
                momento += i * imagem[i, j]

        return momento

def encontrar_bordas(I):

    # É responsável por encontrar as bordas em uma imagem binária representada pela matriz I.
    # A função implementa um algoritmo de seguimento de bordas baseado em conectividade no
    # sentido horario dos pixels.

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

def limiarizar_imagem(imagem, limiar,tipo):
    # Realiza a limiarização de uma imagem, ou seja, atribui valores binários (0 ou 1) aos
    # pixels da imagem com base em um valor de limiar


    # complexidade:
    # limiarizar_imagem é O(height * width), onde height e width são as dimensões da imagem.

    imagem_limiarizada = imagem

    # obter as dimensões da imagem.
    height = imagem.shape[0]
    width = imagem.shape[1]

    # Condição para imagem com fundo branco
    if tipo ==1:
        for y in range(height):
            for x in range(width):
                # usa o limiar para atribuir um novo valor ao pixel analisado
                if imagem[y][x]< limiar:
                    imagem_limiarizada[y][x]= 1
                else:
                    imagem_limiarizada[y][x] = 0

    # Condição para imagem com fundo preto
    elif tipo == 0:
        for y in range(height):
            # usa o limiar para atribuir um novo valor ao pixel analisado
            for x in range(width):
                if imagem[y][x]> limiar:
                    imagem_limiarizada[y][x]= 1
                else:
                    imagem_limiarizada[y][x] = 0

    # Retorna a imagem limiarizada do tipo Logical (0 ou 1)
    return imagem_limiarizada

def f_norm_cc(crv_dist, crv_dist_comp):
    # realiza a normalização de duas curvas e em seguida
    # calcula a correlação circular entre elas.

    # Complexidade:
    # A complexidade da função é O(n), onde n é o tamanho
    # das curvas ou da matriz de correlação

    # Normalização das curvas
    # Calcula o deslocamento em relação à média das curvas crv_dist e crv_dist_comp
    x1 = crv_dist - np.mean(crv_dist)
    x2 = crv_dist_comp - np.mean(crv_dist_comp)

    # Normaliza as curvas dividindo-as pelo desvio padrão
    # Cada curva é dividida pelo seu próprio desvio padrão
    y1 = x1 / np.sqrt(np.sum(x1 ** 2))
    y2 = x2 / np.sqrt(np.sum(x2 ** 2))

    plo1 = y1
    plo2 = y2

    # matriz para armazenar os pontos deCorrelação
    correlacao = np.zeros(500)

    for k in range(500):
        # Realiza um deslocamento circular da curva y2
        y2 = np.roll(y2, 1)
        # Calcula a correlação entre as curvas y1 e y2
        correlacao[k] = np.sum(y1 * y2)

        ## Faz o plot da correlação entre as curvas
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

    #obtem o maior valor obtido na correlção
    ret = np.max(correlacao)

    # Retorna o maior valor obtido na correlção valores entre 0 e 1
    #sendo 1 o maior valor de similardades entres as curvas
    return ret

def f_interpolation(x, y, num):
    #  realiza a interpolação linear de um conjunto de pontos (x, y) para um novo
    #  número especificado de pontos


    # complexidade:
    # complexidade da função interp1d define a complexidade da função, que é de O(n).

    x_vals = np.arange(1, len(x) + 1)

    #  gera um novo array com num pontos igualmente espaçados
    #  entre 1 e o tamanho de x. Esses pontos representam os novos pontos
    #  onde a interpolação será realizada.
    xi = np.linspace(1, len(x), num)

    #  responsáveis pela interpolação linear dos pontos
    f_rows = interp1d(x_vals, y, kind='linear', fill_value="extrapolate")
    f_cols = interp1d(x_vals, x, kind='linear', fill_value="extrapolate")

    new_rows = f_rows(xi)
    new_cols = f_cols(xi)

    # retorna os valores interpolados correspondentes a y e x.
    return new_cols, new_rows

def curv_dist_2(imagem1):
    #  realiza operações para extrair informações  da imagem,
    #  como a localização das bordas e as distâncias entre os pontos de borda e o centroide.


    # complexidade:
    #  O(num), dependendo do tamanho da imagem e do número de pontos desejados para interpolação.


    # Normalizar os valores para o intervalo [0, 1]
    imagem_normalizada2 = imagem1 / 255.0

    # imagem_invertida2 = np.abs(imagem_normalizada2 - 1)

    plt.imshow(imagem_normalizada2, cmap='gray')
    # plt.title("curva")
    # plt.show()

    # Chamada da função para encontrar as bordas
    bordas_colunas2, bordas_linhas2 = encontrar_bordas(imagem_normalizada2)

    # # Imprime as posições dos pixels de borda
    # for linha, coluna in zip(bordas_linhas2, bordas_colunas2):
    #     imagem_normalizada2[linha, coluna] = 0  # Valor de pixel modificado
    #     cv2.imshow("Imagem com Bordas", imagem_normalizada2)
    #     cv2.waitKey(50)  # Pausa de 0,5 segundos

    #iniciaçização dos parametros dos calculo do momento de inercia
    ordem_q2 = 0
    ordem_p2 = 0

    # Cálculo dos momentos de Inércia
    momento_m00_2 = calcular_momentos(imagem_normalizada2, ordem_q2, ordem_p2, "m00")
    momento_m10_2 = calcular_momentos(imagem_normalizada2, ordem_q2, ordem_p2, "m10")
    momento_m01_2 = calcular_momentos(imagem_normalizada2, ordem_q2, ordem_p2, "m01")

    #Calculo centroide
    Centroide_vertical2 = int(momento_m10_2 / momento_m00_2)
    Centroide_horizontal2 = int(momento_m01_2 / momento_m00_2)


    #calculo da inetrpolação para padronizar o numero de cordenadas de pixels de borda
    bordas_x2, bordas_y2 = f_interpolation(bordas_colunas2, bordas_linhas2, 500)



    # Vetor de para armazenar os valores de distâncias
    distancias2 = []

    # Cálculo das distâncias euclidianas entre cada ponto de borda e o centroide.
    for i in range(len(bordas_y2)):
        distancia = np.sqrt((bordas_y2[i] - Centroide_vertical2) ** 2 + ( bordas_x2[i] - Centroide_horizontal2) ** 2)
        distancias2.append(distancia)

    # Retorna um vetor contendo as distâncias calculadas.
    return(distancias2)

def seg_extr_carc(imagem):

    # Define um valor para a limiarização da imagem de entrada
    limiar = 150

    # Chama a função para mimiarizar a imagem
    imagem = limiarizar_imagem(imagem, limiar, 0)

    # Converte a imagem para o tipo 'uint8'
    imagem = imagem.astype('uint8') * 255

    # Etapa de rotulmaneto para realizar a seguemnetação da região deinetresse.
    n_label, label_img = cv2.connectedComponents(imagem)


    # Ignorar o valor 0 durante o cálculo da contagem
    #  linear em relação ao número de pixels da imagem, O(N).
    valores, contagem = np.unique(label_img[label_img != 0], return_counts=True)


    # Verificar se existem valores não nulos na matriz
    if len(valores) > 0:
        # Encontra o valor mais frequente
        valor_mais_frequente = valores[np.argmax(contagem)]

        #encontra a regiãoemque a placa esta
        # print("Valor mais frequente (exceto 0):", valor_mais_frequente)
    else:
        print("A matriz não contém valores diferentes de zero.")

    limiar = valor_mais_frequente # Atribui um limiar para seguementação da região de interesse

    # Monta uma imagem nova com a região de interesse no valor 1 e o restante com 0
    imagem_interesse1 = np.where(label_img == limiar, 1, 0)


    #encontra as posiçoes dos pixels com valor 1
    indices_1 = np.argwhere(imagem_interesse1 == 1)

    # Obtém as coordenadas dos cantos da imagem para realizar um corte na região de interesse
    canto_superior_esquerdo = (np.min(indices_1[:, 0]), np.min(indices_1[:, 1]))
    canto_superior_direito = (np.min(indices_1[:, 0]), np.max(indices_1[:, 1]))
    canto_inferior_esquerdo = (np.max(indices_1[:, 0]), np.min(indices_1[:, 1]))
    canto_inferior_direito = (np.max(indices_1[:, 0]), np.max(indices_1[:, 1]))


    # Definir as coordenadas do retângulo envolvendo a região de interesse
    x = np.min(indices_1[:, 1])
    y = np.min(indices_1[:, 0])
    width = np.max(indices_1[:, 1]) - np.min(indices_1[:, 1])
    height = np.max(indices_1[:, 0]) - np.min(indices_1[:, 0])

    # Extrair a região de interesse  da imagem original
    imagem_cortada = imagem_interesse1[y:y+height, x:x+width]

    # # Exibir a imagem cortada com título
    # plt.imshow(imagem_cortada, cmap='gray')
    # plt.title("Imagem Cortada")
    # plt.show()

    # Converte a imagem cortada em uma máscara binária, em que os pixels com valor
    # menor ou igual a 0 são definidos como 1 e os demais como 0.
    imagem_interesse1 = imagem_cortada <= 0

    # plt.imshow(imagem_interesse1, cmap='gray')
    # plt.show()


    # Aplica a função que realiza a 'limpeza de pixel de borda'
    borda_img_limpa = clear_border(imagem_interesse1)


    # Converte a imagem para o tipo 'uint8'
    borda_img_limpa = borda_img_limpa.astype('uint8') * 255


    # Aplicar a função de análise de componentes.
    imagem_interesse2 = cv2.connectedComponentsWithStats(borda_img_limpa,4,cv2.CV_32S)
    (totalLabels, label_ids, values, centroid) = imagem_interesse2


    # Inicializar uma nova imagem para armazenar todos os componentes de saída.
    imagem_carc_all = np.zeros(borda_img_limpa.shape, dtype="uint8")


    # Realiza uma segmentação baseado nos tamanhos de tamanhos de areas
    areamax=0
    for k in range(1, totalLabels):
        aux = values[k, cv2.CC_STAT_AREA]
        if areamax < aux:
            areamax = aux  # guarda o valor da maior area de pixels
            # print(areamax)

    alturamax = 0
    for k in range(1, totalLabels):
        aux_2 = values[k, cv2.CC_STAT_HEIGHT]
        if alturamax < aux_2:
            alturamax = aux_2  # guarda o valor da maior area de pixels
            # print(areamax)

    # cria um limiar que fara a eliminação das regioes que não tenham
    # pelomenos 40% do tamanho maximo e 80%da altura maxima
    limiarareaMax = areamax*0.4
    limiar_altura = alturamax*0.8

    # print(limiarareaMax)

    imagens_recortadas = []  # Inicializa o vetor para guardar os carcteres encontrados

    borda = 5  # Largura em pixels de aumento da borda

    for i in range(1, totalLabels):
        area = values[i, cv2.CC_STAT_AREA]  # Acessa os componentes rotulados e obtém a área
        altura = values[i, cv2.CC_STAT_HEIGHT]  # Acessa os componentes rotulados e obtém a altura


        # Eliminação das regioes que não tenham pelo menos 40% da
        #  maior area e 80% da maior altura, seguido de um corte para isolar cada caracter
        if (area > limiarareaMax) and (area <= areamax) and (altura> limiar_altura):


            # operação para sobrepor os pixels brancos na imagem_carc_all
            componentMask = (label_ids == i).astype("uint8") * 255
            imagem_carc_all = cv2.bitwise_or(imagem_carc_all, componentMask)

            # Obtendo as informações do retângulo delimitador
            x, y, w, h = values[i, cv2.CC_STAT_LEFT], values[i, cv2.CC_STAT_TOP], values[i, cv2.CC_STAT_WIDTH], values[
                i, cv2.CC_STAT_HEIGHT]

            # Cortando a região de interesse
            imagem_recortada = imagem_carc_all[y:y + h, x:x + w]

            # Adicionando borda preta à imagem recortada
            imagem_recortada_com_borda = cv2.copyMakeBorder(imagem_recortada, borda, borda, borda, borda,
                                                            cv2.BORDER_CONSTANT, value=0)

            # Realiza umaoperação morfologica para tratar a região de interesse
            # Definir o kernel de dilatação
            kernel = np.ones((3, 3), np.uint8)  # Tamanho e forma do kernel podem ser ajustados

            # Realizar a dilatação na imagem
            imagem_recortada_com_borda = cv2.dilate(imagem_recortada_com_borda, kernel, iterations=1)


            # Guardar as coordenadas do centróide
            centroide_x = x + (w // 2)
            centroide_y = y + (h // 2)
            coordenadas_centroide = (centroide_x, centroide_y)

            # Adicionar a imagem recortada com a borda e as coordenadas do centróide à lista
            imagens_recortadas.append((imagem_recortada_com_borda, coordenadas_centroide))

    # criar uma matriz ordenada usando a pisição crescente do centróide x
    imagens_ordenadas = sorted(imagens_recortadas, key=lambda x: x[1][0])
    # print(len(imagens_ordenadas))


    # Verifica se a região processada contem pelo menos 7 caracteres
    if len(imagens_ordenadas) < 7:

        # cria um vetor vazio
        vazio = []

        # retorna o vetor vazio e uma Flag para a o algoritmo de Lpr
        return vazio, 1

    # print(imagens_ordenadas[0][0])

    # plt.imshow(imagem_carc_all, cmap='gray')
    # plt.title("xxxxxxxxxxxxxxx")
    # plt.show()


    # Carregue a tupla salva do arquivo usando pickle
    with open("tupla.base", "rb") as arquivo:
        similaridades = pickle.load(arquivo)



    # print(len(imagens_ordenadas))

    ocr_saida = []

    for k in range(len(imagens_ordenadas)):

        # plt.imshow(imagens_ordenadas[k][0], cmap='gray')
        # plt.show()

        bla=curv_dist_2(imagens_ordenadas[k][0])

        # print(f_norm_cc(bla, similaridades[26][0]))

        max=0

        for r in range(len(similaridades)):
            auxmax = f_norm_cc(bla, similaridades[r][0])
            if auxmax > max:
                max = auxmax
                sr = r

        ocr_saida.append(similaridades[sr][1])

    # print(ocr_saida)

    # with open("placa.txt","w") as arquivo:
    #     arquivo.write(" ".join(ocr_saida))


    # plt.imshow(imagem_carc_all, cmap='gray')
    # plt.show()

    return ocr_saida, 0
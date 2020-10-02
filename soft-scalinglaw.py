"""
	Copyright 2020 Martín Zapata Martínez
	
	This file is part of soft-scalinglaw.
    soft-scalinglaw is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    soft-scalinglaw is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with soft-scalinglaw.  If not, see <https://www.gnu.org/licenses/>.
"""

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import openpyxl as ox
from os import scandir, getcwd, mkdir, path

def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]

def ajuste_minimos_cuadrados(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(x * x)
    sum_xy = sum(x * y)
    a = (sum_y * sum_x2 - sum_x * sum_xy) / (n * sum_x2 - sum_x * sum_x)  
    b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    s = np.sqrt(sum((y - a - b * x) ** 2)/(n - 2))
    s_a = s * np.sqrt(sum_x2 / (n * sum_x2 - sum_x * sum_x))
    s_b = s * np.sqrt(n / (n * sum_x2 - sum_x * sum_x))
    return a, b, s_a, s_b

def test_recta(x, a, b):
    return a + b * x

def numero_bins(x, binwidth):
    rango_maximo = max(x)
    z = int(rango_maximo / binwidth)
    new_range = z * binwidth
    return new_range, z 

def get_sumanormalizada(archivo, fila_inicio, fila_final, col_inicio, col_final):
    libro = ox.load_workbook('./datos/' + archivo)
    hoja = libro.active 
    votos = [] 

    for x in range(fila_inicio, fila_final): 
        votoscol = []
        for y in range (col_inicio, col_final): 
            votoscol.append(hoja.cell(row = x, column = y).value)
        votos.append(votoscol)

    array = np.array(votos)
    suma = sum(array) 
    total_votos = sum(suma)

    suma_normalizada = suma / total_votos
    return suma_normalizada

def execution(archivo, suma_normalizada, binwidth):
    if not path.exists('./resultados/'):
        mkdir('./resultados/')

    if not path.exists('./resultados/histogramas_' + archivo + '/'):
        mkdir('./resultados/histogramas_' + archivo + '/')
    
    if not path.exists('./resultados/ajuste_' + archivo + '/'):
        mkdir('./resultados/ajuste_' + archivo + '/')

    new_range, n_bins = numero_bins(suma_normalizada, binwidth)

    datos_hist = plt.hist(suma_normalizada, bins = n_bins, range = (0, new_range))
    plt.xlim(0., 0.01)
    plt.xlabel('$v$')
    plt.ylabel('$N$')
    e = str(binwidth)
    plt.savefig('./resultados/histogramas_' + archivo + '/' + e + '_bins.png')
    plt.clf()
    
    x = datos_hist[1]
    x_i = np.zeros(len(x)-1)

    for i in range(len(x_i)):
        x_i[i] = (x[i] + x[i+1]) / 2.

    x = x_i 
    y = datos_hist[0]

    indices = []

    for i in range(0, len(y)):
        if y[i] <= 1.:
            indices.append(i)

    if indices != []:
        indices=np.array(indices)
        x_new=np.delete(x,indices)
        y_new=np.delete(y,indices)

        x=np.log10(x_new)
        y=np.log10(y_new)
        print(max(x), min(x), max(x)-min(x))

    else:
        x = np.log10(x)
        y = np.log10(y)
        print(max(x), min(x), max(x)-min(x))

    if len(x) <= 2:
        print('No hay suficientes puntos:', binwidth, archivo)


    a, b, s_a, s_b = ajuste_minimos_cuadrados(x, y)

    plt.plot(x, test_recta(x, a, b), 'r-')
    plt.plot(x, y, 'ko')
    plt.xlabel('$\log _{10} v$')
    plt.ylabel('$\log _{10} N$')
    plt.savefig('./resultados/ajuste_' + archivo + '/' + e + '_bins.png')
    plt.clf()
    f = open('./resultados/pendientes.txt', 'a')
    f.write(archivo + '\t' + str(b) +'\t' + str(s_b) + '\t' + str(a) + '\t' + str(s_a) + '\t' + str(binwidth) + '\n') 

def check_parameters(archivo):
    file = open('configuracion.txt', 'r')
    contenido = file.readlines()

    for line in contenido:
        lista_contenido = line.split()
        if lista_contenido[0] == archivo:
            return int(lista_contenido[1]), int(lista_contenido[2]), int(lista_contenido[3]), int(lista_contenido[4])

lista_de_archivos = ls('./datos')

for archivo in lista_de_archivos:
    lista_contenido_1, lista_contenido_2, lista_contenido_3, lista_contenido_4 = check_parameters(archivo)
    suma_normalizada = get_sumanormalizada(archivo, lista_contenido_1, lista_contenido_2, lista_contenido_3, lista_contenido_4)
    print(archivo)
    for i in range(295):
        execution(archivo, suma_normalizada, i * 0.00001 + 0.00005)
        print(i * 0.00001 + 0.00005)
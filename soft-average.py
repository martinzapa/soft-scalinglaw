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
from os import scandir, getcwd

def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]

def media_ponderada(x, s_x):
    w = 1. / (s_x * s_x)
    media = sum(w * x) / sum(w)
    error_media = 1. / np.sqrt(sum(w))
    return media, error_media

def delete_inftys(x, x_err):
    indices = []

    for i in range(len(x)):
        if x_err[i] == 'inf':
            indices.append(i)
    
    if indices == []:
        x = np.array(x)
        x_err = np.array(x_err)
        x = x.astype(float, copy = False)
        x_err = x_err.astype(float, copy = False)
        return x, x_err 

    else:
        indices = np.array(indices)
        x_new = np.delete(x, indices)
        x_err_new = np.delete(x_err, indices)
        x_new = np.array(x_new)
        x_err_new = np.array(x_err_new)
        x_new = x_new.astype(float, copy = False)
        x_err_new = x_err_new.astype(float, copy = False)
        return x_new, x_err_new

def check_parameters(archivo, ancho_min, ancho_max):
    file = open('./resultados/pendientes.txt', 'r')

    valores = []
    errores = []
    
    for line in file.readlines():
        contenido = line.split()
        if contenido[0] == archivo and float(contenido[5]) >= ancho_min and float(contenido[5]) <= ancho_max :
            valores.append(float(contenido[1]))
            errores.append(float(contenido[2]))
        if contenido[0] == archivo:
            nombre = contenido[0]
            aux = nombre.split(sep='_')
            año = aux[1]
            año_archivo = float(año[:4])

    file.close()
    valores, errores = delete_inftys(valores, errores)
    return valores, errores, año_archivo

def media(archivo, ancho_min, ancho_max):
    valores, errores, año_archivo = check_parameters(archivo, ancho_min, ancho_max)
    media_archivo, error_media_archivo = media_ponderada(valores, errores)
    return media_archivo, error_media_archivo, año_archivo

print('Ancho mínimo de bin:')
ancho_bins_min = float(input())

print('Ancho máximo de bin:')
ancho_bins_max = float(input())

lista_de_archivos = ls('./datos')
medias_archivos = []
errores_medias_archivos = []
años = []


for archivo in lista_de_archivos:
    media_archivo, error_media_archivo, año_archivo = media(archivo, ancho_bins_min,  ancho_bins_max)
    medias_archivos.append(media_archivo)
    errores_medias_archivos.append(error_media_archivo)
    años.append(año_archivo)

años = [1977., 1979., 1982., 1986., 1989., 1993., 1996., 2000., 2004., 2008., 2011., 2015., 2016., 2019., 2019.5]
file_out = open('./resultados/medias_anos.txt', 'w')
file_out.write(str(años))
file_out.write(str(medias_archivos))
file_out.write(str(errores_medias_archivos))


errores_medias_archivos_2 = np.zeros(len(errores_medias_archivos))

for i in range(len(errores_medias_archivos)):
    errores_medias_archivos_2[i] = 2 * errores_medias_archivos[i]


plt.plot(años, medias_archivos, 'ko', markersize = 3)
plt.plot(años, medias_archivos, 'k-', linewidth = 0.5)
plt.errorbar(años, medias_archivos, yerr = errores_medias_archivos_2, ecolor='r', fmt='none', hold=True, elinewidth=0.5, capsize=2)
plt.xlabel('Año')
plt.ylabel('Pendiente de la recta')
plt.show()

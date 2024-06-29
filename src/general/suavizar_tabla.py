import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter


# Definir una función de segundo grado para el ajuste
def func(x, a, b, c):
    return a * x ** 2 + b * x + c


def suavizar_curve_fit(csv_original, csv_suavizado, eje_x='X', eje_y='Y', csv_errores='tablas/error_segun_curve_fit.csv'):
    # Leer el archivo CSV
    df = pd.read_csv(csv_original)

    # Extraer columnas X, Y y Time
    X = df[eje_x].values
    Y = df[eje_y].values
    Time = df['Time'].values

    # Ajustar la función cuadrática a los datos de X
    params_x, covariance_x = curve_fit(func, np.arange(len(X)), X)
    errors_x = np.sqrt(np.diag(covariance_x))  # Errores estándar de los parámetros de X

    # Ajustar la función cuadrática a los datos de Y
    params_y, covariance_y = curve_fit(func, np.arange(len(Y)), Y)
    errors_y = np.sqrt(np.diag(covariance_y))  # Errores estándar de los parámetros de Y

    # Generar los valores suavizados para X e Y utilizando las funciones ajustadas
    X_suavizado = func(np.arange(len(X)), *params_x)
    Y_suavizado = func(np.arange(len(Y)), *params_y)

    # Redondear los números a cuatro dígitos decimales
    X_suavizado = np.round(X_suavizado, 4)
    Y_suavizado = np.round(Y_suavizado, 4)

    # Crear una nueva tabla con los valores suavizados
    df_suavizado = pd.DataFrame({
        'X': X_suavizado,
        'Y': Y_suavizado,
        'Time': Time
    })

    # Guardar la nueva tabla en un archivo CSV
    df_suavizado.to_csv(csv_suavizado, index=False)

    # Crear una tabla con los datos de los errores
    df_errores = pd.DataFrame({
        'Parámetro': ['a', 'b', 'c'],
        'X (Valor)': np.round([params_x[0], params_x[1], params_x[2]], 6),
        'X (Error)': np.round([errors_x[0], errors_x[1], errors_x[2]], 6),
        'Y (Valor)': np.round([params_y[0], params_y[1], params_y[2]], 6),
        'Y (Error)': np.round([errors_y[0], errors_y[1], errors_y[2]], 6)
    })

    # Guardar las tablas en archivos CSV
    df_suavizado.to_csv(csv_suavizado, index=False)
    df_errores.to_csv(csv_errores, index=False)



def suavizar_savitzky(csv_original, csv_suavizado):
    # Leer el archivo CSV
    df = pd.read_csv(csv_original)

    # Extraer columnas X, Y y Time
    X = df['X'].values
    Y = df['Y'].values
    Time = df['Time'].values

    # Aplicar el filtro de Savitzky-Golay a los datos de X e Y
    window_length = 5  # Longitud de la ventana, debe ser impar
    polyorder = 2  # Orden del polinomio, usualmente 2 o 3

    X_suavizado = savgol_filter(X, window_length, polyorder)
    Y_suavizado = savgol_filter(Y, window_length, polyorder)

    # Redondear los números a cuatro dígitos decimales
    X_suavizado = np.round(X_suavizado, 4)
    Y_suavizado = np.round(Y_suavizado, 4)

    # Calcular los residuos
    residuos_X = X - X_suavizado
    residuos_Y = Y - Y_suavizado

    # Calcular la desviación estándar de los residuos
    error_std_X = np.std(residuos_X)
    error_std_Y = np.std(residuos_Y)

    # Crear una nueva tabla con los valores suavizados
    df_suavizado = pd.DataFrame({
        'X': X_suavizado,
        'Y': Y_suavizado,
        'Time': Time
    })

    # Guardar la nueva tabla en un archivo CSV
    df_suavizado.to_csv(csv_suavizado, index=False)

    # Imprimir detalles del suavizado
    print("\nResultados del suavizado con Savitzky-Golay:")
    print(f"Longitud de la ventana: {window_length}")
    print(f"Orden del polinomio: {polyorder}")
    print(f"Error estándar de los valores suavizados para X: {error_std_X:.6f}")
    print(f"Error estándar de los valores suavizados para Y: {error_std_Y:.6f}")


def graficar(csv_original, csv_suavizado, nombre_archivo="grafico.png", titulo="Grafico"):
    # Leer los archivos CSV
    df1 = pd.read_csv(csv_original)
    df2 = pd.read_csv(csv_suavizado)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))

    # Graficar los datos del segundo archivo
    plt.plot(df2['X'], df2['Y'], label='Ajuste curve fit', color='red', linestyle='-', linewidth=1)

    # Graficar los datos del primer archivo
    plt.plot(df1['X'], df1['Y'], label='Original', color='blue', linestyle='-', linewidth=1)

    # Etiquetas y título
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(titulo)
    plt.legend()

    # Guardar la gráfica como una imagen
    plt.savefig(nombre_archivo)

    # Mostrar la gráfica
    plt.show()

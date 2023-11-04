# -*- coding: utf-8 -*-
"""RetoEXPO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XSUwRaPaEORqVsA6NaVHTDV1n2f_urH4

Versión de Python
"""

!python --version

"""# Proyecto"""

from google.colab import drive
drive.mount('/content/drive')

"""## Librerias

### Instalación
"""

!pip install --upgrade ydata_profiling

"""### Importación"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport
# %matplotlib inline

"""### Versiones"""

print("Versión de Pandas: " ,pd.__version__)
print("Versión de Numpy: " ,np.__version__)

"""## Establecemos una semilla"""

SEED= 201

"""## Importacion de datos

"""

df = pd.read_csv("/content/sample_data/data.csv")

"""## Analisis

"""

df

"""### Tratamiendo de datos"""

df.isna().sum().sort_values(ascending = False)

def estadisticos_cont(num):

    #Calculamos describr
    estadisticos = num.describe().T

    #agregamos la mediana
    estadisticos['median'] = num.median()

    #retornamos el resultado
    return(estadisticos)

estadisticos_cont(df.select_dtypes('number'))

"""### Analisis de los mejores modelos para los datos"""

# load sample dataset
!pip install pycaret
from pycaret.datasets import get_data

# load sample dataset
from pycaret.datasets import get_data
data = pd.read_csv('/content/sample_data/data.csv')

!pip install --upgrade scipy

from pycaret.classification import ClassificationExperiment
s = ClassificationExperiment()
s.setup(data, target = 'Result', session_id = 123)

# OOP API
best = s.compare_models()

"""### Exportación del analisis a HTML."""

df_pro = df.copy()

profile = ProfileReport(df_pro, title = "Profiling Report")

profile.to_widgets()

profile.to_file("your_report.html")

"""## Machine Learning"""

df_ml = df.copy()

#Separación predictoras y target
x = df_ml.drop(columns='Result')
y = df_ml['Result']

"""### Importación de herramientas"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.tree import plot_tree

"""### Separación de datos"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = SEED)

"""### Modelos

#### Arbol de decisión
"""

ac = DecisionTreeClassifier()

"""##### Optimización para el modelo"""

params = {
    'max_depth': np.arange(2, 17),
    'criterion': ['gini', 'entropy'],
    'max_features': np.arange(2, 11),
    'min_samples_leaf': np.arange(10, 210, 10),
}

clf = RandomizedSearchCV(
    ac,
    params,
    n_iter=100,
    cv=5,
    verbose=1,
)

# Entrenar el modelo
clf.fit(x_train, y_train)

# Imprimir los mejores parámetros
print(clf.best_params_)

model=clf.best_estimator_

"""##### Validación del modelo"""

pred = clf.predict(x_test)
accuracy=clf.score(x_test,y_test)
print("área bajo la curva característica: ",roc_auc_score(y_test,pred))
print("Precisión: ", accuracy)
confusion_matrix(y_test,pred)

"""##### Grafica"""

plt.figure(figsize = (50,50))

plot_tree(model,
          feature_names= x_test.columns,
          impurity = False,
          node_ids = True,
          proportion = True,
          rounded = True,
          precision = 2);

df['scoring_result'] = clf.predict_proba(df_ml.drop(columns = 'Result'))[:, 1]

df.to_excel('resultado_con_scoring.xlsx')

"""##### Exportación del modelo"""

import joblib

# Guardar el modelo en un archivo .h5
joblib.dump(ac, 'ac.h5')
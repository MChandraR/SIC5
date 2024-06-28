import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Untuk mengabaikan peringatan
import warnings
warnings.filterwarnings("ignore")

# Memuat dataset
data = pd.read_csv("dataset.csv")

# Menampilkan informasi dasar tentang dataset
print(data.info())
print(data.describe())
print(data.head())

# Mengubah variabel kategori menjadi variabel dummy
data = pd.get_dummies(data, columns=['Type'], drop_first=True)

# Memisahkan fitur dan target
X = data.drop(['UDI', 'Product ID', 'Machine failure', 'TWF'], axis=1)
y = data['TWF']

# Membagi data menjadi set pelatihan dan pengujian
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standarisasi fitur
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Menggunakan Random Forest sebagai model prediksi
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Melakukan prediksi pada data pengujian
y_pred = model.predict(X_test)

# Menampilkan laporan klasifikasi
print(classification_report(y_test, y_pred))

# Menampilkan matriks kebingungan
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt="d")
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Menampilkan akurasi
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

from sklearn.model_selection import GridSearchCV

# Menentukan parameter yang akan dioptimasi
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth': [4, 6, 8, 10],
    'criterion': ['gini', 'entropy']
}

# Melakukan Grid Search dengan Cross Validation
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Menampilkan parameter terbaik
print(f'Best parameters: {grid_search.best_params_}')

# Menggunakan model terbaik
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)

# Mengevaluasi model terbaik
print(classification_report(y_test, y_pred_best))
accuracy_best = accuracy_score(y_test, y_pred_best)
print(f'Best Accuracy: {accuracy_best}')

"""
Módulo de predicción y análisis predictivo.
Modelos de Machine Learning para predecir áreas propensas a mosquitos.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent tkinter errors
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc


class PredictorMosquitos:
    """Modelo predictivo para áreas propensas a mosquitos."""
    
    def __init__(self, df_imagery):
        """
        Inicializa el predictor.
        
        Args:
            df_imagery: DataFrame con datos de imagery/cobertura
        """
        self.df = df_imagery
        self.modelo = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        self.resultados = {}
    
    def preparar_datos(self):
        """Prepara los datos para el modelo predictivo."""
        print("=" * 60)
        print("🔧 PREPARANDO DATOS PARA MODELO PREDICTIVO")
        print("=" * 60)
        
        # Definir características (features)
        features = [
            'ceoTREES_CANOPYCOVER',
            'ceoBUSH_SCRUB',
            'ceoGRASS',
            'ceoImperviousSurface'
        ]
        
        # Filtrar características que existen
        features_existentes = [f for f in features if f in self.df.columns]
        
        if not features_existentes:
            print("⚠️  No se encontraron características necesarias")
            return False
        
        # Variable objetivo: presencia de agua (proxy para mosquitos)
        target_col = 'ceoWaterLakePondedContainer'
        
        if target_col not in self.df.columns:
            print(f"⚠️  Columna objetivo '{target_col}' no encontrada")
            return False
        
        print(f"\n📊 Características seleccionadas:")
        for f in features_existentes:
            print(f"   • {f}")
        
        print(f"\n🎯 Variable objetivo: {target_col}")
        print(f"   (Presencia de agua como proxy para hábitat de mosquitos)")
        
        # Preparar datos
        X = self.df[features_existentes].copy()
        
        # Eliminar filas con valores faltantes
        X = X.dropna()
        
        # Variable objetivo: 1 si hay agua, 0 si no
        y = (self.df.loc[X.index, target_col] > 0).astype(int)
        
        self.feature_names = features_existentes
        
        print(f"\n📈 Tamaño del dataset:")
        print(f"   Total de muestras: {len(X)}")
        print(f"   Muestras con agua (clase 1): {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
        print(f"   Muestras sin agua (clase 0): {len(y)-y.sum()} ({(len(y)-y.sum())/len(y)*100:.1f}%)")
        
        # Dividir en entrenamiento y prueba
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        print(f"\n✂️  División de datos:")
        print(f"   Entrenamiento: {len(self.X_train)} muestras")
        print(f"   Prueba: {len(self.X_test)} muestras")
        
        return True
    
    def entrenar_modelo(self):
        """Entrena el modelo Random Forest."""
        print("\n" + "=" * 60)
        print("🤖 ENTRENANDO MODELO RANDOM FOREST")
        print("=" * 60)
        
        if self.X_train is None:
            print("⚠️  Primero debes preparar los datos")
            return False
        
        # Crear y entrenar modelo
        self.modelo = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        print("\n🔄 Entrenando modelo...")
        self.modelo.fit(self.X_train, self.y_train)
        print(" Modelo entrenado exitosamente")
        
        # Evaluar en conjunto de entrenamiento
        train_score = self.modelo.score(self.X_train, self.y_train)
        print(f"\n📊 Precisión en entrenamiento: {train_score:.2%}")
        
        # Evaluar en conjunto de prueba
        test_score = self.modelo.score(self.X_test, self.y_test)
        print(f"📊 Precisión en prueba: {test_score:.2%}")
        
        self.resultados['train_score'] = train_score
        self.resultados['test_score'] = test_score
        
        return True
    
    def validacion_cruzada(self, cv=5):
        """Realiza validación cruzada del modelo."""
        print("\n" + "=" * 60)
        print(f"🔄 VALIDACIÓN CRUZADA ({cv}-fold)")
        print("=" * 60)
        
        if self.modelo is None:
            print("⚠️  Primero debes entrenar el modelo")
            return None
        
        print(f"\nRealizando validación cruzada con {cv} folds...")
        
        # Combinar datos de entrenamiento y prueba para validación cruzada
        X_completo = pd.concat([self.X_train, self.X_test])
        y_completo = pd.concat([self.y_train, self.y_test])
        
        scores = cross_val_score(self.modelo, X_completo, y_completo, cv=cv, scoring='accuracy')
        
        print(f"\n📊 Resultados de validación cruzada:")
        print(f"   Scores por fold: {[f'{s:.2%}' for s in scores]}")
        print(f"   Promedio: {scores.mean():.2%}")
        print(f"   Desviación estándar: {scores.std():.2%}")
        
        self.resultados['cv_scores'] = scores
        self.resultados['cv_mean'] = scores.mean()
        
        return scores
    
    def analizar_importancia_features(self):
        """Analiza la importancia de cada característica."""
        print("\n" + "=" * 60)
        print("🔍 IMPORTANCIA DE CARACTERÍSTICAS")
        print("=" * 60)
        
        if self.modelo is None:
            print("⚠️  Primero debes entrenar el modelo")
            return None
        
        # Obtener importancias
        importancias = self.modelo.feature_importances_
        indices = np.argsort(importancias)[::-1]
        
        print("\nImportancia de características (de mayor a menor):")
        for i, idx in enumerate(indices, 1):
            print(f"   {i}. {self.feature_names[idx]}: {importancias[idx]:.4f}")
        
        self.resultados['feature_importance'] = dict(zip(self.feature_names, importancias))
        
        # Crear gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(importancias)), importancias[indices], color='steelblue')
        plt.xticks(range(len(importancias)), 
                  [self.feature_names[i] for i in indices], 
                  rotation=45, ha='right')
        plt.title('Importancia de Características en el Modelo', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Característica')
        plt.ylabel('Importancia')
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/importancia_features.png')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n Gráfico guardado: {output_path}")
        plt.close()
        
        return importancias
    
    def evaluar_modelo(self):
        """Evalúa el modelo con métricas detalladas."""
        print("\n" + "=" * 60)
        print("📈 EVALUACIÓN DETALLADA DEL MODELO")
        print("=" * 60)
        
        if self.modelo is None:
            print("⚠️  Primero debes entrenar el modelo")
            return None
        
        # Predicciones
        y_pred = self.modelo.predict(self.X_test)
        y_pred_proba = self.modelo.predict_proba(self.X_test)[:, 1]
        
        # Reporte de clasificación
        print("\n📊 Reporte de Clasificación:")
        print(classification_report(self.y_test, y_pred, 
                                   target_names=['Sin agua', 'Con agua']))
        
        # Matriz de confusión
        cm = confusion_matrix(self.y_test, y_pred)
        
        # Visualizar matriz de confusión
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title('Matriz de Confusión', fontsize=14, fontweight='bold')
        plt.ylabel('Valor Real')
        plt.xlabel('Predicción')
        plt.xticks([0.5, 1.5], ['Sin agua', 'Con agua'])
        plt.yticks([0.5, 1.5], ['Sin agua', 'Con agua'])
        plt.tight_layout()
        
        output_path = Path('data/output/matriz_confusion.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n Matriz de confusión guardada: {output_path}")
        plt.close()
        
        # Curva ROC
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Tasa de Falsos Positivos')
        plt.ylabel('Tasa de Verdaderos Positivos')
        plt.title('Curva ROC', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        output_path = Path('data/output/curva_roc.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f" Curva ROC guardada: {output_path}")
        plt.close()
        
        self.resultados['roc_auc'] = roc_auc
        self.resultados['confusion_matrix'] = cm
        
        return {'roc_auc': roc_auc, 'confusion_matrix': cm}
    
    def predecir_nuevas_areas(self, nuevos_datos):
        """
        Predice la probabilidad de presencia de mosquitos en nuevas áreas.
        
        Args:
            nuevos_datos: DataFrame con las mismas características del modelo
        
        Returns:
            Array con probabilidades de presencia de mosquitos
        """
        if self.modelo is None:
            print("⚠️  Primero debes entrenar el modelo")
            return None
        
        # Verificar que tenga las columnas necesarias
        columnas_faltantes = set(self.feature_names) - set(nuevos_datos.columns)
        if columnas_faltantes:
            print(f"⚠️  Faltan columnas: {columnas_faltantes}")
            return None
        
        # Predecir
        probabilidades = self.modelo.predict_proba(nuevos_datos[self.feature_names])[:, 1]
        
        return probabilidades
    
    def resumen_completo(self):
        """Genera un resumen completo del análisis predictivo."""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL MODELO PREDICTIVO")
        print("=" * 60)
        
        if self.resultados:
            print(f"\n🎯 RENDIMIENTO DEL MODELO:")
            if 'train_score' in self.resultados:
                print(f"   Precisión en entrenamiento: {self.resultados['train_score']:.2%}")
            if 'test_score' in self.resultados:
                print(f"   Precisión en prueba: {self.resultados['test_score']:.2%}")
            if 'cv_mean' in self.resultados:
                print(f"   Promedio validación cruzada: {self.resultados['cv_mean']:.2%}")
            if 'roc_auc' in self.resultados:
                print(f"   AUC-ROC: {self.resultados['roc_auc']:.2f}")
            
            if 'feature_importance' in self.resultados:
                print(f"\n🔍 CARACTERÍSTICAS MÁS IMPORTANTES:")
                sorted_features = sorted(self.resultados['feature_importance'].items(), 
                                       key=lambda x: x[1], reverse=True)
                for feature, importance in sorted_features[:3]:
                    print(f"   • {feature}: {importance:.4f}")
        
        print("\n" + "=" * 60)
    
    def ejecutar_analisis_completo(self):
        """Ejecuta el análisis predictivo completo."""
        print("\n🚀 INICIANDO ANÁLISIS PREDICTIVO COMPLETO\n")
        
        # Preparar datos
        if not self.preparar_datos():
            print("❌ Error al preparar datos")
            return None
        
        # Entrenar modelo
        if not self.entrenar_modelo():
            print("❌ Error al entrenar modelo")
            return None
        
        # Análisis adicionales
        self.validacion_cruzada()
        self.analizar_importancia_features()
        self.evaluar_modelo()
        self.resumen_completo()
        
        print("\n ANÁLISIS PREDICTIVO COMPLETO FINALIZADO")
        print("📁 Revisa la carpeta 'data/output/' para ver los resultados\n")
        
        return self.resultados


if __name__ == "__main__":
    # Ejemplo de uso
    from utils.data_loader import DataLoader
    
    loader = DataLoader()
    loader.cargar_todos()
    
    predictor = PredictorMosquitos(loader.get_imagery())
    predictor.ejecutar_analisis_completo()

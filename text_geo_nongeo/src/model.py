import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pickle


X = pd.read_csv(r'C:\Users\Asus\PycharmProjects\Mehrshad\text_geo_nongeo\data\tfidf_matrix.csv')
df = pd.read_csv(r'C:\Users\Asus\PycharmProjects\Mehrshad\text_geo_nongeo\data\processed_dataset.csv')
y = df['label']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# with open('model.pkl','wb') as f:
#     pickle.dump(model,f)

sns.heatmap(confusion_matrix(y_test, y_pred), annot=True)
# plt.savefig('confusion_matrix.png')
plt.show()

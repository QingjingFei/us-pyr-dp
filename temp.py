from sklearn import metrics

y_true = [1, 3, 3, 2, 2, 2]
y_pred = [3, 3, 2, 2, 1, 1]
target_names = ['class 0', 'class 1', 'class 2']
print(metrics.classification_report(y_true, y_pred, target_names=target_names))

matrix = metrics.confusion_matrix(y_true, y_pred)
print(matrix)
print(matrix.sum(axis=1))
matrix.diagonal()/matrix.sum(axis=1)
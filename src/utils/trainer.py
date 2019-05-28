from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV

def train(X_train, X_test, y_train, y_test, method, gridsearch=False):
    if gridsearch:
        if method == 'rf':
            tuned_parameters = [{'n_estimators': [100, 200, 300], 'criterion': ['gini', 'entropy'],
                                 'max_depth': [2, 5, 7, 10]}]
            clf = GridSearchCV(RandomForestClassifier(), tuned_parameters, cv=5)
    else:
        if method == 'rf':
            clf = RandomForestClassifier(n_estimators=300, max_depth=10, n_jobs=12, random_state=0)
        elif method == 'svm':
            clf = svm.SVC(gamma='scale')
        elif method == 'xgb':
            clf = XGBClassifier(n_estimators=200, n_jobs=12, random_state=0)
        elif method == 'lr':
            clf = LogisticRegression(random_state=42, class_weight='balanced', penalty='l1', C=0.1, solver='liblinear')

    clf.fit(X_train, y_train)
    # print("Best params:", clf.best_params_)
    y_pred = clf.predict(X_test)

    print("Train score:", clf.score(X_train, y_train))
    acc, p, r, f1 = accuracy_score(y_test, y_pred), precision_score(y_test, y_pred), recall_score(y_test, y_pred), f1_score(y_test, y_pred)
    print("Predict:", (X_test.shape[0], acc, p, r, f1))

    return (X_test.shape[0], acc, p, r, f1)

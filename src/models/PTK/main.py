from sklearn.svm import SVC
from src.models.PTK.propagation_tree_kernel import propagation_tree_kernel_function
from src.data.pheme_dataloader import load_data
from sklearn.metrics import accuracy_score
from random import shuffle
from sklearn.model_selection import train_test_split

def shuffle_data(tree_list, y):
    index = [i for i in range(len(tree_list))]
    new_tree_list = []
    new_y = []
    shuffle(index)
    for i in index:
        new_tree_list.append(tree_list[i])
        new_y.append(y[i])

    return new_tree_list, new_y

if __name__ == '__main__':
    tree_list, y = load_data('/data/rumor_detection/data/pheme/pheme_v2_extend/all-rnr-annotated-threads/temp')
    # tree_list, y = shuffle_data(tree_list, y)
    X_train, X_test, y_train, y_test = train_test_split(tree_list, y, test_size=0.3, random_state=0)
    print("Data size:", len(tree_list))

    clf = SVC(kernel='precomputed')
    gram_train = propagation_tree_kernel_function(X_train, X_train)
    clf.fit(gram_train, y_train)

    gram_test = propagation_tree_kernel_function(X_test, X_train)
    y_pred = clf.predict(gram_test)
    # print('y_pred', y_pred)
    print('accuracy', accuracy_score(y_test, y_pred))

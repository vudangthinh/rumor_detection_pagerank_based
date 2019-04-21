from sklearn.svm import SVC
from src.models.PTK.propagation_tree_kernel import propagation_tree_kernel_function
from src.models.PTK.pheme_dataloader import load_data
from sklearn.metrics import accuracy_score
from random import shuffle

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
    tree_list, y = load_data('/Users/thinhvu/Documents/projects/6392078/all-rnr-annotated-threads')
    tree_list, y = shuffle_data(tree_list, y)
    print(len(tree_list))
    print(len(y))
    print('y', y)
    clf = SVC(kernel='precomputed')
    gram = propagation_tree_kernel_function(tree_list, tree_list)
    clf.fit(gram, y)

    y_pred = clf.predict(gram)
    print('y_pred', y_pred)
    print('accuracy', accuracy_score(y, y_pred))

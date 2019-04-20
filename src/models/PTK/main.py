from sklearn.svm import SVC
from src.models.PTK.propagation_tree_kernel import propagation_tree_kernel_function

def load_data():
    pass

if __name__ == '__main__':
    clf = SVC(kernel=propagation_tree_kernel_function)
    load_data()
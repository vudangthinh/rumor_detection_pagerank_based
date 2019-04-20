# def recursive_items(dictionary, root, root_time):
#     for key, value in dictionary.items():
#         if type(value) is dict:
#             if root:
#                 t = 5
#                 root_time = t
#             else:
#                 print('t', root_time)
#             print(key, value)
#             recursive_items(value, False, root_time)
#         else:
#             print(key, value)
# 
# a = {'a': {1: {1: 2, 3: 4}, 2: {5: 6}}}
# 
# recursive_items(a, True, 0)


# from treelib import Node, Tree
# tree = Tree()
# tree.create_node("Harry", "harry")  # root node
# tree.create_node("Jane", "jane", parent="harry")
# tree.create_node("Bill", "bill", parent="harry")
# tree.create_node("Diane", "diane", parent="jane")
# tree.create_node("Mary", "mary", parent="diane")
# tree.create_node("Mark", "mark", parent="jane")
# tree.show()
#
# sub_tree = tree.subtree("diane")
# sub_tree.show()
# print(tree.children(tree.root))



import numpy as np
from sklearn import svm, datasets

# import some data to play with
iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features. We could
                      # avoid this ugly slicing by using a two-dim dataset
Y = iris.target
print(Y)

def my_kernel(X, Y):
    """
    We create a custom kernel:

                 (2  0)
    k(X, Y) = X  (    ) Y.T
                 (0  1)
    """
    print(X.shape, Y.shape)
    M = np.array([[2, 0], [0, 1.0]])
    return np.dot(np.dot(X, M), Y.T)


h = .02  # step size in the mesh

# we create an instance of SVM and fit out data.
clf = svm.SVC(kernel=my_kernel)
clf.fit(X, Y)






import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

from src.data_loader import DataLoader as DL



def train_in_batches(data_size, clf=MLPClassifier(), batch_size=1000):
    # check if data_size is multiple of 100
    if data_size % batch_size != 0:
        raise f"data_size must be multiple of {batch_size}, is {data_size}"

    dl = DL()
    classes = None
    for i in range(0, data_size, batch_size):
        
        # Load data
        data, labels = dl.load_data_batches(batch_size=batch_size, skip=i, return_1d=True)

        # Split with 0 test_size (only shuffle basically)
        X_train, _, y_train, _ = train_test_split(data, labels, test_size=1, shuffle=True)

        # Get classes from labels
        if classes is None:
            classes = np.sort(np.unique(labels))

        clf.partial_fit(X_train, y_train, classes)

    # Load random test data and train
    test_data, test_labels = dl.load_random_test_data(return_1d=True)

    # print(np.array(test_data).shape, np.array(test_labels).shape)
    # print(clf.score(test_data, test_labels))

    return clf

   

    


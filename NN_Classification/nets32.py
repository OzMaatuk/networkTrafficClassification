import os
from collections import Counter
from itertools import chain
from sklearn.metrics import confusion_matrix
import keras
import keras.layers as layers
from sklearn.metrics import classification_report
import pickle
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import LabelEncoder
from keras.layers import Dropout
import tensorflow as tf
from keras.callbacks import EarlyStopping
import numpy as np
tf.test.gpu_device_name()

# outputs train and test files of ott labels from source pickle after shuffle


def test_train_ott(fname="", train_out="", test_out="", labels=[]):

    # reading pickle file
    with open(fname, 'rb') as handle:
        b = pickle.load(handle)
        # np.random.shuffle(b)  # why shuffle?
        # data = list(chain.from_iterable(
        #     (_dict['Label']) for _dict in b))
        data = b
        # setup histogram object for labels list
        c = Counter(data)
        print(data)
        print('data: ', c)
        train, test = [], []

        _lists = {}
        for label in unique(data):
            _lists[label] = []
        # _lists = {"facebook": [], "dropbox": [], "google": [], 'youtube': [],
        #           "other": [], 'microsoft': [], 'teamviewer': [], 'twitter': []}

        for curr_dict in b:
            for label in labels:
                if curr_dict['Label'] == label:
                    _lists[label].append(curr_dict)

        for label in _lists.values():
            train.extend(label[:int(len(label)*0.7)])
            test.extend(label[int(len(label)*0.7):])

    print('train: ', Counter(list(chain.from_iterable(
        (_dict['Label']) for _dict in train))))
    print('test: ', Counter(list(chain.from_iterable(
        (_dict['Label']) for _dict in test))))

    with open(train_out, 'wb') as handle:
        pickle.dump(train, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(test_out, 'wb') as handle:
        pickle.dump(test, handle, protocol=pickle.HIGHEST_PROTOCOL)

# adding samples as features from files of the predicted labels


def pickle_image_generator_32_ott(input_path, bs, lb, mode="train", aug=None):
    with open(input_path, 'rb') as handle:
        b = pickle.load(handle)
        if mode != "eval":
            np.random.shuffle(b)
        it = iter(b)
        while True:
            # initialize our batches of images and labels
            features = []
            labels = []
            # keep looping until we reach our batch size
            while len(features) < bs:
                # attempt to read the next line of the CSV file
                try:
                    curr_dict = it.__next__()
                except StopIteration:
                    it = iter(b)
                    if mode == "eval":
                        break
                label = curr_dict['Label']
                arr = np.zeros(1500 * 1500, dtype="uint8")
                for key, value in curr_dict.items():
                    if 'label' not in str(key):
                        arr[key] = value
                arr = arr.reshape((1500, 1500))
                # update our corresponding batches lists
                features.append(arr)
                # features.append(arr.reshape(32, 32, 1))
                labels.append(label)
            labels = lb.transform(np.array(labels))
            yield (np.array(features), labels)


TRAIN_PICKLE = "hist_pickles\\train.pickle"
TEST_PICKLE = "hist_pickles\\test.pickle"
results = []
SOURCES = "hist_pickles\\all_pcaps.pickle"
# for SOURCE in SOURCES:
for i in range(0, 5):
    test_train_ott(fname=SOURCES, train_out=TRAIN_PICKLE,
                   test_out=TEST_PICKLE)
    # labels = ['dropbox', 'facebook', 'google',
    #           'microsoft', 'teamviewer', 'twitter', 'youtube']
    testLabels = []
    # initialize the number of epochs to train for and batch size
    NUM_EPOCHS = 75
    BS = 128

    # initialize the total number of training and testing image
    NUM_TRAIN_IMAGES = 0
    NUM_TEST_IMAGES = 0

    # open the training CSV file, then initialize the unique set of class
    # labels in the dataset along with the testing labels
    with open(TRAIN_PICKLE, 'rb') as handle:
        b = pickle.load(handle)
        NUM_TRAIN_IMAGES = len(b)

    with open(TEST_PICKLE, 'rb') as handle:
        b = pickle.load(handle)
        NUM_TEST_IMAGES = len(b)
        for curr_dict in b:
            testLabels.append(curr_dict['Label'])

    print("all test labels")
    print(testLabels)
    lb = LabelBinarizer()
    lb.fit(labels)
    testLabels = lb.transform(testLabels)
    print(testLabels)
    labels = testLabels

    # initialize both the training and testing image generators
    trainGen = pickle_image_generator_32_ott(TRAIN_PICKLE, BS, lb,
                                             mode="train", aug=None)
    testGen = pickle_image_generator_32_ott(TEST_PICKLE, BS, lb,
                                            mode="train", aug=None)
    model = keras.Sequential()

    # Layer 1
    # Conv Layer 1
    model.add(layers.Conv2D(filters=6,
                            kernel_size=5,
                            strides=1,
                            activation='relu',
                            input_shape=(1500, 1500, 1)))
    # Pooling layer 1
    model.add(layers.MaxPooling2D(pool_size=2, strides=2))
    # Layer 2
    # Conv Layer 2
    model.add(layers.Conv2D(filters=16,
                            kernel_size=5,
                            strides=1,
                            activation='relu',
                            input_shape=(15, 15, 10)))
    model.add(Dropout(0.25))
    # Pooling Layer 2
    model.add(layers.MaxPooling2D(pool_size=2, strides=2))
    # Flatten
    model.add(layers.Flatten())
    # Layer 3
    # Fully connected layer 1
    model.add(layers.Dense(units=120, activation='relu'))
    # Layer 4
    # Fully connected layer 2
    model.add(layers.Dense(units=84, activation='relu'))
    # Layer 5
    model.add(Dropout(0.5))
    # Output Layer
    model.add(layers.Dense(units=len(lb.classes_), activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])

    es = EarlyStopping(monitor='val_loss', mode='min', patience=20)

    H = model.fit_generator(
        trainGen,
        steps_per_epoch=NUM_TRAIN_IMAGES // BS,
        validation_data=testGen,
        validation_steps=NUM_TEST_IMAGES // BS,
        epochs=NUM_EPOCHS,
        callbacks=[es])

    model.save('mod.h5')

    # serialize model to JSON
    model_json = model.to_json()
    with open("model_ott_10s.json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model.save_weights("model_ott_10s_weights.h5")
    print("Saved model to disk")

    # re-initialize our testing data generator, this time for evaluating
    testGen = pickle_image_generator_32_ott(TEST_PICKLE, BS, lb,
                                            mode="eval", aug=None)

    # make predictions on the testing images, finding the index of the
    # label with the corresponding largest predicted probability
    predIdxs = model.predict_generator(testGen,
                                       steps=(NUM_TEST_IMAGES // BS) + 1)

    predIdxs = np.argmax(predIdxs, axis=1)

    # show a nicely formatted classification report
    print("[INFO] evaluating network...")
    report = classification_report(testLabels.argmax(axis=1), predIdxs,
                                   target_names=lb.classes_)
    print(report)
    matrix = confusion_matrix(testLabels.argmax(axis=1), predIdxs)
    print(matrix)
    results.append([SOURCE, matrix, report])

print(results)

with open("/content/32_rr_ott_results.txt", "a") as res_file:
    for result in results:
        res_file.write(str(result[0]))
        res_file.write(str(result[1]))
        res_file.write(str(result[2]))
        res_file.write("\n")

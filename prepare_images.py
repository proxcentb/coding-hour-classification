from os import makedirs, listdir
from os.path import join as join_path
from shutil import rmtree as removedir, copy
from random import shuffle

removedir('sorted_images', ignore_errors=True)
for label in listdir('created_images'):
    label_path = join_path('created_images', label)
    images_paths = [join_path(label_path, filename) for filename in listdir(label_path)]
    
    shuffle(images_paths)
    test_images_len = int(len(images_paths) * 0.2)

    test_from = images_paths[:test_images_len]
    train_from = images_paths[test_images_len:]

    test_to = join_path('sorted_images/test', label)
    makedirs(test_to)
    for path in test_from:
        copy(path, test_to)

    train_to = join_path('sorted_images/train', label)
    makedirs(train_to)
    for path in train_from:
        copy(path, train_to)
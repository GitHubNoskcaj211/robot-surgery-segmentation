from prepare_data import data_path


def get_split(fold, cropped_train):
    folds = {0: [4, 2],
             1: [2, 4],
             2: [3, 4],
             3: [1, 4]}

    train_path = data_path / cropped_train

    print(f'My train path is: {train_path}')

    train_file_names = []
    val_file_names = []

    for instrument_id in range(1, 5):
        if instrument_id in folds[fold]:
            val_file_names += list((train_path / ('instrument_dataset_' + str(instrument_id)) / 'images').glob('*'))
        else:
            train_file_names += list((train_path / ('instrument_dataset_' + str(instrument_id)) / 'images').glob('*'))

    return train_file_names, val_file_names

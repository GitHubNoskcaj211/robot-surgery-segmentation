"""
[1] Merge masks with different instruments into one binary mask
[2] Crop black borders from images and masks
"""
from pathlib import Path

from tqdm import tqdm
import cv2
import numpy as np

data_path = Path('Dataset')

train_path = data_path / 'instrument_1_4_training'

cropped_train_path = data_path / 'cropped_train'
cropped_train_path_right = data_path / 'cropped_train_right'

original_height, original_width = 1080, 1920
height, width = 1024, 1280
h_start, w_start = 28, 320

binary_factor = 255
parts_factor = 85
instrument_factor = 32

shift_i = 10
shift_j = 13
def create_right_label_from_left_label(left_label):
  label_right = np.zeros((height, width), dtype=np.uint8)
  for i in range(height):
    for j in range(width):
      right_i = round(i + shift_i)
      right_j = round(j + shift_j)
      if right_i >= 0 and right_i < height:
        if right_j >= 0 and right_j < width:
          label_right[right_i, right_j] = left_label[i, j]
  return label_right

if __name__ == '__main__':
    for instrument_index in range(1, 5):
        instrument_folder = 'instrument_dataset_' + str(instrument_index)

        (cropped_train_path / instrument_folder / 'images').mkdir(exist_ok=True, parents=True)

        binary_mask_folder = (cropped_train_path / instrument_folder / 'binary_masks')
        binary_mask_folder.mkdir(exist_ok=True, parents=True)

        parts_mask_folder = (cropped_train_path / instrument_folder / 'parts_masks')
        parts_mask_folder.mkdir(exist_ok=True, parents=True)

        instrument_mask_folder = (cropped_train_path / instrument_folder / 'instruments_masks')
        instrument_mask_folder.mkdir(exist_ok=True, parents=True)

        (cropped_train_path_right / instrument_folder / 'images').mkdir(exist_ok=True, parents=True)

        binary_mask_folder_right = (cropped_train_path_right / instrument_folder / 'binary_masks')
        binary_mask_folder_right.mkdir(exist_ok=True, parents=True)

        parts_mask_folder_right = (cropped_train_path_right/ instrument_folder / 'parts_masks')
        parts_mask_folder_right.mkdir(exist_ok=True, parents=True)

        instrument_mask_folder_right = (cropped_train_path_right / instrument_folder / 'instruments_masks')
        instrument_mask_folder_right.mkdir(exist_ok=True, parents=True)

        mask_folders = list((train_path / instrument_folder / 'ground_truth').glob('*'))
        # mask_folders = [x for x in mask_folders if 'Other' not in str(mask_folders)]

        for file_name in tqdm(list((train_path / instrument_folder / 'left_frames').glob('*'))):
            img = cv2.imread(str(file_name))
            old_h, old_w, _ = img.shape

            img = img[h_start: h_start + height, w_start: w_start + width]
            cv2.imwrite(str(cropped_train_path / instrument_folder / 'images' / (file_name.stem + '.png')), img)

            mask_binary = np.zeros((old_h, old_w))
            mask_parts = np.zeros((old_h, old_w))
            mask_instruments = np.zeros((old_h, old_w))

            for mask_folder in mask_folders:
                mask = cv2.imread(str(mask_folder / file_name.name), 0)

                if 'Bipolar_Forceps' in str(mask_folder):
                    mask_instruments[mask > 0] = 1
                elif 'Prograsp_Forceps' in str(mask_folder):
                    mask_instruments[mask > 0] = 2
                elif 'Large_Needle_Driver' in str(mask_folder):
                    mask_instruments[mask > 0] = 3
                elif 'Vessel_Sealer' in str(mask_folder):
                    mask_instruments[mask > 0] = 4
                elif 'Grasping_Retractor' in str(mask_folder):
                    mask_instruments[mask > 0] = 5
                elif 'Monopolar_Curved_Scissors' in str(mask_folder):
                    mask_instruments[mask > 0] = 6
                elif 'Other' in str(mask_folder):
                    mask_instruments[mask > 0] = 7

                if 'Other' not in str(mask_folder):
                    mask_binary += mask

                    mask_parts[mask == 10] = 1  # Shaft
                    mask_parts[mask == 20] = 2  # Wrist
                    mask_parts[mask == 30] = 3  # Claspers

            mask_binary = (mask_binary[h_start: h_start + height, w_start: w_start + width] > 0).astype(
                np.uint8) * binary_factor
            mask_parts = (mask_parts[h_start: h_start + height, w_start: w_start + width]).astype(
                np.uint8) * parts_factor
            mask_instruments = (mask_instruments[h_start: h_start + height, w_start: w_start + width]).astype(
                np.uint8) * instrument_factor

            cv2.imwrite(str(binary_mask_folder / file_name.name), mask_binary)
            cv2.imwrite(str(parts_mask_folder / file_name.name), mask_parts)
            cv2.imwrite(str(instrument_mask_folder / file_name.name), mask_instruments)

        for file_name in tqdm(list((train_path / instrument_folder / 'right_frames').glob('*'))):
            img = cv2.imread(str(file_name))
            old_h, old_w, _ = img.shape

            img = img[h_start: h_start + height, w_start: w_start + width]
            cv2.imwrite(str(cropped_train_path_right / instrument_folder / 'images' / (file_name.stem + '.png')), img)

            mask_binary = np.zeros((old_h, old_w))
            mask_parts = np.zeros((old_h, old_w))
            mask_instruments = np.zeros((old_h, old_w))

            for mask_folder in mask_folders:
                mask = cv2.imread(str(mask_folder / file_name.name), 0)

                if 'Bipolar_Forceps' in str(mask_folder):
                    mask_instruments[mask > 0] = 1
                elif 'Prograsp_Forceps' in str(mask_folder):
                    mask_instruments[mask > 0] = 2
                elif 'Large_Needle_Driver' in str(mask_folder):
                    mask_instruments[mask > 0] = 3
                elif 'Vessel_Sealer' in str(mask_folder):
                    mask_instruments[mask > 0] = 4
                elif 'Grasping_Retractor' in str(mask_folder):
                    mask_instruments[mask > 0] = 5
                elif 'Monopolar_Curved_Scissors' in str(mask_folder):
                    mask_instruments[mask > 0] = 6
                elif 'Other' in str(mask_folder):
                    mask_instruments[mask > 0] = 7

                if 'Other' not in str(mask_folder):
                    mask_binary += mask

                    mask_parts[mask == 10] = 1  # Shaft
                    mask_parts[mask == 20] = 2  # Wrist
                    mask_parts[mask == 30] = 3  # Claspers

            mask_binary = (mask_binary[h_start: h_start + height, w_start: w_start + width] > 0).astype(
                np.uint8) * binary_factor
            mask_parts = (mask_parts[h_start: h_start + height, w_start: w_start + width]).astype(
                np.uint8) * parts_factor
            mask_instruments = (mask_instruments[h_start: h_start + height, w_start: w_start + width]).astype(
                np.uint8) * instrument_factor

            cv2.imwrite(str(binary_mask_folder_right / file_name.name), create_right_label_from_left_label(mask_binary))
            cv2.imwrite(str(parts_mask_folder_right / file_name.name), create_right_label_from_left_label(mask_parts))
            cv2.imwrite(str(instrument_mask_folder_right / file_name.name), create_right_label_from_left_label(mask_instruments))

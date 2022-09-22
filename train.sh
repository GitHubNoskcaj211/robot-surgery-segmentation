#!/bin/bash

for i in 0 1 2 3
do
    python train.py \
        --device-ids 0 \
        --batch-size 1 \
        --fold $i \
        --workers 0 \
        --type "binary" \
        --lr 0.00005 \
        --n-epochs 10 \
        --jaccard-weight 0.3 \
        --model UNet11 \
        --train_crop_height 1024 \
        --train_crop_width 1280 \
        --val_crop_height 1024 \
        --val_crop_width 1280
done

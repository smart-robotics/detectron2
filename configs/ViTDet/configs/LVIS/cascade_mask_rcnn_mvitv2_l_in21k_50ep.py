from detectron2 import model_zoo

from .cascade_mask_rcnn_mvitv2_b_in21k_100ep import (
    dataloader,
    lr_multiplier,
    train,
    optimizer,
)

model = model_zoo.get_config("ViTDet/configs/LVIS/cascade_mask_rcnn_mvitv2_b_in21k_100ep.py").model

model.backbone.bottom_up.embed_dim = 144
model.backbone.bottom_up.depth = 48
model.backbone.bottom_up.num_heads = 2
model.backbone.bottom_up.last_block_indexes = (1, 7, 43, 47)
model.backbone.bottom_up.drop_path_rate = 0.5

train.init_checkpoint = "detectron2://ImageNetPretrained/mvitv2/MViTv2_L_in21k.pyth"

train.max_iter = train.max_iter // 2  # 100ep -> 50ep
lr_multiplier.scheduler.milestones = [
    milestone // 2 for milestone in lr_multiplier.scheduler.milestones
]
lr_multiplier.scheduler.num_updates = train.max_iter
lr_multiplier.warmup_length = 250 / train.max_iter

optimizer.lr = 4e-5

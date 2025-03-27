_base_ = ['mmaction::_base_/default_runtime.py']

custom_imports = dict(imports='models')

pretrained = 'data/pretrain/ImageNet_1K_LSTM.pth'  # Location of pre-trained model

# The download link for the original pre-trained model (ImageNet-1K) is: 'https://download.openmmlab.com/mmaction/v1.0/recognition/swin/swin_tiny_patch4_window7_224.pth'

model = dict(
    type='Recognizer3D',
    backbone=dict(
        type='SwinTransformer3D',
        arch='tiny',
        pretrained=None,
        pretrained2d=False,
        patch_size=(2, 4, 4),
        window_size=(8, 7, 7),
        mlp_ratio=4.,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.1,
        patch_norm=True),
    data_preprocessor=dict(
        type='ActionDataPreprocessor',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        format_shape='NCTHW'),
    cls_head=dict(
        type='I3DHead',
        in_channels=768,#768
        num_classes=101,
        spatial_type='avg',
        dropout_ratio=0.5,
        average_clips='prob'))

# dataset settings
dataset_type = 'RawframeDataset'
data_root = '/data/students/mmaction2/data/ucf101/rawframes_rgb+flow_sparse'
data_root_val = '/data/students/mmaction2/data/ucf101/rawframes_rgb+flow_sparse'
split = 1  # official train/test splits. valid numbers: 1, 2, 3
ann_file_train = f'/data/students/mmaction2/data/ucf101/ucf101_train_split_{split}_rgb+flow_sparse_rawframes.txt'
ann_file_val = f'/data/students/mmaction2/data/ucf101/ucf101_val_split_{split}_rgb+flow_sparse_rawframes.txt'
ann_file_test = f'/data/students/mmaction2/data/ucf101/ucf101_val_split_{split}_rgb+flow_sparse_rawframes.txt'

file_client_args = dict(io_backend='disk')
train_pipeline = [
    # dict(type='DecordInit', **file_client_args),
    dict(type='SampleFrames', clip_len=128, frame_interval=1, num_clips=1),
    dict(type='RawFrameDecode', **file_client_args),
    # dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='RandomResizedCrop'),
    dict(type='Resize', scale=(224, 224), keep_ratio=False),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='PackActionInputs')
]
val_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=64,
        frame_interval=1,
        num_clips=1,
        test_mode=True),
    dict(type='RawFrameDecode', **file_client_args),
    # dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='PackActionInputs')
]
test_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=64,
        frame_interval=1,
        num_clips=1,
        test_mode=True),
    dict(type='RawFrameDecode', **file_client_args),
    # dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 224)),
    dict(type='ThreeCrop', crop_size=224),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='PackActionInputs')
]

train_dataloader = dict(
    batch_size=4,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        data_prefix=dict(img=data_root),
        pipeline=train_pipeline))
val_dataloader = dict(
    batch_size=2,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        data_prefix=dict(img=data_root_val),
        pipeline=val_pipeline,
        test_mode=True))
test_dataloader = dict(
    batch_size=2,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        data_prefix=dict(img=data_root_val),
        pipeline=test_pipeline,
        test_mode=True))

val_evaluator = dict(type='AccMetric')
test_evaluator = val_evaluator

train_cfg = dict(
    type='EpochBasedTrainLoop', max_epochs=50, val_begin=1, val_interval=5)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

optim_wrapper = dict(
    type='AmpOptimWrapper',
    optimizer=dict(
        type='AdamW', lr=1e-3, betas=(0.9, 0.999), weight_decay=0.05),
    accumulative_counts=8,
    constructor='SwinOptimWrapperConstructor',
    paramwise_cfg=dict(
        absolute_pos_embed=dict(decay_mult=0.),
        relative_position_bias_table=dict(decay_mult=0.),
        norm=dict(decay_mult=0.),
        backbone=dict(lr_mult=0.1)))

param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=0.1,
        by_epoch=True,
        begin=0,
        end=5,
        convert_to_iter_based=True),
    dict(
        type='CosineAnnealingLR',
        T_max=50,
        eta_min=0,
        by_epoch=True,
        begin=0,
        end=50)
]

default_hooks = dict(
    checkpoint=dict(interval=3, max_keep_ckpts=5), logger=dict(interval=100))

# Default setting for scaling LR automatically
#   - `enable` means enable scaling LR automatically
#       or not by default.
#   - `base_batch_size` = (4 GPUs) x (4 samples per GPU).
auto_scale_lr = dict(enable=False, base_batch_size=16)

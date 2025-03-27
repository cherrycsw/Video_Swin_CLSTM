import argparse
import os
import os.path as osp
import cv2
import numpy as np


def stackFlowChannel(path, dest):
    flowFileNumber = getFlowFileNumber(path) + 1
    flow_tmpl = '{}_{:05d}.jpg'
    for i in range(1, flowFileNumber):
        flow_x_names = osp.join(path, flow_tmpl.format('flow_x', i))
        flow_y_names = osp.join(path, flow_tmpl.format('flow_y', i))

        # 读取两张灰度图像
        gray_image1 = cv2.imread(flow_x_names, cv2.IMREAD_GRAYSCALE)
        gray_image2 = cv2.imread(flow_y_names, cv2.IMREAD_GRAYSCALE)

        # 创建一个三通道的图像，初始化为0
        stacked_image = np.zeros((gray_image1.shape[0], gray_image1.shape[1], 3), dtype=np.uint8)

        # 将两张灰度图像分别放入堆叠图像的不同通道，蓝色通道全部填充为0
        stacked_image[:, :, 0] = gray_image1  # 第一个通道
        stacked_image[:, :, 1] = gray_image2  # 第二个通道

        # 存储堆叠后的图像
        flow_names = osp.join(dest, flow_tmpl.format('flow_', i))
        cv2.imwrite(flow_names, stacked_image)


def getFlowFileNumber(path):
    # 指定文件夹路径
    folder_path = path  # 替换为实际文件夹的路径

    # 搜索包含特定字符串的文件
    search_string = "flow_x"
    matching_files = [file for file in os.listdir(folder_path) if search_string in file]

    # 统计匹配的文件数量
    file_count = len(matching_files)
    return file_count


def parse_args():
    parser = argparse.ArgumentParser(description='Extract flow and RGB images')
    parser.add_argument(
        '--input',
        help='videos for frame extraction, can be'
             'single video or a video list, the video list should be a txt file '
             'and just consists of filenames without directories')
    parser.add_argument(
        '--prefix',
        default='',
        help='the prefix of input '
             'videos, used when input is a video list')
    parser.add_argument(
        '--dest',
        default='',
        help='the destination to save '
             'extracted frames')
    parser.add_argument(
        '--save-rgb', action='store_true', help='also save '
                                                'rgb frames')
    parser.add_argument(
        '--rgb-tmpl',
        default='img_{:05d}.jpg',
        help='template filename of rgb frames')
    parser.add_argument(
        '--flow-tmpl',
        default='{}_{:05d}.jpg',
        help='template filename of flow frames')
    parser.add_argument(
        '--start-idx',
        type=int,
        default=1,
        help='the start '
             'index of extracted frames')
    parser.add_argument(
        '--method',
        default='tvl1',
        help='use which method to '
             'generate flow')
    parser.add_argument(
        '--bound', type=float, default=20, help='maximum of '
                                                'optical flow')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if args.input.endswith('.txt'):
        lines = open(args.input).readlines()
        lines = [x.strip() for x in lines]
        videos = [osp.join(args.prefix, x) for x in lines]
        dests = [osp.join(args.dest, x) for x in lines]
        for video, dest in zip(videos, dests):
            path1=video+"/"
            path2=dest+"/"
            stackFlowChannel(path1, path2)

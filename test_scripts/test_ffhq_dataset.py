import math
import os
import torch
import torchvision.utils

from basicsr.data import build_dataloader, build_dataset


def main():
    """Test FFHQ dataset."""
    opt = {
        'dist': False,
        'gpu_ids': [0],
        'phase': 'train',
        'name': 'FFHQ',
        'type': 'FFHQDataset',
        'dataroot_gt': 'datasets/ffhq/ffhq_256.lmdb',
        'io_backend': dict(type='lmdb'),
        'use_hflip': True,
        'mean': [0.5, 0.5, 0.5],
        'std': [0.5, 0.5, 0.5],
        'use_shuffle': True,
        'num_worker_per_gpu': 1,
        'batch_size_per_gpu': 4,
        'dataset_enlarge_ratio': 1,
    }

    os.makedirs('tmp', exist_ok=True)

    dataset = build_dataset(opt)
    data_loader = build_dataloader(dataset, opt, num_gpu=0, dist=opt['dist'], sampler=None)

    nrow = int(math.sqrt(opt['batch_size_per_gpu']))
    padding = 2 if opt['phase'] == 'train' else 0

    print('start...')
    for i, data in enumerate(data_loader):
        if i > 5:
            break
        print(i)

        gt = data['gt']
        print(torch.min(gt), torch.max(gt))
        gt_path = data['gt_path']
        print(gt_path)
        torchvision.utils.save_image(
            gt, f'tmp/gt_{i:03d}.png', nrow=nrow, padding=padding, normalize=True, range=(-1, 1))


if __name__ == '__main__':
    main()

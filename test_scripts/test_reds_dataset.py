import math
import os
import torchvision.utils

from basicsr.data import build_dataloader, build_dataset


def main(mode='folder'):
    """Test reds dataset.

    Args:
        mode: There are two modes: 'lmdb', 'folder'.
    """
    opt = {'dist': False, 'phase': 'train', 'name': 'REDS', 'type': 'REDSDataset'}
    if mode == 'folder':
        opt['dataroot_gt'] = 'datasets/REDS/train_sharp'
        opt['dataroot_lq'] = 'datasets/REDS/train_sharp_bicubic'
        opt['dataroot_flow'] = None
        opt['meta_info_file'] = 'basicsr/data/meta_info/meta_info_REDS_GT.txt'
        opt['io_backend'] = dict(type='disk')
    elif mode == 'lmdb':
        opt['dataroot_gt'] = 'datasets/REDS/train_sharp_with_val.lmdb'
        opt['dataroot_lq'] = 'datasets/REDS/train_sharp_bicubic_with_val.lmdb'
        opt['dataroot_flow'] = None
        opt['meta_info_file'] = 'basicsr/data/meta_info/meta_info_REDS_GT.txt'
        opt['io_backend'] = dict(type='lmdb')

    opt['val_partition'] = 'REDS4'
    opt['num_frame'] = 5
    opt['gt_size'] = 256
    opt['interval_list'] = [1]
    opt['random_reverse'] = True
    opt['use_hflip'] = True
    opt['use_rot'] = True

    opt['use_shuffle'] = True
    opt['num_worker_per_gpu'] = 1
    opt['batch_size_per_gpu'] = 16
    opt['scale'] = 4

    opt['dataset_enlarge_ratio'] = 1

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

        lq = data['lq']
        gt = data['gt']
        key = data['key']
        print(key)
        for j in range(opt['num_frame']):
            torchvision.utils.save_image(
                lq[:, j, :, :, :], f'tmp/lq_{i:03d}_frame{j}.png', nrow=nrow, padding=padding, normalize=False)
        torchvision.utils.save_image(gt, f'tmp/gt_{i:03d}.png', nrow=nrow, padding=padding, normalize=False)


if __name__ == '__main__':
    main()

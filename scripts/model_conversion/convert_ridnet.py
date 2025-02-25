import torch
from collections import OrderedDict

from basicsr.archs.ridnet_arch import RIDNet

if __name__ == '__main__':
    ori_net_checkpoint = torch.load(
        'experiments/pretrained_models/RIDNet/RIDNet_official_original.pt', map_location=lambda storage, loc: storage)
    rid_net = RIDNet(3, 64, 3)
    new_ridnet_dict = OrderedDict()

    rid_net_namelist = [name for name, param in rid_net.named_parameters()]
    for count, (name, param) in enumerate(ori_net_checkpoint.items()):
        new_ridnet_dict[rid_net_namelist[count]] = param
    rid_net.load_state_dict(new_ridnet_dict)
    torch.save(rid_net.state_dict(), 'experiments/pretrained_models/RIDNet/RIDNet.pth')

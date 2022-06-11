import pickle
from typing import List
import os
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader


def load_data(path: str, training: bool = True, fix_width: bool = False):
    """
    用于加载 EvalImage 数据集，继承于torch.utils.data.Dataset

    Args:
        path (string): 存放中间文件的目录
        training (bool, optional): 为True时加载训练集，为False时加载测试集，默认为True
        fix_width (bool, optional): 为True时将图片缩放到固定宽度，为False时宽度不固定，默认为False

    Return:
        加载的训练集或者测试集
    """
    if training:
        batch_size = 128 if fix_width else 1
        filename = os.path.join(path, 'train' + ('_fix_width' if fix_width else '') + '.pkl')
        if os.path.exists(filename):
            dataset = pickle.load(open(filename, 'rb'))
        else:
            print('==== Loading data.. ====')
            dataset = EvalImageSet(training=True, fix_width=fix_width)
            pickle.dump(dataset, open(filename, 'wb'), True)
        dataloader = DataLoader(dataset, batch_size=batch_size,
                                shuffle=True, num_workers=4)
    else:
        batch_size = 128 if fix_width else 1
        filename = os.path.join(path, 'test' + ('_fix_width' if fix_width else '') + '.pkl')
        if os.path.exists(filename):
            dataset = pickle.load(open(filename, 'rb'))
        else:
            print('==== Loading data.. ====')
            dataset = EvalImageSet(training=False, fix_width=fix_width)
            pickle.dump(dataset, open(filename, 'wb'), True)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    return dataloader


def read_eval_txt(path: str, training=True) -> List[str]:
    """
    用于读取 eval.txt

    Args:
        path (string): eval.txt文件所在位置
        training (bool, optional): 为True时加载训练集，为False时加载测试集，默认为True

    Return:
        加载的训练集或者测试集
    """
    if training:
        b, e = 0, 300
    else:
        b, e = 300, 342
    with open(path, encoding='utf8') as f:
        i = 0
        while True:
            line = f.readline()
            if not line:
                break
            if b <= i <= e:
                yield line.strip('\n').split('\t')
            i = i + 1


class FixHeightResize(object):
    """
    对图片做固定高度的缩放
    """

    def __init__(self, height: int = 32, minwidth: int = 100):
        self.height = height
        self.minwidth = minwidth

    # img 为 PIL.Image 对象
    def __call__(self, img: Image) -> Image:
        w, h = img.size
        width = max(int(w * self.height / h), self.minwidth)
        return img.resize((width, self.height), Image.ANTIALIAS)


class EvalImageSet(Dataset):
    """
    用于加载Evalset数据集，继承于torch.utils.data.Dataset

    Args:
        training (bool, optional): 为True时加载训练集，为False时加载测试集，默认为True
        fix_width (bool, optional): 为True时将图片缩放到固定宽度，为False时宽度不固定，默认为False
    """

    def __init__(self, training: bool = True, fix_width: bool = False):
        self.imgs_path, self.label = zip(*[(x, y) for x, y in read_eval_txt('data/eval.txt', training)])

        # 图片缩放 + 转化为灰度图 + 转化为张量
        transform = [transforms.Resize((32, 100), Image.ANTIALIAS)
                     if fix_width else FixHeightResize(32)]
        transform.extend([transforms.Grayscale(), transforms.ToTensor()])
        transform = transforms.Compose(transform)

        # 加载图片
        self.img = [transform(Image.open(img_path)) for img_path in self.imgs_path]

    # 以下两个方法必须要重载
    def __len__(self, ):
        return len(self.img)

    def __getitem__(self, idx):
        return self.img[idx], self.label[idx]

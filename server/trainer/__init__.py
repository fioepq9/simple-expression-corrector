import torch
from torchvision import transforms

from .models.crnn import CRNN, LabelTransformer
from .loader.load_eval import FixHeightResize, DataLoader


def correct(img) -> bool:
    letters = '1234567890-=+.×÷'
    labeltransformer = LabelTransformer(letters)
    # 图片缩放 + 转化为灰度图 + 转化为张量
    transform = [FixHeightResize(32)]
    transform.extend([transforms.Grayscale(), transforms.ToTensor()])
    transform = transforms.Compose(transform)
    # use gpu or not
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    net = CRNN(1, len(letters) + 1)
    net.load_state_dict(torch.load("./trainer/asset/crnn.pth", map_location=torch.device('cpu')))
    if use_cuda:
        net.to(device)
    net.eval()
    imgs = [transform(img)]
    dataloader = DataLoader(imgs)
    for img in dataloader:
        img.to(device)
        outputs = net(img)  # length × batch × num_letters
        outputs = outputs.max(2)[1].transpose(0, 1)  # batch × length
        outputs = labeltransformer.decode(outputs.data)
    output = outputs[0]

    output = output.split('=')
    if len(output) != 2:
        print(f'output: {output}, length = {len(output)}')
        return False
    try:
        output[0] = output[0].replace('×', '*')
        output[0] = output[0].replace('÷', '/')
        out = float(eval(output[0]))
        real = float(output[1])
    except:
        print(f'exception occur, eval: {output[0]}')
        return False
    print(f'left:{output[0]}, out: {out}, real: {real}')
    return abs(out - real) <= 1e-3

import os

from torch.utils.data import DataLoader

from .convnet import ConvNet
from .crnn import CRNN
import torch
import config
from torchvision import transforms
import torchvision.transforms.functional
import numpy as np
from PIL import Image

global model


def init_model():
    global model


def image_to_tensor(image):
    gray_image = transforms.functional.to_grayscale(image)  # 转换为灰度图
    resized_image = transforms.functional.resize(gray_image, [28, 28])
    input_image_tensor = transforms.functional.to_tensor(resized_image)
    input_image_tensor_norm = transforms.functional.normalize(input_image_tensor, [0.1302], [0.3069])  # 正则化
    return input_image_tensor_norm


def run_model_convnet(input_tensor):
    global model
    model_input = input_tensor.unsqueeze(0)
    with torch.no_grad():
        model_output = model(model_input)[0]
    model_prediction = model_output.detach().numpy().argmax()
    return model_prediction


def debug_model_convnet(input_tensor):  # 输出原始的概率信息
    global model
    model_input = input_tensor.unsqueeze(0)
    with torch.no_grad():
        model_output = model(model_input)[0]
    model_prediction = model_output.detach().numpy()
    return np.exp(model_prediction)


def post_process(output):
    return str(output)


class FixHeightResize(object):
    """
    对图片做固定高度的缩放
    """

    def __init__(self, height=32, minwidth=100):
        self.height = height
        self.minwidth = minwidth

    # img 为 PIL.Image 对象
    def __call__(self, img):
        w, h = img.size
        width = max(int(w * self.height / h), self.minwidth)
        return img.resize((width, self.height), Image.ANTIALIAS)


def judge(image_path: str) -> str:
    letters = '1234567890+-.÷×='
    labeltransformer = LabelTransformer(letters)
    # 图片缩放 + 转化为灰度图 + 转化为张量
    transform = [FixHeightResize(32)]
    transform.extend([transforms.Grayscale(), transforms.ToTensor()])
    transform = transforms.Compose(transform)
    # use gpu or not
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    net = CRNN(1, len(letters) + 1)
    if os.path.exists(config.PATH_TO_MODEL):
        net.load_state_dict(torch.load(config.PATH_TO_MODEL, map_location=torch.device('cpu')))
    net.to(device)
    net.eval()
    imgs = [transform(Image.open(image_path))]
    dataloader = DataLoader(imgs, batch_size=1, shuffle=False)
    for img in dataloader:
        img.to(device)
        outputs = net(img)  # length × batch × num_letters
        outputs = outputs.max(2)[1].transpose(0, 1)  # batch × length
        outputs = labeltransformer.decode(outputs.data)
        return post_process(outputs[0])


class LabelTransformer(object):
    """
    字符编码解码器

    Args:
        letters (str): 所有的字符组成的字符串
    """

    def __init__(self, letters):
        self.encode_map = {letter: idx + 1 for idx, letter in enumerate(letters)}
        self.decode_map = ' ' + letters

    def encode(self, text):
        if isinstance(text, str):
            length = [len(text)]
            result = [self.encode_map[letter] for letter in text]
        else:
            length = []
            result = []
            for word in text:
                length.append(len(word))
                result.extend([self.encode_map[letter] for letter in word])
        return torch.IntTensor(result), torch.IntTensor(length)

    def decode(self, text_code):
        result = []
        for code in text_code:
            word = []
            for i in range(len(code)):
                if code[i] != 0 and (i == 0 or code[i] != code[i - 1]):
                    word.append(self.decode_map[code[i]])
            result.append(''.join(word))
        return result

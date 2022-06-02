from .convnet import ConvNet
import torch
import config
from torchvision import transforms
import torchvision.transforms.functional
import numpy as np
from PIL import Image

global model


def init_model():
    global model
    model = ConvNet()
    model.load_state_dict(torch.load(config.PATH_TO_MODEL, map_location="cpu"))
    model.eval()


def image_to_tensor(image):
    gray_image = transforms.functional.to_grayscale(image)  # 转换为灰度图
    resized_image = transforms.functional.resize(gray_image, [28, 28])
    input_image_tensor = transforms.functional.to_tensor(resized_image)
    input_image_tensor_norm = transforms.functional.normalize(input_image_tensor, [0.1302], [0.3069])  # 正则化
    return input_image_tensor_norm


def run_model(input_tensor):
    global model
    model_input = input_tensor.unsqueeze(0)
    with torch.no_grad():
        model_output = model(model_input)[0]
    model_prediction = model_output.detach().numpy().argmax()
    return model_prediction


def debug_model(input_tensor):  # 输出原始的概率信息
    global model
    model_input = input_tensor.unsqueeze(0)
    with torch.no_grad():
        model_output = model(model_input)[0]
    model_prediction = model_output.detach().numpy()
    return np.exp(model_prediction)


def post_process(output):
    return str(output)


def judge(image_path: str) -> str:
    image = Image.open(image_path)
    input_tensor = image_to_tensor(image)
    output = run_model(input_tensor)
    return post_process(output)

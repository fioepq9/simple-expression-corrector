import Image
import torch
from torchvision import transforms

from .models.crnn import CRNN
from .loader.load_eval import FixHeightResize

def correct(img) -> bool:
    # reconstructure image
    transform = [transforms.Resize((32, 100), Image.ANTIALIAS)
                     if fix_width else FixHeightResize(32)]
    transform = transforms.Compose(transform)
    img = transform(img)
    img = img.to(
        torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
    )
    # load model net
    model_path = f"trainer/asset/crnn.pth"
    net = CRNN(1, len('1234567890-=+.×÷') + 1)
    if torch.cuda.is_available():
        net.load_state_dict(
            torch.load(model_path, map_location=torch.device('cpu'))
        )
    else:
        net.load_state_dict(torch.load(model_path))
    # predict
    outputs = net(img)  # length × batch × num_letters
    outputs = outputs.max(2)[1].transpose(0, 1)  # batch × length
    outputs = labeltransformer.decode(outputs.data)
    # eval
    outputs = outputs.split('=')
    if len(outputs) != 2:
        return False
    try:
        out = eval(outputs[0])
    except:
        return False
    return out == outputs[1]

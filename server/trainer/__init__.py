import Image
from torchvision import transforms

from .loader import FixHeightResize

def correct(img) -> bool:
    transform = [transforms.Resize((32, 100), Image.ANTIALIAS)
                     if fix_width else FixHeightResize(32)]
    transform = transforms.Compose(transform)
    img = transform(img)
    img = img.to(
        torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
    )
    outputs = self.net(img)  # length × batch × num_letters
    outputs = outputs.max(2)[1].transpose(0, 1)  # batch × length
    outputs = labeltransformer.decode(outputs.data)
    
    outputs = outputs.split('=')
    if len(outputs) != 2:
        return False
    try:
        out = eval(outputs[0])
    except:
        return False
    return out == outputs[1]

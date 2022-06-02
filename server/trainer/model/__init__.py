import os

import torch.optim as optim
import torch

import model.crnn
from trainer import loader
from trainer.model import crnn


def train(root, start_epoch, epoch_num, letters,
          net=None, lr=0.1, fix_width=True):
    """
    Train CRNN model

    Args:
        root (str): Root directory of dataset
        start_epoch (int): Epoch number to start
        epoch_num (int): Epoch number to train
        letters (str): Letters contained in the data
        net (CRNN, optional): CRNN model (default: None)
        lr (float, optional): Coefficient that scale delta before it is applied
            to the parameters (default: 1.0)
        fix_width (bool, optional): Scale images to fixed size (default: True)

    Returns:
        CRNN: Trained CRNN model
    """

    # load data
    trainloader = loader.load_data(root, training=True, fix_width=fix_width)
    if not net:
        # create a new model if net is None
        net = crnn.CRNN(1, len(letters) + 1)
    # loss function
    criterion = torch.nn.CTCLoss()
    # Adadelta
    optimizer = optim.Adadelta(net.parameters(), lr=lr, weight_decay=1e-3)
    # use gpu or not
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        net = net.to(device)
        criterion = criterion.to(device)
    else:
        print("*****   Warning: Cuda isn't available!  *****")

    # get encoder and decoder
    labeltransformer = LabelTransformer(letters)

    print('====   Training..   ====')
    # .train() has any effect on Dropout and BatchNorm.
    net.train()
    for epoch in range(start_epoch, start_epoch + epoch_num):
        print('----    epoch: %d    ----' % (epoch,))
        loss_sum = 0
        for i, (img, label) in enumerate(trainloader):
            label, label_length = labeltransformer.encode(label)
            img = img.to(device)
            optimizer.zero_grad()
            # put images in
            outputs = net(img)
            output_length = torch.IntTensor(
                [outputs.size(0)] * outputs.size(1))
            # calc loss
            loss = criterion(outputs, label, output_length, label_length)
            # update
            loss.backward()
            optimizer.step()
            loss_sum += loss.item()
        print('loss = %f' % (loss_sum,))
    print('Finished Training')
    return net


def test(root, net, letters, fix_width=True):
    """
    Test CRNN model

    Args:
        root (str): Root directory of dataset
        letters (str): Letters contained in the data
        net (CRNN, optional): trained CRNN model
        fix_width (bool, optional): Scale images to fixed size (default: True)
    """

    # load data
    trainloader = loader.load_data(root, training=True, fix_width=fix_width)
    testloader = loader.load_data(root, training=False, fix_width=fix_width)
    # use gpu or not
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        net = net.to(device)
    else:
        print("*****   Warning: Cuda isn't available!  *****")
    # get encoder and decoder
    labeltransformer = LabelTransformer(letters)

    print('====    Testing..   ====')
    # .eval() has any effect on Dropout and BatchNorm.
    net.eval()
    acc = []
    for _loader in (testloader, trainloader):
        correct = 0
        total = 0
        for i, (img, origin_label) in enumerate(_loader):
            img = img.to(device)

            outputs = net(img)  # length × batch × num_letters
            outputs = outputs.max(2)[1].transpose(0, 1)  # batch × length
            outputs = labeltransformer.decode(outputs.data)
            correct += sum([out == real for out, real in zip(outputs, origin_label)])
            total += len(origin_label)
        # calc accuracy
        acc.append(correct / total * 100)
    print('testing accuracy: ', acc[0], '%')
    print('training accuracy: ', acc[1], '%')


def main(epoch_num, lr=0.1, training=True, fix_width=True):
    """
    Main

    Args:
        training (bool, optional): If True, train the model, otherwise test it (default: True)
        fix_width (bool, optional): Scale images to fixed size (default: True)
        :param fix_width:
        :param training:
        :param lr:
        :param epoch_num:
    """

    model_path = ('fix_width_' if fix_width else '') + 'crnn.pth'
    letters = '1234567890+-.÷×='
    root = './'
    if training:
        net = crnn.CRNN(1, len(letters) + 1)
        start_epoch = 0
        # if there is pre-trained model, load it
        if os.path.exists(model_path):
            print('Pre-trained model detected.\nLoading model...')
            net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        if torch.cuda.is_available():
            print('GPU detected.')
        net: model.crnn.CRNN = train(root, start_epoch, epoch_num, letters,
                                     net=net, lr=lr, fix_width=fix_width)
        # save the trained model for training again
        torch.save(net.state_dict(), model_path)
        # test
        test(root, net, letters, fix_width=fix_width)
    else:
        net = crnn.CRNN(1, len(letters) + 1)
        if os.path.exists(model_path):
            net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        test(root, net, letters, fix_width=fix_width)


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

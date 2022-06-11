import os
from typing import Tuple
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

import loader


class CRNN(nn.Module):
    """
    CRNN模型

    Args:
        in_channels (int): 输入的通道数，如果是灰度图则为1，如果没有灰度化则为3
        out_channels (int): 输出的通道数（类别数），即样本里共有多少种字符
    """

    def __init__(self, in_channels: int, out_channels: int):
        super(CRNN, self).__init__()
        self.in_channels: int = in_channels
        hidden_size: int = 256
        # CNN 结构与参数
        self.cnn_struct: Tuple = ((64,), (128,), (256, 256), (512, 512), (512,))
        self.cnn_paras: Tuple = ((3, 1, 1), (3, 1, 1),
                                 (3, 1, 1), (3, 1, 1), (2, 1, 0))
        # 池化层结构
        self.pool_struct: Tuple = ((2, 2), (2, 2), (2, 1), (2, 1), None)
        # 是否加入批归一化层
        self.batch_norm: Tuple = (False, False, False, True, False)
        self.cnn: nn.Sequential = self._get_cnn_layers()
        # RNN 两层双向LSTM。pytorch中LSTM的输出通道数为hidden_size * num_directions,这里因为是双向的，所以num_directions为2
        self.rnn1: nn.LSTM = nn.LSTM(self.cnn_struct[-1][-1], hidden_size, bidirectional=True)
        self.rnn2: nn.LSTM = nn.LSTM(hidden_size * 2, hidden_size, bidirectional=True)
        # 最后一层全连接
        self.fc: nn.Linear = nn.Linear(hidden_size * 2, out_channels)
        # 初始化参数，不是很重要
        self._initialize_weights()

    def forward(self, x):  # input: height=32, width>=100
        x = self.cnn(x)  # batch, channel=512, height=1, width>=24
        x = x.squeeze(2)  # batch, channel=512, width>=24
        x = x.permute(2, 0, 1)  # width>=24, batch, channel=512
        x = self.rnn1(x)[0]  # length=width>=24, batch, channel=256*2
        x = self.rnn2(x)[0]  # length=width>=24, batch, channel=256*2
        l, b, h = x.size()
        x = x.view(l * b, h)  # length*batch, hidden_size*2
        x = self.fc(x)  # length*batch, output_size
        x = x.view(l, b, -1)  # length>=24, batch, output_size
        return x

    # 构建CNN层
    def _get_cnn_layers(self) -> nn.Sequential:
        cnn_layers = []
        in_channels = self.in_channels
        for i in range(len(self.cnn_struct)):
            for out_channels in self.cnn_struct[i]:
                cnn_layers.append(
                    nn.Conv2d(in_channels, out_channels, *(self.cnn_paras[i])))
                if self.batch_norm[i]:
                    cnn_layers.append(nn.BatchNorm2d(out_channels))
                cnn_layers.append(nn.ReLU(inplace=True))
                in_channels = out_channels
            if self.pool_struct[i]:
                cnn_layers.append(nn.MaxPool2d(self.pool_struct[i]))
        return nn.Sequential(*cnn_layers)

    def _initialize_weights(self) -> None:
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, np.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()


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


class Trainer:
    def __init__(self, path: str, letters: str, epoch_num: int, lr: float, fix_width: bool = True, net: CRNN = None):
        """
        Train CRNN model

        Args:
            path (str): save the data
            letters (str): Letters contained in the data
            epoch_num (int): Epoch number to train
            lr (float): Coefficient that scale delta before it is applied
                to the parameters
            net (CRNN, optional): CRNN model (default: None)
            fix_width (bool, optional): Scale images to fixed size (default: True)
        """
        self.path = path
        self.letters = letters
        self.epoch_num = epoch_num
        self.lr = lr
        self.fix_width = fix_width
        self.net = net
        if not net:
            # create a new model if net is None
            self.net = CRNN(1, len(letters) + 1)

    def train(self) -> CRNN:
        """
        Train CRNN model

        Returns:
            CRNN: Trained CRNN model
        """

        # load data
        train_loader = loader.load_data(self.path, training=True, fix_width=self.fix_width)
        # loss function
        criterion: nn.CTCLoss = nn.CTCLoss()
        # Adadelta
        optimizer: optim.Adadelta = optim.Adadelta(self.net.parameters(), lr=self.lr, weight_decay=1e-3)
        # use gpu or not
        use_cuda: bool = torch.cuda.is_available()
        device: torch.device = torch.device('cuda' if use_cuda else 'cpu')
        if use_cuda:
            self.net = self.net.to(device)
            criterion = criterion.to(device)
        else:
            print("*****   Warning: Cuda isn't available!  *****")

        # get encoder and decoder
        labelTransformer: LabelTransformer = LabelTransformer(self.letters)

        print('====   Training..   ====')
        # .train() has any effect on Dropout and BatchNorm.
        self.net.train()
        for epoch in range(self.epoch_num):
            print('----    epoch: %d    ----' % (epoch,))
            loss_sum = 0
            for i, (img, label) in enumerate(train_loader):
                label, label_length = labelTransformer.encode(label)
                img = img.to(device)
                optimizer.zero_grad()
                # put images in
                outputs = self.net(img)
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
        return self.net

    def test(self):
        """
        Test CRNN model
        """

        # load data
        trainloader = loader.load_data(self.path, training=True, fix_width=self.fix_width)
        testloader = loader.load_data(self.path, training=False, fix_width=self.fix_width)
        # use gpu or not
        use_cuda = torch.cuda.is_available()
        device = torch.device('cuda' if use_cuda else 'cpu')
        if use_cuda:
            self.net = self.net.to(device)
        else:
            print("*****   Warning: Cuda isn't available!  *****")
        # get encoder and decoder
        labeltransformer = LabelTransformer(self.letters)

        print('====    Testing..   ====')
        # .eval() has any effect on Dropout and BatchNorm.
        self.net.eval()
        acc = []
        for _loader in (testloader, trainloader):
            correct = 0
            total = 0
            for i, (img, origin_label) in enumerate(_loader):
                img = img.to(device)

                outputs = self.net(img)  # length × batch × num_letters
                outputs = outputs.max(2)[1].transpose(0, 1)  # batch × length
                outputs = labeltransformer.decode(outputs.data)
                correct += sum([out == real for out, real in zip(outputs, origin_label)])
                total += len(origin_label)
            # calc accuracy
            acc.append(correct / total * 100)
        print('testing accuracy: ', acc[0], '%')
        print('training accuracy: ', acc[1], '%')

    def Do(self, training: bool = True):
        """
            Main

            Args:
                training (bool, optional): If True, train the model, otherwise test it (default: True)
            """

        model_path = os.path.join(self.path, ('fix_width_' if self.fix_width else '') + 'crnn.pth')
        # if there is pre-trained model, load it
        if os.path.exists(model_path):
            print('Pre-trained model detected.\nLoading model...')
            if torch.cuda.is_available():
                print('GPU detected.')
                self.net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            else:
                self.net.load_state_dict(torch.load(model_path))
        if training:
            # if there is pre-trained model, load it
            if os.path.exists(model_path):
                print('Pre-trained model detected.\nLoading model...')
                if torch.cuda.is_available():
                    print('GPU detected.')
                    self.net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
                else:
                    self.net.load_state_dict(torch.load(model_path))
            self.net: CRNN = self.train()
            # save the trained model for training again
            torch.save(self.net.state_dict(), model_path)
        self.test()

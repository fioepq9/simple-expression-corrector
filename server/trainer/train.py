import argparse
from trainer import model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--epoch_num', type=int, default=1, help='number of epochs to train for (default=20)')
    parser.add_argument('--lr', type=float, default=0.03, help='learning rate for optim (default=0.1)')
    parser.add_argument('--test', action='store_true', help='Whether to test directly (default is training)')
    parser.add_argument('--fix_width', action='store_true',
                        help='Whether to resize images to the fixed width (default is True)')
    opt = parser.parse_args()
    print(opt)
    model.main(opt.epoch_num, lr=opt.lr, training=False, fix_width=opt.fix_width)

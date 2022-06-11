from models import crnn

if __name__ == '__main__':
    trainer = crnn.Trainer(path='asset', letters='1234567890-=+.×÷',
                           epoch_num=20, lr=0.1, fix_width=False)
    trainer.Do(training=True)

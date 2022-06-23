# import sys
# sys.path.insert(0, '/yolov5-master/')
from utils.datasets import *
from utils.utils import *
from trainer import *
import cv2
import os


def get_model():
    weights = './weights/best.pt'
    device = torch.device("cuda" if (torch.cuda.is_available()) else "cpu")
    # google_utils.attempt_download(weights)
    model = torch.load(weights, map_location=device)['model']
    model.to(device).eval()
    return model


def letterbox(img, new_shape=(416, 416), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)
    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = new_shape
        ratio = new_shape[0] / shape[1], new_shape[1] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2
    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


def detect(model, im0s, uid, pid, jid):
    t0 = time.time()
    device = torch.device("cuda" if (torch.cuda.is_available()) else "cpu")
    img = letterbox(im0s, new_shape=640)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    pred = model(img, augment=False)[0]
    pred = non_max_suppression(pred, 0.4, 0.5,
                               fast=True, classes=None, agnostic=False)

    acc, total = 0, 0
    for i, det in enumerate(pred):  # detections per image
        im0 = im0s
        if det is not None and len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            for *xyxy, conf, cls in det:
                label = ['1', '0']
                colors = [(0, 255, 0), (0, 0, 255)]
                flag = 0
                # 0 answer right green
                # 1 answer error red
                if conf > 0.75:
                    temp = im0[int(xyxy[1]): int(xyxy[3]), int(xyxy[0]): int(xyxy[2])]
                    image = Image.fromarray(cv2.cvtColor(temp, cv2.COLOR_BGR2RGB))
                    flag = 0 if correct(image) else 1
                    acc += 1 if flag == 0 else 0
                    total += 1

                im0 = plot_one_box(xyxy, im0, label=label[flag], color=colors[flag], line_thickness=1)
    print('Done. (%.3fs)' % (time.time() - t0))
    with open('log.txt', mode='a+', encoding='utf-8') as f:
        f.write(f'user: {uid}, origin: {pid}, judge_id: {jid}, acc: {acc / total * 100:.2f}%\n')
    return im0

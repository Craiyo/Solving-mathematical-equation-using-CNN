from keras.models import model_from_json
import cv2
import numpy as np

json_file = open('math.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("math.h5")


def predication(path):
    train_data = []
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 1)
    dilation = cv2.dilate(img,kernel,iterations = 1)
    img = dilation
    if img is not None:
        # images.append(img)
        img = ~img
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        ctrs, ret = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w = int(28)
        h = int(28)
        train_data = []
        # print(len(cnt))
        rects = []
        for c in cnt:
            x, y, w, h = cv2.boundingRect(c)
            rect = [x, y, w, h]
            rects.append(rect)
        # print(rects)
        bool_rect = []
        for r in rects:
            l = []
            for rec in rects:
                flag = 0
                if rec != r:
                    if r[0] < (rec[0] + rec[2] + 10) and rec[0] < (r[0] + r[2] + 10) and r[1] < (
                            rec[1] + rec[3] + 10) and \
                            rec[1] < (r[1] + r[3] + 10):
                        flag = 1
                    l.append(flag)
                if rec == r:
                    l.append(0)
            bool_rect.append(l)
        # print(bool_rect)
        dump_rect = []
        for i in range(0, len(cnt)):
            for j in range(0, len(cnt)):
                if bool_rect[i][j] == 1:
                    area1 = rects[i][2] * rects[i][3]
                    area2 = rects[j][2] * rects[j][3]
                    if area1 == min(area1, area2):
                        dump_rect.append(rects[i])
        # print(len(dump_rect))
        final_rect = [i for i in rects if i not in dump_rect]
        # print(final_rect)
        for r in final_rect:
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            im_crop = thresh[y:y + h + 10, x:x + w + 10]

            im_resize = cv2.resize(im_crop, (28, 28))

            im_resize = np.reshape(im_resize, (28, 28, 1))
            train_data.append(im_resize)

    s = ''
    lis = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', '+', '*']

    for i in range(len(train_data)):
        train_data[i] = np.array(train_data[i])
        train_data[i] = train_data[i].reshape(1, 28, 28, 1)
        result = np.argmax(loaded_model.predict(train_data[i]))
        s = s + lis[result]

    return s
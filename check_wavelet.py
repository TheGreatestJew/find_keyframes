import cv2
import os
import imagehash
from PIL import Image
import time

start_time = time.time()
# Read the video from specified path
cam = cv2.VideoCapture("D:\\pycharm_projects\\find_keyframes\\vid.mp4")
try:

    # creating a folder named data
    if not os.path.exists('data1'):
        os.makedirs('data1')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

try:

    # creating a folder named data
    if not os.path.exists('data_key_wavelet'):
        os.makedirs('data_key_wavelet')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0

while (True):

    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        print('#-------------------------------------#')
        name_curr = './data1/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name_curr)

        # writing the extracted images
        cv2.imwrite(name_curr, frame)
        # average hash
        # wavelet hashing
        time7 = time.time()
        wavelet_Hash_curr = imagehash.whash(Image.open(name_curr))
        time8 = time.time()
        print('wavelet hash: ' + str(wavelet_Hash_curr))
        print("%s seconds " % (time8 - time7))

        # start to put current hashes in a list
        currentframe_configs = str(wavelet_Hash_curr)
        print('configs for current frame' + name_curr)
        print(currentframe_configs)
        if currentframe >= 1:
            prevframe = currentframe - 1
            name_prev = './data1/frame' + str(prevframe) + '.jpg'
            wavelet_Hash_prev = imagehash.whash(Image.open(name_prev))
            # start to put previous hashes in a list
            print('configs for previous frame' + name_prev)
            prevframe_configs = str(wavelet_Hash_prev)

            print(prevframe_configs)

            # difference between current frame and previous one
            Hash_subtraction = str(wavelet_Hash_curr - wavelet_Hash_prev)

            print('HASH: difference between current frame and previous frame: ')
            print(Hash_subtraction)


            # Get keyframes in a folder
            if (wavelet_Hash_curr - wavelet_Hash_prev) >= 25:
                print('key frame is:' + str(currentframe))
                name_key = './data_key_wavelet/frame' + str(currentframe) + '.jpg'
                print('Creating...' + name_key)
                # writing the extracted images
                cv2.imwrite(name_key, frame)
        currentframe += 1
        print('#-------------------------------------#')
    else:
        break
print(cam.get(cv2.CAP_PROP_FRAME_COUNT))
fps_amount = cam.get(cv2.CAP_PROP_FRAME_COUNT)
print(cam.get(cv2.CAP_PROP_FPS))
exec_time = (time.time() - start_time)
print("--- %s seconds ---" % exec_time)
average_time_per_oper = exec_time / fps_amount
print("--- %s seconds ---" % average_time_per_oper)
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
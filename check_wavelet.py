import cv2
import os
import imagehash
from PIL import Image
import time
from matplotlib import pyplot as plt
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
wavelet_subtraction = '0'
Hash_wavelet = []
Hash_wavelet.append(wavelet_subtraction)
counter_of_curr_frames = []
time_of_oper = 0
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
        time_of_oper += (time8 - time7)
        print(" %s seconds " % time_of_oper)

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
            wavelet_subtraction = str(wavelet_Hash_curr - wavelet_Hash_prev)
            Hash_wavelet.append(wavelet_subtraction)

            print('HASH: difference between current frame and previous frame: ')
            print(Hash_subtraction)


            # Get keyframes in a folder
            if (wavelet_Hash_curr - wavelet_Hash_prev) >= 25:
                print('key frame is:' + str(currentframe))
                name_key = './data_key_wavelet/frame' + str(currentframe) + '.jpg'
                print('Creating...' + name_key)
                # writing the extracted images
                cv2.imwrite(name_key, frame)
        counter_of_curr_frames.append(currentframe)
        currentframe += 1
        print('#-------------------------------------#')
    else:
        break
print(cam.get(cv2.CAP_PROP_FRAME_COUNT))
fps_amount = cam.get(cv2.CAP_PROP_FRAME_COUNT)
print(cam.get(cv2.CAP_PROP_FPS))
exec_time = (time.time() - start_time)
print("--- %s seconds ---" % exec_time)
average_time_per_oper = time_of_oper/fps_amount
print("---average time per operation: %s seconds ---" % average_time_per_oper)
plt.plot(counter_of_curr_frames, Hash_wavelet, label='wavelet Hash')
plt.xlabel("Frames")
plt.ylabel("Wavelet Hash substracted values")
plt.legend()
plt.show()
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
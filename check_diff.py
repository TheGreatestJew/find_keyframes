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
        os.makedirs('ddata1')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

try:

    # creating a folder named data
    if not os.path.exists('data_key_diff'):
        os.makedirs('data_key_diff')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0
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
        # difference hashing
        time5 = time.time()
        diffHash_curr = imagehash.dhash(Image.open(name_curr))
        time6 = time.time()
        print('difference hash: ' + str(diffHash_curr))
        time_of_oper += (time6 - time5)
        print(" %s seconds " % time_of_oper)

        # start to put current hashes in a list
        currentframe_configs = str(diffHash_curr)
        print('configs for current frame' + name_curr)
        print(currentframe_configs)
        if currentframe >= 1:
            prevframe = currentframe - 1
            name_prev = './data1/frame' + str(prevframe) + '.jpg'
            diffHash_prev = imagehash.dhash(Image.open(name_prev))
            # start to put previous hashes in a list
            print('configs for previous frame' + name_prev)
            prevframe_configs = str(diffHash_prev)

            print(prevframe_configs)

            # difference between current frame and previous one
            Hash_subtraction = str(diffHash_curr - diffHash_prev)

            print('HASH: difference between current frame and previous frame: ')
            print(Hash_subtraction)


            # Get keyframes in a folder
            if (diffHash_curr - diffHash_prev) >= 25:
                print('key frame is:' + str(currentframe))
                name_key = './data_key_diff/frame' + str(currentframe) + '.jpg'
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
average_time_per_oper = time_of_oper/fps_amount
print("---average time per operation: %s seconds ---" % average_time_per_oper)
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
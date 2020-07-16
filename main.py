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
    if not os.path.exists('data_key1'):
        os.makedirs('data_key1')

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
        #average hash
        time1 = time.time()
        aver_Hash_curr = imagehash.average_hash(Image.open(name_curr))
        time2 = time.time()
        print('average hash: ' + str(aver_Hash_curr))
        print(" %s seconds " % (time2 - time1))
        #perception hash
        time3 = time.time()
        percep_Hash_curr = imagehash.phash(Image.open(name_curr))
        time4 = time.time()
        print('perception hash: ' + str(percep_Hash_curr))
        print(" %s seconds " % (time4 - time3))
        # difference hashing
        time5 = time.time()
        diffHash_curr = imagehash.dhash(Image.open(name_curr))
        time6 = time.time()
        print('difference hash: ' + str(diffHash_curr))
        print(" %s seconds " % (time6 - time5))
        #wavelet hashing
        time7= time.time()
        wavelet_Hash_curr = imagehash.whash(Image.open(name_curr))
        time8 = time.time()
        print('wavelet hash: ' + str(wavelet_Hash_curr))
        print("%s seconds " % (time8 - time7))


        #start to put current hashes in a list
        currentframe_configs = [str(aver_Hash_curr),
                                str(percep_Hash_curr),
                                str(diffHash_curr),
                                str(wavelet_Hash_curr)]
        print('configs for current frame' + name_curr)
        print (currentframe_configs)
        if currentframe >= 1:
            prevframe = currentframe - 1
            name_prev = './data1/frame' + str(prevframe) + '.jpg'
            aver_Hash_prev = imagehash.average_hash(Image.open(name_prev))
            # perception hash
            percep_Hash_prev = imagehash.phash(Image.open(name_prev))
            # difference hashing
            diffHash_prev = imagehash.dhash(Image.open(name_prev))
            # wavelet hashing
            wavelet_Hash_prev = imagehash.whash(Image.open(name_prev))
            # start to put previous hashes in a list
            print('configs for previous frame' + name_prev)
            prevframe_configs = [str(aver_Hash_prev),
                                 str(percep_Hash_prev),
                                 str(diffHash_prev),
                                 str(wavelet_Hash_prev)]
            print(prevframe_configs)
            print('\n')
            #difference between current frame and previous one
            Hash_subtraction = [str(aver_Hash_curr - aver_Hash_prev),
                                str(percep_Hash_curr - percep_Hash_prev),
                                str(diffHash_curr - diffHash_prev),
                                str(wavelet_Hash_curr - wavelet_Hash_prev)]
            print('HASH: difference between current frame and previous frame: ')
            print(Hash_subtraction)
            print('\n')

            #Get keyframes in a folder
            if (wavelet_Hash_curr - wavelet_Hash_prev) >= 25:
                print('key frame is:' + str(currentframe))
                name_key = './data_key1/frame' + str(currentframe) + '.jpg'
                print('Creating...' + name_key)
                # writing the extracted images
                cv2.imwrite(name_key, frame)
        currentframe += 1
        print('#-------------------------------------#')
    else:
        break
print(cam.get(cv2.CAP_PROP_FRAME_COUNT))
print(cam.get(cv2.CAP_PROP_FPS))
print("--- %s seconds ---" % (time.time() - start_time))
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
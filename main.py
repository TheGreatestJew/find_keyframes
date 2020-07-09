import cv2
import os
import imagehash
from PIL import Image
# Read the video from specified path
cam = cv2.VideoCapture("D:\\pycharm_projects\\find_keyframes\\vid2.mp4")
try:

    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

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
        name_curr = './data/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name_curr)

        # writing the extracted images
        cv2.imwrite(name_curr, frame)
        #shannon_entropy(data.camera())
        #average hash
        aver_Hash_curr = imagehash.average_hash(Image.open(name_curr))
        print('average hash: ' + str(aver_Hash_curr))
        #perception hash
        percep_Hash_curr = imagehash.phash(Image.open(name_curr))
        print('perception hash: ' + str(percep_Hash_curr))
        # difference hashing
        diffHash_curr = imagehash.dhash(Image.open(name_curr))
        print('difference hash: ' + str(diffHash_curr))
        #wavelet hashing
        wavelet_Hash_curr = imagehash.whash(Image.open(name_curr))
        print('wavelet hash: ' + str(wavelet_Hash_curr))


        #start to put current hashes in a list
        currentframe_configs = [str(aver_Hash_curr),
                                str(percep_Hash_curr),
                                str(diffHash_curr),
                                str(wavelet_Hash_curr)]
        print('configs for current frame' + name_curr)
        print (currentframe_configs)
        if currentframe >= 1:
            prevframe = currentframe - 1
            name_prev = './data/frame' + str(prevframe) + '.jpg'
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
            #The most optimal image hash algorithm is wavelet_hash, according to observation of hash's output
            if (wavelet_Hash_curr - wavelet_Hash_prev) > 11:
                print('key frame is:' + str(currentframe))
        currentframe += 1
        print('#-------------------------------------#')
    else:
        break
print(cam.get(cv2.CAP_PROP_FRAME_COUNT))
print(cam.get(cv2.CAP_PROP_FPS))
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
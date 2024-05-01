import os
import cv2
import imagehash
from PIL import Image
import time
from matplotlib import pyplot as plt
start_time = time.time()
# Read the video from specified path
cam = cv2.VideoCapture("C:\\Users\\tishc\\Desktop\\keyframes\\find_keyframes\\Darling.mp4")
try:

    # creating a folder named data
    if not os.path.exists('data_dar'):
        os.makedirs('data_dar')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

try:

    # creating a folder named data
    if not os.path.exists('data_key_aver'):
        os.makedirs('data_key_aver')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')



# frame
currentframe = 0
aver_subtraction = '0'
Hash_aver = []
Hash_aver.append(aver_subtraction)
counter_of_curr_frames = []
time_of_oper = 0
while (True):

    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        print('#-------------------------------------#')
        name_curr = './data_dar/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name_curr)

        # writing the extracted images
        cv2.imwrite(name_curr, frame)
        #average hash
        time1 = time.time()
        aver_Hash_curr = imagehash.average_hash(Image.open(name_curr))
        time2 = time.time()
        print('average hash: ' + str(aver_Hash_curr))
        time_of_oper += (time2 - time1)
        print(" %s seconds " % time_of_oper)



        #start to put current hashes in a list
        currentframe_configs = str(aver_Hash_curr)
        print('configs for current frame' + name_curr)
        print (currentframe_configs)
        if currentframe >= 1:
            prevframe = currentframe - 1
            name_prev = './data_dar/frame' + str(prevframe) + '.jpg'
            aver_Hash_prev = imagehash.average_hash(Image.open(name_prev))
            # start to put previous hashes in a list
            print('configs for previous frame' + name_prev)
            prevframe_configs = str(aver_Hash_prev)

            print(prevframe_configs)
            #difference between current frame and previous one
            Hash_subtraction = str(aver_Hash_curr - aver_Hash_prev)
            aver_subtraction = str(aver_Hash_curr - aver_Hash_prev)
            Hash_aver.append(aver_subtraction)

            print('HASH: difference between current frame and previous frame: ')
            print(Hash_subtraction)

            #Get keyframes in a folder
            if (aver_Hash_curr - aver_Hash_prev) >= 25:
                print('key frame is:' + str(currentframe))
                name_key = './data_key_aver/frame' + str(currentframe) + '.jpg'
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
plt.plot(counter_of_curr_frames, Hash_aver, label='average Hash')
plt.xlabel("Frames")
plt.ylabel(" Average Hash substracted values")
plt.legend()
plt.show()
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
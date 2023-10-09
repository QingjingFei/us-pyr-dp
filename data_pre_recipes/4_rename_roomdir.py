import os, cv2, time
import shutil
import numpy as np

start = time.time()
old_path1 = r'png_rename (2)\png_rename'
new_path1 = r'png_rename (2)\png_renew'

try:
    shutil.rmtree(new_path1)
except:
    os.makedirs(new_path1)

for file1 in os.listdir(old_path1):
    old_path2 = os.path.join(old_path1, file1)
    new_path2 = os.path.join(new_path1, file1)
    
    for file2 in os.listdir(old_path2):
        surgery = file2 if file2.endswith('m') else file2.split('room')[0] + 'room'
        old_path3 = os.path.join(old_path2, file2)
        print(old_path3)

        for file3 in os.listdir(old_path3):
            old_path4 = os.path.join(old_path3, file3)
            new_file = surgery + '_' + file3
            new_path3 = os.path.join(new_path2, new_file)
            os.makedirs(new_path3)
            for file4 in os.listdir(old_path4):
                img_mask = cv2.imdecode(np.fromfile(os.path.join(old_path4, file4), dtype=np.uint8), -1)  # BGR
                cv2.imencode('.png', img_mask)[1].tofile(os.path.join(new_path3, file4))  # BGR

print('done')
print('time = ', time.time()-start)
import os
import shutil


if __name__ == '__main__':
    
    mask_path = r'./DOING/20230605_dcm'
    origin_path = r'./DOING/20230605_png'


    cnt = 0
    for roomDir in sorted(os.listdir(origin_path)):
        if roomDir.startswith('.'):
            continue
        # maskRdir = os.path.join(mask_path, 'y' + roomDir)
        maskRdir = os.path.join(mask_path, roomDir)
        originRdir = os.path.join(origin_path, roomDir)
        # completeRdir = os.path.join(complete_path, roomDir)
        for patientDir in sorted(os.listdir(originRdir)):
            if patientDir.startswith('.'):
                continue
            maskPdir = os.path.join(maskRdir, patientDir)
            originPdir = os.path.join(originRdir, patientDir)
            # completePdir = os.path.join(completeRdir, patientDir)
            for file in sorted(os.listdir(originPdir)):
                if file.startswith('.'):
                    continue
                file = os.path.splitext(file)[0] + '.png'
                if not os.path.exists(os.path.join(maskPdir, file)):
                    print('File %s does not exitst!' % os.path.join(maskPdir, file))
                cnt +=1
                # else:
                #     print('File %s already exists!' % os.path.join(maskPdir, file))
    print('Totally %d files!' % cnt)
    print('All Done!!!')
                    


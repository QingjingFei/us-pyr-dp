import os
import re
import shutil
import pandas as pd


def parse_info(patient_dir):
    fields = os.path.basename(patient_dir).split('_')
    ga = fields[1]
    return {'GA': ga}

def gen_dataset(src_folder, dst_folder):
    pid, idx, idxFalse = 0, 0, 0

    for roomDir in sorted(os.listdir(src_folder)):
        if roomDir.startswith('.'):
            continue
        
        srcRdir = os.path.join(src_folder, roomDir)
        for patientDir in sorted(os.listdir(srcRdir)):
            if patientDir.startswith('.'):
                continue

            srcPdir = os.path.join(srcRdir, patientDir)
            pid += 1
            for file in sorted(os.listdir(srcPdir)):
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(srcPdir, file)

                ga = parse_info(srcPdir)['GA']

                try:
                    matchObj = re.match('(\d{2})w(\d)d', ga)
                    week = int(matchObj.group(1))
                    day = int(matchObj.group(2))
                except AttributeError:
                    print(ga)

                if week < 22 or week > 41:
                    idxFalse += 1
                    print('ERROR!!!!!')
                    print('%s: GA out of index! ' % file_path)
                    continue
                if week <= 41 and day <= 6:
                    idx += 1
                    ga = round(week+day/7, 2)
                    file = str(idx) + '_' + str(pid) + '_' + str(ga) + '.png'
                    dst_path = os.path.join(dst_folder, file)
                    shutil.copyfile(file_path, dst_path)
    print('%d imgs in the GA range.' % idx)
    print('%d imgs out of the GA range.' % idxFalse)



if __name__ == '__main__':
    src_folder = r'/data/US-Image/fetal_lungs_png_origin_hz_980x735'
    dst_folder = r'../ExcludeData/dataset_origin_ga'
    
    # make sure that dst_folder is empty.
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)
    os.makedirs(dst_folder)

    gen_dataset(src_folder, dst_folder)
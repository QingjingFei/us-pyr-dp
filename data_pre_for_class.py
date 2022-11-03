import os
import re
import shutil
import pandas as pd


def parse_info(patient_dir):
    fields = os.path.basename(patient_dir).split('_')
    ga = fields[1]
    return {'GA': ga}

def gen_dataset(src_folder, dst_folder):
    idx = 0
    classes = []

    for roomDir in sorted(os.listdir(src_folder)):
        if roomDir.startswith('.'):
            continue
        
        srcRdir = os.path.join(src_folder, roomDir)
        for patientDir in sorted(os.listdir(srcRdir)):
            if patientDir.startswith('.'):
                continue

            srcPdir = os.path.join(srcRdir, patientDir)
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
                idx += 1

                if week <= 29 and day <= 6:
                    classes.append(0)
                elif week <= 36 and day <= 6:
                    classes.append(1)
                elif week <= 41 and day <= 6:
                    classes.append(2)
                else:
                    print('ERROR!!!!!')
                    print('%s: GA out of index! ' % file_path)
                dst_path = os.path.join(dst_folder, str(idx) + '.png')
                shutil.copyfile(file_path, dst_path)
    pngs = [str(i+1) + '.png' for i in range(idx)]
    df = pd.DataFrame({'US_png': pngs, 'Class': classes})
    df.to_csv(r'./us_GA.csv', index=False)
    
    return df



                


if __name__ == '__main__':
    src_folder = r'/data/US-Image/masked_data'
    dst_folder = r'./dataset'

    gen_dataset(src_folder, dst_folder)
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
    classes, pngs = [], []
    
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
                
                # GA classification
                if week < 20 or week > 41:
                    idxFalse += 1
                    print('ERROR!!!!!')
                    print('%s: GA out of index! ' % file_path)
                    continue
                elif week <= 29 and day <= 6:   # 20w0d-29w6d
                    classes.append(0)
                elif week <= 36 and day <= 6:   # 30w0d-36w6d
                    classes.append(1)
                else:                           # 37w0d-41w6d
                    classes.append(2)
                idx += 1
                filename = str(idx) + '_' + str(pid) + '_' + str(ga) + '.png'
                pngs.append(filename)
                dst_path = os.path.join(dst_folder, filename)
                shutil.copyfile(file_path, dst_path)

    df = pd.DataFrame({'US_png': pngs, 'Class': classes})
    
    return df


if __name__ == '__main__':
    src_folder = r'/data/US-Image/masked_data_980x735,665'
    dst_folder = r'ExcludeData/dataset_masked,665'
    
    # make sure that dst_folder is empty.
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)
    os.makedirs(dst_folder)

    df = gen_dataset(src_folder, dst_folder)
    df.to_csv(r'ExcludeData/GA_class,665.csv', index=False)
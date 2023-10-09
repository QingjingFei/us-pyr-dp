import easyocr, re, cv2, os, shutil
import numpy as np
from PIL import Image


def readfile(jpg_path, des_png_path):
    wrong_list = []
    num = 0
    last_name = ''
    last_week = ''

    for patientdir in sorted(os.listdir(jpg_path)):
        patient_jpg_dir = os.path.join(jpg_path, patientdir)
        info_list = patientdir.split('_')
        
        for jpg_file in sorted(os.listdir(patient_jpg_dir)):
            file_name, ext = os.path.splitext(jpg_file)
            num += 1
            print(f"正在处理第{num}个文件: {os.path.join(patient_jpg_dir, jpg_file)}")
            try:
                img = cv2.imdecode(np.fromfile(os.path.join(patient_jpg_dir, jpg_file), dtype=np.uint8), -1)
            except cv2.error as e:
                print("Error!!!!!!!!!!!!!!!!!!!!!  该文件可能存在问题，读取失败！")
                os.remove(os.path.join(patient_jpg_dir, jpg_file))
                wrong_list.append(os.path.join(patient_jpg_dir, jpg_file))
                continue
            result = recognition(img)
            room, patient, week, hz, year, hour = match(result, info_list)
            # print('\nname:', patient, '\ntime:', year + hour, '\nhz:', hz, '\nweek:', week)
            new_png_file = file_name + ',' + hz + '.png'
            new_folder = f'{room}_{patient}_{week}_{year}{hour}'
            
            if patient != last_name or week != last_week:
                new_path = os.path.join(des_png_path, new_folder)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
            
            jpg = Image.open(os.path.join(patient_jpg_dir, jpg_file))
            jpg.save(os.path.join(new_path, new_png_file))
            last_name = patient
            last_week = week
            
    print('已删除以下存在问题的文件：')   
    for _ in wrong_list:
        print(_)        
    # print(f'Debug --------------- {jpg_path} 文件夹处理完毕！')
                

def recognition(img):
    reader = easyocr.Reader(['en'], gpu=True)
    return reader.readtext(img)

def match(result, info_list):
    room, patient, week, hz, year, hour = '', '', '', '', '', ''
    room = re.search(r'\d+', info_list[1]).group() + 'room'
    patientCHN = info_list[2]
    # try:
    #     patient = re.search(r'([a-zA-Z ]{2,}{[2-5]\d}?)F?', folder).group(1).upper().strip()
    # except AttributeError:
    #     matched = re.search(r'([a-zA-Z ]{2,})-?[Ff]?-?([2-5]\d)[FfYy]?', folder)
    #     patient = matched.group(1).upper().strip() + matched.group(2)
    for out in result:
        age_x = re.search(r'([a-zA-Z]{2,} ?)-?[Ff]?-?([2-5SZ][\dbIlOoSsZ])[Ff]?|([a-zA-Z]{2,} ?)-?[Ff]?-?([2-5SZ][\dbIlOoSsZ])[Yy]?$', out[1])
        if age_x and bool(re.search(r'FR', age_x.group(1), re.IGNORECASE)):
            age_x = None
        year_x = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}$', out[1])
        hour_x = re.search(r'([012]\d\s*[:.]\s*\d{2})\s*[:.]\s*\d{2}$', out[1])
        hz_x = re.search(r'[\dbIlOoSsZA]{2,3}Hz', out[1])
        week_x = re.search(r'[\dbIlOoSsZ]{2}w[\dbIliOoSsZ]d', out[1])
        if age_x and patient == '':
            patient_name = patientCHN
            patient_age = age_x.group(2)
            patient_name = patient_name.replace('-', '')
            patient_age = patient_age.replace('b', '6')
            patient_age = patient_age.replace('I', '1')
            patient_age = patient_age.replace('l', '1')
            patient_age = patient_age.replace('O', '0')
            patient_age = patient_age.replace('o', '0')
            patient_age = patient_age.replace('S', '5')
            patient_age = patient_age.replace('s', '5')
            patient_age = patient_age.replace('Z', '2')
            patient = patient_name + patient_age
        if year_x:
            year = re.sub(r'[-/]', '', year_x.group(0))
        if hour_x:
            hour = re.sub(r'[:.\s]', '', hour_x.group(1))
        if hz_x:
            hz = hz_x.group(0).replace('I', '1')
            hz = hz.replace('l', '1')
            hz = hz.replace('b', '6')
            hz = hz.replace('O', '0')
            hz = hz.replace('o', '0')
            hz = hz.replace('S', '5')
            hz = hz.replace('s', '5')
            hz = hz.replace('Z', '7')
            hz = hz.replace('A', '4')
        if week_x:
            week = week_x.group(0).replace('I', '1')
            week = week.replace('l', '1')
            week = week.replace('i', '1')
            week = week.replace('b', '6')
            week = week.replace('O', '0')
            week = week.replace('o', '0')
            week = week.replace('S', '5')
            week = week.replace('s', '5')
            week = week.replace('Z', '2')
    
    if patient == '':
        patient =  patientCHN
    return room, patient, week, hz, year, hour

if __name__ == '__main__':
    jpg_path = r'./DOING/6.28处理'
    des_png_path = r'./DOING/6.28处理_rename__'
    readfile(jpg_path, des_png_path)
    print('All missions have finished.')
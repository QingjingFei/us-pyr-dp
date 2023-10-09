import easyocr, re, cv2, os, shutil
import numpy as np

def readfile(png_path, dcm_path, des_png_path, des_dcm_path):
    # wrong_list = []
    num = 0
    last_name = ''
    last_week = 0

    for patientdir in sorted(os.listdir(png_path)):
        patient_png_dir = os.path.join(png_path, patientdir)
        patient_dcm_dir = os.path.join(dcm_path, patientdir)
        for child in sorted(os.listdir(patient_png_dir)):
            cwd_png_dir = os.path.join(patient_png_dir, child)
            cwd_dcm_dir = os.path.join(patient_dcm_dir, child)
            while os.path.isdir(cwd_png_dir):
                current_png_path = os.path.join(cwd_png_dir, sorted(os.listdir(cwd_png_dir))[0])
                current_dcm_path = os.path.join(cwd_dcm_dir, sorted(os.listdir(cwd_dcm_dir))[0])
                cwd_png_dir = current_png_path
                cwd_dcm_dir = current_dcm_path
            png_dir = os.path.dirname(cwd_png_dir)
            dcm_dir = os.path.dirname(cwd_dcm_dir)
            for dcm_file in sorted(os.listdir(dcm_dir)):
                dcm_name, ext = os.path.splitext(dcm_file)
                png_file = dcm_name + '.png'
                num += 1
                print(f"正在处理第{num}个文件: {os.path.join(png_dir, png_file)}")

                img = cv2.imdecode(np.fromfile(os.path.join(png_dir, png_file), dtype=np.uint8), -1)
                result = recognition(img)
                patient, week, hz, year, hour = match(result, patientdir)
                # print('\nname:', patient, '\ntime:', year + hour, '\nhz:', hz, '\nweek:', week)
                new_png_file = dcm_name + ',' + hz + '.png'
                new_dcm_file = dcm_name + ',' + hz + '.dcm'
                new_folder = f'{patient}_{week}_{year}{hour}'
                if patient != last_name or week != last_week:
                    png_dir_rename = os.path.join(des_png_path, new_folder)
                    dcm_dir_rename = os.path.join(des_dcm_path, new_folder)
                    if not os.path.exists(png_dir_rename):
                        os.makedirs(png_dir_rename)
                    if not os.path.exists(dcm_dir_rename):
                        os.makedirs(dcm_dir_rename)
                shutil.copyfile(os.path.join(png_dir, png_file), os.path.join(png_dir_rename, new_png_file))
                shutil.copyfile(os.path.join(dcm_dir, dcm_file), os.path.join(dcm_dir_rename, new_dcm_file))
                last_name = patient
                last_week = week
            break
        # print(f'Debug --------------- {png_dir} 文件夹处理完毕！')
                

def recognition(img):
    reader = easyocr.Reader(['en'], gpu=True)
    return reader.readtext(img)

def match(result, folder):
    patient, week, hz, year, hour = '', '', '', '', ''
    try:
        patient = re.search(r'([a-zA-Z ]{2,}{[2-5]\d}?)F?', folder).group(1).upper().strip()
    except AttributeError:
        matched = re.search(r'([a-zA-Z ]{2,})-?[Ff]?-?([2-5]\d)[FfYy]?', folder)
        patient = matched.group(1).upper().strip() + matched.group(2)
    for out in result:
        name_x = re.search(r'([a-zA-Z ]{2,}-?[2-5][\dbIlOoSsZ])F?[^H][^z]', out[1])  # r'([a-zA-Z-]{2,}[2-5][\dIlOoS])F?[^Hh][^z]'
        year_x = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}$', out[1])
        hour_x = re.search(r'([012]\d\s*[:.]\s*\d{2})\s*[:.]\s*\d{2}$', out[1])
        hz_x = re.search(r'[\dbIlOoSsZA]{2}Hz', out[1])
        week_x = re.search(r'[\dbIlOoSsZ]{2}w[\dbIliOoSsZ]d', out[1])
        if name_x and patient == '':
            name_x = name_x.group(1).upper().strip()
            name_x = name_x.split(' ')[0]
            patient_name = name_x[:-2]
            patient_age = name_x[-2:]
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
            
    return patient, week, hz, year, hour

if __name__ == '__main__':
    png_path = r'./DOING/20230830_png__'
    dcm_path = r'./DOING/20230830_dcm__'
    des_png_path = r'./DOING/20230830_png_rename__'
    des_dcm_path = r'./DOING/20230830_dcm_rename__'
    readfile(png_path, dcm_path, des_png_path, des_dcm_path)
    print('All missions have finished.')
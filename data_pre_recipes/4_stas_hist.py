import os, re
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 负号

#%% 辅助函数
def hash(dict, temp):
    if temp not in dict:
            dict[temp] = 1
    else:
        dict[temp] += 1
    return dict

def sortdict(dict):
    sorted_keys = sorted(dict.keys())
    sorted_dict = {}
    for key in sorted_keys:
        sorted_dict[key] = dict[key]
    return sorted_dict

#%% 读取信息
file_path1 = r'E:\python program\fetal\20231008_summarize\png_rename (2)\png_renew'
save_path = r'E:\python program\fetal\20231008_summarize\figure'

gestationalage_dict, imagenumber_dict, consultingroom_dict, frequency_dict, maternalage_dict = {}, {}, {}, {}, {}
for file1 in os.listdir(file_path1):
    file_path2 = os.path.join(file_path1, file1)
    for file2 in os.listdir(file_path2):
        file_path3 = os.path.join(file_path2, file2)

        gestational_age = int(file2.split('_')[2].split('w')[0])  #胎龄
        gestationalage_dict = hash(gestationalage_dict, gestational_age)
        
        image_number = len(os.listdir(file_path3))  #一次超声检查的超声图像张数分布
        imagenumber_dict = hash(imagenumber_dict, image_number)

        consulting_room = file2.split('_')[0]  #设备（诊室）
        consultingroom_dict = hash(consultingroom_dict, consulting_room)

        maternal_age  = int(file2.split('_')[1][-2:])  #孕妇年龄
        maternalage_dict = hash(maternalage_dict, maternal_age)
        
        for file in os.listdir(file_path3):  #频率hz
            match = re.search(r'(\d+)Hz', file).group(1)
            frequency_dict = hash(frequency_dict, match)
      
print('胎龄:', gestationalage_dict, '\n', '图像张数:', imagenumber_dict, '\n', '诊室:', consultingroom_dict, '\n', '设备（频率）:', frequency_dict, '\n', '孕妇年龄:', maternalage_dict, '\n')

#%% 绘图

plt.figure()
plt.bar(gestationalage_dict.keys(), gestationalage_dict.values())
for key in gestationalage_dict.keys():
    plt.text(key, gestationalage_dict[key]+0.6, gestationalage_dict[key], fontsize = 12, style = 'italic', weight = 'light', horizontalalignment='center')
plt.title("胎龄分布", fontsize=18)
plt.xticks(list(gestationalage_dict.keys()))
plt.xlabel("weekends", fontsize=14)
plt.ylabel("amount", fontsize=14)
plt.grid(alpha=0.4, linestyle=':')
plt.savefig(os.path.join(save_path, 'gestational_age.png'))

plt.figure()
plt.bar(imagenumber_dict.keys(), imagenumber_dict.values())
for key in imagenumber_dict.keys():
    plt.text(key, imagenumber_dict[key]+0.6, imagenumber_dict[key], fontsize = 12, style = 'italic', weight = 'light', horizontalalignment='center')
plt.title("每个病人一次超声检查的超声图像张数分布", fontsize=14)
plt.xticks(list(imagenumber_dict.keys()))
plt.xlabel('Number of ultrasound images', fontsize=14)
plt.ylabel('amount', fontsize=14)
plt.grid(alpha=0.4, linestyle=':')
plt.savefig(os.path.join(save_path, 'image_number.png'))

plt.figure()
plt.bar(consultingroom_dict.keys(), consultingroom_dict.values())
for key in consultingroom_dict.keys():
    plt.text(key, consultingroom_dict[key]+0.6, consultingroom_dict[key], fontsize = 12, style = 'italic', weight = 'light', horizontalalignment='center')
plt.title("设备（诊室）分布", fontsize=18)
plt.xlabel("consulting room", fontsize=14)
plt.ylabel("amount", fontsize=14)
plt.grid(alpha=0.4, linestyle=':')
plt.savefig(os.path.join(save_path, 'consulting_room.png'))

plt.figure()
frequency_dict = sortdict(frequency_dict)
plt.bar(frequency_dict.keys(), frequency_dict.values())
for key in frequency_dict.keys():
    plt.text(key, frequency_dict[key]+0.6, frequency_dict[key], fontsize = 12, style = 'italic', weight = 'light', horizontalalignment='center')
plt.title("设备频率分布", fontsize=18)
plt.xlabel("Hz", fontsize=14)
plt.ylabel('amount', fontsize = 14)
plt.grid(alpha=0.4, linestyle=':')
plt.savefig(os.path.join(save_path, 'frequency.png'))

plt.figure()
plt.bar(maternalage_dict.keys(), maternalage_dict.values())
for key in maternalage_dict.keys():
    plt.text(key, maternalage_dict[key]+0.6, maternalage_dict[key], fontsize = 12, style = 'italic', weight = 'light', horizontalalignment='center')
plt.title("孕妇年龄分布", fontsize=18)
plt.xlim((int(min(list(maternalage_dict.keys())))-1, int(max(list(maternalage_dict.keys())))+1))
plt.xticks(list(maternalage_dict.keys()))
plt.xlabel("age", fontsize=14)
plt.ylabel("amount", fontsize=14)
plt.grid(alpha=0.4, linestyle=':')
plt.savefig(os.path.join(save_path, 'maternal_age.png'))

# plt.show()

print('have done')
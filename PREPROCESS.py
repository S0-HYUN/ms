import pandas as pd

for i2 in range(13, 14):
    print("--- [ %d 데이터 ] ---"%(i2))
    if i2<10: # 파일 읽기 + '\n' 제거
        with open('C:\\Users\\soso\\Desktop\\data\\S0%d_DAY1_EXPT2_DRIVE.txt' % (i2), "r", encoding='utf-8') as f:
            original_data = f.read().splitlines()
    else:
        with open('C:\\Users\\soso\\Desktop\\data\\S%d_DAY1_EXPT2_DRIVE.txt' % (i2), "r",encoding='utf-8') as f:
            original_data = f.read().splitlines()

    original_data = original_data[4:]

    a = []
    for i in range(len(original_data)):
        b = original_data[i].replace(",", "").replace('"',"").split("\t")
        a.append(b[0:49])  # 한 row씩 list에 저장 (2차원 list)s, column 개수는 50개

    trigger_idx = []  # trigger가 있는 index 찾기 for 실험 시작과 끝 자르기
    for i in range(1, len(a)):  # 첫번째 행은 column이름들
        if a[i][48] != '': # trigger(digital) 까지의 column
            if float(a[i][48]) != 0.0:
                trigger_idx.append(i)
    print("trigger_idx: ", trigger_idx)

    clean_tab = pd.DataFrame(a, columns=a[0])
    cut_tab = clean_tab.loc[trigger_idx[0]: trigger_idx[-1]]
    print("length 변화: %d -> %d" % (len(clean_tab), len(cut_tab)))

    cut_tab = cut_tab[['Time (s)', 'Fp1(uV)', 'Fp2(uV)', 'AF3(uV)', 'AF4(uV)', 'F7(uV)', 'F8(uV)',
        'F3(uV)', 'Fz(uV)', 'F4(uV)', 'FC5(uV)', 'FC6(uV)', 'T7(uV)', 'T8(uV)',
        'C3(uV)', 'C4(uV)', 'CP5(uV)', 'CP6(uV)', 'P7(uV)', 'P8(uV)', 'P3(uV)',
        'Pz(uV)', 'P4(uV)', 'PO7(uV)', 'PO8(uV)', 'PO3(uV)', 'PO4(uV)', 'O1(uV)',
        'O2(uV)', 'ECG.(uV)', 'Resp.(Ω)', 'PPG(ADU)', 'GSR(Ω)', 'Packet Counter(DIGITAL)',
        'TRIGGER(DIGITAL)']]

    newdata = cut_tab.astype(float)  # 문자형을 float으로 변환

    start_idx = trigger_idx[0]  # 시작 9를 입력한 idx
    end_idx = trigger_idx[len(trigger_idx) - 1]  # 마지막 trigger을 입력한 idx
    trigger_mok_idx = [0] + [x // 30000 for x in trigger_idx[1:]]
    trigger = list(newdata[newdata.iloc[:, -1] != 0]["TRIGGER(DIGITAL)"])  # trigger
    print("Trigger: ", trigger)

    marker_row = list(range(0, trigger_mok_idx[-1] + 1))
    for i, j in enumerate(marker_row):
        if j not in trigger_mok_idx:
            trigger.insert(i, 0.0)
    trigger[0] = 0.0  # 첫번째 trigger를 0으로 변화
    print("변한 Trigger:", trigger)

    print(start_idx, end_idx)
    newdata.iloc[:, -1] = 0  # trigger를 모두 0을 초기화

    first_idx=list(range(0, end_idx-start_idx+1, 30000))
    for i in first_idx:
        print(i,i+30000-1,trigger[i//30000])
        if i // 30000 <= len(trigger) - 1:
            newdata.iloc[i:i + 30000 - 1, -1] = trigger[i//30000]  # trigger 삽입
        else:
            newdata.iloc[i :, -1] = trigger[i//30000]  # trigger 삽입

    # down sampling 250hZ
    idxs = list(range(start_idx, start_idx+len(newdata), 2))
    downsample_data = newdata.loc[idxs]

    if i2 < 10:
        downsample_data.to_csv("C:\\Users\\soso\\Desktop\\store\\S0%d_DAY1_EXPT2_DRIVE_preprocess.csv" % (i2), columns=newdata.columns)  # 저장
    else:
        downsample_data.to_csv("C:\\Users\\soso\\Desktop\\store\\S%d_DAY1_EXPT2_DRIVE_preprocess.csv" % (i2), columns=newdata.columns)  # 저장
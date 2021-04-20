import numpy as np
import pandas as pd
import mne
import matplotlib.pyplot as plt
import sklearn


def data_loading(path, subject_num, day, expt) :
  preprocessed_data=pd.read_csv(path + "S%d_DAY%d_EXPT%d_DRIVE_preprocess2.csv" %(subject_num, day, expt))
  #preprocessed_data=preprocessed_data.drop(["Unnamed: 0"],axis=1) # preprocess 다시 돌려서 나온 데이터 사용시 이부분 제거
  eeg_data = preprocessed_data.drop(["Time (s)", "Packet Counter(DIGITAL)","ECG.(uV)","Resp.(Ω)",   "PPG(ADU)",   "GSR(Ω)","Packet Counter(DIGITAL)","TRIGGER(DIGITAL)"], axis=1) # time이랑 packet counter column 제거
  eeg_col_names = list(preprocessed_data.columns)  # list로
  return preprocessed_data, eeg_data, eeg_col_names # name에는 time이 포함되어 있음

def create_array(dfdata, col_names, fs, ch_types, scale = 1) : 
  info = mne.create_info(ch_names = col_names, sfreq = fs, ch_types = ch_types)
  temp = dfdata.values
  temp = temp.T * scale
  s_array = mne.io.RawArray(temp, info)
  return s_array

def bandpass_filter(arrdata, preprocessed_data) :
  filtered_data = arrdata.filter(l_freq = 1., h_freq=50.,  picks='eeg', fir_design='firwin', skip_by_annotation='edge')
  
  filtered_df = filtered_data.to_data_frame() # filtered_df : filtering한 후, 전체 변수 다 있으면서 데이터프레임 형식. (time include)
  filtered_df['Time (s)'] = preprocessed_data['Time (s)']
  filtered_df = filtered_df.drop(['time'], axis = 1) # 자동으로 생기는 time변수 제거
  
  filtered_df_trigger = filtered_df.copy()
  filtered_df_trigger['TRIGGER(DIGITAL)'] = preprocessed_data['TRIGGER(DIGITAL)']
  return filtered_data, filtered_df, filtered_df_trigger
  
def show_plot(arrdata) :
  arrdata.plot()
  plt.show()


data_path = "C:\\Users\\soso\\Desktop\\store\\" # 데이터 경로 설정
subject_num = 13 # 피험자 번호
day = 1  # 1/2 
expt = 2 # 1/2 
preprocessed_data, eeg_data, eeg_col_names = data_loading(data_path, subject_num, day, expt)
fs = 250 # freq 250hZ 설정

ch_names = ["Fp1","Fp2","AF3","AF4","F7","F8","F3","Fz","F4","FC5",
            "FC6","T7","T8","C3","C4","CP5","CP6","P7","P8","P3","Pz",
            "P4","PO7","PO8","PO3","PO4","O1","O2"] # 채널 이름 설정
ch_types = ["eeg"] * 28
s_array = create_array(eeg_data, ch_names, fs, ch_types, scale = (1e-6))
#show_plot(s_array)

montage = mne.channels.make_standard_montage("standard_1005")
s_array.set_montage(montage = montage)


filtered_arr, filter_df, filter_df_trigger = bandpass_filter(s_array, preprocessed_data)
show_plot(filtered_arr)
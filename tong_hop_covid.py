from crawler import Crawl
from extract import Extract

def check_number_patient(df):
    patient_code = df['Bệnh nhân'].apply(lambda x: int(x.replace('BN','')))
    patient_code = patient_code.values
    error = []
    for i in range(len(patient_code)-1):
        next_patient_code = patient_code[i] + 1
        if next_patient_code < patient_code[i+1]:
            e = 'Thiếu BN{} - BN{}'.format(next_patient_code, patient_code[i+1]-1)
            error.append(e)
        elif patient_code[i] == patient_code[i+1]:
            e = 'Thừa BN{}'.format(patient_code[i])
            error.append(e)
    print("Số lượng bệnh nhân đã tổng hợp:", len(patient_code))
    if len(error) == 0:
        print("Tổng hợp ĐỦ! happy for you")
    else:
        print("Tổng hợp LỖI:")
        for e in error:
            print(e)

if __name__ == "__main__":
    # Crawl dữ liệu trên trang của Bộ Y Tế
    results = Crawl(executable_path='./chromedriver').get_data_crawler()

    # Tổng hợp thông tin
    # df_covid_night = Extract(results[0]).extract_info()
    df_covid_lunch = Extract(results[1]).extract_info()
    df_covid_morning = Extract(results[2]).extract_info()

    # Kiểm tra lại thông tin
    # print("Tối")
    # check_number_patient(df_covid_night)
    print("tối 18 7")
    check_number_patient(df_covid_lunch)
    print("sáng 18 7")
    check_number_patient(df_covid_morning)

    # Xuất ra file excel
    # df_covid_night.to_excel('/home/huyphuong/Desktop/tong_hop_covid_sang1907.xlsx')
    df_covid_lunch.to_excel('/home/huyphuong/Desktop/tong_hop_covid_toi_1807.xlsx')
    df_covid_morning.to_excel('/home/huyphuong/Desktop/tong_hop_covid_sang_1807.xlsx')
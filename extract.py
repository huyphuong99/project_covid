import re
import pandas as pd

class Extract:
    def __init__(self, data, province):
        self.data = data
        self.province = province

    def extract_patient(self, desc):
        start_idx = re.search(r'[(][B][N]\d{4,8}', desc).start()
        end_idx = re.search(r'[B]{0,1}[N]{0,1}\d{4,8}[)]', desc).end()
        return desc[start_idx:end_idx]

    def get_patient(self, desc):
        extract = self.extract_patient(desc)
        patients = [patient.strip() for patient in extract[1:-1].split(',')]
        list_patient = []
        for patient in patients:
            if '-' in patient:
                start_patient = int(patient.split('-')[0][2:])
                end_patient = int(patient.split('-')[1][2:]) if patient.split('-')[1][:2] == 'BN' else int(patient.split('-')[1])
                for i in range(start_patient, end_patient + 1):
                    list_patient.append('BN{}'.format(i))
            else:
                list_patient.append(patient)
        return list_patient

    def extract_address(self, desc):
        if 'được cách ly ngay sau khi nhập cảnh' in desc:
            return 'Nhập cảnh'
        start_idx = desc.find('ghi nhận tại') + len('ghi nhận tại')
        end_idx = desc.find(':', start_idx) if desc.find(':', start_idx) != -1 else desc.find(',', start_idx)
        return ' '.join(desc[start_idx:end_idx].split()[1:])

    def extract_note(self, desc):
        if 'được cách ly ngay sau khi nhập cảnh' in desc:
            start_idx = desc.find('được cách ly ngay sau khi nhập cảnh')
        else:
            start_idx = desc.find('ghi nhận tại')
            start_idx = desc.find(':', start_idx) if desc.find(':', start_idx) != -1 else desc.find(',', start_idx)
            start_idx += 1
        return desc[start_idx:]

    def get_date(slef, time_line):
        return re.findall(r'\d{1,2}[/-]{1}\d{1,2}[/-]{1}\d{4}', str(time_line))

    def extract_date_positive(self, desc):
        start_idx = desc.find('Kết quả xét nghiệm ngày')
        end_idx = desc.find('.', start_idx)
        return self.get_date(desc[start_idx: end_idx])

    def extract_info_province(self):
        info = self.data["Content"][0].lower().split(",")
        res = {}
        for i in info:
            find_start = i.index("(")+1
            find_end = i.index(")")
            number = i[find_start: find_end]
            for p in self.province:
                index_i = i.find(p.lower())
                text = i[index_i: index_i + len(p)]
                if text == p.lower():
                    res[p] = number
                    break
        return res









    def extract_info(self):
        patient, public_date, positive_date, address, note = [], [], [], [], []
        for content in self.data['Content']:
            # Bệnh nhân
            n_patient = len(self.get_patient(content))
            patient += self.get_patient(content)
            # Địa chỉ
            address += [self.extract_address(content)]*n_patient
            # Ghi chú
            note += [self.extract_note(content)]*n_patient
            # Ngày dương tính
            po_date = self.extract_date_positive(content)
            if len(po_date) == 0:
                po_date = self.get_date(self.data['Time header'][0])
            positive_date += po_date*n_patient
        # Ngày công bố
        public_date = self.get_date(self.data['Time header'][0])*len(patient)
        return pd.DataFrame({'Bệnh nhân':patient, 'Ngày công bố': public_date, 'Ngày dương tính': positive_date, 'Địa điểm': address, 'Ghi chú': note}).sort_values(by=['Bệnh nhân'])

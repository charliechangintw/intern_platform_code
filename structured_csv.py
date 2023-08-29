import pandas as pd
import numpy as np
import re

def structure_csv(input_path):
    df_csv = pd.read_csv(input_path)

    output_df = pd.DataFrame(columns=['subject_id', 'name', 'unitNo'])

    for index, row in df_csv.iterrows():
        # 讀取檔案內容
        content = row['text']
        subject_id = row['subject_id']

        # 使用正則表達式，可以參考https://regex101.com/
        #--------------------------------------------------
        # 找name
        name = []
        matches = re.findall(r'Name\s*:\s*(\w+)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    name.append(['null'])
                else:
                    name.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            name.append(['null'])
        if not name:
            name = ['null']  
        # print("name =", name)
        #--------------------------------------------------
        #找unitNo
        unitNo = []
        matches = re.findall(r'Unit\s*No:\s*(\w+)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    unitNo.append(['null'])
                else:
                    unitNo.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            unitNo.append(['null'])
        if not unitNo:
            unitNo = ['null']  
        #--------------------------------------------------
        #找admissionDate
        admissionDate = []
        matches = re.findall(r'Admission\s*Date:\s*(\w+)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    admissionDate.append(['null'])
                else:
                    admissionDate.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            admissionDate.append(['null'])
        if not admissionDate:
            admissionDate = ['null']  
        #--------------------------------------------------
        #找dischargeDate
        dischargeDate = []
        matches = re.findall(r'Discharge\s*Date:\s*(\w+)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    dischargeDate.append(['null'])
                else:
                    dischargeDate.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            dischargeDate.append(['null'])
        if not dischargeDate:
            dischargeDate = ['null']  
        #--------------------------------------------------
        #找birth
        birth = []
        matches = re.findall(r'Date of Birth:\s*(\w+)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    birth.append(['null'])
                else:
                    birth.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            birth.append(['null'])
        if not birth:
            birth = ['null']  
        #--------------------------------------------------
        #找sex
        sex = []
        matches = re.findall(r'Sex:\s*(\w+)', content)
        # 將結果存儲到陣列中
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    sex.append(['null'])
                else:
                    sex.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            sex.append(['null'])
        if not sex:
            sex = ['null']    
        # print("sex =", sex)
        #--------------------------------------------------
        #找service
        service = []
        matches = re.findall(r'Service:\s*(\w+)', content)
        # 將結果存儲到陣列中
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    service.append(['null'])
                else:
                    service.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            service.append(['null'])
        if not service:
            service = ['null']
        #--------------------------------------------------
        #找allergies
        allergies = [] 
        matches = re.findall(r'Allergies:(.*?)Attending:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    allergies.append(['null'])
                else:
                    allergies.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            allergies.append(['null'])
        if not allergies:
            allergies = ['null']
        # print("allergies:", allergies)
        #--------------------------------------------------
        #找attending
        attending = []
        matches = re.findall(r'Attending:\s*(\w+)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    attending.append(['null'])
                else:
                    attending.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            attending.append(['null'])
        if not attending:
            attending = ['null']
        #--------------------------------------------------
        #找chiefComplaint
        chiefComplaint = []
        matches = re.findall(r'Chief\s*Complaint:\s*(.*)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    chiefComplaint.append(['null'])
                else:
                    chiefComplaint.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            chiefComplaint.append(['null'])
        if not chiefComplaint:
            chiefComplaint = ['null']
        #--------------------------------------------------
        #找majorSurgicalOrInvasiveProcedure
        procedure = []
        matches = re.findall(r'Major Surgical or Invasive Procedure:\s*(.*?)\s*(?:\n|$)', content)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    procedure.append(['null'])
                else:
                    procedure.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            procedure.append(['null'])
        if not procedure:
            procedure = ['null']
        # print("procedure =", procedure)
        #--------------------------------------------------
        #找historyOfPresentIllness 
        historyOfPresentIllness = [] 
        matches = re.findall(r'History of Present Illness:(.*?)Past Medical History:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    historyOfPresentIllness.append(['null'])
                else:
                    historyOfPresentIllness.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            historyOfPresentIllness.append(['null'])
        if not historyOfPresentIllness:
            historyOfPresentIllness = ['null']
                # print("historyOfPresentIllness =", historyOfPresentIllness)
        #--------------------------------------------------
        #找pastMedicalHistory
        pastMedicalHistory = [] 
        matches = re.findall(r'Past Medical History:(.*?)Social History:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    arrapastMedicalHistoryy.append(['null'])
                else:
                    # 這邊換行符號有替換成空格
                    pastMedicalHistory.append([re.sub(r'\n', ' ', match).strip('___ \n')])
        else :
            pastMedicalHistory.append(['null'])
        if not pastMedicalHistory:
            pastMedicalHistory = ['null']
        # print("pastMedicalHistory =", pastMedicalHistory)
        #--------------------------------------------------
        #找socialHistory
        socialHistory = [] 
        matches = re.findall(r'Social History:(.*?)Family History:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    socialHistory.append(['null'])
                else:
                    socialHistory.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            socialHistory.append(['null'])
        if not socialHistory:
            socialHistory = ['null']
        # print("socialHistory =", socialHistory)
        #--------------------------------------------------
        #找familyHistory
        familyHistory = [] 
        matches = re.findall(r'Family History:(.*?)Physical Exam:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    familyHistory.append(['null'])
                else:
                    familyHistory.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            familyHistory.append(['null'])
        if not familyHistory:
            familyHistory = ['null']
        # print("familyHistory =", familyHistory)
        #--------------------------------------------------
        #找physicalExam
        physicalExam = [] 
        matches = re.findall(r'Physical Exam:(.*?)Admission physical exam:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    physicalExam.append(['null'])
                else:
                    physicalExam.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            physicalExam.append(['null'])
        if not physicalExam:
            physicalExam = ['null']
        # print("physicalExam:", physicalExam)
        #--------------------------------------------------
        #找admissionPhysicalExam
        admissionPhysicalExam = [] 
        matches = re.findall(r'Admission physical exam:(.*?)Discharge Physical Exam:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    admissionPhysicalExam.append(['null'])
                else:
                    # 這邊換行符號有替換成空格
                    admissionPhysicalExam.append([re.sub(r'\n', ' ', match).strip('___ \n')])
        else :
            admissionPhysicalExam.append(['null'])
        if not admissionPhysicalExam:
            admissionPhysicalExam = ['null']
        # print("admissionPhysicalExam =", admissionPhysicalExam)
        #--------------------------------------------------
        #找dischargePhysicalExam
        dischargePhysicalExam = [] 
        matches = re.findall(r'Discharge Physical Exam:(.*?)Pertinent Results:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    dischargePhysicalExam.append(['null'])
                else:
                    #這邊換行符號有替換成空格
                    dischargePhysicalExam.append([re.sub(r'\n', ' ', match).strip('___ \n')])
        else :
            dischargePhysicalExam.append(['null'])
        if not dischargePhysicalExam:
            dischargePhysicalExam = ['null']
        # print("dischargePhysicalExam =",  dischargePhysicalExam)
        #--------------------------------------------------
        #找pertinentResults
        pertinentResults = [] 
        matches = re.findall(r'Pertinent Results:(.*?)Colonoscopy', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    pertinentResults.append(['null'])
                else:
                    pertinentResults.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            pertinentResults.append(['null'])
        if not pertinentResults:
            pertinentResults = ['null']
        # print("pertinentResults =",  pertinentResults)
        #--------------------------------------------------
        #找dischargeMedications * * * * * 
        dischargeMedications = [] 
        matches = re.findall(r'Discharge Medications:(.*?)Discharge Disposition:', content, re.DOTALL)
        if matches:
            for match in matches:
                medication_lines = [line.strip() for line in match.splitlines() if line.strip()]
                dischargeMedications.append(medication_lines)
        else:
            dischargeMedications.append(['null'])
        if not dischargeMedications:
            dischargeMedications = [['null']]
        # print("dischargeMedications", dischargeMedications)
        #--------------------------------------------------
        #找dischargeDisposition
        dischargeDisposition = [] 
        matches = re.findall(r'Discharge Disposition:(.*?)Discharge Diagnosis:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    dischargeDisposition.append(['null'])
                else:
                    dischargeDisposition.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            dischargeDisposition.append(['null'])
        if not dischargeDisposition:
            dischargeDisposition = ['null']
        # print("dischargeDisposition =", dischargeDisposition)
        #--------------------------------------------------
        #找dischargeDiagnosis
        dischargeDiagnosis = [] 
        matches = re.findall(r'Discharge Diagnosis:(.*?)Discharge Condition:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    dischargeDiagnosis.append(['null'])
                else:
                    #這邊換行符號有替換成空格
                    dischargeDiagnosis.append([re.sub(r'\n', ' ', match).strip('___ \n')])
        else :
            dischargeDiagnosis.append(['null'])
        if not dischargeDiagnosis:
            dischargeDiagnosis = ['null']
        # print("dischargeDiagnosis =", dischargeDiagnosis)
        #--------------------------------------------------
        #找dischargeCondition
        dischargeCondition = [] 
        matches = re.findall(r'Discharge Condition:(.*?)Discharge Instructions:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    array.append(['null'])
                else:
                    dischargeCondition.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            dischargeCondition.append(['null'])
        if not dischargeCondition:
            dischargeCondition = ['null']
        # print("dischargeCondition =", dischargeCondition)
        #--------------------------------------------------
        #找dischargeInstructions
        dischargeInstructions = [] 
        matches = re.findall(r'Discharge Instructions:(.*?)Followup Instructions:', content, re.DOTALL)
        if matches:
            for match in matches:
                if match.strip() == "___" or match.strip() == "None." or match.strip() == "":
                    dischargeInstructions.append(['null'])
                else:
                    dischargeInstructions.append([re.sub(r'\n', '', match).strip('___ \n')])
        else :
            dischargeInstructions.append(['null'])
        if not dischargeInstructions:
            dischargeInstructions = ['null']
        # print("dischargeInstructions =", dischargeInstructions)
        #-------------------------------------------------- 

        #以表格的形式輸出
        data = {
            'subject_id': subject_id,
            'name': name,
            'unitNo': unitNo,
            'admissionDate': admissionDate,
            'dischargeDate': dischargeDate,
            'birth': birth,
            'sex': sex,
            'service': service,
            'allergies': allergies,
            'attending': attending,
            'chiefComplaint': chiefComplaint,
            'procedure': procedure,
            'historyOfPresentIllness': historyOfPresentIllness,
            'pastMedicalHistory': pastMedicalHistory,
            'socialHistory': socialHistory,
            'familyHistory': familyHistory,
            'physicalExam': physicalExam,
            'admissionPhysicalExam': admissionPhysicalExam,
            'dischargePhysicalExam': dischargePhysicalExam,
            'pertinentResults': pertinentResults,
            'dischargeDisposition': dischargeDisposition,
            'dischargeDiagnosis': dischargeDiagnosis,
            'dischargeCondition': dischargeCondition,
            'dischargeInstructions': dischargeInstructions,
        }
        df = pd.DataFrame(data)
        df = df.explode('name').reset_index(drop=True)
        df = df.explode('unitNo').reset_index(drop=True)
        df = df.explode('admissionDate').reset_index(drop=True)
        df = df.explode('dischargeDate').reset_index(drop=True)
        df = df.explode('birth').reset_index(drop=True)
        df = df.explode('sex').reset_index(drop=True)
        df = df.explode('service').reset_index(drop=True)
        df = df.explode('allergies').reset_index(drop=True)
        df = df.explode('attending').reset_index(drop=True)
        df = df.explode('chiefComplaint').reset_index(drop=True)
        df = df.explode('procedure').reset_index(drop=True)
        df = df.explode('historyOfPresentIllness').reset_index(drop=True)
        df = df.explode('pastMedicalHistory').reset_index(drop=True)
        df = df.explode('socialHistory').reset_index(drop=True)
        df = df.explode('familyHistory').reset_index(drop=True)
        df = df.explode('physicalExam').reset_index(drop=True)
        df = df.explode('admissionPhysicalExam').reset_index(drop=True)
        df = df.explode('dischargePhysicalExam').reset_index(drop=True)
        df = df.explode('pertinentResults').reset_index(drop=True)
        df = df.explode('dischargeDisposition').reset_index(drop=True)
        df = df.explode('dischargeDiagnosis').reset_index(drop=True)
        df = df.explode('dischargeCondition').reset_index(drop=True)
        df = df.explode('dischargeInstructions').reset_index(drop=True)
        
        # 將輸出 DataFrame 合併到空 DataFrame
        output_df = pd.concat([output_df, df], ignore_index=True)

        print(output_df)
        
    return output_df


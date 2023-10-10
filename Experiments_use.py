import numpy as np
import pandas as pd
import os
from pathlib import Path
import openai


empty = '[EMPTY]'
not_generated_trigger = "\n\n\n[PASTE_GENERATED_TEXT_HERE]"
'''def skills_to_print(row):
    skills_list = ['python', 'java', 'c++', 'matlab', 'sas', 'database', 'software','calculus', 'statistics', 'machine learning', 'linear algebra']
    skills_available = [skill if row[skill] else '' for skill in skills_list]
    skills_available = list(filter(lambda x: x != '', skills_available))
    return ', '.join(skills_available)'''# didn't match with the student info, need to redefine
def skills_to_print(row):
    skills_list = ['python', 'java', 'c++', 'matlab', 'sas', 'database', 'software', 'calculus', 'statistics', 'machine learning', 'linear algebra']
    student_skills = [skill for skill in skills_list if row[skill] == '1']
    return ', '.join(student_skills)
    '''if not student_skills:
        return ''
    elif len(student_skills) == 1:
        return student_skills[0]
    else:
        return ', '.join(student_skills[:-1]) + ' and ' + student_skills[-1]'''



def PromptGenerator(row):
    # control variables
    PromptVersion = row["PromptVersion"]
    InitialWord = row['FirstPromptWord']
    IntentPurpose = row["IntentPurpose"]
    skillsorknowledge = row["SkillsOrKnowledge"]
    SkillsList = skills_to_print(row)
    TalkSkills = row['TalkAboutSkills']
    race = row['race'] # do we need to consider about race?
    TalkRace = row["TalkAboutRace"]
    major = row['undergrad1_major']
    gpa = row["undergrad1_gpa"]
    # print(row["undergrad1_gpa"])
    # print(gpa)
    SOIlen = row["length"]
    program = row["program"]

    #
    Program = f"{program}" if not pd.isna(program) else ''
    #do we need to consider applicants' race?
    if major or major == 'Null':
        Major = None
    Major = f"{major}" if not pd.isna(major) else ''
    Skills = f"{skillsorknowledge} in {SkillsList}" if TalkSkills and SkillsList else ''

    if SOIlen == 'Null':
        SOIlen = None
        # print("got null")
    if PromptVersion == 1:
        GPA = f"with {gpa} GPA, " if not gpa else ''
        Race= f"your race is {race}, " if row['TalkAboutRace'] and not pd.isna(race) else '' 
        Skills = f"and {skillsorknowledge} in {SkillsList}" if TalkSkills and SkillsList else ''    
        return f"{InitialWord} you are applying for a graduate program in {Program}at Fordham University. Write a statement of {IntentPurpose} that explains your reasons for pursuing this program, {Race}and how your undergraduate major in {Major}, {GPA}{Skills}have prepared you for success in the program. The statement should have around {f'{SOIlen} words.' if SOIlen else ''}"
    elif PromptVersion == 2:# Killer -- adding Tell a story
        GPA = f"GPA of {gpa} and " if not gpa else ''
        Race= f"your race is {race}, " if row['TalkAboutRace'] and not pd.isna(race) else '' 
        Skills = f"{skillsorknowledge} in {SkillsList} " if TalkSkills and SkillsList else ''
        return f"{InitialWord} you are applying for a graduate program in {Program} at Fordham University. Write a statement of {IntentPurpose} telling a story that explains your reasons for pursuing this program, {Race}and how your undergraduate major in {Major},{GPA}{Skills}have prepared you for success in this mater's program. The statement should have around {f'{SOIlen} words.' if SOIlen else ''}"
    elif PromptVersion == 3:
        GPA = f", my gpa is {gpa}" if not gpa else ''
        Race= f"{race}" if row['TalkAboutRace'] and not pd.isna(race) else '' 
        Skills = f", and I know {SkillsList} " if TalkSkills and SkillsList else ''
        # print("type 3", Skills)
        return f"Write a statement of {IntentPurpose} for a master's in {Program} at Fordham University. My undergrad is {Major}, {GPA}{Skills}. The statement should have around {f'{SOIlen} words.' if SOIlen else ''}"
    elif PromptVersion == 4:
        GPA = f", your GPA is {gpa}, " if not gpa else ''
        Race= f"{race}" if row['TalkAboutRace'] and not pd.isna(race) else '' 
        Skills = f", and you are skilled in {Skills}" if TalkSkills and SkillsList else ''
        # print("Type 4", Skills)
        return f"Write a statement of {IntentPurpose} for a master's in {Program} at Fordham University. {InitialWord} you are an undergrad in {Major}{GPA}{Skills}. The statement should have around {f'{SOIlen} words.' if SOIlen else ''}"
    else:
        return np.nan

#students_info = pd.read_excel('/Users/a3552324/Desktop/project/merged-
# data-without-TOEFL-final.xlsx')
students_info = pd.read_csv('/Users/a3552324/Desktop/merged_data_add_length_copy.csv')
students_info.drop(['gre_verified_verbal', 'gre_verified_verbal_percentile','permanent_country','gre_verified_quantitative', 
'gre_verified_quantitative_percentile', 'gre_verified_analytical_writing','gre_verified_analytical_writing_percentile', 'toefl_ibt_verified_total', 'toefl_ibt_verified_listening', 'toefl_ibt_verified_reading', 'toefl_ibt_verified_writing','toefl_ibt_verified_speaking','ielts_verified_overall_band_score','ielts_verified_listening','ielts_verified_reading','ielts_verified_writing','ielts_verified_speaking','merit_aid_yes_no'],inplace=True,axis=1)
students_info["ID"] = students_info["ID"].map(lambda x: "0"+str(x))
students_info["PromptVersion"] = np.random.choice([1,2,3,4], size=len(students_info))
#students_info['age_at_submission'] = students_info['age_at_submission'].map(lambda x: round(x))
students_info['undergrad1_gpa'] = students_info['undergrad1_gpa'].map(lambda x: round(x,2) if x > 3.40 else np.nan)
students_info.replace({'Unknown':np.nan},inplace=True)
students_info.replace({'OTHER':np.nan},inplace=True)
students_info["ExplainPlease"] = np.random.choice([True, False], size=len(students_info))
students_info["TalkAboutAge"] = np.random.choice([True, False], size=len(students_info),p=[.05,.95])
#students_info["TalkAboutCountry"] = np.random.choice([True, False], size=len(students_info),p=[.2,.8])
students_info["TalkAboutRace"] = np.random.choice([True, False], size=len(students_info),p=[.2,.8])
students_info["TalkAboutSkills"] = np.random.choice([True, False], size=len(students_info),p=[.95,.05]) #not work
students_info["SkillsOrKnowledge"] = np.random.choice(['skills', 'knowledge'], size=len(students_info))
students_info["FirstPromptWord"] = np.random.choice(["Imagine", "Assume", "Think","Let's say"], size=len(students_info))
students_info["IntentPurpose"] = np.random.choice(["intent", "purpose"], size=len(students_info))
#students_info["SOILen"] = np.random.randint(300, 700, size=len(students_info)) #match with the original one?
#students_info["ProvideSOILen"] = np.random.choice([True, False], size=len(students_info),p=[.2,.8])
#students_info["TalkAboutSuccessInProgram"] = np.random.choice([True, False], size=len(students_info), p=[0.65, 0.35])
students_info["Prompt"] = students_info.apply(PromptGenerator,axis=1)

# Cleaning prompt generator output
students_info["Prompt"] = students_info["Prompt"].map(lambda x: x.replace(empty, "")).replace("  ", " ")
students_info["Prompt"] = students_info["Prompt"].map(lambda x: x + not_generated_trigger)
# Create 
save_dest = Path('Generated_Prompt_SOI_new')
save_dest.mkdir(exist_ok=True)
# save_generated_SOI_path = Path('ChatGPTProjectData/generated_SOI')
# save_generated_SOI_path.mkdir(exist_ok=True)
# Loop through dataframe and create files
# print(students_info)

OpenAI_API_KEY = "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"
openai.api_key = OpenAI_API_KEY
model_id = 'gpt-3.5-turbo'

GeneratedSOIs = []
for _, row in students_info.iterrows():
    Prompt = row["Prompt"]
    conversation = []
    conversation.append({"role": "system", "content": Prompt})
    try:
        '''add a try block to check empty letters'''
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=conversation)
        
        GeneratedSOI = response.choices[-1].message.content.lstrip().replace("\n\n","\n")
        GeneratedSOIs.append(GeneratedSOI)

        print(len(GeneratedSOIs))
    except:
        print('error')

#create GeneratedSOIs_new dataset
students_info["AIGenerated"] = GeneratedSOIs
students_info[["ID", "Prompt", "AIGenerated"]].to_csv(os.path.join(os.getcwd(), "GeneratedSOIs_new.csv"), index=False)
len(GeneratedSOIs)
df_test = pd.read_csv("GeneratedSOIs_new.csv", dtype=str)
print(df_test)


file_path = os.path.join(save_dest,filename)
if Path(file_path).exists():
    with open(file_path, 'r') as f:
        read_content = f.read()        
        if not_generated_trigger not in read_content:
            pass
        else:
            with open(file_path, 'w') as f:
                f.write(content)    
else:
    with open(file_path, 'w') as f:
        f.write(content)



                
  # if not saved_model.exists():

    # with open('GeneratedPrompts/'+filename, 'w') as f:
    #     f.write(content)
    
    
    # filename = row['ID\n(delete)']+f'_{idx}_generatedSOI.txt'
    # file_path = os.path.join('ChatGPTProjectData/generated_SOI', filename)
    # if os.path.getsize(filename) == 0:
    #     with open('GeneratedPrompts/'+filename, 'w') as f:
    #         pass
    

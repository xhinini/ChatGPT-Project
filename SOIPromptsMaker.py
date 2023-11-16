import numpy as np
import pandas as pd
import os
import random
from pathlib import Path

empty = '[EMPTY]'
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def skills_to_print(row):
    skills_list = ['python', 'java', 'c++', 'matlab', 'sas', 'database', 'software', 'calculus', 'statistics', 'machine learning', 'linear algebra']
    student_skills = [skill for skill in skills_list if row[skill] == '1']
    return ', '.join(student_skills)

def get_random_insight():
    insights = [
        "reflecting on my journey so far",
        "considering the challenges I've overcome",
        "thinking about how my experiences have shaped me",
        "contemplating my academic and professional growth"
    ]
    return random.choice(insights)

def PromptGenerator(row):
    # Extracting and processing data from row
    PromptVersion = row["PromptVersion"]
    InitialWord = row['FirstPromptWord']
    IntentPurpose = row["IntentPurpose"]
    skillsorknowledge = row["SkillsOrKnowledge"]
    SkillsList = skills_to_print(row)
    TalkSkills = row['TalkAboutSkills']
    race = row['race']
    TalkRace = row["TalkAboutRace"]
    major = row['undergrad1_major']
    gpa = row["undergrad1_gpa"]
    SOIlen = row["SOILen"]
    program = row["program"]

    # Building components of the prompt
    Program = f" {program}" if not pd.isna(program) else ''
    Major = f" {major}" if not pd.isna(major) and major != 'Null' else 'an undergraduate degree'
    Skills = f" {skillsorknowledge} in {SkillsList}" if TalkSkills and SkillsList else ''
    GPA = f" with a GPA of {gpa}, " if not pd.isna(gpa) and gpa else ''
    Race = f" As someone from a {race} background, " if TalkRace and not pd.isna(race) else ''
    Insight = get_random_insight()

    # Different prompt versions
    if PromptVersion == 1:
        return f"{InitialWord}, you are applying for a graduate program in {Program} at Fordham University. Write a statement of {IntentPurpose} explaining why you are interested in this field and how your major {Major}{GPA}{Skills} have prepared you for this advanced study. Aim for around {SOIlen} words. Make it sound personal and human."
    
    elif PromptVersion == 2:
        return f"Imagine you are in an interview for Fordham University's {Program} program. {Race}How would you describe your academic journey, including your studies {Major}{GPA}, and how does your {skillsorknowledge} in {SkillsList} align with this program? Limit your response to {SOIlen} words. Make it sound personal and human."

    elif PromptVersion == 3:
        LifeLesson = random.choice(["a challenging project", "a significant achievement", "a turning point in your academic journey"])
        return f"For your application to the {Program} program at Fordham University, describe {LifeLesson} that highlights your {IntentPurpose}. Focus on how your experiences in {Major}{GPA}{Skills} have influenced your decision to pursue this field. The statement should be approximately {SOIlen} words. Make it sound personal and human."

    elif PromptVersion == 4:
        CareerObjective = random.choice(["to drive innovation", "to lead in research", "to make impactful contributions"])
        return f"In your application for the {Program} program at Fordham University, discuss your career objective {CareerObjective} in the field. Elaborate on how your academic background {Major}{GPA} and {skillsorknowledge} like {SkillsList} support this goal. Aim for about {SOIlen} words. Make it sound personal and human."

    # Adding a new version for variety
    elif PromptVersion == 5:
        PersonalQuality = random.choice(["perseverance", "creativity", "analytical skills"])
        return f"Write a Statement of Intent for Fordham University's {Program} program, focusing on a personal quality like {PersonalQuality} that you believe will be key to your success. Discuss how this, along with your studies {Major}{GPA}{Skills}, has prepared you for graduate studies. Target around {SOIlen} words. Make it sound personal and human."

    else:
        return np.nan

students_info = pd.read_csv('merged_data_add_length.csv')
# students_info.drop(['gre_verified_verbal', 'gre_verified_verbal_percentile','permanent_country','gre_verified_quantitative', 
# 'gre_verified_quantitative_percentile', 'gre_verified_analytical_writing','gre_verified_analytical_writing_percentile', 'toefl_ibt_verified_total', 'toefl_ibt_verified_listening', 'toefl_ibt_verified_reading', 'toefl_ibt_verified_writing','toefl_ibt_verified_speaking','ielts_verified_overall_band_score','ielts_verified_listening','ielts_verified_reading','ielts_verified_writing','ielts_verified_speaking','merit_aid_yes_no'],inplace=True,axis=1)
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
students_info["SOILen"] = np.random.randint(300, 800, size=len(students_info)) 

students_info["Prompt"] = students_info.apply(PromptGenerator,axis=1)

# Cleaning prompt generator output
students_info["Prompt"] = students_info["Prompt"].map(lambda x: x.replace(empty, "")).replace("  ", " ")
#students_info["Prompt"] = students_info["Prompt"].map(lambda x: x + not_generated_trigger)

students_info[["ID", "Prompt"]].to_csv(os.path.join(os.getcwd(), "Prompts_new_SOIs.csv"), index=False)
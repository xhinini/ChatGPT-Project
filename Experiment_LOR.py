import pandas as pd
import numpy as np
import os
from pathlib import Path
import openai

empty = '[EMPTY]'
not_generated_trigger = "\n\n\n[PASTE_GENERATED_TEXT_HERE]"


def get_relationship(relationship, gender):
    #gender = 'he' if row['applicant_gender'] == 'Male' else 'she'
    
    if relationship == 'Academic':
        return f"{gender} is my student"
    elif relationship == 'Work':
        return f"{gender} is my employee"
    elif relationship == 'Friend':
        return f"{gender} is my friend"
    elif relationship in ['Other', 'Unknown']:
        return ""
    else:
        return relationship

def PromptGenerator(row):
    PromptVersion = row["PromptVersion"]
    InitialWord = row['FirstPromptWord']
    #student_id = row['id']
    student = row['Name']
    major = row['program']
    gender = 'he' if row['applicant_gender'] == 'Male' else 'she'
    gender_pronoun = 'him' if row['applicant_gender'] == 'Male' else 'her'
    relationship = get_relationship(row['recommender_role'], gender)
    LORlen = row["length"]
    experience = row['RelatedExperience']
    interest = row['RelatedInterest']
    

    if PromptVersion == 1:
        return f"Please write a letter of recommendation for {student} who is applying for {major} at Fordham University. Describe {gender_pronoun} skills, qualifications, and experiences, especially in {experience}, that makes {gender} a strong candidate for this program. And {relationship}. The statement should have around {f'{LORlen} words.' if LORlen else ''}"
    elif PromptVersion == 2:
        return f"Please write a recommendation letter for {student} who wishes to pursue a master's degree in {major} at Fordham University. {student} has consistently demonstrated hard work, creativity, and dedication, especially in {experience}. And {relationship}. The statement should have around {f'{LORlen} words.' if LORlen else ''}"
    elif PromptVersion == 3: #modify the version
        return f"{InitialWord} {relationship}, and you are going to write a recommendation letter for {gender_pronoun} to apply for a master's degree in {major} at Fordham University. Describe the student's strong passion for {interest}. The statement should have around {f'{LORlen} words.' if LORlen else ''}"
    elif PromptVersion == 4: #add a new version of prompt
        return f"{InitialWord} you are writing a recommendation letter for {student}. {gender} wants to apply for a master's degree in {major} at Fordham Univeristy. And {relationship}. The statement should have around {f'{LORlen} words.' if LORlen else ''}"
    else:
        return np.nan

lor_info = pd.read_csv('/Users/a3552324/Desktop/project/scores_applicant_ratings.csv')
lor_info["id"] = lor_info["id"]
lor_info["PromptVersion"] = np.random.choice([1,2,3,4], size=len(lor_info))
lor_info["FirstPromptWord"] = np.random.choice(["Imagine", "Assume", "Think","Let's say"], size=len(lor_info))
lor_info["RelatedInterest"] = np.random.choice(["data science", "machine learning", "artificial intelligence", "statistics", "big data", "data visualization"], size=len(lor_info))
lor_info["RelatedExperience"] = np.random.choice([ "academic", "work", "industry","research"], size = len(lor_info))
lor_info["length"] = np.random.randint(166, 624, size=len(lor_info))
#get a real name for each applicant to make more flow
boys_name = ["Liam", "Hiroshi", "Miguel", "Luca", "Mohamed", "Rajesh", "Ivan", "Wei", "Carlos", "Jean", "Emil", "Aleksander", "Sebastian", "Johan", "Kai", "Aarav", "Oscar", "Yuki", "Diego", "Matteo",
            "Youssef", "Vijay", "Dmitri", "Jun", "Joao", "Pierre", "Gustav", "Piotr", "Felix", "Bram", "Lono", "Dev", "George", "Haruto", "Francisco", "Giovanni", "Ahmed", "Amit", "Alexei", "Chen",
            "Pedro", "Louis", "Erik", "Jakub", "Max", "Pieter", "Akoni", "Rohan", "Henry", "Daiki", "Alvaro", "Francesco", "Omar", "Sanjay", "Nikolai", "Feng", "Rafael", "Theo", "Lars", "Tomasz",
            "Tobias", "Sven", "Keanu", "Arjun", "Jack", "Kaito", "Javier", "Antonio", "Sami", "Pranav", "Sergei", "Long", "Tiago", "Hugo", "Nils", "Marek", "Leon", "Thijs", "Mana", "Nikhil"]
girls_name = ["Emma", "Yui", "Sofia", "Giulia", "Fatima", "Priya", "Anastasia", "Ling", "Ana", "Marie", "Elsa", "Zofia", "Emma", "Anna", "Leilani", "Aanya", "Olivia", "Haruka", "Lucia", "Chiara",
            "Nour", "Anjali", "Ekaterina", "Mei", "Clara", "Camille", "Astrid", "Agnieszka", "Sophie", "Fleur", "Kailani", "Diya", "Charlotte", "Aiko", "Carmen", "Alessia", "Aisha", "Pooja", "Maria", "Yan",
            "Beatriz", "Chloe", "Freja", "Magdalena", "Hannah", "Lotte", "Noelani", "Riya", "Mia", "Sakura", "Valentina", "Bianca", "Layla", "Radha", "Tatiana", "Qing", "Larissa", "Alice", "Ingrid", "Katarzyna",
            "Lena", "Eva", "Malie", "Shreya", "Isabella", "Rin", "Natalia", "Serena", "Maha", "Sunita", "Olga", "Hui", "Mariana", "Amelie", "Greta", "Ewa", "Greta", "Sofie", "Nalani", "Tanvi"]
def get_name(gender):
    if gender == 'Male':
        return np.random.choice(boys_name)
    elif gender == 'Female':
        return np.random.choice(girls_name)
    else:
        return "Unknown"
lor_info["Name"] = lor_info['applicant_gender'].apply(lambda gender: get_name(gender))

lor_info["Prompt"] = lor_info.apply(PromptGenerator,axis=1)
# Cleaning prompt generator output
lor_info["Prompt"] = lor_info["Prompt"].map(lambda x: x.replace(empty, "")).replace("  ", " ")

# Create 
save_dest = Path('Generated_Prompt_LOR_new')
save_dest.mkdir(exist_ok=True)
# save_generated_LOR_path = Path('ChatGPTProject/generated_LOR')
# save_generated_LOR_path.mkdir(exist_ok=True)

# Loop through dataframe and create files
'''for idx, row in lor_info.iterrows():
    #filename = row['id']+f'_{idx}_GeneratedLORPrompt.txt'
    filename = str(row['id']) + f'_{idx}_GeneratedLORPrompt.txt'
    content = row['Prompt']
    
    if Path('Generated_Prompt_LOR_new/'+filename).exists():
        with open('Generated_Prompt_LOR_new/'+filename, 'r') as f:
            read_content = f.read()        
            if not_generated_trigger not in read_content:
                pass
            else:
                with open('Generated_Prompt_LOR_new/'+filename, 'w') as f:
                    f.write(content)    
    else:
        with open('Generated_Prompt_LOR_new/'+filename, 'w') as f:
            f.write(content)'''

#Generated LORs
OpenAI_API_KEY = "Your API Key" #Put your API key here
openai.api_key = OpenAI_API_KEY
model_id = 'gpt-3.5-turbo'

GeneratedLORs = []
for _, row in lor_info.iterrows():
    Prompt = row["Prompt"]
    conversation = []
    conversation.append({"role": "system", "content": Prompt})

    while True:
        try:
            '''add a try block to check empty letters'''
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=conversation) #may need to upgrade openai to use ChatCompletion pip -U openai

            GeneratedLOR = response.choices[-1].message.content.lstrip().replace("\n\n","\n")
            
            if not GeneratedLOR.strip():  # Check if the response is empty
                raise ValueError("Empty response received")
                
            GeneratedLORs.append(GeneratedLOR)
            print(len(GeneratedLORs))
            break  # If successful, exit the while loop and move to the next prompt

        except Exception as e:
            print(f'Error: {e}')

#create GeneratedSOIs_new dataset
lor_info["AIGenerated"] = GeneratedLORs
lor_info[["id", "Prompt", "AIGenerated"]].to_csv(os.path.join(os.getcwd(), "GeneratedLORs_new.csv"), index=False)
len(GeneratedLORs)
df_test = pd.read_csv("GeneratedLORs_new.csv", dtype=str)
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

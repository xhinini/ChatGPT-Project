import pandas as pd
import numpy as np
import os
import random
# from pathlib import Path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
empty = '[EMPTY]'


def get_relationship(relationship, gender):
    # Expanded descriptions based on the recommender's role
    if relationship == 'Academic':
        return f"{gender} is my student, whom I have taught in several courses"
    elif relationship in ('Work', 'Industry'):
        return f"{gender} is my employee/coworker, with whom I have worked closely on various projects"
    elif relationship == 'Friend':
        return f"{gender} is my friend, and I have known {gender} for many years"
    elif relationship in ['Other', 'Unknown']:
        return ""
    else:
        return relationship

def PromptGenerator(row):
    PromptVersion = row["PromptVersion"]
    InitialWord = row['FirstPromptWord']
    student = row['Name']
    major = row['program']
    gender = 'he' if row['applicant_gender'] == 'Male' else 'she'
    gender_pronoun = 'him' if row['applicant_gender'] == 'Male' else 'her'
    relationship = get_relationship(row['recommender_role'], gender)
    LORlen = row["length"]
    experience = row['RelatedExperience']
    interest = row['RelatedInterest']
    specificity = row['specificity']
    positivity = row['positivity']

    # Incorporating ratings and additional data into the prompts
    details_request = " Please provide specific examples. Feel free to make this up" if specificity > 2 else ""
    improvement_suggestion = " Mention any areas for improvement. Feel free to make this up" if positivity < 1 else ""
    add_personal_touch = random.choice([True, False])
    personal_note = " Make it sound personal and not AI generated." if add_personal_touch else ""

    if PromptVersion == 1:
        return f"{InitialWord}, write a letter of recommendation for {student} who is applying for {major} at Fordham University.{details_request}{personal_note} Highlight {gender_pronoun} skills, qualifications, and experiences, particularly in {experience}, demonstrating {gender} as a strong candidate for this program.{improvement_suggestion} And {relationship}. The statement should be approximately {LORlen} words."
    elif PromptVersion == 2:
        return f"{InitialWord}, you are preparing a recommendation letter for {student} who aspires to pursue a master's in {major} at Fordham University.{details_request} {student} has shown consistent hard work, creativity, and dedication, especially in {experience}.{improvement_suggestion} And {relationship}.{personal_note} The letter should be about {LORlen} words."
    elif PromptVersion == 3: 
        return f"{InitialWord}, as {relationship}, you are tasked with writing a recommendation letter for {student} for a master's degree in {major} at Fordham University.{details_request} Emphasize the student's strong passion for {interest} and how it aligns with their career goals.{improvement_suggestion}{personal_note} The statement should be around {LORlen} words."
    elif PromptVersion == 4:
        return f"{InitialWord}, in your capacity as {relationship}, you are endorsing {student} for a master's degree in {major} at Fordham University.{details_request} Discuss how {gender} stands out in terms of academic achievements and personal qualities.{improvement_suggestion} The letter should be approximately {LORlen} words.{personal_note} "
    else:
        return np.nan

# Read the dataset
file_path = 'scores_applicant_ratings.csv'  # Update the path if necessary
lor_info = pd.read_csv(file_path)

# Additional setup for the dataset
lor_info["PromptVersion"] = np.random.choice([1,2,3,4], size=len(lor_info))
lor_info["FirstPromptWord"] = np.random.choice(["Imagine", "Assume", "Think", "Let's say"], size=len(lor_info))
lor_info["RelatedInterest"] = np.random.choice(["data science", "machine learning", "artificial intelligence", "statistics", "big data", "data visualization"], size=len(lor_info))
lor_info["RelatedExperience"] = np.random.choice(["academic", "work", "industry", "research"], size=len(lor_info))
lor_info["length"] = np.random.randint(166, 624, size=len(lor_info))

#get a real name for each applicant to make more flow
def get_name(gender):
    boys_name = ["Liam", "Hiroshi", "Miguel", "Luca", "Mohamed", "Rajesh", "Ivan", "Wei", "Carlos", "Jean", "Emil", "Aleksander", "Sebastian", "Johan", "Kai", "Aarav", "Oscar", "Yuki", "Diego", "Matteo",
            "Youssef", "Vijay", "Dmitri", "Jun", "Joao", "Pierre", "Gustav", "Piotr", "Felix", "Bram", "Lono", "Dev", "George", "Haruto", "Francisco", "Giovanni", "Ahmed", "Amit", "Alexei", "Chen",
            "Pedro", "Louis", "Erik", "Jakub", "Max", "Pieter", "Akoni", "Rohan", "Henry", "Daiki", "Alvaro", "Francesco", "Omar", "Sanjay", "Nikolai", "Feng", "Rafael", "Theo", "Lars", "Tomasz",
            "Tobias", "Sven", "Keanu", "Arjun", "Jack", "Kaito", "Javier", "Antonio", "Sami", "Pranav", "Sergei", "Long", "Tiago", "Hugo", "Nils", "Marek", "Leon", "Thijs", "Mana", "Nikhil"]
    girls_name = ["Emma", "Yui", "Sofia", "Giulia", "Fatima", "Priya", "Anastasia", "Ling", "Ana", "Marie", "Elsa", "Zofia", "Emma", "Anna", "Leilani", "Aanya", "Olivia", "Haruka", "Lucia", "Chiara",
            "Nour", "Anjali", "Ekaterina", "Mei", "Clara", "Camille", "Astrid", "Agnieszka", "Sophie", "Fleur", "Kailani", "Diya", "Charlotte", "Aiko", "Carmen", "Alessia", "Aisha", "Pooja", "Maria", "Yan",
            "Beatriz", "Chloe", "Freja", "Magdalena", "Hannah", "Lotte", "Noelani", "Riya", "Mia", "Sakura", "Valentina", "Bianca", "Layla", "Radha", "Tatiana", "Qing", "Larissa", "Alice", "Ingrid", "Katarzyna",
            "Lena", "Eva", "Malie", "Shreya", "Isabella", "Rin", "Natalia", "Serena", "Maha", "Sunita", "Olga", "Hui", "Mariana", "Amelie", "Greta", "Ewa", "Greta", "Sofie", "Nalani", "Tanvi"]
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
lor_info[["filename", "Prompt"]].to_csv(os.path.join(os.getcwd(), "Prompts_new_LORs.csv"), index=False)
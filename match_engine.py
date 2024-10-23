import random

import pandas as pd
import streamlit as st


def match(df1, df2):
    class Lead:
        def __init__(self, name, prefs=None):
            self.name = name
            if prefs is None:
                self.prefs = []
            else:
                self.prefs = prefs

    class Compliment:
        def __init__(self, name, prefs=None):
            self.name = name
            if prefs is None:
                self.prefs = []
            else:
                self.prefs = prefs

    """
    Making list of lists of data 
    [
        [x, [pref1, pref2, pref3]]
        [x, [pref1, pref2, pref3]]
        [x, [pref1, pref2, pref3]]
    ]
    """
    # lead_list = df1.apply(lambda row: [str(row[0]), list(map(str, row[1:]))], axis=1).tolist()
    lead_list = df1.apply(
        lambda row: [
            str(int(row[0])) if isinstance(row[0], float) and row[0].is_integer() else str(row[0]),
            # Convert to int if row[0] is a float and is an integer
            [
                str(int(x)) if pd.api.types.is_numeric_dtype(type(x)) else str(x)
                # Convert to int if numeric, else keep as string
                for x in row[1:]
                if x is not None and not pd.isna(x)  # Exclude None and NaN values
            ]
        ],
        axis=1
    ).tolist()

    # compliment_list = df2.apply(lambda row: [str(row[0]), list(map(str, row[1:]))], axis=1).tolist()
    compliment_list = df2.apply(
        lambda row: [
            str(int(row[0])) if isinstance(row[0], float) and row[0].is_integer() else str(row[0]),
            # Convert to int if row[0] is a float and is an integer
            [
                str(int(x)) if pd.api.types.is_numeric_dtype(type(x)) else str(x)
                # Convert to int if numeric, else keep as string
                for x in row[1:]
                if x is not None and not pd.isna(x)  # Exclude None and NaN values
            ]
        ],
        axis=1
    ).tolist()

    # Making Lead and Compliment objects from data
    all_leads = [Lead(x, prefs) for [x, prefs] in lead_list]
    all_compliments = [Compliment(x, prefs) for [x, prefs] in compliment_list]

    # Function to make compliment object from name
    def make_compliment(item_name):
        compliment = [x for x in all_compliments if x.name == item_name][0]
        return compliment

    # Function to make lead object from name
    def make_lead(item_name):
        lead = [x for x in all_leads if x.name == item_name][0]
        return lead

    # Function to calculate points
    # if compliment/lead not in lead/compliment prefs - points = 0
    # lead points = 10 + length of prefs - pref no. of compliment
    # comp points = 5.1 + length of prefs - pref no. of compliment
    def calc_points(lead_obj, comp_obj):
        lead_points = [10 + len(lead_obj.prefs) - lead_obj.prefs.index(comp_obj)
                       if comp_obj in lead_obj.prefs
                       else 0][0]
        comp_points = [5.1 + len(comp_obj.prefs) - comp_obj.prefs.index(lead_obj)
                       if lead_obj in comp_obj.prefs
                       else 0][0]

        return lead_points + comp_points

    # Making Lead prefs into corresponding compliment objects and sorting prefs according to points
    for lead in all_leads:
        lead.prefs = [make_compliment(x) for x in lead.prefs]
        lead.prefs = sorted(lead.prefs, key=lambda x: calc_points(lead, x), reverse=True)

    # Making Compliment prefs into corresponding lead objects and sorting prefs according to points
    for compliment in all_compliments:
        compliment.prefs = [make_lead(x) for x in compliment.prefs]
        compliment.prefs = sorted(compliment.prefs, key=lambda x: calc_points(x, compliment), reverse=True)

    # List to hold tentative couples
    couples = []

    # Initiating free lists
    free_leads = all_leads
    free_compliments = all_compliments

    while len(free_leads) > 0:

        # control variable to break the for loop and move on with next lead
        made_couple = False

        for lead in free_leads:

            # For compliments in leads prefs
            for compliment in lead.prefs:

                # if compliment is free
                if compliment in free_compliments:
                    couples.append([lead, compliment])
                    free_leads.remove(lead)
                    free_compliments.remove(compliment)
                    made_couple = True
                    # Break out of inner for loop
                    break

                # Break out of outer for loop
                if made_couple:
                    break

                # if compliment is not free
                else:
                    existing_couple = [couple for couple in couples if couple[1] == compliment][0]
                    existing_couple_points = calc_points(existing_couple[0], compliment)
                    potential_couple_points = calc_points(lead, compliment)
                    # if existing couples points higher than potential couple
                    if existing_couple_points >= potential_couple_points:
                        pass
                    # if existing couples points lower than potential couple
                    else:
                        couples.remove(existing_couple)
                        couples.append([lead, compliment])
                        free_leads.remove(lead)
                        free_leads.append(existing_couple[0])
                        made_couple = True
                        # Break out of inner for loop
                        break

                # Break out of outer for loop
                if made_couple:
                    break

                # if no couple with compliments in leads prefs
                else:
                    check_list = [x for x in free_compliments]
                    best_compliment = max(check_list, key=lambda x: calc_points(lead, x))
                    if calc_points(lead, best_compliment) > 0:
                        couples.append([lead, best_compliment])
                        free_leads.remove(lead)
                        free_compliments.remove(best_compliment)
                        made_couple = True
                        # Break out of inner for loop
                        break

                    # choose random compliment
                    else:
                        random_list = [x for x in free_compliments]
                        random_compliment = random.choice(random_list)
                        couples.append([lead, random_compliment])
                        free_leads.remove(lead)
                        free_compliments.remove(random_compliment)
                        made_couple = True
                        # Break out of inner for loop
                        break

            # Break out of outer for loop
            if made_couple:
                break

    named_couples = [[x.name for x in sublist] for sublist in couples]

    # Getting summary data
    # lead:
    def count_occurrences_lead(list1, list2):
        count = 0
        for item1 in list1:
            for sublist in list2:
                if sublist[0] == item1[0]:
                    if item1[1] in sublist[1]:
                        count += 1
        return count

    # Getting lead summary
    lead_summary = [count_occurrences_lead(named_couples, lead_list), len(lead_list)]

    # compliment:
    def count_occurrences_compliment(list1, list2):
        count = 0
        for item1 in list1:
            for sublist in list2:
                if sublist[0] == item1[1]:
                    if item1[0] in sublist[1]:
                        count += 1
        return count

    # Getting compliment summary
    compliment_summary = [count_occurrences_compliment(named_couples, compliment_list), len(lead_list)]
    return named_couples, lead_summary, compliment_summary
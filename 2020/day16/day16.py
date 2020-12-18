# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 12:40:30 2020

@author: celine.gross
"""
import re
import numpy as np

with open('input_day16.txt', 'r') as file:
    puzzle = [line.strip() for line in file if len(line) >1]


# Part 1

def parse(data):
    index_mine = data.index('your ticket:')
    index_others = data.index('nearby tickets:')
    
    # Parse rules
    rules = {}
    regex = r"(\w+(?:\s\w+)?): (\d+)-(\d+) or (\d+)-(\d+)"
    for i in range(index_mine):
        match = re.search(regex, data[i])
        rules[match.group(1)] = [(int(match.group(2)), int(match.group(3))), 
                                  (int(match.group(4)), int(match.group(5)))]
    
    # Parse my ticket
    myticket = [int(d) for d in data[index_mine+1].split(',')]
    
    # Parse other tickets
    tickets = [[int(d) for d in line.split(',')] for line in data[index_others+1:]]
    
    return rules, myticket, tickets


def extract_invalid(rules, ticket):
    invalid = []
    for field in ticket:
        if any(v[0][0] <= field <= v[0][1] or v[1][0] <= field <= v[1][1] for v in rules.values()):
            continue
        invalid.append(field)          
    return invalid


def sum_invalid(rules, tickets):
    all_invalid = []
    for ticket in tickets:
        all_invalid += extract_invalid(rules, ticket)
    return sum(all_invalid)


rules, myticket, tickets = parse(puzzle)
print("There are {} invalid tickets.".format(sum_invalid(rules, tickets)))


# Part 2

valid_tickets = [t for t in tickets if len(extract_invalid(rules, t)) == 0]

def score(rules, ticket):
    rule_score = []
    for rule, value in rules.items():
        score = []
        for field in ticket:
            if value[0][0] <= field <= value[0][1] or value[1][0] <= field <= value[1][1]:
                score.append(1)
            else:
                score.append(0)
        rule_score.append(score)
    return np.stack(rule_score)


def compute_score(rules, tickets):
    field_list = list(rules.keys())
    # Generate aggregate matrix
    total_scores = np.zeros((len(field_list), len(field_list)))
    for i, t in enumerate(tickets):
        total_scores += score(rules, t)
    # Normalise matrix
    total_scores = total_scores//len(tickets)
    return total_scores
    

def map_fields(rules, tickets):
    total_scores = compute_score(rules, tickets)
    field_list = list(rules.keys())
    fields_dict = {}
    while sum(sum(total_scores)) > 0:
        for i, row in enumerate(total_scores):
            if sum(row) == 1:
                index = list(row).index(1)
                fields_dict[field_list[i]] = index
                total_scores[:, index] = 0
                break
        continue               
    return fields_dict


def run(rules, tickets, ticket):
    fields_dict = map_fields(rules, tickets)
    indexes = [v for k,v in fields_dict.items() if 'departure' in k ]
    total = 1
    for i in indexes:
        total *= ticket[i]
    return total


print("Part 2 answer is ", run(rules, valid_tickets, myticket))

   
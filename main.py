#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re


# hosszredukció
def reduce_rules_length():
    N = rules.keys()
    for key in N:
        s = rules[key]
        for i in range(len(s)):
            if len(s[i]) > 2:
                whole = s[i]
                s[i] = whole[0] + '[' + whole[1:] + ']'
                whole = whole[1:]
                while len(whole) > 2:
                    rules['[' + whole + ']'] = [whole[0] + '[' + whole[1:] + ']']
                    whole = whole[1:]
                rules['[' + whole + ']'] = [whole]


# e-mentesítés
def eliminate_empty_rules():
    H = set()
    for key in rules:
        if '_' in rules[key]:
            H.add(key)
            rules[key].remove('_')
    while True:
        Hn = set()
        for key in rules:
            if key not in H:
                s = rules[key]
                for i in range(len(s)):
                    if set(s[i]) & H == set(s[i]):
                        Hn.add(key)
        if H | Hn == H:
            break
        else:
            H = H | Hn
    for key in rules:
        s = rules[key]
        for i in range(len(s)):
            if re.match('^[a-zA-Z]{2}$|^[a-zA-Z]\[[a-zA-Z]+\]$', s[i]):
                a, b = re.findall('^[a-zA-Z]', s[i])[0], re.findall('\[[a-zA-Z]+\]$|[a-zA-Z]$', s[i])[0]
                if a in H and b not in rules[key] and key != b:
                    rules[key].append(b)
                if b in H and a not in rules[key] and key != a:
                    rules[key].append(a)


# láncmentesítés
def eliminate_unit_rules():
    def unit(key):
        H = set(rules[key]) & set(rules.keys())
        for e in H:
            rules[key].remove(e)
            if len(set(rules[key]) & set(rules.keys())) != 0:
                unit(e)
            rules[key] = list(set(rules[key]) | set(rules[e]))

    for key in rules:
        unit(key)


# álnemterminálisok bevezetése
def eliminate_nonsolitary_terminals():
    N = rules.keys()
    H = []
    for key in N:
        s = rules[key]
        H.extend(re.findall('[a-z]', ''.join(rules[key])))
        for i in range(len(s)):
            s[i] = re.sub('^(?P<t>[a-z])(?P<n>.+)', 'Q(\g<t>)\g<n>', s[i])
            s[i] = re.sub('(?P<n>.+)(?P<t>[a-z])$', '\g<n>Q(\g<t>)', s[i])
    for e in set(H):
        rules['Q(' + e + ')'] = [e]


def contains(a):
    keys = {}

    def element(a):
        if a not in keys.keys():
            keys.setdefault(a, set())
            if len(a) == 1:
                for key in rules:
                    s = rules[key]
                    for i in range(len(s)):
                        if a == s[i]:
                            keys[a].add(key)
            else:
                for i in range(1, len(a)):
                    for e, f in [(x, y) for x in element(a[:i]) for y in element(a[i:])]:
                        for key in rules:
                            s = rules[key]
                            for j in range(len(s)):
                                if s[j] == e + f:
                                    keys[a].add(key)
        return keys[a]

    element(a)
    if start in keys[a]:
        return 'tartalmazza'
    else:
        return 'nem tartalmazza'


def write():
    print 'Nem-terminalisok: ' + str(rules.keys())
    print 'Szabalyok:'
    for key in rules:
        print key + ': ' + str(rules[key])


def read(filename):
    f = open(filename, 'r')
    for lines in f:
        line = lines.split(':', 1)
        key = line[0].strip()
        rules.setdefault(key, [])
        rule = line[1].split('|')
        for s in rule:
            rules[key].append(s.strip())
    f.close()


rules = {}
start = 'S'

print 'Chomsky normal forma'
fajl = raw_input('Add meg a fajlnevet: ')
read(fajl)
print '\nA beolvasott nyelvtan'
print 'Kezdoszimbolum: ' + start
write()
print '\nHosszredukcio'
reduce_rules_length()
write()
print '\nEpszilon-mentesites'
eliminate_empty_rules()
write()
print '\nLancmentesites'
eliminate_unit_rules()
write()
print '\nAlnemterminalisok bevezetese'
eliminate_nonsolitary_terminals()
write()
print '\nBenne van-e egy adott szo a nyelvtanban: (a "0" karakterre kilep a program)'
while True:
    word = raw_input('Adj meg egy szot: ')
    if word == '0':
        break
    else:
        print 'A nyelvtan ' + str(contains(word)) + ' az "' + word + '" szot.'

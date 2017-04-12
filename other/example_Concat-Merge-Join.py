# -*- coding: utf-8 -*-
"""
Examples for Concat, Merge and Join
@author: catalinayepes
"""
import pandas as pd

df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
'B': ['B0', 'B1', 'B2', 'B3'],
'C': ['C0', 'C1', 'C2', 'C3'],
'D': ['D0', 'D1', 'D2', 'D3']},
index=[0, 1, 2, 3])

df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
'B': ['B4', 'B5', 'B6', 'B7'],
'C': ['C4', 'C5', 'C6', 'C7'],
'D': ['D4', 'D5', 'D6', 'D7']},
index=[4, 5, 6, 7])

df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
'B': ['B8', 'B9', 'B10', 'B11'],
'C': ['C8', 'C9', 'C10', 'C11'],
'D': ['D8', 'D9', 'D10', 'D11']},
index=[8, 9, 10, 11])

simple_concat = pd.concat([df1, df2]), df3])


append_columns = pd.concat([df1, df2, df3], axis=1, ignore_index=True)

test = df1.append([df2, df3], ignore_index=True)

df4 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3', 'A4'],
'second': ['B5', 'B7', 'B1', 'B3', 'B4'],
'third': ['C5', 'C7', 'C1', 'C3', 'C4'],})

empty_df = pd.DataFrame(columns={'A'})

simple_join = df1.join(df4, lsuffix='join')
join2 = df1.join(df2, lsuffix='join')


test2 = df1.append(df4)

test3 = pd.concat([df1, df2, df4], axis=1, ignore_index=True)

s1 = pd.Series(['X0', 'X1', 'X2', 'X3'], name='X')

test4 = pd.concat([df1, s1], axis=1)


simple_merge = pd.merge(df1, df4, how='outer', on=['A'])

test5 = pd.concat([simple_merge, s1], axis=1)


dfa = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
'B': ['B0', 'B1', 'B2', 'B3'],
'C': ['C0', 'C1', 'C2', 'C3'],
'D': ['D0', 'D1', 'D2', 'D3']},
index=['i0', 'i1', 'i2', 'i3'])

dfb = pd.DataFrame({'aa': ['A4', 'A5', 'A6', 'A7'],
'ab': ['B4', 'B5', 'B6', 'B7'],
'ac': ['C4', 'C5', 'C6', 'C7'],
'ad': ['D4', 'D5', 'D6', 'D7']},
index=['i0', 'i1', 'i6', 'i7'])
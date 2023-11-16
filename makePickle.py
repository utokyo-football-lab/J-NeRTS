import pandas as pd
import numpy as np
from collections import OrderedDict
import json
# df = pd.read_excel("raw_playlog_edited.xlsx", index_col=0)
# label = pd.read_pickle("prefecture_label.pkl")
# aaa = pd.DataFrame(np.array([["未進学", -1]]), columns=label.columns)
# label = pd.concat([aaa, label], axis=0)
# aaa = pd.DataFrame(np.array([["その他", -1]]), columns=label.columns)
# label = pd.concat([aaa, label], axis=0)

# label.reset_index(inplace=True, drop=True)
# column_tuples = [["", "", "", "", "", "youth", "youth", "youth", "college", "college", "college", "senior", "senior", "senior"],
#                  ["year", "name", "competition", "type", "category", "team", "region",
#                      "prefecture", "team", "region", "prefecture", "team", "region", "prefecture"]
#                  ]
# df = pd.DataFrame(df.values, columns=column_tuples)
# df.columns.names = ['1段目', '2段目']

# result_dict = {}
# aaa = df.columns.unique().to_list()
# bbb = df.index.to_list()

# region_id = {"北海道": "1", "東北": " 2", "北信越": "3", "関東": "4",
#              "東海": "5", "関西": "6", "中国": "7", "四国": "8", "九州": "9", "未進学": "-1", "その他": "-1"}
# category_id = {"ユース": "1", "街クラブ": "3", "高体連": "2", "その他": "-1"}
# type_id = {"大卒": "2", "高卒": "1"}
# competition_id = {"j1": "1", "j2": "2", "j3": "3"}

# for ccc in bbb:
#     result_dict[ccc] = dict()
#     for col_level_1 in aaa:
#         if len(col_level_1[0]) != 0:
#             if col_level_1[0] not in result_dict[ccc]:
#                 result_dict[ccc][col_level_1[0]] = dict()
#             result_dict[ccc][col_level_1[0]][col_level_1[1]
#                                              ] = df[col_level_1].values[ccc]
#         else:
#             result_dict[ccc][col_level_1[1]] = df[col_level_1].values[ccc]
#     result_dict[ccc]["youth"]["prefecture_id"] = label[label["prefecture_name"]
#                                                        == result_dict[ccc]["youth"]["prefecture"]].prefecture_id.values[0]
#     result_dict[ccc]["youth"]["region_id"] = region_id[result_dict[ccc]
#                                                        ["youth"]["region"]]
#     result_dict[ccc]["senior"]["prefecture_id"] = label[label["prefecture_name"]
#                                                         == result_dict[ccc]["senior"]["prefecture"]].prefecture_id.values[0]
#     result_dict[ccc]["senior"]["region_id"] = region_id[result_dict[ccc]
#                                                         ["senior"]["region"]]
#     result_dict[ccc]["college"]["prefecture_id"] = label[label["prefecture_name"]
#                                                          == result_dict[ccc]["college"]["prefecture"]].prefecture_id.values[0]
#     result_dict[ccc]["college"]["region_id"] = region_id[result_dict[ccc]
#                                                          ["college"]["region"]]
#     result_dict[ccc]["category_id"] = category_id[result_dict[ccc]["category"]]
#     result_dict[ccc]["type_id"] = type_id[result_dict[ccc]["type"]]
#     result_dict[ccc]["competition_id"] = competition_id[result_dict[ccc]["competition"]]

# print(result_dict)
# with open("J-NeRTS_20231003.json", mode="wt", encoding="utf-8") as f:
#     json.dump(result_dict, f, ensure_ascii=False, indent=2)

df = pd.read_json("J-NeRTS.json")
df = df.T

df['youth_team'] = df['youth'].apply(lambda x: x['team'])
df['youth_region'] = df['youth'].apply(lambda x: x['region'])
df['youth_prefecture'] = df['youth'].apply(lambda x: x['prefecture'])
df['youth_prefecture_id'] = df['youth'].apply(lambda x: x['prefecture_id'])
df['youth_region_id'] = df['youth'].apply(lambda x: x['region_id'])

df['senior_team'] = df['senior'].apply(lambda x: x['team'])
df['senior_region'] = df['senior'].apply(lambda x: x['region'])
df['senior_prefecture'] = df['senior'].apply(lambda x: x['prefecture'])
df['senior_prefecture_id'] = df['senior'].apply(lambda x: x['prefecture_id'])
df['senior_region_id'] = df['senior'].apply(lambda x: x['region_id'])

df['college_team'] = df['college'].apply(lambda x: x['team'])
df['college_region'] = df['college'].apply(lambda x: x['region'])
df['college_prefecture'] = df['college'].apply(lambda x: x['prefecture'])
df['college_prefecture_id'] = df['college'].apply(lambda x: x['prefecture_id'])
df['college_region_id'] = df['college'].apply(lambda x: x['region_id'])

df.drop(columns=['youth', "college", "senior"], inplace=True)

print(df)
df.to_pickle("J-NeRTS_20231003.pkl")

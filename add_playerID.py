import pandas as pd
import json

with open("J-NeRTS_old.json", mode="rt", encoding="utf-8") as f:
	data = json.load(f)	

df = pd.read_csv("raw_playlog.txt",dtype=str)
playerID=df["player_id"].values



print(playerID)
for (i,id)in zip(range(0,len(playerID)),playerID):
    data[str(i)]["player_id"]=id

with open("J-NeRTS.json", mode="wt", encoding="utf-8") as f:
	json.dump(data, f, ensure_ascii=False, indent=2)
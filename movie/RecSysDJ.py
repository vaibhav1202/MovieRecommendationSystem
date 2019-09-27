import pandas as pd
import os

def read_df():
    data_file = "data/u.data"
    data_file = os.path.dirname(__file__) + "/" + data_file    
    item_file = "data/u.item"
    item_file = os.path.dirname(__file__) + "/" + item_file    
    df = pd.read_csv(data_file, sep="\t", header=None, names=["user_id", "item_id", "rating", "nahi_pata"])
    df2 = pd.read_csv(item_file, sep="|",encoding="ISO-8859-1", header=None)
    df2 = df2[[0,1]]
    df2.columns = ["item_id", "title"]
    df = df.merge(df2, on="item_id")
    return df

def get_top_rated(df, thr=80, no=10):
    df3 = df.groupby("title").rating.mean()
    df4 = pd.DataFrame(df3)
    df4["no"] = df.groupby("title").rating.count()
    df5 = df4[df4["no"]>thr]
    return df5.sort_values(["rating"], ascending=[0]).head(no)


def get_most_reviewed_popu(df, no=10):
    df3 = df.groupby("title").rating.sum()
    df6 = pd.DataFrame(df3)
    df6["no"] = df.groupby("title").rating.count()
    maxno = df6["no"].max()
    df6["rating"] = df6["rating"]/maxno
    return df6.sort_values(["rating"], ascending=[0]).head(no)

def get_curated(df, thr=40, no=10):
    df3 = df.groupby("title").rating.mean()
    df7 = pd.DataFrame(df3)
    df7["no"] = df.groupby("title").rating.count()
    df8 = df7[df7["no"]>thr]
    maxno = df8["no"].max()
    df8["rating"] += df8["no"]/maxno - 0.5
    return df8.sort_values(["rating"], ascending=[0]).head(no)

def get_sim(df, movie_matrix, movie_name,thr=40,  no=10):    
    SW_user_rating = movie_matrix[movie_name]
    similar_to_sw=movie_matrix.corrwith(SW_user_rating)
    corr_SW = pd.DataFrame(similar_to_sw, columns=['correlation'])
    corr_SW.dropna(inplace=True)    
    dftemp = df.groupby("title").rating.count()
    dftemp = pd.DataFrame(dftemp)
    corr_SW.index.names = ["title"]
    print("="*50)
    print(corr_SW.head())
    print("="*50)
    print(dftemp.head())
    corr_SW = corr_SW.merge(dftemp, on="title")
    corr_SW = corr_SW[corr_SW['rating'] > thr]
    return corr_SW.sort_values(by='correlation', ascending=False).head(no)

def get_sim_users_reviews(df, movie_matrix, uid, thr= 20):
    SW_user_rating = movie_matrix.loc[uid]
    similar_to_sw=movie_matrix.corrwith(SW_user_rating, axis=1)
    similar_to_sw.head()
    corr_SW = pd.DataFrame(similar_to_sw, columns=['correlation'])
    corr_SW.dropna(inplace=True)
    coUsers = df.groupby("user_id").rating.count()
    coUsers = pd.DataFrame(coUsers)
    coUsers.columns = ["no"]
    coUsers.head()
    corr_SW = corr_SW.join(coUsers['no'])
    corr_SW = corr_SW[corr_SW['no'] > thr]
    corr_SW = corr_SW.sort_values(by='correlation', ascending=False)
    corr_SW = corr_SW[corr_SW['correlation'] > 0.5]
    corr_SW = corr_SW.sort_values(by='correlation', ascending=False)
    uids = corr_SW.index
    newDf = df[df.user_id.isin(uids)]
    return newDf

def get_sim_user_top_rated(df, movie_matrix, uid, thr=20):
    newDf = get_sim_users_reviews(df, movie_matrix, uid, thr=20)
    return get_top_rated(newDf, 10, 10)

def get_year_reviews(df, st_y, end_y):
    df['valid'] = df.title.apply(lambda x: (x.strip()[-5:-1]).isnumeric())
    newDf=df[df['valid']]
    newDf['year'] = newDf.title.apply(lambda x: int((x.strip()[-5:-1]))) 
    newDf=newDf[newDf['year']>=st_y]
    newDf=newDf[newDf['year']<=end_y]
    return newDf

def read_movie_matrix():
    data_file = "movie_matrix.csv"
    data_file = os.path.dirname(__file__) + "/" + data_file        
    movie_matrix = pd.read_csv(data_file)
    return movie_matrix

if __name__ == "__main__":
    df = read_df()
    movie_matrix = df.pivot_table(index='user_id', columns='title', values='rating')
    movie_matrix.to_csv("movie_matrix.csv")


# get_curated(df)
# get_most_reviewed_popu(df)
# get_top_rated(df, 80, 10)
# get_sim(movie_matrix, 'Star Wars (1977)', 40) #title
# get_sim_user_top_rated(df, movie_matrix, 1)  #apna id
# get_sim_users_reviews(df, movie_matrix, 1) #apna id
# newdf2 = get_year_reviews(df, 1998, 1998) #year st and end
# get_top_rated(newdf2, 10,10) 


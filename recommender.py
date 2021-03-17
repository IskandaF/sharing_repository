# from app import db
# from app.models import Profile, ProfileSchema, Idea, User, UserSchema, Connection
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from itertools import islice


sample_data="sample_data_Iskander.csv"
fake_users=pd.read_csv(sample_data)
example_user_id=1
connections=pd.read_csv("connections_data.csv")

# personality_weights={}

# 1. Query all profile
# 2. Put the profiles into the pandas dataset

# The


class Recommendation:
    def __init__(self,user_id):
        self.big5=["Extraversion","Agreeableness","Conscientiousness","Neuroticism","Openness"]
        importance_index={"Openness":0.9,"Extraversion":0.8,"Agreeableness":0.7,"Neuroticism":0.5,"Conscientiousness":0.4}
        diversity_inverse={"Openness":False,"Extraversion":False,"Agreeableness":False,"Neuroticism":True,"Conscientiousness":True}
        
        
        # self.
        self.df=fake_users
        self.connections=connections
        self.overall_scores={}
        self.user_id=user_id
        # users_list=Profile.query.all()
        # self.df=df = pd.read_sql(users_list.query, db)
    
    def get_recommendations_list(self,n):
        """
        input:the number of first elements
        outputs: sorted dictionary with similarity scores between target user and each other user
        """
        recommendation=self.main_recommender(self.user_id,self.overall_scores,self.df)
        print(recommendation)
        sorted_recommendation=self.sorted_dictionary(recommendation)
        print( sorted_recommendation)
        return self.take(n,sorted_recommendation.items())

    def take(self,n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, n))



    def sorted_dictionary(self,dictionary):

        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1],reverse=True)}
    def main_recommender(self,user_id,overall_scores,df):
        """
        input: user_id (integer), targeted_skills (list), personality_traits (dictionary)
        outputs: people suggestions as a dictionary with score
        """
    #   load the dataset 
        self.personality_language(df)
        self.skills_analyser(df)
        print(self.overall_scores)


        self.count_mutual_connections()
        
        return self.overall_scores


    def personality_language(self,df):
        """
        input: df (pandas dataframe), personality traits (list)
        outputs: dictionary {user_index:mean_difference}
        """
            # Cosine similarity
        user_qualities={}

        # Filling our user qualities
        for i in big5:
            user_qualities[i]=fake_users.loc[example_user_id][i]
        users_mean_difference=[]
        # Filling our user qualities

        # Creating the list for cosine difference    
        users_cosine_difference={}

        # Cosine difference algorithm
        for index, row in df.iterrows():

            if index!=example_user_id:
        #         print("Next User")
                mean_difference=0
                for i in big5:
                    else:
                    mean_difference+=abs(user_qualities[i]-row[i])
                    for s in big5:
#                         compare each trait to other trait to check the diversity 
                mean_difference/=len(big5)
                
                if i=="Neuroticism":
                    users_mean_difference.append([index,(mean_difference)])
                    self.overall_scores[index]=(mean_difference)*importance_index[i]
                else: 
                    users_mean_difference.append([index,(10-mean_difference)])
                    self.overall_scores[index]=(10-mean_difference)*importance_index[i]


            
            if row["Language"]!=df.loc[example_user_id]["Language"]:
                self.overall_scores[index]-=2
#         print(self.overall_scores)
        return self.overall_scores
    
    def skills_analyser(self,df):
        example_user_skills=fake_users.loc[example_user_id]["Skills"].split(",")
        # get the targeted skills lost
        targeted_skills=[]
        # Delet the final comma 
        del example_user_skills[-1]
        user_skills_list=[]
        for index,row in fake_users.iterrows():
    
            if index!=self.user_id:
                current_user_skills=row["Skills"].split(",")
                del current_user_skills[-1]
                similarities=set(example_user_skills) & set(current_user_skills)
                user_skills_list.append([index,len(similarities)])
                self.overall_scores[index]+=len(similarities)
        return self.overall_scores

    def count_mutual_connections(self):
        """
        input:user_id (integer), connections datafraem
        output: dictionary {user_index:number_of mutual connections}
        """


        user_connections=[]
        print(self.connections.head())


        for index, row in self.connections.iterrows():
            if row["connection_initiator"]==self.user_id and row["connection"]!=self.user_id:
                user_connections.append(row["connection"])
            if row["connection"]==self.user_id and row["connection_initiator"]!=self.user_id:
                user_connections.append(row["connection_initiator"])
            
        mutual_connections={}
        for index, row in self.connections.iterrows():
            for i in user_connections:
                if i==row["connection"] and i!=self.user_id and row["connection_initiator"]!=self.user_id:
                    try:
                        mutual_connections[row["connection_initiator"]]+=1
                    except KeyError:
                        mutual_connections[row["connection_initiator"]] =1
                if i==row["connection_initiator"] and i!=self.user_id and row["connection"]!=self.user_id:
                    try:
                        mutual_connections[row["connection"]]+=1
                    except KeyError:
                        mutual_connections[row["connection"]] = 1
        print(mutual_connections)
        for key,value in mutual_connections.items():
            # add all connections to the overall score
            if key<1000:
                self.overall_scores[key]+=value
        return (self.overall_scores)


recommender=Recommendation(example_user_id)
print(recommender.get_recommendations_list(5))
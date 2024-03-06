from CBR import *
df_problemes = pd.read_csv('data/problems4000_not_0_0_0.csv')
init_time = time()
rs = createRS(from_model= False, casebase=df_problemes)

rs.save('recomanador')



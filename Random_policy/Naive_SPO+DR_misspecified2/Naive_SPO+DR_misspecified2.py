from utility_functions_sgd import * 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge,Lasso
import mkl

mkl.set_num_threads(1)

def generate_data_interactive(noise_low,noise_high,B_true, n, p, v, polykernel_degree = 3, 
                              noise_half_width = 0.01, constant = 3):
    (d, _) = B_true.shape
    X = np.random.normal(size=(p, n))
    #X = np.random.randn(p, n)
    #X = np.random.uniform(0,2,size=(p,n))
    poly = PolynomialFeatures(degree = polykernel_degree, interaction_only = True, include_bias = False)
    X_new = np.transpose(poly.fit_transform(np.transpose(X)))
    
    c_expected = np.matmul(B_true, X_new) + constant 
    epsilon =  np.random.uniform(noise_low,noise_high,size=(d,n))
    c_observed = c_expected + epsilon

    X_true = np.concatenate((np.reshape(np.ones(n), (1, -1)), X_new), axis = 0)
    X_false=X_true[:6,:]
    
    Y_transpose_Z_observed=np.zeros((1,n))
    Y_transpose_Z_expected=np.zeros((1,n))
    Z=np.zeros((d,n))
    idxs_array=np.zeros((1,n))
    
    for i in range(n):
        idxs = np.random.randint(0, 70, size=1)
        temp_Y_transpose_Z_observed=np.dot(c_observed[:,i],feasible_vector[idxs[0]])
        temp_Y_transpose_Z_expected=np.dot(c_expected[:,i],feasible_vector[idxs[0]])
        Y_transpose_Z_observed[0,i]=temp_Y_transpose_Z_observed
        Y_transpose_Z_expected[0,i]=temp_Y_transpose_Z_expected
        Z[:,i]=feasible_vector[idxs[0]]
        idxs_array[0,i]=idxs
    return [X_false, X_true, c_observed, c_expected,Y_transpose_Z_observed,Y_transpose_Z_expected,Z,idxs_array]

n_train_seq = np.array([400,  600,  800,  1000, 1200, 1400, 1600])
#n_train_seq = np.array([400,  600])
n_holdout_seq = n_train_seq
n_train_max = 3000
n_holdout_max = 3000
n_test = 1000
runs = 50
n_jobs = 50

#numiter = 1000; batchsize = 10; long_factor = 1;

(A_mat, b_vec) = read_A_and_b()

(A_mat_new,b_vec_new)=read_A_and_b('A_and_b_new.csv')
feasible_matrix_row=pd.read_excel('feasible_matrix_row.xlsx',header=None)
feasible_matrix_column=pd.read_excel('feasible_matrix_column.xlsx',header=None)

#Removes all lines that are Nan
feasible_matrix_row=feasible_matrix_row.dropna(axis=0,how='all')
feasible_matrix_column=feasible_matrix_column.dropna(axis=0,how='all')

feasible_row=[]
feasible_column=[]
for i in range(70):
    feasible_row.append(feasible_matrix_row.iloc[5*i:5*i+5,:])
    feasible_column.append(feasible_matrix_column.iloc[4*i:4*i+4,:])

feasible_vector=[]
for i in range(70):
    temp_vector=np.zeros(40)
    temp_vector[0]=feasible_row[i].iloc[0,0]
    temp_vector[2]=feasible_row[i].iloc[0,1]
    temp_vector[4]=feasible_row[i].iloc[0,2]
    temp_vector[6]=feasible_row[i].iloc[0,3]
    temp_vector[9]=feasible_row[i].iloc[1,0]
    temp_vector[11]=feasible_row[i].iloc[1,1]
    temp_vector[13]=feasible_row[i].iloc[1,2]
    temp_vector[15]=feasible_row[i].iloc[1,3]
    temp_vector[18]=feasible_row[i].iloc[2,0]
    temp_vector[20]=feasible_row[i].iloc[2,1]
    temp_vector[22]=feasible_row[i].iloc[2,2]
    temp_vector[24]=feasible_row[i].iloc[2,3]
    temp_vector[27]=feasible_row[i].iloc[3,0]
    temp_vector[29]=feasible_row[i].iloc[3,1]
    temp_vector[31]=feasible_row[i].iloc[3,2]
    temp_vector[33]=feasible_row[i].iloc[3,3]
    temp_vector[36]=feasible_row[i].iloc[4,0]
    temp_vector[37]=feasible_row[i].iloc[4,1]
    temp_vector[38]=feasible_row[i].iloc[4,2]
    temp_vector[39]=feasible_row[i].iloc[4,3]
    temp_vector[1]=feasible_column[i].iloc[0,0]
    temp_vector[3]=feasible_column[i].iloc[0,1]
    temp_vector[5]=feasible_column[i].iloc[0,2]
    temp_vector[7]=feasible_column[i].iloc[0,3]
    temp_vector[8]=feasible_column[i].iloc[0,4]
    temp_vector[10]=feasible_column[i].iloc[1,0]
    temp_vector[12]=feasible_column[i].iloc[1,1]
    temp_vector[14]=feasible_column[i].iloc[1,2]
    temp_vector[16]=feasible_column[i].iloc[1,3]
    temp_vector[17]=feasible_column[i].iloc[1,4]
    temp_vector[19]=feasible_column[i].iloc[2,0]
    temp_vector[21]=feasible_column[i].iloc[2,1]
    temp_vector[23]=feasible_column[i].iloc[2,2]
    temp_vector[25]=feasible_column[i].iloc[2,3]
    temp_vector[26]=feasible_column[i].iloc[2,4]
    temp_vector[28]=feasible_column[i].iloc[3,0]
    temp_vector[30]=feasible_column[i].iloc[3,1]
    temp_vector[32]=feasible_column[i].iloc[3,2]
    temp_vector[34]=feasible_column[i].iloc[3,3]
    temp_vector[35]=feasible_column[i].iloc[3,4]
    feasible_vector.append(temp_vector)
    
#Check feasible vector
count=0
for i in range(70):
    if np.dot(A_mat,feasible_vector[i]).all()==b_vec.all():
        count=count+1
        #print(count)
Sigma_matrix=np.zeros((40,40))
for i in range(70):
    temp_matrix=np.outer(feasible_vector[i],feasible_vector[i])
    Sigma_matrix=Sigma_matrix+temp_matrix
    
Sigma_matrix=Sigma_matrix/70
rank = np.linalg.matrix_rank(Sigma_matrix)
print(rank)

p = 3
polykernel_degree = 3
grid_dim = 5
noise_half_width = 0.25
constant  = 3
verbose = False 
(A_mat, b_vec) = read_A_and_b()
(n_nodes, n_edges) = A_mat.shape
noise_high=0.5
noise_low=-0.5


X = np.random.normal(size=(p, 50))
poly = PolynomialFeatures(degree = polykernel_degree, interaction_only = True, include_bias = False)
X_new = np.transpose(poly.fit_transform(np.transpose(X)))
(p2, _) = X_new.shape

np.random.seed(18)
B_true = np.random.rand(n_edges, p2) 
data_train_1 = [generate_data_interactive(noise_low,noise_high,B_true, n_train_max, p, feasible_vector,polykernel_degree = polykernel_degree, noise_half_width = noise_half_width, constant = constant) for run in range(runs)]
data_holdout_1 = [generate_data_interactive(noise_low,noise_high,B_true, n_holdout_max, p, feasible_vector,polykernel_degree = polykernel_degree, noise_half_width = noise_half_width, constant = constant) for run in range(runs)]
data_test_1 = generate_data_interactive(noise_low,noise_high,B_true, n_test, p,feasible_vector, polykernel_degree = polykernel_degree, noise_half_width = noise_half_width, constant = constant) 

data_train_2 = [generate_data_interactive(noise_low,noise_high,B_true, n_train_max, p, feasible_vector,polykernel_degree = polykernel_degree, noise_half_width = noise_half_width, constant = constant) for run in range(runs)]
data_holdout_2 = [generate_data_interactive(noise_low,noise_high,B_true, n_holdout_max, p, feasible_vector,polykernel_degree = polykernel_degree, noise_half_width = noise_half_width, constant = constant) for run in range(runs)]
data_test_2 = generate_data_interactive(noise_low,noise_high,B_true, n_test, p,feasible_vector, polykernel_degree = polykernel_degree, noise_half_width = noise_half_width, constant = constant) 

data_test=[]
for i in range(len(data_test_1)):
  data_test.append(np.hstack((data_test_1[i],data_test_2[i])))

data_test_cost_exp=np.zeros((70,2*n_test))
for i in range(2*n_test):
    for j in range(70):
      data_test_cost_exp[j,i]=np.dot(data_test[3][:,i],feasible_vector[j])
data_test.append(data_test_cost_exp)

lambda_max = 100
num_lambda = 10
lambda_min_ratio = 1e-3
lambda_min = lambda_max*lambda_min_ratio
lambdas = np.exp(np.linspace(np.log(lambda_min), np.log(lambda_max), num = num_lambda))
lambdas = np.round(lambdas, 2)
lambdas = np.concatenate((np.array([0, 0.001, 0.01]), lambdas))
gammas = np.array([0.01, 0.1, 0.5, 1, 2])


output = "experiment_No_kernel.txt"
with open(output, 'w') as f:
    print("start", file = f)
    
################
#  No kernel  ##
################
with open(output, 'a') as f:
    print("################" , file = f)
    print("#  no_kernel   #", file = f)
    print("################" , file = f)

regret_all_Wrong_CDR = []
validation_all_Wrong_CDR = []
time_all_Wrong_CDR = []
loss_all_Wrong_CDR = []

regret_all_Wrong_IPW_Ideal_DR = []
validation_all_Wrong_IPW_Ideal_DR = []
time_all_Wrong_IPW_Ideal_DR = []
loss_all_Wrong_IPW_Ideal_DR = []

regret_all_CDR= []
validation_all_CDR = []
time_all_CDR = []
loss_all_CDR = []

regret_all_IPW_Ideal_DR= []
validation_all_IPW_Ideal_DR = []
time_all_IPW_Ideal_DR = []
loss_all_IPW_Ideal_DR = []

for i in range(len(n_train_seq)):

    n_train_true = n_train_seq[i]
    n_train = int(n_train_true/2)
    n_holdout_true = n_holdout_seq[i] 
    n_holdout = int(n_holdout_true/2)
    
    data_train_1_used=[[] for i in range(runs)]
    data_train_2_used=[[] for i in range(runs)]
    data_holdout_1_used=[[] for i in range(runs)]
    data_holdout_2_used=[[] for i in range(runs)]
    data_train=[[] for i in range(runs)]
    data_holdout=[[] for i in range(runs)]
    data_total=[[] for i in range(runs)]
    
    for k in range(runs):
        for i in range(len(data_train_1[k])):
            data_train_1_used[k].append(data_train_1[k][i][:,:n_train])
            data_train_2_used[k].append(data_train_2[k][i][:,:n_train])
            data_holdout_1_used[k].append(data_holdout_1[k][i][:,:n_holdout])
            data_holdout_2_used[k].append(data_holdout_2[k][i][:,:n_holdout])

    for k in range(runs):
        for i in range(len(data_train_1[k])):
            data_train[k].append(np.hstack((data_train_1_used[k][i],data_train_2_used[k][i])))
            data_holdout[k].append(np.hstack((data_holdout_1_used[k][i],data_holdout_2_used[k][i])))
    
    data_train_stratified=[[[] for l in range(70)] for i in range(runs)]
    for k in range(runs):
      unique, counts = np.unique(data_train[k][7], return_counts=True)
      if len(unique)==70:
           counts_new=counts
      else:
           counts_new=np.zeros(70)
           for m in range(len(unique)):
               counts_new[int(unique[m])]=counts[m]
      for m in range(70):
        for l in range(len(data_train[k])):
            (a,b)=data_train[k][l].shape
            temp_array=np.zeros((a,int(counts_new[m])))
            num=0
            for j in range(n_train_true):            
                if data_train[k][7][0,j]==m:
                   temp_array[:,num]=data_train[k][l][:,j]
                   num=num+1
            data_train_stratified[k][m].append(temp_array)
            
    for k in range(runs):
        temp_array_false=np.zeros((70,n_train_true))
        temp_array_true=np.zeros((70,n_train_true))
        for m in range(70):
              (a,b)=data_train_stratified[k][m][0].shape
              if b !=0:
                  X_False=data_train_stratified[k][m][0]
                  X_true=data_train_stratified[k][m][1]
                  Y=data_train_stratified[k][m][4]
                  False_model=LinearRegression(fit_intercept = False)
                  True_model=LinearRegression(fit_intercept = False)
                  False_model.fit(np.transpose(X_False), np.transpose(Y))
                  True_model.fit(np.transpose(X_true), np.transpose(Y))
                  c_hat_false=False_model.predict(np.transpose(data_train[k][0]))
                  c_hat_true=True_model.predict(np.transpose(data_train[k][1]))
                  c_hat_false=np.transpose(c_hat_false)
                  c_hat_true=np.transpose(c_hat_true)
                  temp_array_false[m,:]=c_hat_false
                  temp_array_true[m,:]=c_hat_true        
              else:
                  False_model=LinearRegression(fit_intercept = False)
                  True_model=LinearRegression(fit_intercept = False)
                  X_False=data_train[k][0]
                  X_true=data_train[k][1]
                  Y=data_train[k][4]
                  False_model.fit(np.transpose(X_False), np.transpose(Y))
                  True_model.fit(np.transpose(X_true), np.transpose(Y))
                  c_hat_false=False_model.predict(np.transpose(data_train[k][0]))
                  c_hat_true=True_model.predict(np.transpose(data_train[k][1]))
                  c_hat_false=np.transpose(c_hat_false)
                  c_hat_true=np.transpose(c_hat_true)
                  temp_array_false[m,:]=c_hat_false
                  temp_array_true[m,:]=c_hat_true 
        data_train[k].append(temp_array_false)
        data_train[k].append(temp_array_true)
        
        
    data_holdout_stratified=[[[] for l in range(70)] for i in range(runs)]
    for k in range(runs):
      unique, counts = np.unique(data_holdout[k][7], return_counts=True)
      if len(unique)==70:
           counts_new=counts
      else:
           counts_new=np.zeros(70)
           for m in range(len(unique)):
               counts_new[int(unique[m])]=counts[m]
      for m in range(70):
        for l in range(len(data_holdout[k])):
            (a,b)=data_holdout[k][l].shape
            temp_array=np.zeros((a,int(counts_new[m])))
            num=0
            for j in range(n_holdout_true):            
                if data_holdout[k][7][0,j]==m:
                   temp_array[:,num]=data_holdout[k][l][:,j]
                   num=num+1
            data_holdout_stratified[k][m].append(temp_array)
            
    for k in range(runs):
        temp_array_false=np.zeros((70,n_holdout_true))
        temp_array_true=np.zeros((70,n_holdout_true))
        
        for m in range(70):
              (a,b)=data_holdout_stratified[k][m][0].shape
              if b !=0:
                  X_False=data_holdout_stratified[k][m][0]
                  X_true=data_holdout_stratified[k][m][1]
                  Y=data_holdout_stratified[k][m][4]
                  False_model=LinearRegression(fit_intercept = False)
                  True_model=LinearRegression(fit_intercept = False)
                  False_model.fit(np.transpose(X_False), np.transpose(Y))
                  True_model.fit(np.transpose(X_true), np.transpose(Y))
                  c_hat_false=False_model.predict(np.transpose(data_holdout[k][0]))
                  c_hat_true=True_model.predict(np.transpose(data_holdout[k][1]))
                  c_hat_false=np.transpose(c_hat_false)
                  c_hat_true=np.transpose(c_hat_true)
                  temp_array_false[m,:]=c_hat_false
                  temp_array_true[m,:]=c_hat_true        
              else:
                  False_model=LinearRegression(fit_intercept = False)
                  True_model=LinearRegression(fit_intercept = False)
                  X_False=data_holdout[k][0]
                  X_true=data_holdout[k][1]
                  Y=data_holdout[k][4]
                  False_model.fit(np.transpose(X_False), np.transpose(Y))
                  True_model.fit(np.transpose(X_true), np.transpose(Y))
                  c_hat_false=False_model.predict(np.transpose(data_holdout[k][0]))
                  c_hat_true=True_model.predict(np.transpose(data_holdout[k][1]))
                  c_hat_false=np.transpose(c_hat_false)
                  c_hat_true=np.transpose(c_hat_true)
                  temp_array_false[m,:]=c_hat_false
                  temp_array_true[m,:]=c_hat_true
                  
        data_holdout[k].append(temp_array_false)
        data_holdout[k].append(temp_array_true)
        
    for k in range(runs):
        unique, counts = np.unique(data_train[k][7], return_counts=True)
        if len(unique)==70:
           IPW_score=counts/n_train_true
        else:
           IPW_score=0.00001*np.ones(70)
           for m in range(len(unique)):
               IPW_score[int(unique[m])]=counts[m]/n_train_true
        false_data_train_cost_hat=np.zeros((70,n_train_true))
        true_data_train_cost_hat=np.zeros((70,n_train_true))
        false_data_train_cost_ideal_hat=np.zeros((70,n_train_true))
        true_data_train_cost_ideal_hat=np.zeros((70,n_train_true))
        for j in range(n_train_true):
            false_data_train_cost_hat[int(data_train[k][7][0,j]),j]=(data_train[k][4][0,j]-data_train[k][8][int(data_train[k][7][0,j]),j])/IPW_score[int(data_train[k][7][0,j])]
            true_data_train_cost_hat[int(data_train[k][7][0,j]),j]=(data_train[k][4][0,j]-data_train[k][9][int(data_train[k][7][0,j]),j])/IPW_score[int(data_train[k][7][0,j])]
            false_data_train_cost_ideal_hat[int(data_train[k][7][0,j]),j]=70*(data_train[k][4][0,j]-data_train[k][8][int(data_train[k][7][0,j]),j])
            true_data_train_cost_ideal_hat[int(data_train[k][7][0,j]),j]=70*(data_train[k][4][0,j]-data_train[k][9][int(data_train[k][7][0,j]),j])
        data_train[k].append(false_data_train_cost_hat)
        data_train[k].append(true_data_train_cost_hat)
        data_train[k].append(false_data_train_cost_ideal_hat) 
        data_train[k].append(true_data_train_cost_ideal_hat) 
     
    for k in range(runs):
        unique, counts = np.unique(data_holdout[k][7], return_counts=True)
        if len(unique)==70:
           IPW_score=counts/n_train_true
        else:
           IPW_score=0.00001*np.ones(70)
           for m in range(len(unique)):
               IPW_score[int(unique[m])]=counts[m]/n_holdout_true
        false_data_holdout_cost_hat=np.zeros((70,n_holdout_true))
        true_data_holdout_cost_hat=np.zeros((70,n_holdout_true))
        false_data_holdout_cost_ideal_hat=np.zeros((70,n_holdout_true))
        true_data_holdout_cost_ideal_hat=np.zeros((70,n_holdout_true))
        for j in range(n_holdout_true):
            false_data_holdout_cost_hat[int(data_holdout[k][7][0,j]),j]=(data_holdout[k][4][0,j]-data_holdout[k][8][int(data_holdout[k][7][0,j]),j])/IPW_score[int(data_holdout[k][7][0,j])]
            true_data_holdout_cost_hat[int(data_holdout[k][7][0,j]),j]=(data_holdout[k][4][0,j]-data_holdout[k][9][int(data_holdout[k][7][0,j]),j])/IPW_score[int(data_holdout[k][7][0,j])]
            false_data_holdout_cost_ideal_hat[int(data_holdout[k][7][0,j]),j]=70*(data_holdout[k][4][0,j]-data_holdout[k][8][int(data_holdout[k][7][0,j]),j])
            true_data_holdout_cost_ideal_hat[int(data_holdout[k][7][0,j]),j]=70*(data_holdout[k][4][0,j]-data_holdout[k][9][int(data_holdout[k][7][0,j]),j])
        data_holdout[k].append(false_data_holdout_cost_hat)
        data_holdout[k].append(true_data_holdout_cost_hat)
        data_holdout[k].append(false_data_holdout_cost_ideal_hat) 
        data_holdout[k].append(true_data_holdout_cost_ideal_hat) 
   
    for k in range(runs):        
        train_DR_array_false_Sample_IPW=data_train[k][10]+data_train[k][8]
        train_DR_array_false_Ideal_IPW=data_train[k][12]+data_train[k][8]
        train_DR_array_true_Sample_IPW=data_train[k][11]+data_train[k][9]
        train_DR_array_true_Ideal_IPW=data_train[k][13]+data_train[k][9]
        
        data_train[k].append(train_DR_array_false_Sample_IPW)
        data_train[k].append(train_DR_array_false_Ideal_IPW)
        data_train[k].append(train_DR_array_true_Sample_IPW)
        data_train[k].append(train_DR_array_true_Ideal_IPW)
        
        holdout_DR_array_false_Sample_IPW=data_holdout[k][10]+data_holdout[k][8]
        holdout_DR_array_false_Ideal_IPW=data_holdout[k][12]+data_holdout[k][8]
        holdout_DR_array_true_Sample_IPW=data_holdout[k][11]+data_holdout[k][9]
        holdout_DR_array_true_Ideal_IPW=data_holdout[k][13]+data_holdout[k][9]
        
        data_holdout[k].append(holdout_DR_array_false_Sample_IPW)
        data_holdout[k].append(holdout_DR_array_false_Ideal_IPW)
        data_holdout[k].append(holdout_DR_array_true_Sample_IPW)
        data_holdout[k].append(holdout_DR_array_true_Ideal_IPW)
        
    with open(output, 'a') as f:
        print("n_train", n_train_true, file = f)
        print("n_train", n_train_true)
    time1 = time.time()

    res_temp = Parallel(n_jobs = n_jobs, verbose = 3)(delayed(replication_no_kernel)(
                            A_mat_new, b_vec_new, B_true, 
                            data_train[run][0][:, :n_train_true], data_train[run][1][:, :n_train_true], data_train[run][14][:, :n_train_true], data_train[run][14][:, :n_train_true],
                            data_holdout[run][0][:, :n_holdout_true], data_holdout[run][1][:, :n_holdout_true], data_holdout[run][14][:, :n_holdout_true], data_holdout[run][14][:, :n_holdout_true],
                            data_test[0], data_test[1], data_test[2], data_test[8],
                            # numiter = numiter, batchsize = batchsize, long_factor = long_factor,
                            #   loss_stop = loss_stop, tol = tol, stop = stop,
                            gammas = gammas, lambdas = lambdas, lambda_max = None, lambda_min_ratio = None, num_lambda = None,
                            verbose = verbose) for run in range(runs))
    
    regret_temp = [res_0[0] for res_0 in res_temp]
    regret_temp = [pd.DataFrame(res_0, index = [0]) for res_0 in regret_temp]
    regret_temp = pd.concat(regret_temp)
    
    validation_temp = [res_0[1] for res_0 in res_temp]
    validation_temp = [pd.DataFrame(res_0, index = [0]) for res_0 in validation_temp]
    validation_temp = pd.concat(validation_temp)
    
    time_temp = [res_0[2] for res_0 in res_temp]
    time_temp= [pd.DataFrame(res_0, index = [0]) for res_0 in time_temp]
    time_temp = pd.concat(time_temp)
    
    loss_temp = [res_0[3] for res_0 in res_temp]
    
    regret_temp["n"] = n_train_true
    validation_temp["n"] = n_train_true
    time_temp["n"] = n_train_true
    
    with open(output, 'a') as f:
        print("Wrong CDR")
        print("Wrong CDR", file = f)
        print("total time: ", time.time() - time1, file = f)
        print("seperate time", file = f)
        print(time_temp.mean(), file = f)
        print("-------", file = f)
        print("mean regret: ", file = f)
        print(regret_temp.mean(), file = f)      
        print("-------", file = f)
        print("        ", file = f)
        print("        ", file = f)
        
    regret_all_Wrong_CDR.append(regret_temp)
    validation_all_Wrong_CDR.append(validation_temp)
    time_all_Wrong_CDR.append(time_temp)
    loss_all_Wrong_CDR.append(loss_temp)
    
    pd.concat(regret_all_Wrong_CDR).to_csv("regret_no_kernel_Wrong_CDR.csv", index = False)
    pd.concat(validation_all_Wrong_CDR).to_csv("validation_no_kernel_Wrong_CDR.csv", index = False)
    pd.concat(time_all_Wrong_CDR).to_csv("time_no_kernel_Wrong_CDR.csv", index = False)
    pickle.dump(loss_all_Wrong_CDR, open("loss_no_kernel_Wrong_CDR.pkl", "wb"))
    
    with open(output, 'a') as f:
        print("n_train", n_train_true, file = f)
        print("n_train", n_train_true)
    time1 = time.time()

    res_temp = Parallel(n_jobs = n_jobs, verbose = 3)(delayed(replication_no_kernel)(
                            A_mat_new, b_vec_new, B_true, 
                            data_train[run][0][:, :n_train_true], data_train[run][1][:, :n_train_true], data_train[run][16][:, :n_train_true], data_train[run][16][:, :n_train_true],
                            data_holdout[run][0][:, :n_holdout_true], data_holdout[run][1][:, :n_holdout_true], data_holdout[run][16][:, :n_holdout_true], data_holdout[run][16][:, :n_holdout_true],
                            data_test[0], data_test[1], data_test[2], data_test[8],
                            # numiter = numiter, batchsize = batchsize, long_factor = long_factor,
                            #   loss_stop = loss_stop, tol = tol, stop = stop,
                            gammas = gammas, lambdas = lambdas, lambda_max = None, lambda_min_ratio = None, num_lambda = None,
                            verbose = verbose) for run in range(runs))
    
    regret_temp = [res_0[0] for res_0 in res_temp]
    regret_temp = [pd.DataFrame(res_0, index = [0]) for res_0 in regret_temp]
    regret_temp = pd.concat(regret_temp)
    
    validation_temp = [res_0[1] for res_0 in res_temp]
    validation_temp = [pd.DataFrame(res_0, index = [0]) for res_0 in validation_temp]
    validation_temp = pd.concat(validation_temp)
    
    time_temp = [res_0[2] for res_0 in res_temp]
    time_temp= [pd.DataFrame(res_0, index = [0]) for res_0 in time_temp]
    time_temp = pd.concat(time_temp)
    
    loss_temp = [res_0[3] for res_0 in res_temp]
    
    regret_temp["n"] = n_train_true
    validation_temp["n"] = n_train_true
    time_temp["n"] = n_train_true
    
    with open(output, 'a') as f:
        print("True CDR")
        print("True CDR", file = f)
        print("total time: ", time.time() - time1, file = f)
        print("seperate time", file = f)
        print(time_temp.mean(), file = f)
        print("-------", file = f)
        print("mean regret: ", file = f)
        print(regret_temp.mean(), file = f)      
        print("-------", file = f)
        print("        ", file = f)
        print("        ", file = f)
        
    regret_all_CDR.append(regret_temp)
    validation_all_CDR.append(validation_temp)
    time_all_CDR.append(time_temp)
    loss_all_CDR.append(loss_temp)
    
    pd.concat(regret_all_CDR).to_csv("regret_no_kernel_CDR.csv", index = False)
    pd.concat(validation_all_CDR).to_csv("validation_no_kernel_CDR.csv", index = False)
    pd.concat(time_all_CDR).to_csv("time_no_kernel_CDR.csv", index = False)
    pickle.dump(loss_all_CDR, open("loss_no_kernel_CDR.pkl", "wb"))


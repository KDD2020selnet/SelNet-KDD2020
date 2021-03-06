import sys
import numpy as np

#cid = int(sys.argv[1])

real_data_file = sys.argv[1]
data_file = sys.argv[2]
label_file = sys.argv[3]
output_file = sys.argv[4]

real_data = np.load(real_data_file)

data_num = real_data.shape[0]

# read original data
#data_file = '../../training_feats/glove_50_trainingFeats_part' + str(cid) + '_d64_binary_codes.npy'
#data_file = '../../training_feats/face_d128_2M_trainingFeats_part' + str(cid) + '.txt.npy'
data = np.load(data_file)

x_dim = data.shape[1]

print("Shape : ", data.shape)

#label_file = '../../raw_labels/face_d128_2M_trainingFeats_smallSel_part' + str(cid) + '_rawLabels.npy'
labels = np.load(label_file)

#print(labels[0], labels[1], len(labels))

selectivity = np.geomspace(0.0001, 1, 40)

tau_max_per_record = len(selectivity)

# save mixlabels file
data_mixlabels = np.zeros((data.shape[0] * tau_max_per_record, data.shape[1] + 1 + 1))

sc_f = []

selected_tau = 3

for rid in range(data.shape[0]):
    r_ = data[rid]
    np.random.seed(rid)
    sc_ = np.random.choice(tau_max_per_record, selected_tau, replace=False)
    t_max_script = np.max(sc_)
    for i in range(t_max_script):
        tau = labels[rid, i]
        _label = int(data_num * selectivity[i] / 100)
        if (_label - 1) < 0:
            _label = 1
        
        data_mixlabels[rid * tau_max_per_record + i, :x_dim] = data[rid]
        data_mixlabels[rid * tau_max_per_record + i, x_dim] = tau
        data_mixlabels[rid * tau_max_per_record + i, x_dim + 1] = _label
        sc_f.append(rid * tau_max_per_record + i)    

data_mixlabels = np.array(data_mixlabels, dtype=np.float32)
data_mixlabels = data_mixlabels[sc_f]

data_mixlabels = np.unique(data_mixlabels, axis=0)

#output_file = '../data-mixlabels/face_d128_2M_trainingDataL_smallSel_part' + str(cid) + '-mixlabels.txt'

np.save(output_file, data_mixlabels)


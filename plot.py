#!/usr/bin/python 
import sys
import matplotlib.pyplot as plt
import os

def plot(plt,fig_num,subplot_num,data,title,l,h):
    plt.figure(fig_num)
    plt.subplot(subplot_num)
    plt.plot(data)
    plt.title(title)
    plt.ylim((l,h))

fname = sys.argv[1]

max_num_events = 60

fs = []
if os.path.isdir(fname):
    for f in os.listdir(fname):
        fs.append(open(os.path.join(fname,f)))
elif os.path.isfile(fname):
        in_file = open(fname)
        fs.append(in_file)

f_num = 0

for f in fs:
    document_result_mode = True
    header = []
    all_scores = []

    print 'Processing '+f.name
    for line in f:
        if "Document results" in line:
            document_result_mode = True
        elif document_result_mode :
            nl = f.next()
            if "Final Results" in nl or "Final Results" in line:
                break
            header = line.rstrip().split("\t")
            scores = nl.rstrip().split("\t")
            all_scores.append(scores)
            
    scores_inv = [[] for _ in xrange(len(header))]
    for scores in all_scores:
        for index,score in enumerate(scores):
            scores_inv[index].append(score)

    print 'Plotting'

    fig_counts = plt.figure(f_num + 1)
    plt.title('Counts')
    fig_counts.tight_layout()

    fig_f = plt.figure(f_num + 2)
    plt.title('P,R,F-1')
    fig_f.tight_layout()

    fig_type = plt.figure(f_num + 3)
    plt.title('Mention type, Realis type')
    fig_type.tight_layout()

    for h,ss in zip(header , scores_inv):
        if h == 'TP':
            plot(plt,f_num + 1,221,ss,h,0,max_num_events)
            plot(plt,f_num + 1,224,ss,h,0,max_num_events)
        if h == 'FP':
            plot(plt,f_num + 1,222,ss,h,0,max_num_events)
            plot(plt,f_num + 1,224,ss,h,0,max_num_events)
        if h == '#Gold':
            plot(plt,f_num + 1,223,ss,h,0,max_num_events)
            plot(plt,f_num + 1,224,ss,'Combined',0,max_num_events)
        if h == 'Prec':
            plot(plt,f_num + 2,221,ss,h,0,1.2)
            plot(plt,f_num + 2,224,ss,h,0,1.2)
        if h == 'Recall':
            plot(plt,f_num + 2,222,ss,h,0,1.2)
            plot(plt,f_num + 2,224,ss,h,0,1.2)
        if h == 'F1':
            plot(plt,f_num + 2,223,ss,h,0,1.2)
            plot(plt,f_num + 2,224,ss,'Combined',0,1.2)
        if h == 'Type':
            plot(plt,f_num + 3,311,ss,h,0,1.2)
            plot(plt,f_num + 3,313,ss,h,0,1.2)
        if h == 'Realis':
            plot(plt,f_num + 3,312,ss,h,0,1.2)
            plot(plt,f_num + 3,313,ss,'Combined',0,1.2)

    plt.figure(f_num + 1)
    plt.savefig(f.name+'_counts.png', bbox_inches='tight')
    plt.figure(f_num + 2)
    plt.savefig(f.name+'_PRF.png', bbox_inches = 'tight')
    plt.figure(f_num + 3)
    plt.savefig(f.name+'_mentoin_realis.png', bbox_inches = 'tight')

    f_num += 3

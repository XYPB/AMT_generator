import numpy as np
import os
import string

import argparse
from IPython import embed

def error(str):
	print(str)

def fileread(str,breakcode='[[BR]]'):
	fid = open(str,'r')
	a = fid.readlines()
	fid.close()
	return breakcode.join(a)

def getOpts(expt_name):
	opt = getDefaultOpts()
	if expt_name=='example_expt':
		opt['which_algs_paths'] = ['my_alg','baseline_alg']
		opt['Nimgs'] = 1000
		opt['ut_id'] = 'unset' # set this using http://uniqueturker.myleott.com/
		opt['base_url'] = 'https://www.mywebsite.com/example_expt_data/'
		opt['instructions_file'] = './instructions_basic.html'
		opt['short_instructions_file'] = './short_instructions_basic.html'
		opt['consent_file'] = './consent_basic.html'
		opt['use_vigilance'] = False
		opt['paired'] = True
	elif expt_name == 'no_aug_test':
		opt['which_algs_paths'] = [
			"CondAVTransformer_VNet_randshift_2s_no_aug_GH_vqgan_no_earlystop",
		]		 # paths to images generated by algoritms, e.g. {'my_alg','baseline_alg'}
	else:
		# error('no opts defined for experiment %s'%expt_name)
		pass
	opt['expt_name'] = expt_name

	return opt

# All algorithms:
# "CondAVTransformer_VNet_randshift_2s_dropcond_GH_vqgan", "CondAVTransformer_VNet_randshift_2s_GH_vqgan", "CondAVTransformer_VNet_randshift_2s_outside_cond_GH_vqgan", "condition", "target", "CondAVTransformer_VNet_randshift_2s_dropcondvis_GH_vqgan", "CondAVTransformer_VNet_randshift_2s_no_aug_GH_vqgan", "CondAVTransformer_VNet_randshift_2s_style_transfer_GH_vqgan", "onset_baseline"

def getDefaultOpts():
	opt = {}
	opt['expt_name'] = 'unset'
	
	opt['which_algs_paths'] = [
		"onset_baseline", "CondAVTransformer_VNet_randshift_2s_style_transfer_GH_vqgan", "Taming_pretrained",
		"CondAVTransformer_VNet_randshift_2s_dropcond_GH_vqgan_no_earlystop", "CondAVTransformer_VNet_randshift_2s_outside_cond_GH_vqgan_no_earlystop",
		"CondAVTransformer_VNet_randshift_2s_dropcondvis_GH_vqgan_no_earlystop", "CondAVTransformer_VNet_randshift_2s_no_aug_GH_vqgan_no_earlystop",
	]		 # paths to images generated by algoritms, e.g. {'my_alg','baseline_alg'}
	opt['vigilance_path'] = 'vigilance'	   # path to vigilance images
	opt['gt_path'] = 'CondAVTransformer_VNet_randshift_2s_GH_vqgan_no_earlystop'					 # path to gt images
	opt['Nimgs'] = 582						# number of images to test
	opt['Npairs'] = 21						# number of paired comparisons per HIT
	opt['Npractice'] = 5					 # number of practice trials per HIT (number of non-practice trials is opt['Npairs']-opt['Npractice'])
	opt['Nhits'] = 200				 # number of HITs per algorithm
	opt['vigilance_freq'] = 0.05 		   # percent of trials that are vigilance tests
	opt['vigilance_idx'] = [133]
	opt['use_vigilance'] = True			   # include vigilance trials (obviously fake images to check that Turkers are paying attention)	
	opt['ut_id'] = '75ba230549ba66f94106fbb9b4e8a846'					# set this using http://uniqueturker.myleott.com/
	opt['base_url'] = 'https://github.com/XYPB/AMT_test_data/raw/master/'				 # url where images to test are accessible as "opt['base_url']/n.png", for integers n
	opt['instructions_file'] = 'instructions_basic.html'		# instructions appear at the beginning of the HIT
	opt['short_instructions_file'] = 'short_instructions_basic.html'  # short instructions are shown at the top of every trial
	opt['consent_file'] = 'consent_basic.html'			 # informed consent text appears the beginning of the HIT
	opt['im_height'] = 200					# dimensions at which to display the stimuli
	opt['im_width'] = 400					 #
	opt['paired'] = True					  # if True, then fake/n.jpg will be pitted against real/n.jpg; if false, fake/n.jpg will be pitted against real/m.jpg, for random n and m
	opt['filename'] = lambda x : '%i.mp4'%x

	return opt

def checkOpts(opt):
	if(opt['which_algs_paths']=='unset'):
		error('must provide a list of algorithms to test')
	if(opt['ut_id']=='unset'):
		error('must set a unique id for this HIT using http://uniqueturker.myleott.com/')
	if(opt['base_url']=='unset'):
		error('must provide a url where test images are accessible')
	if(opt['instructions_file']=='unset'):
		error('must provide a file containing html formatted instructions to display once at start of experiment')
	if(opt['short_instructions_file']=='unset'):
		error('must provide a file containing html formatted instructions to display on each trial')
	if(opt['consent_file']=='unset'):
		error('must provide a file containing html formatted infromed consent test, display at start of experiment')


def mk_expt(expt_name):
	# expt parameters
	opt = getOpts(expt_name)
	
	# check parameters
	checkOpts(opt)
	
	# make dir for expt, overwriting if it already exists
	if(os.path.exists(opt['expt_name'])):
		os.system('rm -r ./%s'%opt['expt_name'])
	os.mkdir(opt['expt_name'])
	
	# rng('shuffle')
	csv_fname = os.path.join(opt['expt_name'],'expt_input_data.csv')
	
	# make header
	head_algo_A = []
	head_algo_B = []
	head_target = []
	head_condition = []
	head_images_A = []
	head_images_B = []
	
	for i in range(opt['Npairs']):
		head_algo_A.append('algo_A%d'%i)
		head_algo_B.append('algo_B%d'%i)
		head_target.append('target%d'%i)
		head_condition.append('condition%d'%i)
		head_images_A.append('image_A%d'%i)
		head_images_B.append('image_B%d'%i)
	head_algo_A = [head_algo_A,]
	head_algo_B = [head_algo_B,]
	head_target = [head_target,]
	head_condition = [head_condition,]
	head_images_A = [head_images_A,]
	head_images_B = [head_images_B,]

	A = len(opt['which_algs_paths'])
	H = opt['Nhits'] # number of hits
	I = opt['Nimgs']
	N = opt['Npairs'] # number of images per hit

	which_alg = np.random.randint(A, size=H*N)
	which_ind0 = np.random.randint(I, size=H*N)
	which_ind1 = which_ind0 if(opt['paired']) else np.random.randint(I, size=H*N)
	which_side = np.random.randint(2, size=H*N)
	vigilance = np.random.randint(opt['Npractice'], N, size=H)
	print(np.unique(which_alg, return_counts=True))

	algo_A = []
	algo_B = []
	target_video = []
	condition_video = []
	image_A = []
	image_B = []
	for (nn, data) in enumerate(zip(which_alg,which_ind0,which_ind1,which_side)):
		cur_which_alg, cur_which_ind0, cur_which_ind1, cur_which_side = data
		idx = nn % N
		h = int(nn // N)
		if idx == vigilance[h]:
			vigilance_idx = opt['vigilance_idx'][np.random.randint(len(opt['vigilance_idx']))]
			target_video.append(('target/'+opt['filename'](vigilance_idx)))
			condition_video.append(('vigilance_cond/'+opt['filename'](vigilance_idx)))
			if (cur_which_side==0):
				algo_A.append('CondAVTransformer_VNet_randshift_2s_GH_vqgan')
				algo_B.append(opt['vigilance_path'])
				image_A.append(('target_sound/'+opt['filename'](vigilance_idx)))
				image_B.append(('%s/'+opt['filename'](vigilance_idx))%opt['vigilance_path'])
			else:
				algo_A.append(opt['vigilance_path'])
				algo_B.append('CondAVTransformer_VNet_randshift_2s_GH_vqgan')
				image_A.append(('%s/'+opt['filename'](vigilance_idx))%opt['vigilance_path'])
				image_B.append(('target_sound/'+opt['filename'](vigilance_idx)))
			continue

		cur_alg_name = opt['which_algs_paths'][cur_which_alg]
		target_video.append(('target/'+opt['filename'](cur_which_ind0 % 194)))
		condition_video.append(('condition/'+opt['filename'](cur_which_ind0)))
		if(cur_which_side==0):
			algo_A.append('CondAVTransformer_VNet_randshift_2s_GH_vqgan')
			algo_B.append(cur_alg_name)
			if "Taming" in cur_alg_name:
				cur_which_ind1 = cur_which_ind1 % 194
			image_A.append(('%s/'+opt['filename'](cur_which_ind0))%opt['gt_path'])
			image_B.append(('%s/'+opt['filename'](cur_which_ind1))%cur_alg_name)
		else:
			algo_A.append(cur_alg_name)
			algo_B.append('CondAVTransformer_VNet_randshift_2s_GH_vqgan')
			if "Taming" in cur_alg_name:
				cur_which_ind0 = cur_which_ind0 % 194
			image_A.append(('%s/'+opt['filename'](cur_which_ind0))%cur_alg_name)
			image_B.append(('%s/'+opt['filename'](cur_which_ind1))%opt['gt_path'])

	algo_A = np.array(algo_A).reshape((H,N))
	algo_B = np.array(algo_B).reshape((H,N))
	target_video = np.array(target_video).reshape((H,N))
	condition_video = np.array(condition_video).reshape((H,N))
	image_A = np.array(image_A).reshape((H,N))
	image_B = np.array(image_B).reshape((H,N))

	head_algo_A = np.array(head_algo_A)
	head_algo_B = np.array(head_algo_B)
	head_target = np.array(head_target)
	head_condition = np.array(head_condition)
	head_images_A = np.array(head_images_A)
	head_images_B = np.array(head_images_B)

	csv_out = np.concatenate((np.concatenate((head_algo_A, head_algo_B, head_target, head_condition, head_images_A, head_images_B),axis=1),
		np.concatenate((algo_A, algo_B, target_video, condition_video, image_A, image_B),axis=1)),axis=0)

	fid = open(csv_fname,'w')
	for i in range(csv_out.shape[0]):
		for j in range(csv_out.shape[1]-1):
			fid.write(csv_out[i,j]+',')
		fid.write(csv_out[i,-1])
		fid.write('\n')
	fid.close()
	
	breakcode='[[BR]]'

	# html code generator
	# embed()
	html = fileread('index_template.html',breakcode=breakcode)
	
	html = html.replace('{{UT_ID}}', opt['ut_id'])
	html = html.replace('{{BASE_URL}}', opt['base_url'])
	
	html = html.replace('{{INSTRUCTIONS}}', fileread(opt['instructions_file'],breakcode=breakcode))
	html = html.replace('{{SHORT_INSTRUCTIONS}}', fileread(opt['short_instructions_file'],breakcode=breakcode))
	html = html.replace('{{CONSENT}}', fileread(opt['consent_file'],breakcode=breakcode))
	
	html = html.replace('{{IM_DIV_HEIGHT}}', '%i'%(opt['im_height']+2))
	html = html.replace('{{IM_DIV_WIDTH}}', '%i'%(opt['im_width']+2))
	html = html.replace('{{IM_HEIGHT}}', '%i'%(opt['im_height']))
	html = html.replace('{{IM_WIDTH}}', '%i'%(opt['im_width']))
	
	html = html.replace('{{N_PRACTICE}}', '%i'%(opt['Npractice']))
	html = html.replace('{{TOTAL_NUM_IMS}}', '%i'%(opt['Npairs']))
	
	s = ('').join(['sequence_helper("${algo_A%d}","${algo_B%d}","${target%d}","${condition%d}","${image_A%d}","${image_B%d}");\n'%(i,i,i, i,i,i) for i in range(opt['Npairs'])])
	html = html.replace('{{SEQUENCE}}', s)

	s = []
	s = ('').join(['<input type="hidden" name="selection_sync%d" id="selection_sync%d" value="unset">\n<input type="hidden" name="selection_timbre%d" id="selection_timbre%d" value="unset">\n'%(i,i,i,i) for i in range(opt['Npairs'])])
	html = html.replace('{{SELECTION}}', s)
	
	fid = open(os.path.join(opt['expt_name'],'index.html'),'w')
	fid.writelines(html.split(breakcode))
	fid.close()




parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-n','--name', type=str, default='experiments name')
parser.add_argument('-u','--unique_worker', type=str, default='75ba230549ba66f94106fbb9b4e8a846')

args = parser.parse_args()
mk_expt(args.name)


from xrootdpyfs import XRootDPyFS
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser
from tqdm import tqdm
import sys
import os
import subprocess

# CMSSW_10_6_18 is used to develop this script

# Usage: python xrootdcp.py [source site] [source folder] [target folder] [sample folder] (-n [nCPUs], -f[fullpath])
# Note: Please setup the cms software and request the proxy before using this code
# some transfer examples:

# Find the newest directroy to transfer automatically
# python xrootdcp.py -n 10 NCHC /store/group/phys_smp/ggNtuples/13TeV/mc/V09_04_13_04/job_fall17_gjet_pt40_MGG_80toInf /data6/ggNtuples/V10_02_10_05 job_fall17_gjet_pt40_MGG_80toInf

# Determine which directory you want to transfer by yourself
# python xrootdcp.py -n 10 NCHC /store/group/phys_smp/ggNtuples/13TeV/mc/V09_04_13_04/job_fall17_gjet_pt40_MGG_80toInf/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/crab_job_fall17_gjet_pt40_MGG_80toInf/210412_010358/0000 /data6/ggNtuples/V10_02_10_05 job_fall17_gjet_pt40_MGG_80toInf -f True

def get_parser():
    parser = ArgumentParser(description = "This program can be used to transfer samples from a XRootD directory to local via xrdcp.")
    parser.add_argument("site", help = "name of the remote site (EOS, NCHC, ..)", type = str)
    parser.add_argument("source", help = "remote path to the sample (/store/....)", type = str)
    parser.add_argument("target", help = "local path for the sample", type = str)
    parser.add_argument("sample", help = "name of the sample", type = str)
    parser.add_argument("-n", "--nCPU", default = 10, help = "the number of CPUs you want to use to transfer the files (default value: 10)", type = int)
    parser.add_argument("-f", "--fullpath", default = False, help = "use full remote path to the smaple or not", type = bool)

    return parser

def listdir(dir):
    filelist, tmplist = [], []
    for i in range(0, 4): # there are 3 layers after the directory of the sample name (crab defult?)
        lsInfo = subprocess.check_output("xrdfs %s ls %s" %(siteInfo[site][0], dir), shell = True)
        lsInfo_list = lsInfo.split("\n")
        del lsInfo_list[-1]
        
        if (len(lsInfo_list) == 1):
            dir = lsInfo_list[0]
        if (i == 2 and len(lsInfo_list) != 1): # find the newest directory
            Time = []
            for j in lsInfo_list:
                tlist = j.split("/")
                time = int(tlist[-1].replace("_", ""))
                Time.append(time)
            if len(Time) == 0:
                print("[ERROR] Empty directory: %s" %(dir))
                print(">>> NULL return from the command: xrdfs %s ls %s" %(siteInfo[site][0], dir))
                subprocess.check_output("rm -r %s/status_%s" %(os.getcwd(), sample), shell = True)
                sys.exit(-1)

            Time_ind = Time.index(max(Time)) 
            dir = lsInfo_list[Time_ind]
        if (i == 3):
            tmplist = lsInfo_list

    for j in tmplist:
        getfl = subprocess.check_output("xrdfs %s ls %s" %(siteInfo[site][0], j), shell = True)
        getfl_list = getfl.split("\n")
        del getfl_list[-1]

        filelist = filelist + getfl_list

    print("%i files are found in"%(len(filelist)))
    for k in tmplist:
        print("root://" + siteInfo[site][0] + k)
    
    return filelist

def copy(file):
    inpath = ""
    if (full == True):
        inpath = "root://" + siteInfo[site][0] + siteInfo[site][1] + source + "/" + file
    else: 
        inpath = "root://" + siteInfo[site][0] + file

    try:
        output = subprocess.check_output(["xrdcp", "-S", "15", '--silent', inpath, target+"/"+sample], stderr = subprocess.STDOUT)
    
    except subprocess.CalledProcessError as error:
        progress = file.replace(".root", ".txt")
        with open("%s/status_%s/transfer_%i.txt" %(os.getcwd(), sample, ind[file]), "w") as f:
            f.write("An error happens when it transfers %s\n" %file)
            f.write(error.output)
            f.close

def main():
    pool = Pool(n)
    for i in tqdm(pool.imap_unordered(copy, DL), total = len(DL)): 
        pass
    pool.close()
    pool.join()

    if not os.listdir("%s/status_%s" %(os.getcwd(), sample)):
        subprocess.check_output("rm -r %s/status_%s" %(os.getcwd(), sample), shell = True)
    else:
        print("[ERROR information] %s/status_%s" %(os.getcwd(), sample))

if __name__ == "__main__" :
    parser = get_parser()
    args = parser.parse_args()
    site, source, target, sample, n , full = args.site, args.source, args.target, args.sample, args.nCPU, args.fullpath

    siteInfo = {
    #   alias:       "xrootd_endpoint",           "remote_prefix")
        "EOS"        : ("eoscms.cern.ch/",        "/eos/cms"),
        "NCHC"       : ("se01.grid.nchc.org.tw/", "/cms")
    }

    if not os.path.exists("%s/status_%s" %(os.getcwd(), sample)):
        os.makedirs("%s/status_%s" %(os.getcwd(), sample))

    if not os.path.exists("%s/%s" %(target, sample)):
        print("[Creation] %s/%s" %(target, sample))
        os.makedirs("%s/%s" %(target, sample))

    sys.stdout = open("%s/%s/transfer.log" %(target, sample), "w")

    DL = []
    if(full == True):
        fs = XRootDPyFS("root://"+ siteInfo[site][0] + siteInfo[site][1] + source)
        DL = fs.listdir() # get the file list in the directory
        print("[Files] %i files are found in" %(len(DL)))
        print("root://" + siteInfo[site][0] + siteInfo[site][1] + source)
    else:
        DL = listdir(siteInfo[site][1] + source)
    
    Outp = [k for k in range(len(DL))]
    zipObj = zip(DL, Outp)
    ind = dict(zipObj)
    
    state = main()
    sys.stdout.close()

    sys.exit(state)

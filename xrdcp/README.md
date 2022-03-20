# Transference of smaples
```xrootdcp.py``` is used to transfer samples from a XRootD directory such as **EOS** or **NCHC** to local(**chip02**) via xrdcp. It transfers many files in parallel using the package ```multiprocessing```.
If you don't have ```multiprocessing```, please install it via 
```bash
$ pip install multiprocessing
```
## Usage 
**Prerequisites:** Please try to follow the steps in [this page](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#BasicGrid)
- **To have a valid Grid certificate:** If you don't have the Grid certificate, you can get it in https://ca.cern.ch/ca/. The Grid certificate is a .p12 file such as **mycert.p12**. The password is recommanded to be the same as the password used for lxplus.
- Make sure your certificate is correctly mapped to your account: <br>
- Place the p12 certificate file in the .globus directory of your home area. If the .globus directory doesn't exist, create it.
    ```bash
      $ cd ~
      $ mkdir .globus
      $ cd ~/.globus
      $ mv /path/to/mycert.p12 .
    ```
- Execute the following shell commands
    ```bash
      $ rm -f usercert.pem
      $ rm -f userkey.pem
      $ openssl pkcs12 -in mycert.p12 -clcerts -nokeys -out usercert.pem
      $ openssl pkcs12 -in mycert.p12 -nocerts -out userkey.pem
      $ chmod 400 userkey.pem
      $ chmod 400 usercert.pem
    ```
- Check the info about the proxy
    ```bash
      $ voms-proxy-info -all
    ```
**Start** <br>
- Set up the CMSSW and request the proxy. You can request the proxy via 
    ```bash 
    $ voms-proxy-init --voms cms --valid 168:00
    ```
- Execution
    ```bash
    # Find the newest directroy to transfer automatically
    # python xrootdcp.py -n 10 NCHC /store/group/phys_smp/ggNtuples/13TeV/mc/V09_04_13_04/job_fall17_gjet_pt40_MGG_80toInf /data6/ggNtuples/V10_02_10_05 job_fall17_gjet_pt40_MGG_80toInf

    # Determine which directory you want to transfer by yourself
    # python xrootdcp.py -n 10 -f True NCHC /store/group/phys_smp/ggNtuples/13TeV/mc/V09_04_13_04/job_fall17_gjet_pt40_MGG_80toInf/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/crab_job_fall17_gjet_pt40_MGG_80toInf/210412_010358/0000 /data6/ggNtuples/V10_02_10_05 job_fall17_gjet_pt40_MGG_80toInf
    
    $ python xrootdcp.py [source site] [source folder] [target folder] [sample folder] (-n [nCPUs], -f[fullpath])
    ```
    1. ```source site:``` [EOS, NCHC]
        ```
        EOS: root://eoscms.cern.ch//eos/cms
        NCHC: root://se01.grid.nchc.org.tw/cms
        ```
    2. ```source folder:``` /path/to/the/sample_name
    3. ```target folder:``` /path/to/the/VXX_XX_XX_XX
    4. ```sample folder:``` The directory under target folder to put the trasferred smple files.
    5. ```nCPU:``` The number of nCPUs determines how many CPUs would work parallelly to transfer the files. The default number is **10**, if you don't use ```-n [nCPUs]``` to assign the number.
    6. ```fullpath:``` you can determine which directory you want to transfer by yourself, otherwise it will transfer the newest sample automatically.
- Please check the transference status in directory **status**. The txt files which contain the **[ERROR]** information happened when the program transfered the files.
> **_NOTE:_**  Please use python instead of python3 to execute this code.

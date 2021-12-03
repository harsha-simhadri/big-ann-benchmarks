**Hardware Configuration And Cost**
We use the price of $10,817.37 shown by Dell for the [configuration](https://www.dell.com/en-us/work/shop/servers-storage-and-networking/poweredge-r740-rack-server/spd/poweredge-r740/pe_r740_12248b_vi_vp?configurationid=5e1b59fc-f6d6-4331-9c9d-12bebcffcba0) including two dual Xeon Gold 6240 on Dell PowerEdge R740 rack server with 64GB DRAM. Actual purchase price might be less than this price due to discounts to Microsoft. Additional cost of $925 for Samsung PM1725a 3.2TB NVMe SSD quoted [here](https://harddiskdirect.com/pm1725a-samsung-ssd.html). Both price estimates obtained online on October 30th 2021. Total price of $11742.


**Hardware Access**
No access to non-Microsoft accounts. However, this is a typical machine that can be purchased from Dell and involves no special hardware.

**No Source Declarations**
All source code released [here](https://github.com/Microsoft/Diskann). Uses Intel MKL libraries for math. 

**Hardware Setup And Software Installation**
No special setup beyond what is required in tracks T1 and T2. 

**Run Competition Algorithm**
Typical run
```
python3 run.py --t3 --definitions t3/diskann-vm-ls8v2/algos.yaml --dataset deep-1B
```
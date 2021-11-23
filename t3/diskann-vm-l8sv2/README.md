**Hardware Configuration And Cost**
This is a standard Azure VM. Pricing obtained from [Azure link](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/) for West US 2 data center on Oct 30th 2021. Pricing is what is displayed to public, and does not include any volume/special discounts or internal pricing.

```
Instance    vCPU(s) RAM     Temporary storage   NVMe Disk   Pay as you go   1 year reserved	3 year reserved Spot 
L8sv2       8   	64 GiB	80 GiB          	1 x 1.9 TB	$0.624/hour     $0.3975/hour    $0.2640/hour    $0.1311/hour
```

Using the spot price and 4 year time multiplier suggested by George, the cost is USD4593. This reflects the total cost of operation in the cloud and not just upfront hardware cost. 


**Hardware Access**
Open access. Any one can checkout a VM.


**No Source Declarations**
All source code released [here](https://github.com/Microsoft/Diskann). Uses Intel MKL libraries for math. 

**Hardware Setup And Software Installation**
No special setup beyond what is required in tracks T1 and T2. 


**Run Competition Algorithm**
Typical run
```
python3 run.py --t3 --definitions t3/diskann-vm-ls8v2/algos.yaml --dataset deep-1B
```
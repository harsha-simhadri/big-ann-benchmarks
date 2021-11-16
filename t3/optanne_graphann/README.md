# OptANNe GraphANN
  
This README contains information required for T3 Track submissions.

## Hardware Configuration And Cost

|Part                    |Model                                                    |No. |Unit Price                                       |Total Price|
|------------------------|---------------------------------------------------------|----|-------------------------------------------------|-----------|
|Integrated 1U System    |[Supermicro SYS-120-TNR](cost/BIGANN_system_invoce.pdf)  |   1|                                        $13576.20|  $13576.20|
|                        |w/2X Intel Xeon Gold 6330N Processor                     |    |                                                 |          -|
|                        |w/16X Intel Optane Persistent Memory 200 Series          |    |                                                 |          -|
|                        |w/Network card, boot drive, etc.                         |    |                                                 |          -|
|                        |[w/16X 16GB DDR4-3200 RDIMM](cost/DRAM16.pdf)            |  16|                                              $82|          -|
|Replacement DRAM        |w/16X 32GB DDR4(cost/DRAM32.pdf)                         |  16|                                 ($150-$82) = $68|      $1088|
|Total                   |                                                         |    |                                                 |  $14664.20|

## Hardware Access

The hardware components are commercially available ( see hardware table above ).

For more information, please contact the T3 participant Sourabh Dongaonkar sourabh.dongaonkar@intel.com.

## No Source Code Declarations

All components of the software are open-source.

## Hardware Setup And Software Installation

Please consult the following [installation readme]("INSTALLATION_README.md") for detailed setup instructions.

### Competition Index Files

Currently the competition index files must be downloaded and installed manually.

Download all the index files from [here](tbd) (TBD) and unpack into the cloned repo's data directory.

You will need to adjust the submission algos.yaml config file to reflect the local path to your index files.

## Run The Competition Algorithm

Please see the [run script]("run.sh") for an example.


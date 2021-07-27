# T3 Track

## Table Of Contents

- [Introduction](#introduction)  
- [For Participants](#for_participants) 
  - [Getting Started](#getting_started) 
  - [Developing Your Algorithm](#developing_your_algorithm) 
  - [How To Get Help](#how_to_get_help)
- [For Evaluators](#for_organizers)  
  - [Evaluating Participant Algorithms](#evaluating_participant_algorithms)
    - [Participant_Sends_Hardware_To_Evaluators](#participant_sends_hardware_to_organizers)
    - [Participant_Gives_Remote_Access_To_Evaluators](#participant_gives_remote_access_to_organizer)
    - [Participant_Runs_And_Submits_Benchmarks](#participant_runs_and_submits_benchmark)
  - [Evaluating Power Consumption](#evaluating_power_consumption)   
## Introduction

The T1 and T2 tracks of the competition restrict the evaluation of algorithms to standard Azure CPU servers with 64GB of RAM and 2TB of SSD.  The only restriction in the T3 track is that the evaluation machine can be any hardware that is commercially available ( including any commercially available add-on PCIe boards ).  T3 will maintain three leaderboards:
* One based on the typical ANN performances metrics recall-vs-throughput
* One based on power consumption
* One based on hardware cost

Participants must submit their algorithm via a pull request and an index file upload.  Participants are not required to submit proprietary source code such as software drivers or firmware.

Competition evaluators will evaluate the participant's algorithm and hardware via one of these options:
* Participants send their hardware to the organizers at the participant's expense.
* Participants give organizers remote access to the hardware.
* Participants run the evaluation benchmarks on their own, and send the results to the organizers.

## For_Participants

### Requirements

You will need the following installed on your machine:
* Python ( we tested with Anaconda using an environment created for Python version 3.8.5 )
* Note that we tested everything on Ubuntu Linux 18.04 but other environments should be possible.
* It's assumed that all the software drivers and services need to support your hardware are installed.  For example, to run the T3 baseline, your system must have a Cuda 11 compatibile GPU, Cuda 11.0, and the cuda 11.0 docker run time installed.

### Getting_Started

This section will present a small tutorial about how to use this framework and several of the key scripts you will use throughout the development of your algorithm and eventual submission.

First, clone this repository and cd into the project directory:
```
git clone <REPO_URL>
```
Install the python package requirements:
```
pip install -r requirements.txt
```
Create a small, sample dataset:
```
python create_dataset.py --dataset random-xs
```
Build the docker container for the T3 baseline:
```
python install.py --dockerfile t3/faiss_t3/Dockerfile
```
Run a benchmark evaluation using the algorithm's definition file:
```
python run.py --t3 --definitions t3/faiss_t3/algos.yaml
```
Please note that the *t3* flag is important.  

Now analyze the results:
```
python plot.py --dataset random-xs
```
This will place a plot of the algorithms performance, recall-vs-throughput, into the *results/* directory.

### Developing_Your_Dockerfile

First, please create a short name for your team without spaces or special characters.  Henceforth in these instructions, this will be referenced as [your_team_name].

Create a custom branch off main in this repository:
```
git checkout -b t3/[your_team_name]
```
In the *t3/* directory, create a sub-directory using that name.
```
mkdir t3/[your_team_name]
```
This framework evaluates algorithms in Docker containers.  Your algorithm's Dockerfile should live in your team's subdirectory at *t3/[your_team_name]*.  Ideally, your Docker file should contain everything needed to install and run your algorithm on an system with the same hardware.  Given the nature of T3, this will not likely be possible since custom hardware host drivers and certain low level host libraries require an installation step outside of Docker.  Please make your best effort to include as much as possible within your Docker container as we want to promote as much transparency as possible among participants.

Please consult the Dockerfile in *t3/faiss_t3/algos.yaml* as an example.

To build your Docker container, run:
```
python install.py --dockerfile t3/[your_team_name]/Dockerfile
```

### Developing_Your_Algorithm

Develop and add your algorithm to the *benchmarks/algorithms* directory.
* You will need to subclass from the BaseANN class in *benchmarks/algorithms/base.py* and implement the functions of that parent class.
* You should consult the examples already in the directory.
T
As you develop and test your algorithm, you will likley need to test on smaller datasets.  This framework provides a way to create datasets of various sizes.  For example, to create a dataset with 10000 20-dimensional random floating point vectors, run:
```
python create_dataset.py --dataset random-xs
```
To see a complete list of datasets, run the following:
```
python create_dataset.py --help
```
When you are ready to test on the competition datasets, use the create_dataset.py script as follows:
```
python create_dataset.py --dataset [sift-1B|bigann-1B|text2image-1B|msturing-1B|msspacev-1B|ssnpp-1B]
```
To benchmark your algorithm, first create an algorithm configuration yaml in your teams directory called *algos.yaml.*  This file contains the index build parameters and query parameters that will get passed to your algorithm at run-time.  Please look at this example *t3/faiss_t3/algos.yaml.*

Now you can benchmark your algorithm using the run.py script:
```
python run.py --t3  --definitions t3/[your_team_name]/algos.yaml --dataset random-xs
```
This will write the results into various files in the *results/* directory.

Now you can analyze the results by running:
```
python plot.py --definitions t3/[your_team_name]/algos.yaml --dataset random-xs
```
This will place a plot of the algorithms performance, recall-vs-throughput, into the *results/* directory.

The plot.py script supports other benchmarks.  To see a complete list, run:
```
python plot.py --help
```

### Submitting_Your_Algorithm

A submission is composed of the following:
* 1 index binary file (  choose your best index )
* 1 *algos.yaml* with only one set of build parameters and at most 10 sets of query parameters ( put it into the *t3/[your_team_name]/* directory. )
* Your algorithm's python class ( put it into the *benchmark/algorithms/* directory. )

All but the binary index file can be submitted with a pull request of your custom branch.

We will provide you with an upload area for your binary index file during the competition.

Additional information may be required to qualify for all the leaderboards:
* To qualify for the cost leaderboard, please include evidence of the MSRP of all the components of your entire system.  Put this evidence into the *t3/[your_team_name]/* directory.
* If all of the source code cannot be included in your pull request, please provide an explanation of what the non-open-source part of the software does (host drivers, firmware, etc.) Put this explanation as a text file into the t3/[your_team_name]/ directory.

### How_To_Get_Help

There are several ways to get help as you develop your algorithm:
* You can submit an issue at this github repositry.
* Send an email to the competition's T3 organizer, gwilliams@gsitechnology.com
* Send en email to the competition's google-group.

## For_Evaluators

### Evaluating_Participant_Algorithms

How a participant' algorithm is benchmarked will depend on how they registered for the T3 competition, one of these options:
* Participant sent hardware to competition evaluator at participant's expense.
* Participant is giving the competition valuator remote SSH access to their machine.
* Participant will run the evaluation framework on their own and send the benchmark results to the competition evaluator.

Evaluation steps for each mode are detailed in the next sections.

### Participant_Sends_Hardware_To_Evaluators

Evaluators will work with participant's that send hardware during on-boarding. Hardware will be sent at the participant's expense.

Evaluators and participants will work closely to make sure the hardware is properly installed and configured.

Evaluators may allow remote access to the machines in order to complete the setup, as needed.

### Participant_Gives_Remote_Access_To_Evaluators

Participants give competition evaluators access to remote machines via SSH.

### Participant_Runs_And_Submits_Benchmarks

This is a very special case, and not all participant's will have this option.  In this case, the participant will run the evaluation on their own.  They will export the data to a CSV via the export.py script and send it to the the competition evaluators.  Participants are still required to submit a pull request and upload their best index.

## Evaluating_Power_Consumption

The hardware chassis which houses all the hardware must support the IPMI management interface.

Determine the IP address, port, and authentication credentials of that interface.

Follow the instructions at IPMICAP open-source project ( http://www.github.com/fractalsproject/ipmicap ) to access the IPMI and configure it to listen to an available port number.

Capture the machine IP address of the machine which is running IPMICAP ( it does not have to be the same machine as the target hardware. )

Now run the following for each competition dataset:
```
python run.py --dataset [DATASET] --t3 --definitions [DEFINITION FILE] --powercapture [IPMICAP_MACHINE_IP]:[IPMICAP_LISTEN_PORT]:[TIME_IN_SECONDS]
```
This will monitor power consumption over that period of time ( 10 seconds is a good number ).

You can retrieve a plot of the power consumptions ( measures as watt*seconds/query ) using the plot.py script.




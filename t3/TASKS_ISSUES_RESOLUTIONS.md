
# BigANN Challenge T3 Tasks, Issues, and Resolutions

In the spirit of maintaining a fair and open competition, we will be tracking all important remaining tasks and issues, and their respective resolution - and making that all public here on this README.  All competition rankings and winners will be "unofficial" until all tasks and issues have been resolved.

Participants should send their questions and issues to the T3 organizer directly (gwilliams@gsitechnology.com), or to the competition google group at big-ann-organizers@googlegroups.com.  Note that some issues may require a complete re-evaluation of an algorithm on its respective hardware, or may require additional information from a participant or competition organizer(s).

## Tasks (open)

* [T3 Organizer self-report] In the private set evaluation, there are issues with the msspace-v ground truth file preventing any submission evaluation and scoring on that dataset.
* [T3 Organizer self-report] In the private set evaluation, there are issues with some submissions crashing on either/both deep-1B and msspacev-1b thus preventing any scoring on that dataset.
* [Microsoft to T3 Organizer] Currently, DiskANN cannot qualify for power and cost benchmarks due to issue with running IPMICAP ( python ipmi in particular seems to be the issue. )
  * PENDING RESOLUTION: [T3 Organizer to Microsoft] We will work on local dcmi support in the IPMICAP server.
* [T3 Organizer to Microsoft] Need to retrieve "results" h5py files from MS DiskANN remote machine.

## Issues (open)

* [T3 Organizer self-report] The "opex" power cost for an Nvidia submission seems impossibly low ($80).
  * PENDING RESOLUTION: We need to measure quiescent power of a system and establish the min power consumption and troubleshoot the DCMI power reporting on the NVidia system.

## Resolutions

* [GSI asked] What does NQ mean?
  * [T3 Organizer responded] It could mean 1) team did not submit a qualifying algorithm for the benchmark 2) team decided did not participate in that benchmark 3) unable to get some key data for the benchmark (such as power or system cost, or both ).
* [T3 Organizer self-report] Need to retrieve "results" h5py files from NVidia's remote machine.
  * Done on 11/23/2021
* [T3 Organizer to NVidia] Need to retrieve power monitoring "results" h5py files from NVidia's remote machine.
  * Done on 11/23/2021 and subsequently on changes to algos.yaml
* [GSI to T3 Organizer] Need better documentation for how to extract power benchmark from plot.py script.
  * Answered via email.  Basically, you need to supply "wspq" as an explicit metric you want to retrieve using the chosen axis.  Run "python ploy.py --help" to get more information.
* [GSI to T3 Organizers] We cannot reproduce the baseline performance on SSNPP on same/similar hardware.
  * Organizer repeated the eval and it was the same.  It could have been an issue with faiss (gpu) library and version.
* [GSI to T3 Organizers] Have you discussed taking power also on the recall working point and not just on the throughput working point?
[GSI asks T3 Organizers] Since some algorithms implement smart caching mechanisms to simulate real life scenarios and since the competition framework sends the same queries again and again 50 time for each dataset (5 runs x 10 query configurations) which is not a real life case. It is important that competition framework needs to verify the results, automatically (and if not possible manually) that no caching mechanism is used in between runs and in between query configurations. One way is to make sure that the throughput for the runs doesn’t differ much taking into account that there are 5 runs and 10 configurations with the same queries. Probably a better way is to send for different queries or somehow cool down the cache in between runs by sending random queries.
  * The eval framework now implements "possible query response cache" detection and the competition reports this as an anomaly and allows teams to explain why these happen.  It's too late in the competition to establish a policy to deal with these  "anomalies" such as 1) ask team to mitigate the effect 2) cool the cache with random queries 3) throw out the data.
* [T3 Organizer to Microsoft] Currently reported DiskANN CSV results is using an old version of recall computation (ie, not accounting for ties and it will likely affect msspacev-1B recall mostly).
  * This was resolved.  Microsoft exported a new csv with the proper recall.
* [GSI to T3 Organizer] New index for SSNPP and Text2Image requires re-evaluation for those datasets and updated scores.
  * This was done successfully on the public query set.
* [Intel asks T3 Organizer] Why won't there be one winner for T3 that combines all individual benchmarks?
  * We have provided the reason to Intel.  We weren't sure how to combine them in this first competition - likely it will be combined in the future.
* [Intel asks T3 Organizer] Why are power and cost rankings optional for a submission?
  * We have provided the reason to Intel.  We werent sure how easy it would be to support this for all participants in this first competition.
* [T3 Organizer asks NVidia] Can't we use an MSRP from another company as proxy for system cost?
  * We will take the cheapest MSRP from third party seller for the leaderboard (we found 150K).  We've footnoted this in the rankings.



# BigANN Challenge T3 Tasks, Issues, and Resolutions

In the spirit of maintaining a fair and open competition, we will be tracking all important remaining tasks and issues, and their respective resolution - and making that all public here on this README.  All competition rankings and winners will be "unofficial" until all tasks and issues have been resolved.

Participants should send their questions and issues to the T3 organizer directly (gwilliams@gsitechnology.com), or to the competition google group at big-ann-organizers@googlegroups.com.  Note that some issues may require a complete re-evaluation of an algorithm on its respective hardware, or may require additional information from a participant or competition organizer(s).

## Tasks (open)

* [T3 Organizer to Microsoft] Currently reported DiskANN CSV results is using an old version of recall computation (ie, not accounting for ties and it will likely affect msspacev-1B recall mostly).
  * PENDING RESOLUTION: [Microsoft to T3 Organizer] Will re-base and send the CSV.
* [Microsoft to T3 Organizer] Currently, DiskANN cannot qualify for power and cost benchmarks due to issue with running IPMICAP ( python ipmi in particular seems to be the issue. )
  * PENDING RESOLUTION: [T3 Organizer to Microsoft] We will work on local dcmi support in the IPMICAP server.
* [GSI to T3 Organizer] New index for SSNPP and Text2Image requires re-evaluation for those datasets and updated scores.
  * PENDING RESOLUTION: [T3 Organizer to GSI] We ran SSNPP to completion, but having issues with Text2Image.
* [T3 Organizer to Microsoft] Need to retrieve "results" h5py files from MS DiskANN remote machine.

## Issues (open)

* [Intel asks T3 Organizer] Why won't there be one winner for T3 that combines all individual benchmarks?
  * PENDING RESOLUTION: [T3 Organizer to Intel] We have provided the reason.  Hopefully its a good enough explanation and we can soon remove this issue.
* [Intel asks T3 Organizer] Why are power and cost rankings optional for a submission?
  * PENDING RESOLUTION: [T3 Organizer to Intel] We have provided the reason.  Hopefully its a good enough explanation and we can soon remove this issue.
* [GSI to T3 Organizers] We cannot reproduce the baseline performance on SSNPP on same/similar hardware.
  * PENDING RESOLUTION: [T3 Organizer to GSI] We've reproduced on sent the results.  Please approve.
* [T3 Organizer asks NVidia] Can't we use an MSRP from another company as proxy for system cost?
  * PENDING RESOLUTION: [T3 Organizer to NVidia] We will take the cheapest MSRP from third party seller. Please approve.
* [GSI to T3 Organizers] Have you discussed taking power also on the recall working point and not just on the throughput working point?
[GSI asks T3 Organizers] Since some algorithms implement smart caching mechanisms to simulate real life scenarios and since the competition framework sends the same queries again and again 50 time for each dataset (5 runs x 10 query configurations) which is not a real life case. It is important that competition framework needs to verify the results, automatically (and if not possible manually) that no caching mechanism is used in between runs and in between query configurations. One way is to make sure that the throughput for the runs doesn’t differ much taking into account that there are 5 runs and 10 configurations with the same queries. Probably a better way is to send for different queries or somehow cool down the cache in between runs by sending random queries.
  * PENDING RESOLUTION: [T3 Organizers to GSI] We will add "cache detection" countermeasure to the framework and reevaulate all submissions.

## Resolutions

* [GSI asked] What does NQ mean?
  * [T3 Organizer responded] It could mean 1) team did not submit a qualifying algorithm for the benchmark 2) team decided did not participate in that benchmark 3) unable to get some key data for the benchmark (such as power or system cost, or both ).
* [T3 Organizer self-report] Need to retrieve "results" h5py files from NVidia's remote machine.
  * Done on 11/23/2021
* [T3 Organizer to NVidia] Need to retrieve power monitoring "results" h5py files from NVidia's remote machine.
  * Done on 11/23/2021 and subsequently on changes to algos.yaml
* [GSI to T3 Organizer] Need better documentation for how to extract power benchmark from plot.py script.
  * Answered via email.  Basically, you need to supply "wspq" as an explicit metric you want to retrieve using the chosen axis.  Run "python ploy.py --help" to get more information.



# BigANN Challenge T3 Tasks, Issues, and Resolutions

In the spirit of maintaining a fair and open competition, we will be tracking all important remaining tasks and issues, and their respective resolution - and making that all public here on this README.  All competition rankings and winners will be "unofficial" until all tasks and issues have been resolved.

Participants should send their questions and issues to the T3 organizer directly (gwilliams@gsitechnology.com), or to the competition google group at big-ann-organizers@googlegroups.com.  Note that some issues may require a complete re-evaluation of an algorithm on its respective hardware, or may require additional information from a participant or competition organizer(s).

## Tasks (open)

* [T3 Organizer self-report] Currently reported DiskANN CSV results is using an old version of recall computation (ie, not accounting for ties and it will likely affect msspacev-1B recall mostly).
* [T3 Organizer self-report] Currently, DiskANN cannot qualify for power and cost benchmarks due to issue with running IPMICAP ( python ipmi in particular seems to be the issue. )
* [GSI to T3 Organizer] New index for SSNPP and Text2Image requires re-evaluation for those datasets and updated scores.
* [GSI to T3 Organizer] Need better documentation for how to extract power benchmark from plot.py script.
* [T3 Organizer self-report] Need to retrieve "results" h5py files from MS DiskANN remote machine.

## Issues (open)

* [Intel asks T3 Organizer] Why won't there be one winner for T3 that combines all individual benchmarks?
* [Intel asks T3 Organizer] Why are power and cost rankings optional for a submission?
* [GSI to T3 Organizers] We cannot reproduce the baseline performance on SSNPP on same/similar hardware.
* [T3 Organizer asks NVidia] Can't we use an MSRP from another company as proxy for system cost?
* [GSI to T3 Organizers] Have you discussed taking power also on the recall working point and not just on the throughput working point?
[GSI asks T3 Organizers] Since some algorithms implement smart caching mechanisms to simulate real life scenarios and since the competition framework sends the same queries again and again 50 time for each dataset (5 runs x 10 query configurations) which is not a real life case. It is important that competition framework needs to verify the results, automatically (and if not possible manually) that no caching mechanism is used in between runs and in between query configurations. One way is to make sure that the throughput for the runs doesn’t differ much taking into account that there are 5 runs and 10 configurations with the same queries. Probably a better way is to send for different queries or somehow cool down the cache in between runs by sending random queries.

## Resolutions

* [GSI asked] What does NQ mean?
  * [T3 Organizer responded] It could mean 1) team did not submit a qualifying algorithm for the benchmark 2) team decided did not participate in that benchmark 3) unable to get some key data for the benchmark (such as power or system cost, or both ).
* [T3 Organizer self-report] Need to retrieve "results" h5py files from NVidia's remote machine.
  * Done on 11/23/2021
* [T3 Organizer to NVidia] Need to retrieve power monitoring "results" from NVidia's remote machine.
  * Done on 11/23/2021

| dataset        | algorithm                | qps          |
|----------------|--------------------------|--------------|
| yfcc-10M       | pinecone [*]             | 85491.542780 |
| (filter track) | zilliz [*]               | 84596.419213 |
|                | parlayivf                | 37902.113726 |
|                | puck                     | 19193.294823 |
|                | hwtl_sdu_anns_filter [*] | 15059.124141 |
|                | wm_filter                | 14467.961514 |
|                | dhq                      | 13670.864704 |
|                | fdufilterdiskann         | 5679.748583  |
|                | pyanns                   | 5184.844352  |
|                | faissplus                | 3776.539092  |
|                | faiss                    | 3032.534357  |
|                | cufe                     | 2917.132715  |
| text2image-10M | pinecone-ood [*]         | 38087.669026 |
| (OOD track)    | zilliz [*]               | 33240.822128 |
|                | mysteryann               | 22555.248017 |
|                | pyanns                   | 22295.584534 |
|                | mysteryann-dif           | 22491.577263 |
|                | sustech-ood              | 13772.370641 |
|                | puck                     | 8699.573200  |
|                | vamana                   | 6753.344080  |
|                | ngt                      | 6373.934425  |
|                | epsearch                 | 5876.982706  |
|                | diskann                  | 4132.829728  |
|                | cufe                     | 3561.416286  |
| sparse-full    | zilliz [*]               | 10749.188262 |
| (sparse track) | pinecone_smips [*]       | 10439.909652 |
|                | pyanns                   | 8732.172708  |
|                | shnsw                    | 7136.927865  |
|                | nle                      | 2358.590429  |
|                | cufe                     | 104.768194   |
|                | linscan                  | 92.510615    |

[*] not open source

Table lists highest QPS measured with at least 90% recall@10, on the *public* query set.

Last evaluation date: March 1st, 2024 (includes all submission until March 1st, 2024, AOE)

|----------------------------------------------------------|
| dataset         | algorithm             | qps            |
|-----------------|-----------------------|----------------|
| yfcc-10M        | parlayivf             | 37670.703774   |
| (filter track)  | puck                  | 19153.425169   |
|                 | hwtl_sdu_anns_filter  | 15188.577106   |
|                 | wm_filter             | 14076.445534   |
|                 | dhq                   | 13517.047874   |
|                 | fdufilterdiskann      | 5752.463409    |
|                 | pyanns                | 5335.916507    |
|                 | faissplus             | 3625.027286    |
|                 | faiss                 | 3252.682553    |
|                 | cufe                  | 2291.031703    |
|----------------------------------------------------------|
| text2image-10M  | mysteryann            | 22555.248017   |
| (OOD track)     | pyanns [1]            | 22295.584534   |
|                 | mysteryann-dif        | 22491.577263   |
|                 | sustech-ood           | 13772.370641   |
|                 | puck                  | 8699.573200    |
|                 | vamana                | 6753.344080    |
|                 | ngt                   | 6373.934425    |
|                 | epsearch              | 5876.982706    |
|                 | diskann               | 4132.829728    |
|                 | cufe                  | 3561.416286    |
|----------------------------------------------------------|
| sparse-full     | pyanns [1]            | 6499.652881    |
| (sparse track)  | shnsw                 | 5078.449772    |
|                 | NLE-Full              | 1314.194166    |
|                 | nle                   | 1312.961060    |
|                 | sustech-whu [2]       | 788.168885     |
|                 | cufe                  | 97.860465      |
|                 | linscan               | 95.098871      |
|----------------------------------------------------------|


[1] The entry was from an author affiliated with Zilliz, a company involved in the organizing team. The conflict was not disclosed by the author, and was discovered post evaluation.
[2] Build time exceeded 12 hours 

Table lists highest QPS measured with at least 90% recall@10. Private queries were used for yfcc-10M and sparse-full and public queries for text2image-10M.
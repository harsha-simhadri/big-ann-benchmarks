| dataset         | algorithm             | qps            |
|-----------------|-----------------------|----------------|
| yfcc-10M        | parlayivf             | 30744.178014   |
|                 | puck                  | 17160.390356   |
|                 | hwtl_sdu_anns_filter  | 15433.837498   |
|                 | wm_filter             | 13723.065895   |
|                 | fdufilterdiskann      | 6085.293763    |
|                 | pyanns                | 5260.477613    |
|                 | faissplus             | 3851.283822    |
|                 | rubignn               | 3289.234566    |
|                 | faiss                 | 3254.200190    |
| text2image-10M  | pyanns [1]            | 22476.070400   |
|                 | mysteryann-dif        | 17764.966620   |
|                 | mysteryann            | 17665.716757   |
|                 | sustech-ood           | 11594.134313   |
|                 | puck-fizz             | 8460.214238    |
|                 | puck                  | 8167.845988    |
|                 | vamana                | 6322.589569    |
|                 | cufe                  | 3414.617622    |
| sparse-full     | pyanns [1]            | 6280.871386    |
|                 | shnsw                 | 4359.145718    |
|                 | nle                   | 1297.986119    |
|                 | sustech-whu [2]       | 670.864748     |
|                 | cufe                  | 64.665603      |
|                 | linscan               | 63.026394      |

[1] The entry was from an author affiliated with Zilliz, a company involved in the organizing team. The conflict was not disclosed by the author, and was discovered post evaluation.
[2] Build time exceeded 12 hours (13 hours, 34 minutes)

Results with private queries for yfcc-10M and sparse-full and public queries for text2image-10M

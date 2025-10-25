set -x 
set -e 
dest=/tmp/bigann_report_arxiv/

mkdir $dest || rm -rf $dest/*


# get the tex files
#grep \(./ main_arxiv.log  | tr '(' '\n' | sed 's|./\([-/0-9a-z_]*.tex\).*|\1|' | grep .tex | xargs echo

# copy and strip comments
for i in main_arxiv.tex abstract.tex intro.tex tracks.tex evaluation.tex results.tex discussion.tex conclusion.tex
do
    if [ "${i%/*}" != "$i" ]; then 
        mkdir -p $dest/${i%/*}
    fi
    perl -pe 's/(^|[^\\])%.*/\1%/' < $i > $dest/$i
    # remove \iffalse... \fi 
    sed -i '' '/\\iffalse/,/\\fi/d' $dest/$i
done


# which figures are used 
# echo $(  grep \<use  main_arxiv.log  | tr -d '<>' | sed 's/^ *//' | cut -c 4- )

# just copy
for i in \
fig/226264627_90d8eaeb1f.jpg fig/755174504_7a9eee2248.jpg fig/5174840406_01fb734503.jpg fig/PCA_OOD_dim0_1.pdf fig/PCA_OOD_dim2_3.pdf fig/yfcc-10M-2.pdf fig/text2image-10M.png fig/sparse-full.png \
   main_arxiv.bbl 
do 
    if [ "${i%/*}" != "$i" ]; then 
        mkdir -p $dest/${i%/*}
    fi
    cp $i $dest/$i
done


(cd $dest; tar czf /tmp/bigann_report_arxiv.tgz . )

open -R /tmp/bigann_report_arxiv.tgz



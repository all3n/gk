gen(){
  NAME=$1
  TITLE=$2
  #python merge.py $NAME
  pdftocio merge_$NAME.pdf > TOC
  python create-toc.py TOC $TITLE
  python mall.py mintoc.pdf merge_$NAME.pdf out_$NAME.pdf



}


gen shuxue 数学1
gen shuxue1 数学2

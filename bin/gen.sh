BIN=$(dirname $0)
APP_DIR=$(cd $BIN/..;pwd)
export PYTHONPATH=$APP_DIR/python
export TMP_DIR=$APP_DIR/tmp
export FONTS_DIR=$APP_DIR/fonts
export XKS=$TMP_DIR/xks
mkdir -p $TMP_DIR

gen(){
  NAME=$1
  TITLE=$2
  TOC_OUTPUT=$TMP_DIR/toc_$NAME.pdf
  TOC=$TMP_DIR/TOC_$NAME
  MERGE_PDF=$TMP_DIR/merge_$NAME.pdf
  FINAL_PDF=$TMP_DIR/final_$NAME.pdf

  python -m app.merge $XKS/$NAME $MERGE_PDF $TMP_DIR
  pdftocio $MERGE_PDF > $TOC
  python -m app.create_toc $TOC $TITLE $TOC_OUTPUT
  python -m app.mall $TOC_OUTPUT $MERGE_PDF $FINAL_PDF
}


#bash $APP_DIR/bin/copy.sh
#bash $APP_DIR/bin/remove_duplicate.sh


for i in $(ls $XKS);do
  TITLE=$(cat $XKS/$i/file.txt|jq -r .name)
  INDEX=$(cat $XKS/$i/file.txt|jq -r .index)
  gen $i $TITLE-$INDEX
done

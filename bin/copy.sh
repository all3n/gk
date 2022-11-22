BIN=$(dirname $0)
APP_DIR=$(cd $BIN/..;pwd)
export PYTHONPATH=$APP_DIR/python
export TMP_DIR=$APP_DIR/tmp

mkdir -p $TMP_DIR/shuxue
mkdir -p $TMP_DIR/wuli
mkdir -p $TMP_DIR/huaxue
mkdir -p $TMP_DIR/shengwu
mkdir -p $TMP_DIR/yuwen
mkdir -p $TMP_DIR/yingyu



# shuxue
cp $(ls $APP_DIR/data/*/*|grep -v 文科|grep -v 文数|grep 数学)  $TMP_DIR/shuxue/
cp $(ls $APP_DIR/data/*/*|grep 理数)  $TMP_DIR/shuxue/
cp $(ls $APP_DIR/data/*/*|grep 物理)  $TMP_DIR/wuli
cp $(ls $APP_DIR/data/*/*|grep 化学)  $TMP_DIR/huaxue
cp $(ls $APP_DIR/data/*/*|grep 生物)  $TMP_DIR/shengwu
cp $(ls $APP_DIR/data/*/*|grep 语文)  $TMP_DIR/yuwen
cp $(ls $APP_DIR/data/*/*|grep 英语)  $TMP_DIR/yingyu

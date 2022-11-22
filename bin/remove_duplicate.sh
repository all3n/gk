BIN=$(dirname $0)
APP_DIR=$(cd $BIN/..;pwd)
export PYTHONPATH=$APP_DIR/python
export TMP_DIR=$APP_DIR/tmp
export FONTS_DIR=$APP_DIR/fonts
mkdir -p $TMP_DIR


find $TMP_DIR -type f \
    | xargs md5sum \
    | sort -k1,1 \
    | uniq -Dw32 \
    | while read hash file; do 
        [ "${prev_hash}" == "${hash}" ] && rm -v "${file}"
        prev_hash="${hash}"; 
    done

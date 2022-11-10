find . -type f \
    | xargs md5sum \
    | sort -k1,1 \
    | uniq -Dw32 \
    | while read hash file; do 
        [ "${prev_hash}" == "${hash}" ] && rm -v "${file}"
        prev_hash="${hash}"; 
    done

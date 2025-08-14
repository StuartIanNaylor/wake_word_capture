for file in $(find . -name "*.wav"); do
    #echo "$file" # f points to each file
    mv -f "$file" /tmp/tempfile.wav
    base=$(basename -- "$file")
    echo $base
    filename="${base%.*}"
    echo $filename
    #sox --norm=-0.5 /tmp/tempfile.wav -r 48000 -c 1 -b 16 "$filename".wav
    #deepFilter "$filename".wav --no-suffix
    #sox /tmp/tempfile.wav "$filename".wav silence 1 0.2 1%
    #sox /tmp/tempfile.wav "$filename".wav tempo 1.1
    sox /tmp/tempfile.wav "$filename".wav silence 1 0.2 0.1% 1 0.2 1%

done




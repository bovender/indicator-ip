#/bin/sh

if [ $# -lt 2 ]; then
        echo "== Generate manpage for indicator-ip =="
        echo "Usage: $(basename $0) INFILE OUTFILE."
        echo "Where INFILE is the readme file in markdown format"
        echo "and OUTFILE is the target output file."
        exit 1
fi

TEMPFILE="${2}.tmp"

tee > "$TEMPFILE" <<'EOF'
%INDICATOR-IP(1)

# NAME

indicator-ip - Display local and public IP addresses as indicator.

# SYNOPSIS

**indicator-ip** [**-i**|**--interface** *INTERFACE*] [**-u**|**--fetch-ip-url** *URL*]  
**indicator-ip** **--autostart**  
**indicator-ip** **--no-autostart**  
**indicator-ip** **-v**|**-vv|-vvv**  
**indicator-ip** **-V**|**--version**  
**indicator-ip** **-h**|**--help**  

# DESCRIPTION
EOF

sed -r '0,/^## DESCRIPTION/Id' "$1" >> "$TEMPFILE"
sed -r -i 's/^## (.+)$/# \U\1/' "$TEMPFILE"
pandoc --standalone -f markdown -t man "$TEMPFILE" -o "$2"
rm "$TEMPFILE"

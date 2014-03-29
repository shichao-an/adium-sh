#/bin/bash

repodir=$(dirname "../$0")
runscript="$repodir/run.py"

create_run_script ()
{
    [ -f "$runscript" ] && return 0
    cat > "$runscript" <<EOF
#!/usr/bin/env python
from adiumsh import adiumsh


if __name__ == '__main__':
    adiumsh.main()
EOF
    chmod 744 "$runscript"
}

assert_equal ()
{
   [ "$1" = "$2" ] || { echo "Assertion failed: $1 is not equal to $2 " >&2; }
}


create_run_script
"$runscript" send
assert_equal "$?" 2 


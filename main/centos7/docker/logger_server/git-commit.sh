#!/bin/bash
/usr/bin/rsync "$@"
result=$?
(
  if [ $result -eq 0 ]; then
     git -C /git add -A && git -C /git commit -m "committed at $(date +%s)"
  fi
) >/dev/null 2>/dev/null </dev/null

exit $result

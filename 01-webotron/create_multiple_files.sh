#!/bin/bash
for i in {0..9}; do dd if=/dev/urandom of=kitten_web/data/bigfile_${i}.bin bs=1048576 count=1; done


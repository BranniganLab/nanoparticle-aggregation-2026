#!/bin/bash
echo "running frame 553"
sh frame-553_run-umbrella_extend.sh
wait
echo "done running frame 553"
echo "running frame 555"
sh frame-555_run-umbrella.sh
wait
echo "done running frame 555"
echo "running frame 584"
sh frame-584_run-umbrella.sh
wait
echo "done running frame 584"
echo "running frame 594"
sh frame-594_run-umbrella.sh
wait
echo "done running frame 594"
echo "running frame 595"
sh frame-595_run-umbrella.sh
wait
echo "done running frame 595"
echo "running frame 601"
sh frame-601_run-umbrella.sh
wait
echo "done running frame 601"
echo "running frame 607"
sh frame-607_run-umbrella.sh
wait
echo "done running frame 607"
echo "Complete"

#!/bin/sh

set -e

cd "$(dirname "$0")"


echo "setting up the environment"


rm -rf env
python -m venv env
. env/bin/activate

python -m pip install -e .. >/dev/null 2>&1



echo "running unit tests:"

cd ..
python -m py.test tests

cd -

echo "\n\nrunning shell tests"


trap "killall log_monitor" EXIT



cat > conf.yml << EOF
log_file: test_file
tasks:
        Alerts:
                update_interval: 0.01 # time between each update when checking start and end of alerts, in seconds
                average_over: 3 # duration over which we average the requests per seconds
                request_frequency_threshold: 1 # threshold, in average requests per second
EOF

echo -n > test_file
log_monitor conf.yml > out 2> err &
sleep 3

for i in `seq 2`; do
	echo '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123' >> test_file
done

sleep 0.1
if [ -s out ]; then
	echo "alert started too soon"
	exit 1
fi

for i in `seq 2`; do
	echo '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123' >> test_file
done

sleep 0.1
if ! grep -q "Alert: at" out; then
	echo "missing alert"
	exit 1
fi

sleep 2

if grep -q "recovered" out; then
	echo "recovered too early"
	exit 1
fi

sleep 2

if ! grep -q "recovered" out; then
	echo "recovered too late"
	exit 1
fi

if [ -s err ]; then
	echo "errors happened: "
	cat err
	exit 1
fi

echo "\n\nshell tests: success!"

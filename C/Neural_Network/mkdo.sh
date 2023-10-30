#! /bin/bash

function usage() {
	echo "usage: mkdo <file> [-c '<args>'] [-e '<args>'] [-o]"
	exit 0
}

if [ $# -eq 0 ]; then
	usage
fi

# 拡張子を取り除いたファイル名
FILE=${1%.*}
shift

while getopts c:e:oh OPT ; do
	case $OPT in
		c ) VALUE_C=$OPTARG ;;
		e ) VALUE_E=$OPTARG ;;
		o ) VALUE_O="> ${FILE}.out" ;;
		h ) usega ;;
		* ) usage ;;
	esac
done

compile="make ${FILE} ${VALUE_C} ${VALUE_O}"
execute="${FILE} ${VALUE_E}"

echo "$execute" | grep -e '^\./' -e '^~/' -e '^/' || execute="./$execute"

echo "> $compile"
eval "$compile" || exit 1
echo "> $execute"
eval "$execute" || exit 1

exit 0

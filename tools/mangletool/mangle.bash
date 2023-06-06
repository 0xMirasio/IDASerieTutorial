#!/bin/bash
IFS='::' read -a array <<< "$1"

indexes=("${!array[@]}")

prefix=""
middle=""
suffix=""
rettype=""
if [ -z "$2" ]; then
    rettype="void"
fi


for index in "${indexes[@]}"
do
    #echo "$index ${array[index]}"
    if [ $index == ${indexes[-1]} ]; then
    #echo "last"
    middle="$rettype ${array[index]};"
    elif [ -n "${array[index]}" ]; then
    #echo "not empty"
    prefix="${prefix}struct ${array[index]}{"
    suffix="${suffix}};"
    fi
done

if [[ -f "base.cpp" ]]; then
    rm -rf base.cpp
fi

echo "#include <iostream>" > base.cpp
echo "" >> base.cpp

MANGLED=$(echo "$prefix$middle$suffix $rettype $1{}" >> base.cpp ; cat base.cpp | g++ -x c++ -S - -o- | grep "^_.*:$" | sed -e 's/:$//' | head -n 1)
echo "Mangled name = $MANGLED"

#!/bin/sh

rm my-accounting-obfuscat-salt.map

echo -n "simple store/get: "
# simple store
word=$(./obfuscat.py pen-cust1-webshit my-accounting-obfuscat-salt 1)
# and get
resp=$(./obfuscat.py -d $word my-accounting-obfuscat-salt)

[[ "x$resp" == "xpen-cust1-webshit" ]] || {
    echo fail, unexpected response: \"$resp\"
    exit 1
}
echo "OK"

echo -n "get non-existant: "
resp=$(./obfuscat.py -d aardvark my-accounting-obfuscat-salt)

[[ "x$resp" == "xERROR: aardvark not found in my-accounting-obfuscat-salt.map" ]] || {
    echo fail, unexpected response: \"$resp\"
    exit 1
}
echo "OK"

echo -n "add a 2 word entry store/get: "
# simple store
word=$(./obfuscat.py pen-cust2-webshit my-accounting-obfuscat-salt 2)
# and get
resp=$(./obfuscat.py -d $word my-accounting-obfuscat-salt)
[[ "x$resp" == "xpen-cust2-webshit" ]] || {
    echo fail, unexpected response: \"$resp\"
    exit 1
}
echo "OK"

echo -n "detect out of order inputs: "
# and get
resp=$(./obfuscat.py -d adroitness my-accounting-obfuscat-salt)
[[ "x$resp" == "xERROR 'adroitness' is invalid, possibly corrupted input" ]] || {
    echo fail, unexpected response: \"$resp\"
    exit 1
}
echo "OK"

echo -n "detect non-existant word inputs: "
# and get
resp=$(./obfuscat.py -d damnation my-accounting-obfuscat-salt)
[[ "x$resp" == "xERROR 'damnation' is invalid, possibly corrupted input" ]] || {
    echo fail, unexpected response: \"$resp\"
    exit 1
}
echo "OK"

rm my-accounting-obfuscat-salt.map
echo -n "detect duplicates in persisted storage: "
# simple store
word=$(./obfuscat.py pen-cust1-webshit my-accounting-obfuscat-salt 1)
cat my-accounting-obfuscat-salt.map my-accounting-obfuscat-salt.map >asdf
mv asdf my-accounting-obfuscat-salt.map
resp=$(./obfuscat.py pen-cust1-webshit my-accounting-obfuscat-salt 1)
[[ "x$resp" == "xERROR: duplicate detected: pen-cust1-webshit is already in my-accounting-obfuscat-salt.map" ]] || {
    echo fail, unexpected response: \"$resp\"
    exit 1
}
echo "OK"

rm my-accounting-obfuscat-salt.map
echo -n "detect collisions: "
for i in $(seq 256); do
    ./obfuscat.py $i my-accounting-obfuscat-salt 1 >/dev/null
done

resp=$(./obfuscat.py 257 my-accounting-obfuscat-salt 1)
[[ "x$resp" == "xERROR: cannot add new mapping without colliding with other inputs" ]] || {
    echo fail, unexpected response: \"$resp\"
    exit 1
}
echo "OK"

echo cleaning up
rm my-accounting-obfuscat-salt.map

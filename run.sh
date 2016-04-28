# Type 1
#
#

for i in {1..30}
do
	pypy ttp.py --conf conf.txt --type 1 < tests/type1/100_150_10_75.txt
done
echo

# Type 2
#
#

for i in {1..30}
do
	pypy ttp.py --conf conf.txt --type 2 < tests/type2/c280_i279.txt
done
echo

for i in {1..30}
do
	pypy ttp.py --conf conf.txt --type 2 < tests/type2/c280_i1395.txt
done
echo

for i in {1..30}
do
	pypy ttp.py --conf conf.txt --type 2 < tests/type2/c280_i2790.txt
done

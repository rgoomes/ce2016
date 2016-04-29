# Type 1
#
#

rm bests.txt
for i in {1..10}
do
	pypy ttp.py --conf conf.txt --type 1 < tests/type1/100_150_10_75.txt
done
echo
python plots.py bests.txt

# Type 2
#
#

rm bests.txt
for i in {1..10}
do
	pypy ttp.py --conf conf.txt --type 2 < tests/type2/c280_i279.txt
done
echo
python plots.py bests.txt

rm bests.txt
for i in {1..10}
do
	pypy ttp.py --conf conf.txt --type 2 < tests/type2/c280_i1395.txt
done
echo
python plots.py bests.txt

rm bests.txt
for i in {1..10}
do
	pypy ttp.py --conf conf.txt --type 2 < tests/type2/c280_i2790.txt
done
python plots.py bests.txt

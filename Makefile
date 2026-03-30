run:
	python3 apriori.py $(min_sup) $(input) $(output)

clean:
	rm -f output.txt
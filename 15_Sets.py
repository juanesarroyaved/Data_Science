#Sets (conjuntos)

if __name__ == '__main__':

	s = set([1,2,3])
	t = set([3,4,5])
	u = set([1,2,3,4,5])
	v = set([1,2])

	union = s.union(t)
	interseccion = s.intersection(t)
	diferencia = s.difference(t)
	subset = s.issubset(u)
	superset = s.issuperset(v)
	contiene = 1 in s
	no_contiene = 4 not in s

	print(s,
		t,
		union,
		diferencia,
		subset,
		superset,
		contiene,
		no_contiene)

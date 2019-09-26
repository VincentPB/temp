var cvssData = {
	labels: [
		['AV'],
		['AC'],
		['PR'],
		['UI'],
		['S'],
		['C'],
		['I'],
		['A'],
	],
	datasets: [{
		backgroundColor: red,
		borderColor: red,
		pointBackgroundColor: red,
		data: [
		/* AV : Network, Adjacent, Local, Physical*/ 0.7,
		/* AC : Low, High */ 1,
		/* PR : None, Low, High */ 0.5,
		/* UI : None, Required */ 1,
		/* S : Unchanged, Changed */ 0,
		/* C : None, Low, High */ 1,
		/* I : idem */ 1,
		/* A : idem */ 0.5
		]
	}]
}
var traitData = {
    "1b": [35,	75,	20,	15,	80,	0,	100,	35,	50,	70],
    "2b": [25,	0,	10,	60,	100,	30,	20,	25,	15,	30],
    "3b": [60,	40,	100,	20,	15,	85,	0,	65,	75,	80],
    "4b": [24,	45,	42,	83,	88,	45,	10,	10,	35,	49],
    "5b": [90,	55,	95,	47,	10,	50,	13,	57,	93,	30],
    "6b": [10,	0,	61,	25,	89,	55,	100,	45,	23,	20],
    "7b": [9,	52,	100,	7,	47,	53,	41,	59,	65,	0],
    "8b": [45,	79,	52,	10,	85,	41,	80,	53,	37,	0],
    "9b": [15,	25,	70,	35,	100,	43,	20,	11,	42,	0],
    "10b": [0,	15,	80,	10,	50,	90,	30,	70,	15,	20],
    "11b": [10,	100,	55,	0,	20,	25,	79,	42,	50,	25],
    "12b": [35,	90,	15,	0,	100,	10,	85,	20,	40,	15],
    "13b": [48,	60,	12,	61,	100,	39,	85,	0,	50,	75],
    "14b": [60,	0,	23,	85,	45,	81,	75,	100,	30,	70],
    "15b": [45,	75,	87,	50,	50,	13,	79,	15,	85,	70],
    "16b": [25,	15,	0,	8,	45,	85,	57,	100,	15,	11],
    "17b": [69,	88,	45,	20,	53,	0,	25,	30,	100,	20],
    "18b": [12,	15,	100,	15,	50,	78,	13,	60,	0,	10],
    "19b": [70,	75,	45,	0,	100,	85,	10,	90,	10,	30],
    "20b": [35,	100,	65,	50,	60,	20,	15,	25,	0,	20],
    "21b": [25,	11,	55,	69,	22,	31,	44,	75,	30,	70],
    "23b": [0,	25,	22,	55,	85,	100,	15,	75,	15,	15],
    "24b": [75,	85,	23,	59,	85,	25,	22,	15,	30,	90],
    "25b": [25,	15,	85,	20,	20,	75,	0,	70,	20,	20],
    "26b": [85,	85,	47,	90,	49,	35,	0,	30,	70,	100],
    "27b": [55,	81,	45,	60,	89,	31,	85,	30,	47,	80],
    "28b": [15,	55,	55,	0,	15,	100,	76,	53,	45,	10],
    "29b": [75,	90,	0,	40,	85,	25,	88,	100,	70,	25],
    "30b": [65,	31,	40,	0,	40,	45,	15,	85,	100,	20],
    "31b": [25,	45,	100,	0,	41,	35,	10, 75,	76,	25],
    "32b": [42,	75,	40,	22,	80,	0,	100,	64,	80,	15],
    "33b": [78,	70,	80,	50,	0,	60,	50,	50,	100,	75],
    "34b": [0,	10,	100,	10,	41,	69,	79,	85,	50,	20],
    "35b": [58,	20,	20,	100,	84,	59,	16,	25,	0,	70],
    "36b": [25,	40,	20,	10,	0,	70,	30,	20,	70,	0],
    "37b": [40,	38,	60,	20,	20,	35,	0,	100,	40,	10]
  };

  for (var key in traitData) {
    if (traitData.hasOwnProperty(key)) {
        console.log(key + ": " + traitData[key][2]);
    }
}
# Cosmere

Welcome to the cosmere! We recently discovered this online quiz that can tell us a lot about different orders of the Knights Radiant. On a scale of Free-spirited to Disciplined, what percent disciplined is the ideal Dustbringer?

Flag format - byuctf{percentage} (ie, byuctf{45})

https://www.brandonsanderson.com/official-knights-radiant-order-quiz/

Please note, THIS IS NOT OUR WEBSITE. You cannot use automated tools of any kind. You don't have to script this one. Figure it out.

## Challenge

So first thing I did for this challenge was open up that link and take the quiz. I had my console open looking for some sort of input, and when I submitted the quiz I got some.
```
Trait 1b resulted in 225,625,900,1225,900,2500,2500,225,0,400 script-1.js:580:13
Trait 2b resulted in 625,2500,1600,100,2500,400,900,625,1225,400 script-1.js:580:13
Trait 3b resulted in 100,100,2500,900,1225,1225,2500,225,625,900 script-1.js:580:13
Trait 5b resulted in 1600,25,2025,9,1600,0,1369,49,1849,400 script-1.js:580:13
Trait 6b resulted in 1600,2500,121,625,1521,25,2500,25,729,900 script-1.js:580:13
Trait 7b resulted in 1681,4,2500,1849,9,9,81,81,225,2500 script-1.js:580:13
Trait 8b resulted in 25,841,4,1600,1225,81,900,9,169,2500 script-1.js:580:13
Trait 9b resulted in 1225,625,400,225,2500,49,900,1521,64,2500 script-1.js:580:13
Trait 10b resulted in 2500,1225,900,1600,0,1600,400,400,1225,900 script-1.js:580:13
Trait 11b resulted in 1600,2500,25,2500,900,625,841,64,0,625 script-1.js:580:13
Trait 12b resulted in 225,1600,1225,2500,2500,1600,1225,900,100,1225 script-1.js:580:13
Trait 13b resulted in 4,100,1444,121,2500,121,1225,2500,0,625 script-1.js:580:13
Trait 14b resulted in 100,2500,729,1225,25,961,625,2500,400,400 script-1.js:580:13
Trait 15b resulted in 25,625,1369,0,0,1369,841,1225,1225,400 script-1.js:580:13
Trait 16b resulted in 625,1225,2500,1764,25,1225,49,2500,1225,1521 script-1.js:580:13
Trait 17b resulted in 361,1444,25,900,9,2500,625,400,2500,900 script-1.js:580:13
Trait 18b resulted in 1444,1225,2500,1225,0,784,1369,100,2500,1600 script-1.js:580:13
Trait 19b resulted in 400,625,25,2500,2500,1225,1600,1600,1600,400 script-1.js:580:13
Trait 20b resulted in 225,2500,225,0,100,900,1225,625,2500,900 script-1.js:580:13
Trait 21b resulted in 625,1521,25,361,784,361,36,625,400,400 script-1.js:580:13
Trait 23b resulted in 2500,625,784,25,1225,2500,1225,625,1225,1225 script-1.js:580:13
Trait 24b resulted in 625,1225,729,81,1225,625,784,1225,400,1600 script-1.js:580:13
Trait 25b resulted in 625,1225,1225,900,900,625,2500,400,900,900 script-1.js:580:13
Trait 26b resulted in 1225,1225,9,1600,1,225,2500,400,400,2500 script-1.js:580:13
Trait 27b resulted in 25,961,25,100,1521,361,1225,400,9,900 script-1.js:580:13
Trait 28b resulted in 1225,25,25,2500,1225,2500,676,9,25,1600 script-1.js:580:13
Trait 29b resulted in 625,1600,2500,100,1225,625,1444,2500,400,625 script-1.js:580:13
Trait 30b resulted in 225,361,100,2500,100,25,1225,1225,2500,900 script-1.js:580:13
```

After seeing this I figured the results were being calculated somewhere in `script-1.js` and I would find my answer in there. I went and exfilled the javascript file [here](./code.js).

After parsing the code a little bit, I found this vital information.
```javascript
  var Windrunner = 0;
  var Skybreaker = 1;
  var Dustbringer = 2;
  var Edgedancer = 3;
  var Truthwatcher = 4;
  var Lightweaver = 5;
  var Elsecaller = 6;
  var Willshaper = 7;
  var Stoneward = 8;
  var Bondsmith = 9;
  ...
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
  ...
    {
      promptLeftText: "Free-spirited",
      promptRightText: "Disciplined",
      traitLeft: "15a",
      traitRight: "15b"
    },
```

So three critical things here to find my answer: The index of Dustbringer, the trait table, and then the entry corresponding to disciplined.

I wrote another program, although it wasn't entirely necessary, to print out the entries for Dustbringer.
```javascript
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
```
After running it we can easily see that for `15b` the corresponding number is `87`. You can also see this pretty easily by just looking at the data table.

## Flag

`byuctf{87}`
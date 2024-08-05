# Random

I hid my password behind an impressive sorting machine. The machine is very luck based, or is it?!?!?!?

Author: Connor Chang

## Challenge

This challenge gives us a server.cpp file:
```c++
#include<chrono>
#include<cstdlib>
#include<iostream>
#include<algorithm>
#include<string>
#include<fstream>
#include<thread>
#include<map>
using namespace std;

bool amazingcustomsortingalgorithm(string s) {
    int n = s.size();
    for (int i = 0; i < 69; i++) {
        cout << s << endl;
        bool good = true;
        for (int i = 0; i < n - 1; i++)
            good &= s[i] <= s[i + 1];
        
        if (good)
            return true;

        random_shuffle(s.begin(), s.end());

        this_thread::sleep_for(chrono::milliseconds(500));
    }

    return false;
}

int main() {
    string s;
    getline(cin, s);

    map<char, int> counts;
    for (char c : s) {
        if (counts[c]) {
            cout << "no repeating letters allowed passed this machine" << endl;
            return 1;
        }
        counts[c]++;
    }

    if (s.size() < 10) {
        cout << "this machine will only process worthy strings" << endl;
        return 1;
    }

    if (s.size() == 69) {
        cout << "a very worthy string" << endl;
        cout << "i'll give you a clue'" << endl;
        cout << "just because something says it's random mean it actually is" << endl;
        return 69;
    }

    random_shuffle(s.begin(), s.end());
    
    if (amazingcustomsortingalgorithm(s)) {
        ifstream fin("flag.txt");
        string flag;
        fin >> flag;
        cout << flag << endl;
    }
    else {
        cout << "UNWORTHY USER DETECTED" << endl;
    }
}
```

Running through the code we can pick out the important things:

- In order to win we need `amazingcustomsortingalgorithm` to return true with the string we give
- The string we input is shuffled before checked
- It is checked if it is in alphabetical order
- No duplicate letters allowed
- Needs to be atleast size 10

So I did some digging into this `random_shuffle` function. It turns out that it was depricated in C++11 and removed in C++17. I also found out the random_shuffle function randomly shuffles an item the same way if given that item twice. Therefore taking out some of the randomness. I imagine this is why it was depricated. The function also has an option to give it a RNG seed, which is not utilized here.

Let's test it out:
```
anthony@pwny:~$ nc challs.n00bzunit3d.xyz 10268
abcdefghij
edhiafcbgj
afhiedjcbg
fhgdiecabj
egacibdjfh
^C
anthony@pwny:~$ nc challs.n00bzunit3d.xyz 10268
abcdefghij
edhiafcbgj
afhiedjcbg
fhgdiecabj
```

Here we can see that the string `abcdefghij` is randomized to `edhiafcbgj` both times. So as the challenge description hints, its not entirely random. 

My next thought was, what if I swapped the e with the a, would that place the a at the front where e was?

```
anthony@pwny:~$ nc challs.n00bzunit3d.xyz 10268
ebcdafghij
adhiefcbgj
```

Boom. We we're correct. Now knowing that we can individually derive the order that we need to change the letters in, for it to randomize the string to become `abcdefghij`.

Trial and error I came up with `ehgbaficdj`, which when sent to be randomized, becomes `abcdefghij`. Therefore winning us our flag.

```
anthony@pwny:~$ nc challs.n00bzunit3d.xyz 10268
ehgbaficdj
abcdefghij
n00bz{5up3r_dup3r_ultr4_54f3_p455w0rd_54d51832243e}
```

## Flag

`n00bz{5up3r_dup3r_ultr4_54f3_p455w0rd_54d51832243e}`
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<int> xorResults = {
        98, 222, 123, 236, 220, 185, 246, 157, 139, 204, 53, 17, 120, 62, 218, 141, 241, 67, 202, 18, 201, 8, 253, 160, 240, 3, 15, 250, 15, 52, 4, 5, 93, 21, 150, 133, 118, 25, 243, 104
    };
    std::string originalText;
    unsigned int seed = 1716168252;  
    srand(seed);

    for (int xorValue : xorResults) {
        int randByte = rand() % 256; 
        char originalChar = static_cast<char>(xorValue ^ randByte); 
        originalText += originalChar;
    }

    std::cout << "Original text: " << originalText << std::endl;
    return 0;
}

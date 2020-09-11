#include <iostream> 
#include <fstream> 
#include <vector>
#include <sstream> 


int main()
{
    std::vector<std::string> categories; 
    std::ifstream file; 
    file.open("CategoriesString.txt");

    std::string category; 
    std::string word;
    char comma = ',';
    while(file >> word)
    {
        int length = word.length(); 
        if(word[length-1] != comma)
        {
            category += word + " ";
        }
        else if(word == "Categories" || word[length-1] == comma)
        {
         categories.push_back(category);
         category.erase();
        }
    }
    std::cout<<categories[0]<<std::endl;
}
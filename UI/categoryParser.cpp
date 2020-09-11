#include <iostream> 
#include <fstream> 
#include <vector>
#include <sstream> 
#include <algorithm>

std::vector<std::string> FindDuplicates(std::vector<std::string> categories);
void WriteToFile(std::vector<std::string> categories);

int main()
{
    std::vector<std::string> categories;
    std::vector<std::string> categoriesNoDuplicates;

    std::ifstream file; 
    file.open("CategoriesString.txt");

    for(std::string line; getline(file, line, ',');)
    {
        // store line in string stream
        std::stringstream ss(line);
        for(std::string current; getline(ss, current, ',');)
        {
            categories.push_back(current);
        }
    }
    file.close();
    categoriesNoDuplicates = FindDuplicates(categories);
    WriteToFile(categoriesNoDuplicates);

}

std::vector<std::string> FindDuplicates(std::vector<std::string> categories)
{
    std::vector<std::string>::iterator it; 
    std::sort(categories.begin(), categories.end());
    categories.erase(std::unique(categories.begin(), categories.end()), categories.end());

    return categories;
}
void WriteToFile(std::vector<std::string> categoriesNoDuplicates)
{
    std::ofstream outFile; 
    outFile.open("parsedCategories.txt");
    for(int i = 0; i < categoriesNoDuplicates.size(); i++)
    {
        outFile<<categoriesNoDuplicates[i]<<"\n";
    }
    outFile.close();
}
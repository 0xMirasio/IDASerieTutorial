#include <iostream>

struct Person {
    std::string name;
    int age;
    std::string profession;
};

"""
struct basic_string
{
  char *begin_;
  size_t size;
  union
  {
    size_t capacity_;
    char sso_buffer[16];
  };
};
"""


int main() {
    Person person;
    person.name = "John Doe";
    person.age = 30;
    person.profession = "Dev";

    std::cout << "Nom: " << person.name << std::endl;
    std::cout << "Âge: " << person.age << std::endl;
    std::cout << "Profession: " << person.profession << std::endl;


    return 0;
}
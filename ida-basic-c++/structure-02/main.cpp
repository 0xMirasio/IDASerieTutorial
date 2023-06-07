#include <iostream>

// Classe de base
class Forme {
public:
    virtual void afficher() = 0; // se fera override. 
    virtual ~Forme() {} // Virtual destructor
};

// Classe dérivée
class Cercle : public Forme {
public:
    void afficher() override { 
        std::cout << "Je suis un cercle." << std::endl;
    }
};

"""
struct vtable_cercle
{
  void (__fastcall *afficher_cercle)();
  void (__fastcall *cleanup)();
  void (__fastcall *destructor)();
};
"""

// Classe dérivée
class Carre : public Forme {
public:
    void afficher() override {
        std::cout << "Je suis un carré." << std::endl;
    }
};

int main() {
    Forme* forme1 = new Cercle();
    forme1->afficher();

    Forme* forme2 = new Carre();
    forme2->afficher();

    delete forme1;
    delete forme2;

    return 0;
}


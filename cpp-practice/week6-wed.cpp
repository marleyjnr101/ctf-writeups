#include <iostream>
using namespace std;

      int main(){
        float price_per_item = 350;
        float quantity = 80;
        float discount_percent = 10;
       float  total = price_per_item * quantity;
       float final = total - (total *discount_percent/100);
       cout <<"Subtotal: " << total << endl;
       cout << "After Discount: " << final << endl;
       return 0 ;

      }
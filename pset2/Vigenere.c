#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
 
int shift (char c);
int main(int argc, string argv[])
{
  if(argc != 2)
  {
      printf ("Usage: ./caesar keyword\n");
      return 1;
  }
 
  int n = strlen (argv [1]);
  for (int i = 0; i < n; i ++)
  {
      if (!isalpha (argv[1][i]))
      {
          printf ("Usage: ./caesar keyword\n");
          return 1;
      }
  }
 string s = get_string ("plaintext: ");
 printf ("ciphertext: ");
 int key = 0;
 int pointer = 0;
 for (int k = 0; k < strlen (s); k++)
 {
     if ((s[k] >= 'A' && s[k] <= 'Z') || (s[k] >= 'a' && s[k] <= 'z'))
     {
         key = shift(argv[1][pointer]);
         if (pointer == strlen (argv[1])-1)
         {
             pointer = 0;
         }
         else
         {
             pointer++;
         }
        
         if (s[k]%32 + key%26 <= 26)
         {
             printf ("%c", s[k] + key%26);
         }
         else
         {
             printf ("%c", s[k] - 26 + key%26);
         }
     }
     else
     {
         printf ("%c", s[k]);
     }
 }
 printf ("\n");
}
   
int shift (char c)
{
    int key = 0;
    c = tolower (c);
    char alphabet[26] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
    for (int i = 0; i < 26; i++)
    {
        if (c == alphabet [i])
        {
            key = i;
           
        }
    }
    return key;
}
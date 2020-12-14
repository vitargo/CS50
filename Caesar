#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
 
int main(int argc, string argv[])
{
   int key = 0;
   int n = 0;
 
/*
   if(argc != 2) return 1;
 
   key = atoi (argv[1]);
  
   if(key == 0) return 1;
 
*/
 
   if (argc == 2)
   {
       n = strlen (argv [1]);
       for (int i = 0; i < n; i ++)
       {
         if (argv[1][i] > '0' && argv[1][i] <= '9')
         {
             key = atoi (argv[1]);
         }
         else
         {
             printf ("Usage: ./caesar key\n");
             return 1;
         }
       
       }
   }
   else
   {
       printf ("Usage: ./caesar key\n");
       return 1;
   }
//    printf ("%i\n", key);
   string s = get_string ("plaintext: ");
   printf ("ciphertext: ");
  
   for (int k = 0; k < strlen (s); k++)
   {
       if ((s[k] >= 'A' && s[k] <= 'Z') || (s[k] >= 'a' && s[k] <= 'z'))
       {
           if (s[k]%32 + key%26 < 26)
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

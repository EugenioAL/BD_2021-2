/* strtok example */
#include <stdio.h>
#include <string.h>

int main ()
{
  char str[] =""1";"Poster: 3D sketching and flexible input for surface design: A case study.";"2013";"Anamary Leal|Doug A. Bowman";"0";"2016-07-28 09:36:29";"Poster: 3D sketching and flexible input for surface design: A case study. A Leal, DA Bowman -  Interfaces (3DUI), 2013 IEEE Symposium , 2013 - ieeexplore.ieee.org. ABSTRACT Designing three-dimensional (3D) surfaces is difficult in both the physical world  and in 3D modeling software, requiring background knowledge and skill. The goal of this  work is to make 3D surface design easier and more accessible through natural and  .."";
  char * pch;
  printf ("Splitting string \"%s\" into tokens:\n",str);
  pch = strtok (str," ,.-");
  while (pch != NULL)
  {
    printf ("%s\n",pch);
    pch = strtok (NULL, " ,.-");
  }
  return 0;
}
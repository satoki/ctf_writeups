#include <stdio.h>  			  	 
	
// This challenge should be a	fun	one!    	
	
// Compile with   		   		
//	gccmain.c
// then run with  			 	  
//	./a.out
     		  		 
	
int main()    				 		
	
{     	 	  	 
	
    int show_the_flag	=	0;  		
	
// Pull in the flag using	some	pre-processor hacks!	  
	
char *flag =   		  	  
	
#include "flag.txt"    		   	
	
;     		 			 
	
    if (show_the_flag)		  			
	
    { 	    	 
	
     		 printf( 	 	
	
     			 	  flag
	
     			); 			
	
    } 		  		
	
    else 		  		
	{
     		 while(1)			 
	
     	    		{
	
     		 	   printf(
	
     		    	"Youneedtofindtheflag!"
	
     			  	 );
	
     		 	  }
	
    } 		   		
	
    printf( 			 	  
	
     		 "Something went	wrong!"	
	
    ); 			  	 
	
    return 0;		 	 	
	
}     					 	
	
  
# Pythagorean Tree Fractal 2:Algorithms:100pts
Pythagorean Tree 2  
Because every good thing must have a sequel ;)  
Please see the attached file for more details (and ignore the red dots on the images).  
Note: Don't worry about overlapping squares!  
[PTF2.pdf](PTF2.pdf)  

# Solution
PDFを見るとどうやらピタゴラスの木の70368744177664ステップ目の面積がflagなようだ。  
1ステップ目の面積は25と与えられており、重ならない。  
簡略化のため、1ステップ目の正方形の面積が1である時の2ステップ目の正方形の面積について考えると、1ステップ目の正方形の一辺が1であるので2ステップ目の正方形の一辺は1/√2となり面積は1/2。  
それが二つあるため増加した面積は1であり、1ステップ目の面積分増えている。  
よって70368744177664ステップ目の面積は70368744177664*25=1759218604441600である。  

## flag{1759218604441600}
@ Comments begin with '@' character.  
@ All whitespaces are ignored.  
@ Assign variables using the <- operator.  
<pre>
n <- 5;  
p <- 2;  
z <- 7;  
c <- "hello world";  
</pre>

@ Print statement can print any arithmetic expression, string or variable.  
`bolo z - 5 * 2;`  

@ If statement should be followed by a then statement and end with done statement.  
@ Optionally you can include an else statement.  
@ Grouped binary expressions along with and, or, not are supported.  
<pre>
agar (p >=1 aur p<=2) ya (1 = 1) ya (not (1 = 2)) toh  
    @ Grouped expressions are supported with proper operator precedence.  
    n <- ((2 * 1) + z)  
nahi-toh  
    n <- z - 1;  
    p <- 1  
khatam;  
</pre>
@ While loops execute till the condition is true.  
<pre>
jab-tak n > 0 tab-tak
  p <- p * n;
  bolo p;
  n <- n - 1
khatam
</pre>
@ The last statement in a set of compound statements should not have a semicolon.

# Mathematical details

We will give a precise definition of what is called *Thompson's group $F$* in mathematics, especially group theory.
This algebraic object can be defined in one of several ways. We decide to choose an approach where the elements of $F$ are
some piecewise-linear bijections of the set $\mathbb{R}$ of real numbers.

We will adhere to the convention of writing $fg$ for the composition of functions $f$ and $g$ with the meaning that $g$ acts on the argument first, then $f$ acts on the result, i.e. $fg(x)=f(g(x))$ for all $x$.
By a *dyadic rational* we mean a rational number represented by a fraction with denominator $2^k$ for some integer $k\ge 0$.

## Definition of the group
*Thompson's group $F$* is the group of all functions $f: \mathbb{R} \to \mathbb{R}$ satisfying the following conditions:
- $f$ is an increasing bijection;
- there are finitely many dyadic rationals (called *breakpoints*) $x_1 < \dots < x_n$ such that $f$ restricted to each of the intervals $[x_i, x_{i+1}]$ for $1\le i<n$, is a linear function with slope $2^k$ for some integer $k$;  
- there exist $l, m\in\mathbb{Z}$ such that $f(x) = x + l$  for $x \le x_1$ and $f(x) = x + m$ for $x\ge x_n$.

## Finite presentation and generators
It is known that Thompson's group $F$ admits the following presentation:
$$\left<a,b \;|\; [ab^{-1}, a^{-1}ba], \, [ab^{-1}, a^{-2}ba^{2}\right>,$$
where $[g, h]:=ghg^{-1}h^{-1}$ denotes the commutator of $g$ and $h$.
This presentation maps abstract letters $a$, $b$ to the elements $f_a, f_b \in F$ given by
$$f_a(x)= x - 1 \quad\text{for } x \in \mathbb{R};\qquad 
f_b(x)= 
\begin{cases}
x & \text{for }  x\leq 0,\\
\frac{1}{2} x & \text{for } 0 \leq x \leq 2,\\
x - 1 & \text{for } 2 \leq x.
\end{cases}$$

The functions defined above are called the *standard generators* of $F$.

## Interpretation as *arc forest diagrams*
In the literature, there are several ways of visualizing the elements of $F$. They can be regarded as pairs of binary rooted trees or pairs of infinite forests consisting of such trees. The latter approach was decribed by Belk.
Guba and Sapir studied $F$ as a *diagram group*, where the diagrams resembled some collection of arcs.

We will introduce an interpretation of $F$ in which any element of $F$ can be represented by a diagram consisting of one infinite forest instead of two. Such a forest is built from subintervals of $\mathbb{R}$, which could then be drawn in a picture in form of arcs (semicircles). These diagrams build a bridge between the approaches of Belk and Guba, Sapir.

Let us proceed to the formal definitions.

### Interval tree
An *interval tree* (briefly *tree*) is any finite family $\mathcal{I}$ of bounded, closed (non-degenerated) subintervals of $\mathbb{R}$ satisfying:
- for each $I=[a, b] \in \mathcal{I}$ both $a$ and $b$ are dyadic rationals; 
- there exists $I_{max}=[a, b]\in \mathcal{I}$, called the *root*, such that all the members of $\mathcal{I}$ are contained in $I_{max}$;
- any $I\in \mathcal{I}$ which is not minimal (with respect to inclusion) in $\mathcal{I}$ has precisely two direct predecessors $I_l = [a, b]$, $I_r=[c, d]$ (called the *left child* and *right child* of $I$, respectively) such that $b=c$ and $I=I_l \cup I_r$;
- if $I\in\mathcal{I}$ and its both children $I_l, I_r$ are minimal in $\mathcal{I}$ (i.e. they are *leaves*), then $I_l$, $I_r$ do not have the same length (so they do not divide $I$ into halves).

A tree is called *trivial* if it contains only its root $I_{max}$ and  $I_{max}=[n, n+1]$ for some $n\in \mathbb{Z}$

### Forest
A doubly infinite sequence $(T_n)_{n\in\mathbb{Z}}$ of interval trees is called a *forest* if there exists an increasing sequence $(r_n)_{n\in\mathbb{Z}}$ such that $I_n:=[r_n, r_{n+1}]$ is the root of $T_n$ for each $n\in\mathbb{Z}$, only finitely many trees in the sequence are not trivial and $\bigcup\limits_{n\in\mathbb{Z}} I_n = \mathbb{R}$. 
The *trivial forest* is the forest whose all trees $T_n$ are trivial and the root of $T_n$ is equal to $[n, n+1]$ for each $n\in \mathbb{Z}$.

### Diagram
Suppose that we are given a forest $(T_n)_{n\in\mathbb{Z}}$ of interval trees. We will visualize it in the form of an *arc forest diagram* (briefly *diagram*) as follows. For each tree $T_n$ and interval $[a,b]\in T_n$ we draw in the plane $\mathbb{R}^2$ an arc being the upper half of the circle with center at $(\frac{a+b}{2}, 0)$ and radius $\frac{b-a}{2}$. It is clear that the roots of the trees are represented as *maximal* arcs (there are no arcs above them). In the diagram we mark also the *basepoint* $(r_0, 0)$, where $r_0$ is the left end of the root of $T_0$. Formally, by a diagram we mean the collection of all so constructed arcs together with the basepoint. It is not hard to convince oneself that, given a diagram, it is possible to reconstruct the original forest.

### The correspondence between elements of $F$ and diagrams
Let $f$ be an element of Thompson's group $F$. We will associate a forest and, subsequently, a diagram $D(f)$ with $f$ according to the following algorithm.
1. For each $n\in\mathbb{Z}$ start constructing a tree $T_n$ by defining its root as the interval $I_n=[f(n), f(n+1)]$.
2. If $f$ is linear on $[n, n+1]$, we stop the construction of $T_n$. From the definition of $F$ it follows that, for sufficiently large and sufficiently small $n$, the construction of $T_n$ will be terminated, ending up with a trivial tree.
3. If $f$ is not linear on $[n, n+1]$, we divide that interval into halves and declare the left and right child of $I_n$ to be the image under $f$ of the left and, respectively, right half of $I_n$.
4. We proceed in a loop applying points 2 and 3 to all leaves $L$ of the forest that we have constructed so far, but taking $f^{-1}(L)$ instead of $[n, n+1]$ and $L$ instead of $L$.
5. The construction of the forest is complete when $f$ is linear on  $f^{-1} (L)$ for all the leaves.
6. We transform the forest into a diagram replacing all intervals by arcs and picking $f(0)$ as the basepoint.

It is not hard to check that the correspondence $f\mapsto D(f)$ is one-to-one and for any diagram we can reconstruct the corresponding element of $F$.

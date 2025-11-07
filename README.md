# Da Lamb

## Introduction

Da Lamb is a lambda abstraction language inspired by [de Bruijin Index](https://en.wikipedia.org/wiki/De_Bruijn_index). The basic grammar of da Lamb abstraction is 

$$\lambda^n[v_n, v_{n-1} \cdots v_1](\text{expr}_{v_n, v_{n-1} \cdots v_1})$$

The exponent $n$ of $\lambda$ denotes how many arguments the abstraction eventually takes. Da Lamb supports currying. Whenever an argumetn is input to the abstraction, the exponent of $\lambda$ reduces by one. For example, the identity `id` is defined as `λ[x1](x1)` in da Lamb, and for any expression `X`, `λ[x1](x1) X` evaluates to `X`. 

You can use `L` instead of `λ`, and for variables, da Lamb only checks the index of the variables and ignores the alphabets. Everything that looks like `"[a-z]+" INT` will be parsed as `"v" INT`. Therefore, because da Lamb uses indecies to identify variables, there is no requirement to declare the variables. Everything inside `[...]` are ignored as comments. Therefore, if you compile `L[x1](x1)`, it essentially becomes `λ(v1)`. You can simply write `L(v1)`.

## Usage

Load pre-defined names from `names.json`
```
>>> from lamb inport *
>>> Lamb.load_names()
```

Parse an expression
```
>>> lamb = parse("gcd 3 6")
```

Evaluate the expression
```
>>> print(lamb.eval())
λ^2((v2 (λ((v2 (λ((v2 v1)) v1))) v1)))
```

Print the evaluation steps
```
lamb.dfs_derive()
...
...
...
= λ^2((v2 (λ((v2 (((succ zero) v2) v1))) v1)))
= λ^2((v2 (λ((v2 (((λ^3((v2 ((v3 v2) v1))) zero) v2) v1))) v1)))
= λ^2((v2 (λ((v2 ((λ^2((v2 ((zero v2) v1))) v2) v1))) v1)))
= λ^2((v2 (λ((v2 (λ((v2 ((zero v2) v1))) v1))) v1)))
= λ^2((v2 (λ((v2 (λ((v2 ((false v2) v1))) v1))) v1)))
= λ^2((v2 (λ((v2 (λ((v2 ((λ^2(v1) v2) v1))) v1))) v1)))
= λ^2((v2 (λ((v2 (λ((v2 (λ(v1) v1))) v1))) v1)))
= λ^2((v2 (λ((v2 (λ((v2 v1)) v1))) v1)))
```

## Philosophy
### Why $\lambda^n$?
$\lambda$ is a function that maps any expression to its abstraction, adding a required argument at the front. Repeated abstraction corresponds to function conposition $\lambda \circ \lambda \circ \cdots \circ \lambda = \lambda^n$
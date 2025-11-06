# Da Lamb

## Introduction

Da Lamb is a lambda abstraction language inspired by [de Bruijin Index](https://en.wikipedia.org/wiki/De_Bruijn_index). The basic grammar of da Lamb abstraction is 

$$\lambda^n[v_n, v_{n-1} \cdots v_1](\text{expr}_{v_n, v_{n-1} \cdots v_1})$$

The exponent $n$ of $\lambda$ denotes how many arguments the abstraction eventually takes. Da Lamb supports currying. Whenever an argumetn is input to the abstraction, the exponent of $\lambda$ reduces by one. For example, the identity `id` is defined as `λ[x1](x1)` in da Lamb, and for any expression `X`, `λ[x1](x1) X` evaluates to `X`. 

You can use `L` instead of `λ`, and for variables, da Lamb only checks the index of the variables and ignores the alphabets. Everything that looks like `"[a-z]+" INT` will be parsed as `"v" INT`. Therefor, because da Lamb uses indecies to identify variables, there is no requirement to declare the variables. Everything inside `[...]` are ignored as comments. Therefor, if you compile `L[x1](x1)`, it essentially becomes `λ(v1)`
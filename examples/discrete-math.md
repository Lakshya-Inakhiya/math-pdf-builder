# Discrete Math Essentials

## Logic and Proofs

<div class="definition" markdown="1">
**Contrapositive.** $p \to q$ is logically equivalent to $\neg q \to \neg p$.
</div>

<div class="worked-example" markdown="1">
**Claim.** There are infinitely many primes.

**Proof.** Suppose $p_1, \dots, p_k$ are all the primes and let $N = p_1 p_2 \cdots p_k + 1$. No $p_i$ divides $N$, but $N > 1$ has a prime factor. Contradiction.
</div>

## Induction

$$
\sum_{i=1}^{n} (2i - 1) = n^2
$$

<div class="tips" markdown="1">
**Pattern.** State $P(k)$, add exactly the next term, and close with "by induction".
</div>

## Counting

| Rule | Formula |
|------|---------|
| Permutations | $P(n,r) = \dfrac{n!}{(n-r)!}$ |
| Combinations | $\binom{n}{r} = \dfrac{n!}{r!\,(n-r)!}$ |
| Inclusion–exclusion | $\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert - \lvert A \cap B \rvert$ |

<div class="exam-trap" markdown="1">
**Trap.** Pigeonhole proofs live or die on choosing the holes. Name pigeons and holes explicitly.
</div>

## Graphs

<div class="key-result" markdown="1">
**Euler's formula.** For a connected planar graph, $v - e + f = 2$, so $e \le 3v - 6$ when $v \ge 3$. Since $K_5$ has $10 > 9$ edges, it is not planar.
</div>

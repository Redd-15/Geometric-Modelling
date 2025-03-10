Bezier görbe
============

A de Casteljau-algoritmus
-------------------------

Paul de Faget de Casteljau
https://en.wikipedia.org/wiki/Paul_de_Casteljau

A Bernstein polinom
-------------------

Az :math:`i`-edik :math:`n`-edfokú Bernstein polinomot az alábbi formában definiáljuk:

.. math::

  B_i_n(t) = \binom{n}{i} t^i (1 - t)^{n - i}, \quad i = 0, 1, \ldots, n.

Definíció szerint továbbá

.. math::

  B_0^0(t) = 1, \quad B_i^n(t) = 0, \text{ha } i \notin [0, n].

https://en.wikipedia.org/wiki/Bernstein_polynomial

A Bézier görbe paraméteres alakja
---------------------------------

Pierre Étienne Bézier
https://en.wikipedia.org/wiki/Pierre_B%C3%A9zier

A Bernstein polinom segítségével a Bézier görbét fel tudjuk írni paraméteres alakban.

Kérdések
========

Feladatok
=========

Binomiális együtthatók számítása

* Vizsgáljuk meg a binomiális együttható faktoriálisokkal és rekurzív formulával történő számítási módját!
* Utóbbinál vizsgáljuk meg a gyorsítótárazás hatását!
* Készítsünk méréseket és ábrázoljuk a kapott eredményeket!

A de Casteljau algoritmus

* Implementáljuk a de Casteljau algoritmust!
* Rajzoljuk be egy adott pont számítása esetén a segédvonalakat!
* Oldjuk meg, hogy a kijelölt ponthoz tartozó :math:`t` paramétert lehessen módosítani (például csúszkával vagy görgővel)!


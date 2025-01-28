# H05: Data 2

Balíček `data` z minulého semináře rozšiřte o následující funkcionalitu. Ve zdrojovém kódu urdžujte pořádek a metody seskupujte dle významu.

## Metoda `__len__`

Třídě `DataFrame`, `Series` a `Index` implementujte metodu `__len__` obsluhující volání funkce `len()`. V případě třídy `Series` a `Index` se jedná o počet prvků, v případě `DataFrame` o počet sloupců, tj. počet prvků indexu v atributu `index`.

## Změna atributů `.labels`, `.values` a `.index` na vlastnosti 

Třídě `Index` změnte atribut `.labels` na vlastnost pomocí dekorátoru `@property`, přičemž tato vlastnost nebude nastavitelná.

```python
from data.index import Index

users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

assert users.labels == ["user 1", "user 2", "user 3", "user 4"]
# AttributeError: property 'labels' of 'Index' object has no setter
users.labels = [] 
```

Podobně změnte třídě `IndexedContainer` atribut `.values` na vlastnost pomocí dekorátoru `@property`, přičemž tato vlastnost nebude nastavitelná. Analogicky upravte atribut `.index`, kterému ale definujte i `setter`, přičemž změna hodnoty proběhne jen v případě, že nový `Index` má stejnou délku jako `.values` (v opačném případě nastane `IndexMismatchError`).


```python
from data.indexed_container import IndexedContainer

users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
numbers = IndexedContainer([1, 2, 3, 4], index=users)

assert numbers.values == [1, 2, 3, 4]
# AttributeError: property 'values' of 'IndexedContainer' object has no setter
numbers.values = []

assert numbers.Index == users
# IndexMismatch Error
numbers.index = Index(labels=[42])
# toto nastavení proběhne v pořádku
numbers.index = Index(labels=['a', 'b', 'c', 'd'])
```

## Vlastnost `.shape`

Třídě `DataFrame` a `Series` přidejte vlastnost `.shape`, která pomoci tuple reprezentuje rozměry. Vlastnost se bude počítat při každém volání znovu (použíjte dekorátor `@property`).

```python
from data.series import Series
from data.index import Index
from data.dataframe import DataFrame

users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

salaries = Series([20000, 300000, 20000, 50000], index=users)
names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
cash_flow = Series([-100, 10000, -2000, 1100], index=users)

assert cash_flow.shape == (4, )

data = DataFrame([names, salaries, cash_flow], index=Index(["names", "salary", "cash flow"]))

assert data.shape == (4, 3)
```

## Metody `.from_csv(text, separator=",")`

Implementujte class metody `DataFrame.from_csv(text, separator=",")` a `Series.from_csv(text, separator=",")` umožňující vytvořit odpovídající třídy na základě řetězce hodnot oddělených separátorem. Na rozdělení textu na jednotlivé řádky použíjte `text.splitlines()`.

Hodnoty vždy reprezenrujte jako řetězec, nepřevádějte je na čísla nebo jiné datové typy.

```python
from data.series import Series

input_text = """user 1,user 2,user 3,user 4
Lukas Novak,Petr Pavel,Pavel Petr,Ludek Skocil
"""

data = Series.from_csv(input_text)
assert data.index.labels == ["user 1", "user 2", "user 3", "user 4"]
assert data.values == ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"]
```

```python
from data.dataframe import DataFrame

input_text=""",names,salary,cash flow
user 1,Lukas Novak,20000,-100
user 2,Petr Pavel,300000,10000
user 3,Pavel Petr,20000,-2000
user 4,Ludek Skocil,50000,1100"""

data = DataFrame.from_csv(input_text)

assert data.index.labels == ["names", "salary", "cash flow"]

assert list(data.values[0].values) == list(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"])
assert data.values[0].index.labels == ["user 1", "user 2", "user 3", "user 4"]
assert list(data.values[1].values) == list(["20000", "300000", "20000", "50000"])
assert data.values[1].index.labels == ["user 1", "user 2", "user 3", "user 4"]
assert list(data.values[2].values) == list(["-100", "10000", "-2000", "1100"])
assert data.values[2].index.labels == ["user 1", "user 2", "user 3", "user 4"]

# nezapomeňte, že přetypování na čísla lze řešit následovně (součet všech platů)
data.get("salary").apply(int).sum()
```

## Metody `__str__` a `__repr__` pro třídy `Series` a `DataFrame`

```python
from data.series import Series

users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
salaries = Series([20000, 300000, 20000, 50000], index=users)
```

Očekávaný výstup `print(salaries)` a `repr(salaries)`. Mezi popis a hodnotu vkládejte tabulátor (`\t`).

```
user 1  20000
user 2  300000
user 3  20000
user 4  50000
```

V případě třídy `DataFrame` bude metoda `__repr__` a `__str__` jednoduší:

```
DataFrame(2, 4)
```

Kde `2` (počet řádků) a `4` jsou rozměry dataframu.

## Series operace

Třídě `Series` implementujte následující operace. Veškeré operace pracují po prvcících, výsledkem je vždy nová instance `Series`. Pokud vstupní instance nebudou mít stejnou délku, vyvolejte `ValueError`. V případě, že operace není definovaná pro dané argumenty, vraťte konstantu `NotImplemented`. 

```
__add__ # chování +
__sub__ # chování -
__mul__ # chování *
__truediv__ # chování /
__floordiv__ # chování //
__mod__ # chování %
__pow__ # chování ** nebo pow()
```

Metody implementujte pomoci pomocné metody `Series._apply_operator(self, other, operator)`, která využívá modul `operator` https://docs.python.org/3/library/operator.html. Sčítání pak například tedy můžeme realizovat jako:

```python
import operator

...
self._apply_operator(self, other, operator.add)
...
```

Dále implementujte metodu `__round__(self, precision)` umožňující použití vestavěné funkce `round(number, precision)`. Výsledkem je opět nová instance `Series`. Dokážete použít metodu `Series.apply(self, func)`?

## Lokální testování

Funkčnost řešení ověříte následujícím příkazem:

```bash
pytest
```
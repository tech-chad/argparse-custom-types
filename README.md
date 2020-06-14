# argparse-custom-types

Special custom types for argparse

### How to install
```pip install argparse_custom_types```

### Description
Additional custom types to be used with argparse

### How to use
Import argparse_custom_types setup the custom type then pass the function to the type keyword in argparse.add_argument()


### Types


- **int_range**
  - custom int in range from start to stop (not including) optional step
  ``` python
  def int_range(start: int, stop: int, step: int = 1):
   ```
  - example:
  >``` python
  > t = int_range(5, 21, 5)
  > ```
  >
  >  int types 5, 10, 15, 20 would be accepted
- **int_above**
  ``` python
  def int_above(minimum: int):
  ```
  - int equal to or above the minimum entered
  - example:
  >``` python
  > t = int_above(40)
  > ```
  >
  >  int types 40 and above would be accepted
- **int_below**
  ``` python
  def int_below(maximum: int):
  ```
  - int equal to or below maximum
  - example:
  >``` python
  > t = int_below(25)
  > ```
  >
  >  int types 25 or below would be accepted
- **int_even**
  ``` python
  def int_even(pos_number: bool = True, neg_number: bool = False,include_zero: bool = False):
  ```
  - even int with option to include negative, zero or exclude positive
  - example:
  >``` python
  > t = int_even(neg_number=True)
  > ```
  >
  >  int types 2, -30, 102 would be accepted
  >  int types 1, -29, 101 would not be accepted
- **int_odd**
  ``` python
  def int_odd(pos_number: bool = True, neg_number: bool = False,include_zero: bool = False):
  ```
  - odd int with option to include negative, zero or exclude positive
  - example:
  >``` python
  > t = int_odd(neg_number=True)
  > ```
  >
  >  int types 1, -29, 101 would be accepted
  >  int types 2, -30, 102 would not be accepted
- **in_sequence_strings**
  ``` python
  def in_sequence_strings(sequence: Union[Tuple[str], List[str]],
                          show_on_invalid: bool = False,
                          case_sensitive: bool = True):
  ```
  - Value that is in the tuple or list and returns that value as a string.
  - example:
  >``` python
  > t = in_sequence_strings(["one", "test", "parser"])
  > ```
  >
  >  any value not in the list ["one", "test", "parser"] will not be accepted
  >

- **in_sequence_ints**
- ```python
  def in_sequence_ints(sequence: Union[List[int], Tuple[int]],
                       show_on_invalid: bool = False):
  ```
  - Int value in sequence will be accepted and return a int value


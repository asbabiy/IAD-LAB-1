# Список реализованных функций

## Базовые функции

Работа со справочником реализована через `PonyORM` и базу данных `SQLite`. 

Реализованы все базовые и дополнительные функции. 
Кроме того, реализованы:
- функция сортировки базы данных по разным атрибутам в возрастающем и убывающем порядке (на выбор)
- функция полной очистки справочника.

Весь код логически разделён на три файла:
- основной функционал в `phonebook.py`
- небольшие вспомогательные функции в `supplementary.py`
- функции для валидации и обработки учётных данных в `credhandlers.py`

Для валидации входных данных везде была использована универсальная функция и регулярное выражение.

Ко всем функциям, классам и файлам прописаны докстринги в формате reStructuredText. Был использован Python 3.8. Файл `requirements.txt` приложен.

Ниже в этом файле будет небольшое описание **всех функций и примеров их работы при разных сценариях**.

#### 0. Главное меню справочника

```
WELCOME TO THE PHONEBOOK!

Please choose the number of the desired operation:
(1)  Add new record to the phonebook
(2)  Introduce some changes to the records
(3)  Remove a record from the phonebook
(4)  Get age of the person
(5)  Show all records
(6)  Find records
(7)  Get records by birthday
(8)  Remove a record by phone
(9)  Sort records
(10) Get records with birthday within a month
(11) Get records with the age above/below/exactly N years
(12) Remove all records


Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 1. Просмотр всех записей справочника

```
Here is your phonebook.

id|name     |surname|phone       |office_phone|landline_phone|birth_date
--+---------+-------+------------+------------+--------------+----------
1 |John     |Doe    |89997652378 |None        |None          |1978-04-05
2 |Jane     |Doe    |89991112233 |None        |None          |2000-01-02
3 |Gini     |Doe    |89991010101 |None        |4555555555    |2003-01-03
4 |Kevin    |Doe    |89992304545 |89992003030 |None          |None      
5 |Larry    |Doe    |89998883434 |None        |None          |None      
6 |Tyler    |Doe    |89998884040 |None        |None          |1993-07-05
7 |Josh     |Doe    |89991234567 |None        |None          |1983-12-25
8 |Robert   |Doe    |89993502020 |None        |None          |2010-12-17
23|Guido    |Doe    |89991234567 |None        |None          |1993-05-01
24|Sarah    |Doe    |88999567091 |None        |4888888888    |None      

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 2. Поиск по справочнику

```
You chose to find records. Provide credentials of the person.

NAME >> John
SURNAME >>    
DATE >> 
PERSONAL PHONE NUMBER >> 
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

These are the appropriate records.

id|name|surname|phone      |office_phone|landline_phone|birth_date
--+----+-------+-----------+------------+--------------+----------
1 |John|Doe    |89997652378|None        |None          |1978-04-05

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 3. Добавление новой записи

Имя, фамилия и личный номер телефона обязательны, остальные опциональны.

##### 3.1. Идеальный случай (атрибуты DATE, OFFICE PHONE NUMBER и LANDLINE PHONE NUMBER не являются обязательными и могут быть пропущены)

```
You chose to add a new record. Provide credentials of the person.

NAME >> Alexander
SURNAME >> Doe
DATE >> 09.09.2000
PERSONAL PHONE NUMBER >> 89995556677
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

Alexander Babii was added to your phonebook.


Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 3.2. Неверный ввод

```
You chose to add a new record. Provide credentials of the person.

NAME >> 67dsf6567sdf

It seems to be incorrect. Try again.

NAME >> Ivan
SURNAME >> 66576dsf

It seems to be incorrect. Try again.

SURNAME >> Ivanov
DATE >> dfg543

It seems to be incorrect. Try again.

DATE >> 01.01.1999
PERSONAL PHONE NUMBER >> +79999999999999999999999

It seems to be incorrect. Try again.

PERSONAL PHONE NUMBER >> +79991112233
OFFICE PHONE NUMBER >>                   
LANDLINE PHONE NUMBER >> 

Ivan Ivanov was added to your phonebook.


Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 3.3.1. Имя и фамиля уже есть в справочнике (change)

```
You chose to add a new record. Provide credentials of the person.

NAME >> John  
SURNAME >> DOe
DATE >> 02.01.2002
PERSONAL PHONE NUMBER >> 89991001010
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

This person is already in the phonebook.

Choose one of the options below:
--- 'overwrite' to change the existing record
--- 'change' to change your query
--- 'menu' to return to the menu

OPTION >> change

You chose to change you query. Provide credentials.

NAME >> Nora 
SURNAME >> Doe


Nora Doe was added to your phonebook.


Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 3.3.2. Имя и фамиля уже есть в справочнике (overwrite)

```
You chose to add a new record. Provide credentials of the person.

NAME >> John
SURNAME >> Doe
DATE >> 05.13.2006
PERSONAL PHONE NUMBER >> 89991402386
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

This person is already in the phonebook.

Choose one of the options below:
--- 'overwrite' to change the existing record
--- 'change' to change your query
--- 'menu' to return to the menu

OPTION >> overwrite

Record is overwritten successfully.

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 3.3.3. Имя и фамиля уже есть в справочнике (menu)

Если вписать 'menu', то консоль очистится и выведется главное меню.

#### 4. Удаление записи по имени и фамилии

Оба поля обязательны

##### 4.1. При наличии человека в базе

```
You chose to remove a record. Provide credentials of the person.

NAME >> John
SURNAME >> DOE

This person was removed from your phone book.


Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 4.2. При отсутствии человека в базе

```
You chose to remove a record. Provide credentials of the person.

NAME >> dgdfgfdgsd
SURNAME >> dfgdfgfg

This person isn't in the phonebook.


Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 5. Вывод возраста человека по имени и фамилии

Оба поля обязательны.

##### 5.1. Нормальные входные данные

```
You chose to get someone's age. Provide credentials of the person.

NAME >> jane
SURNAME >> doe

This person is 20 years old.


Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 5.2. Неверные входные данные

```
You chose to get someone's age. Provide credentials of the person.

NAME >> 43543hjjhg43

It seems to be incorrect. Try again.

NAME >> 435435hjhk

It seems to be incorrect. Try again.

NAME >> 
```

#### 6. Изменение любого поля в определённой записи справочника

Все поля опциональны.

##### 6.1. При наличии более чем одного человека в БД

```
You chose to change a record. Provide credentials of the person.

NAME >>        
SURNAME >> 
DATE >> 
PERSONAL PHONE NUMBER >> 
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

There is more than one appropriate row. Provide more details.

id|name     |surname|phone       |office_phone|landline_phone|birth_date
--+---------+-------+------------+------------+--------------+----------
2 |Jane     |Doe    |89991112233 |None        |None          |2000-01-02
3 |Gini     |Doe    |89991010101 |None        |4555555555    |2003-01-03
4 |Kevin    |Doe    |89992304545 |89992003030 |None          |None      
5 |Larry    |Doe    |89998883434 |None        |None          |None      
6 |Tyler    |Doe    |89998884040 |None        |None          |1993-07-05
7 |Josh     |Doe    |89991234567 |None        |None          |1983-12-25
8 |Robert   |Doe    |89993502020 |None        |None          |2010-12-17
23|Guido    |Doe    |89991234567 |None        |None          |1993-05-01
24|Sarah    |Doe    |889995670912|None        |4888888888    |None      
27|Nora     |Doe    |889991001010|None        |None          |None      

NAME >>     
SURNAME >> Babii
DATE >> 
PERSONAL PHONE NUMBER >> 
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

Specify attributes which you want to change.

NAME >> 
SURNAME >> Doe
DATE >> 
PERSONAL PHONE NUMBER >> 
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

Credentials were successfully changed.

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 6.2. При наличии ровного одного подходящего человека в БД.

```
You chose to change a record. Provide credentials of the person.

NAME >> Alexander
SURNAME >> 
DATE >> 
PERSONAL PHONE NUMBER >> 
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

Specify attributes which you want to change.

NAME >> Karl
SURNAME >> 
DATE >> 
PERSONAL PHONE NUMBER >> 
OFFICE PHONE NUMBER >> 
LANDLINE PHONE NUMBER >> 

Credentials were successfully changed.

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

## Дополнительные функции

#### 1. Возможность добавления других видов номеров

Как можно было заметить ранее, в таблице значатся ещё станционарный и рабочий телефоны. Дублирую таблицу.

```
Here is your phonebook.

id|name  |surname|phone       |office_phone|landline_phone|birth_date
--+------+-------+------------+------------+--------------+----------
2 |Jane  |Doe    |89991112233 |None        |None          |2000-01-02
3 |Gini  |Doe    |89991010101 |None        |4555555555    |2003-01-03
4 |Kevin |Doe    |89992304545 |89992003030 |None          |None      
5 |Larry |Doe    |89998883434 |None        |None          |None      
6 |Tyler |Doe    |89998884040 |None        |None          |1993-07-05
7 |Josh  |Doe    |89991234567 |None        |None          |1983-12-25
8 |Robert|Doe    |89993502020 |None        |None          |2010-12-17
23|Guido |Doe    |89991234567 |None        |None          |1993-05-01 
25|Karl  |Doe    |89991402386 |None        |None          |2002-01-02  

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 2. Удаление по номеру телефона

##### 2.1. При наличии одного такого телефона в базе

```
You chose to remove a record given its phone number. Provide the phone number.

PERSONAL PHONE NUMBER >> 89991112233

Record was removed.

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

##### 2.2. При наличии нескольких одинаковых номеров в базе

```
You chose to remove a record given its phone number. Provide the phone number.

PERSONAL PHONE NUMBER >> 89991010101

id|name|surname|phone      |office_phone|landline_phone|birth_date
--+----+-------+-----------+------------+--------------+----------
3 |Gini|Doe    |89991010101|None        |4555555555    |2003-01-03
28|Kyle|Doe    |89991010101|None        |None          |None      

There are multiple records with this phone number.

Enter ID (leftmost column) of the record you want to remove >> 28

Record was removed.

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 3. Поиск и вывод по дате рождения

```
You chose to get records given the birthday. Provide day and month.

BIRTHDAY (DD.MM) >> 03.01

id|name|surname|phone      |office_phone|landline_phone|birth_date
--+----+-------+-----------+------------+--------------+----------
3 |Gini|Doe    |89991010101|None        |4555555555    |2003-01-03

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 4. Просмотр людей, у которых день рождения в течение 30 дней

```
You chose to get a list of the nearest birthdays.

person.name|person.surname
-----------+--------------
Josh       |Doe           
Robert     |Doe           

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 5. Просмотр записей старше/младше/ровно N лет.

```
You chose to select people whose age is above/below/equals N years.
Provide age (e.g. 5) and comparison type (above/below/equals).

AGE >> 15
COMPARISON TYPE >> above

id|name |surname|phone      |office_phone|landline_phone|birth_date
--+-----+-------+-----------+------------+--------------+----------
3 |Gini |Doe    |89991010101|None        |4555555555    |2003-01-03
6 |Tyler|Doe    |89998884040|None        |None          |1993-07-05
7 |Josh |Doe    |89991234567|None        |None          |1983-12-25
23|Guido|Doe    |89991234567|None        |None          |1993-05-01
25|Karl |Doe    |89991402386|None        |None          |2002-01-02

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 6. Сортировка справочника по разным атрибутам

```
Credential you want to sort by (name, surname, birth_date) >> name
Order you want to use for sorting (ascending/descending) >> ascending

Your phonebook sorted by name is below.

id|name  |surname|phone       |office_phone|landline_phone|birth_date
--+------+-------+------------+------------+--------------+----------
6 |Tyler |Doe    |89998884040 |None        |None          |1993-07-05
24|Sarah |Doe    |889995670912|None        |4888888888    |None      
8 |Robert|Doe    |89993502020 |None        |None          |2010-12-17
27|Nora  |Doe    |889991001010|None        |None          |None      
5 |Larry |Doe    |89998883434 |None        |None          |None      
4 |Kevin |Doe    |89992304545 |89992003030 |None          |None      
25|Karl  |Doe    |89991402386 |None        |None          |2002-01-02
7 |Josh  |Doe    |89991234567 |None        |None          |1983-12-25
23|Guido |Doe    |89991234567 |None        |None          |1993-05-01
3 |Gini  |Doe    |89991010101 |None        |4555555555    |2003-01-03

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

#### 7. Полная очистка справочника

##### 7.1. Отказ от очистки

```
Are you sure you want to remove all records? (yes/no) >> no

Operation aborted.

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >>
```

##### 7.2. Согласие на очистку

```
Are you sure you want to remove all records? (yes/no) >> yes

All records were removed.

Please enter:
--- a command number
--- 'quit' to quit
--- 'menu' to return to the menu

COMMAND >> 
```

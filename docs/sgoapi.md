# Документация REST API сетевого города
Эта страница документации будет содержать техническое описание API.  
Не требуется для понимания библиотеки.

## Как водить в систему
### Получение случайных значений
Сначала нужно получить значения `lt`, `var` и `salt`.  
URL: `/webapi/auth/getdata`  
Никаких параметров не требуется.

#### Пример ответа
```
{"lt":"878792729","ver":"679337794","salt":"9369808045"}
```

#### Где эти значения используется

  - `lt` - Только для отправки на форму входа. (Защита от повторных запросов?)
  - `ver` - точно так же как и `lt`
  - `salt` - На форму входа напрямую не отправляется. Используется для хеширования пароля.

### Отправление данных для входа
URL: `/webapi/login`  
**Важно**: Обязательно нужно добавлять заголовок `Referer` или иначе сервер будет кидать ошибку.

#### Параметры

  - `LoginType` - По умолчанию 1. Пока не знаю что каждый из них обозначает.
  - `cid`, `sid`, `pid`, `cn`, `sft` - Регион, Городской округ, Населённый пункт, и т.д…
  - `UN` - Имя пользователя
  - `pw2` - md5 пароля по схеме 3710 hashcat или `md5_str(salt + md5_str(pass))`
  - `PW` - `pw2`, обрезанный по длине пароля.
  - `ver` и `lt`
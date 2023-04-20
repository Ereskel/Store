import aiosqlite


# con = aiosqlite.connect('database.db')
# cur = con.cursor()

# ---------------------------------------- ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ ---------------------------
async def create_database():
    async with aiosqlite.connect('database.db') as con:
        await con.execute("CREATE TABLE IF NOT EXISTS database("
                          "id INTEGER PRIMARY KEY,"
                          "name TEXT,"
                          "username TEXT)")
        await con.commit()


async def add_user(id, name, username):
    async with aiosqlite.connect('database.db') as con:
        await con.execute("INSERT INTO database (id, name, username) VALUES(?, ?, ?)", (id, name, username))
        await con.commit()


async def get_user(id):
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT id FROM database WHERE id = ?', (id,)) as cursor:
            result = await cursor.fetchone()
            return result


# ------------------------------------------------- ТАБЛИЦА ТОВАРОВ --------------------------------------------

async def create_database_staff():
    async with aiosqlite.connect('database.db') as con:
        await con.execute('CREATE TABLE IF NOT EXISTS staff('
                          'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                          'name TEXT,'
                          'city TEXT,'
                          'amount INT,'
                          'description TEXT,'
                          'info TEXT,'
                          'photo INT)')
        await con.commit()


async def admin_add_staff(id, name, city, amount, description, info, photo):
    async with aiosqlite.connect('database.db') as con:
        await con.execute('INSERT INTO staff VALUES(?, ?, ?, ?, ?, ?, ?)',
                          (id, name, city, description, info,
                           amount, photo))
        await con.commit()

'''
Как здесь все работает? Здесь должно быть два типа функции. Две функции get_name_dot и 
'''
async def get_name_dot():
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT id FROM staff') as cursor:
            id = await cursor.fetchone()
            return id


async def get_name():
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT name FROM staff') as cursor:
            name = await cursor.fetchall()
            return name


async def get_city():
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT city FROM staff') as cursor:
            cities = await cursor.fetchall()
            return cities


async def get_description():
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT description FROM staff') as cursor:
            description = await cursor.fetchall()
            return description


async def get_info():
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT info FROM staff') as cursor:
            info = await cursor.fetchall()
            return info


async def get_amount():
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT amount FROM staff') as cursor:
            amount = await cursor.fetchall()
            return amount


async def get_photo():
    async with aiosqlite.connect('database.db') as con:
        async with con.execute('SELECT photo FROM staff') as cursor:
            photo = await cursor.fetchall()
            return photo

# async def get_area():
#    async with aiosqlite.connect('database.db') as con:
#        async with con.execute('SELECT area FROM staff')


#            cities = [row[0] for row in await cursor.fetchall()]


# async def get_user(id):
#    async with aiosqlite.connect("database.db") as db:
#        async with db.execute('SELECT id FROM database WHERE id = ?', (id,)) as cursor:
#            all_users = await cursor.fetchall()
#            return all_users


# async def get_user(id):
#    async with aiosqlite.connect("database.db") as db:
#       async with db.execute('SELECT id FROM database WHERE id = ?', (id,)) as cursor:
#            all_users = await cursor.fetchall()
#            return all_users

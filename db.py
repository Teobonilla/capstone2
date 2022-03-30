import string
# ---------------------
# defaults
# ---------------------
DB_NAME = 'profile.db'
T_NAME = 'users'
# ---------------------
# database handling
# ---------------------
import sqlite3
# reference tutorial: https://www.youtube.com/watch?v=byHcYRpMgI4
def init(db_name = DB_NAME, table_name = T_NAME):
    # connect to database
    # database file is created if it doesn't exist
    conn = sqlite3.connect(db_name)
    # use line below instead if you'd like to use a sqlite database in temporary memory only
    # conn = sqlite3.connect(':memory:')
    #
    # create a cursor
    c = conn.cursor()
    # create a table | DATYPES: null, integer, real, text, blob
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            un text,
            pw text,
            first_name text,
            last_name text,
            email text,
            interests text
        )
    """)
    # commit our command
    conn.commit()
    # close connection (good practice)
    conn.close()

    print(f'Initialized database "{db_name}" and table "{table_name}".')

    return

def un_exists(un, db_name = DB_NAME):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"""SELECT un 
        FROM users 
        WHERE un = '{un}'
    """)
    un_result = c.fetchall()

    result = True if len(un_result) else False

    print(f'db.un_exists("{un}") result = "{result}"')

    conn.close()

    return result

def profile_new(
    un, 
    pw, 
    fn, 
    ln, 
    em, 
    ints,
    db_name = DB_NAME
):
    result = False
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if not un_exists(un):
        c.execute("""INSERT INTO users VALUES (
                ?, 
                ?, 
                ?, 
                ?, 
                ?, 
                ?
            )
        """, (un, pw, fn, ln, em, ints,))
        conn.commit()
        result = True
        print(f'Created new profile for "{un}".')
        pass
    else:
        print(f'CANNOT create new profile. Profile for "{un}" already exists.')
        pass

    conn.close()

    return result


def profile_get(*args, **kwargs):
    uns = []
    print_all = False
    profiles = []
    if len(args):
        for arg in args:
            if type(arg) == str:
                uns.append(arg)
            if type(arg) == list and len(arg) and type(arg[0]) == str:
                for un in arg:
                    uns.append(un)
    
    # print(f'uns = {uns}')

    # handle default kwargs
    if 'db_name' not in kwargs.keys():
        db_name = DB_NAME
        pass
    else:
        db_name = kwargs['db_name']
        pass
    if 'all' in kwargs.keys():
        # print all profiles
        print_all = kwargs['all']
        pass

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    if print_all:
        c.execute(f"""SELECT rowid, * 
            FROM users
            ORDER BY un
        """)
        profiles = c.fetchall()
        pass
    else:
        for un in uns:
            print(f'un = {un}')
            c.execute(f"""SELECT rowid, *
                FROM users 
                WHERE un = '{un}'
            """)
            profiles.append(c.fetchone())



    print(f'db.profile_print("*{args}, **{kwargs}") profiles =')
    for profile in profiles:
        print(profile)

    conn.close()

    return profiles

def un_login(un, pw, db_name = DB_NAME):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"""SELECT rowid, first_name 
        FROM users 
        WHERE un = '{un}' 
        AND pw = '{pw}'
    """)
    # first_name = c.fetchone()
    # first_name = c.fetchmany(3)
    first_name = c.fetchall()

    result = True if len(first_name) else False

    print(f'db.un_login("{un}", "{pw}") result = "{result}"')

    conn.close()

    return result

def profile_update(un, **kwargs):
    # handle default kwargs
    if 'db_name' not in kwargs.keys():
        db_name = DB_NAME
        pass
    else:
        db_name = kwargs['db_name']
        pass

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    for key in kwargs.keys():
        c.execute(f"""UPDATE users 
            SET '{key}' = '{kwargs[key]}'
            WHERE un = '{un}'
        """)

    print(f'db.profile_update({un}, {kwargs}) executed.')

    conn.commit()
    conn.close()

    return

def profile_delete(un, **kwargs):
    # handle default kwargs
    if 'db_name' not in kwargs.keys():
        db_name = DB_NAME
        pass
    else:
        db_name = kwargs['db_name']
        pass

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(f"""DELETE from users 
        WHERE un = '{un}'
    """)

    print(f'db.profile_delete({un}) profile deleted, if it existed in the first place.')

    conn.commit()
    conn.close()

    return

# ----------------------
# Main application function
# ----------------------
def main():
    # Database initialization and tests
    init()
    un_exists('userNameThatDoesNotExist')
    profile_delete('userNameThatDoesNotExist')
    profile_delete('davidDelSol')
    profile_new(
        'davidDelSol',
        'encrypted?',
        'david',
        'aloka',
        'test@preform.io',
        'salsa,extended intelligence,marathon running in a full suit'
    )
    profile_new(
        'Python733t',
        'encrypted?',
        'Doroteo ',
        'Bonilla',
        'doabonilla@yahoo.com',
        'work,school,sleep,repeat'
    )
    un_login('davidDelSol', 'encrypted?')
    profile_update('davidDelSol', pw = 'definitelyNotEncripted!')
    un_login('davidDelSol', 'definitelyNotEncripted!')
    un_exists('davidDelSol')
    profile_get(all = True)
    profile_get(['Python733t'])
    profile_get('Python733t')

    pass

if __name__ == '__main__':
    main()
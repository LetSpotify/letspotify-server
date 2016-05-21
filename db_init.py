import rethinkdb as r
DB_NAME = 'test_db'

db = r.connect(host='localhost', port=28015)
try:
    r.db_create(DB_NAME).run(db)
except:
    print("db already exist, pass.....")
    exit()
    r.db_drop(DB_NAME).run(db)
    r.db_create(DB_NAME).run(db)

db.use(DB_NAME)

r.table_create("login_tokens").run(db)
r.table_create("players").run(db)
r.table_create("rooms").run(db)
r.table_create("user_subscribes").run(db)
r.table_create("users").run(db)

r.table('rooms').index_create('id_uid', [r.row["id"], r.row["uid"]]).run(db)
r.table('rooms').index_create('rid').run(db)
r.table('rooms').index_create('uid').run(db)
r.table('user_subscribes').index_create('rid_uid', [r.row["rid"], r.row["uid"]]).run(db)
r.table('user_subscribes').index_create('rid').run(db)
r.table('user_subscribes').index_create('uid').run(db)
r.table('users').index_create('fid').run(db)

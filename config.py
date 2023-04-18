from environs import Env

path = ('A:\.env')
env = Env()
env.read_env(path)

token = env.str('token')
admins = env.list('admin')
moder_id = env.str('moder_id')


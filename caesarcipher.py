import requests
import hashlib
import json
token= input('Digite o token: ')
s = requests.Session()
r = s.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}'.format(token))
alfabeto ='abcdefghijklmnopqrstuvwxyz'
json_dict = r.json()

with open('answer.json', 'w') as outfile:
    json.dump(json_dict, outfile)

mensagem= json_dict['cifrado']
m = ''
for i in mensagem:
    if i.isalpha():
        i_index = alfabeto.index(i)
        m += alfabeto[(i_index - json_dict['numero_casas']) %len(alfabeto)]
    else:
        m += i
json_dict['decifrado'] = m
hsh = hashlib.sha1()
hsh.update(json_dict['decifrado'].encode('utf-8'))
hash_digested = hsh.hexdigest()
json_dict['resumo_criptografico'] = hash_digested
with open('answer.json', 'w') as outfile:
    json.dump(json_dict, outfile)

arquivo_resolucao = open('answer.json','r')
answer = {"answer":arquivo_resolucao}
post_request = s.post('https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}'.format(token),files = answer)
print(post_request.status_code)
print(post_request.content)
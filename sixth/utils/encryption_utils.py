import rsa
import os
from pathlib import Path
import json
import base64
import copy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

async def post_order_encrypt(public_key, key, data, copy_text, list_key=None):  
    if type(data) == list:
        new_list = []
        for i in data:
            if (type(i) == dict):
                new_deep_copy = copy.deepcopy(i)
                await post_order_encrypt(public_key, None, i, new_deep_copy)
                new_list.append(new_deep_copy)
            elif type(i) == list:
                await post_order_encrypt(public_key, key, i, copy_text, list_key)
            else:
                new_list.append(await encrypt(public_key, str(i)+":::bob_::_johan::sixer"+str(type(i))))
        del copy_text[list_key]
        copy_text.update({list_key:new_list})
        return
    if type(data) != dict:
        copy_text[await encrypt(public_key, key)] = await encrypt(public_key, str(data)+":::bob_::_johan::sixer"+str(type(data)))
        
    for i in data.keys():
        encrypted = await encrypt(public_key, i)
        copy_text[encrypted] = copy_text.pop(i)
        if type(copy_text[encrypted]) == str or type(copy_text[encrypted])==int or type(copy_text[encrypted])==float or type(copy_text[encrypted])==bool:
            if (len(str(copy_text[encrypted]))) < 40:
                copy_text[encrypted] = await encrypt(public_key, str(copy_text[encrypted])+":::bob_::_johan::sixer"+str(type(copy_text[encrypted])))
            else:
                copy_text[encrypted] = str(copy_text[encrypted])
        elif type(copy_text[encrypted]) == list:
            await post_order_encrypt(public_key, i, data[i],copy_text, encrypted)
        else:
            await post_order_encrypt(public_key, i, data[i],copy_text[encrypted])
                                          

async def post_order_decrypt(private_key, key, data, copy_text, list_key=None):   
    if type(data) == list:
        new_list = []
        for i in data:
            if (type(i) == dict):
                new_deep_copy = copy.deepcopy(i)
                await post_order_decrypt(private_key, None, i, new_deep_copy)
                new_list.append(new_deep_copy)
                
            elif type(i) == list:
                await post_order_decrypt(private_key, key, i, copy_text, list_key)
                
            else:
                new_list.append(await parse_word(await decrypt(private_key, i)))
        del copy_text[list_key]
        copy_text.update({list_key:new_list})
        return
    if type(data) != dict:
        copy_text[await decrypt(private_key, key)] = await decrypt(private_key, str(data))
        
    for i in data.keys():
        encrypted = await decrypt(private_key, i)
        copy_text[encrypted] = copy_text.pop(i)
        if type(copy_text[encrypted]) == str or type(copy_text[encrypted])==int or type(copy_text[encrypted])==float:
            try:
                copy_text[encrypted] = await parse_word(await decrypt(private_key, str(copy_text[encrypted])))  
            except:
                copy_text[encrypted] = str(copy_text[encrypted])
        elif type(copy_text[encrypted]) == list:
            await post_order_decrypt(private_key, i, data[i],copy_text, encrypted)
        else:
            await post_order_decrypt(private_key, i, data[i],copy_text[encrypted])

async def parse_word(string: str):
    added_word= ":::bob_::_johan::sixer"
    index = string.find(added_word)
    add = string[index:len(string)]
    real = string.replace(add, "")
    if ("int" in add):
        return int(real)
    if ("float" in add):
        return float(real)
    if ("str" in add):
        return real
    if ("bool" in add):
        return bool(add)

async def encrypt(public_key_txt, data):
    public_key = rsa.PublicKey.load_pkcs1(public_key_txt)

    # Encrypt the data using the public key
    encrypted_data = rsa.encrypt(data.encode(), public_key)
    return base64.b64encode(encrypted_data).decode("ascii") 

async def decrypt(private_key_txt, data):
    decrypt_data=base64.b64decode(data.encode("ascii"))
    private_key = rsa.PrivateKey.load_pkcs1(private_key_txt)
    decrypted_message=rsa.decrypt(decrypt_data,private_key).decode()
    return decrypted_message

import string

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode_base62(nums):

    if nums==0:
        return BASE62[0] 

    stack=[]

    while nums>0:
        rem=nums%62
        stack.append(BASE62[rem])
        nums=nums//62

    result=""

    while stack:
            result+=stack.pop()

    return result
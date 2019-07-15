"""
Requires 'cryptography' module. pip install cryptography.
"""

from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcrKbM1piU_VQAlrwi5Rj15QwZ0-DjBuNYZLN9IYYDO8jNnLo6_KVo6a8ipxi2kV51YpSdugPawk8HrfE9myG52XhQqKxBNAtlnRYfslrrSnfPAZsO4mR_1bdbWa1gVyoMOxMLlsHrkDHX9t3tClvVCOaKGSxkX5CrleOkDphb2CEdBSc='


def main():
    f = Fernet(key)
    decrypted_message = f.decrypt(message)
    print(decrypted_message)


if __name__ == "__main__":
    main()

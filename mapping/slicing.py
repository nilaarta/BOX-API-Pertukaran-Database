# string = "mapping-12313123-encrypt.json"

# # if sr =="mapping":
# #     print("sama")

# # ls = string[-15:]



# sr = string[:-13]+".json"
# print(sr)

# # def extrack_file_name(file_name):
# #     mpfile = file_name[:7]
# #     mapping= False
# #     if mpfile == "mapping":
# #         mapping = True
# #     if mapping:
# #         date = file_name[:-13][8:]
# #     return date, mapping

# # mapi = extrack_file_name(string)
# # print (mapi)
halo = ["a", "b", "c", 100]
def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    s.pop(0)
    # traverse in the string   
    for ele in s:  
        str1 = str1 + str(ele) + ","
    # return string   
    return str1[:-1] 



print (listToString(halo))


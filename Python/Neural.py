import NBModel

# Extract User
nb = NBModel.Models()
user = nb.getUser()
nb.test(user, 'Neural_Model.sav', flag=False)
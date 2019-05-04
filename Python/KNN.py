import NBModel

# Extract User
nb = NBModel.Models()
user = nb.getUser()
nb.test(user, 'Model_KNN.sav')
# Step 1
import pickle
 
# Step 2
'''
In step 2, we use the with keyword with the open function to get
a file handle that points to config.dictionary in the same directory
where we will run load_dictionary_from_file.py.

As with saving the dictionary to file, we supply config.dictionary
as the first input to the open function to indicate the file path
to the file which contains the serialized dictionary. This time
round, we supply the string 'rb' instead of 'wb' to indicate that
we want a file handle that reads binary contents from the file.
'''

with open('config.dictionary', 'rb') as config_dictionary_file:
 
      # Step 3
      config_dictionary = pickle.load(config_dictionary_file)

      # After config_dictionary is read from file
      print(config_dictionary)

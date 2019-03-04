from PIL import Image
import cv2,os,sys,random,binascii
import numpy as np

#convert string to bin
def convert_string_to_bin(string):
	temp = ' '.join('{0:08b}'.format(ord(x), 'b') for x in string)
	array = temp.split(" ")
	return array[::-1]

#convert bin to string
def convert_bin_to_string(string_array):
	temp = string_array
	temp = temp[::-1]
	string = ""
	for i in temp:
		char = int(i,2)
		string += chr(char)
	return string

#and 2 matrix
def and_matrix(matrix,key):
	result = [[0 for m in range(len(matrix[0]))] for n in range(len(matrix))]
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == key[i][j] and matrix[i][j] == 1:
				result[i][j] = 1
			else:
				result[i][j] = 0
	return result


#count and return sum of bit 1
def num_Of_Bit1(matrix):
	tong = 0
	for i in range(len(matrix)):
		for j in range(len(matrix[1])):
			tong += matrix[i][j]
	return tong

#split matrix in to block with mxn size
def divide_matrix(matrix,m,n):
	SumOfSubMatrix = (len(matrix)/m) * (len(matrix[0])/n)
	newRows = len(matrix)/m
	newCols = len(matrix[0])/n
	temp = []
	for i in range(newRows):
		for j in range(newCols):
			subMatrix = [[0 for x in range(n)] for y in range(m)]
			for k in range(m):
				for l in range(n):
					subMatrix[k][l] = matrix[m*i+k][n*j+l]			
			temp.append(subMatrix)
	return temp

#get value of matrix at i,j
def getValue(matrix,i,j):
	return matrix[i][j]

#set value for matrix
def SetValue(matrix,i,j,value):
	matrix[i][j] = value

#merge all submatrix
def merge(matrix,ori_row,ori_col):
	sample = matrix[0]
	m = len(sample)
	n = len(sample[0])
	newRows = ori_row/m
	newCols = ori_col/n
	merge = [[0 for x in range(newCols*n)] for y in range(newRows*m)]
	for i in range(newRows):
		for j in range(newCols):
			temp = matrix[i*newCols+j]
			for k in range(m):
				for l in range(n):
					SetValue(merge,i*m+k, j*n+l,getValue(temp,k,l))
	return merge	

#convert image to matrix
def convert_to_matrix(filename):
	temp=Image.open(filename).convert('L')    
	A = np.array(temp)
	new_A=np.empty((A.shape[0],A.shape[1]),None) 
	new_A = A

	new_A = new_A / 255
	matrix = np.array(new_A)

	return matrix

#save file
def save_file(matrix,filename):
	new_A = np.empty((len(matrix),len(matrix[0])),None)
	new_A = np.array(matrix)
	new_A = new_A * 255
	im = Image.fromarray(new_A)
	im.save(filename)

#find
def find_match(key,matrix,(m,n)):
	temp = []
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == n and key[i][j] == m:
				temp.append((i,j))
	random.shuffle(temp)
	return temp[0]

#reverse matrix
def reverse_matrix(matrix,i,j):
	if matrix[i][j] == 0:
		matrix[i][j] = 1
	elif matrix[i][j] == 1:
		matrix[i][j] = 0

#get random i,j
def get_random(matrix,key,value):
	temp = []
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if key[i][j] == value:
				temp.append((i,j))
	random.shuffle(temp)
	return temp[0]

#main
if __name__ == "__main__":
	if len(sys.argv) >= 4:
		#Encryp
		if sys.argv[1] == "-E" and len(sys.argv) == 6:
			filename_in = sys.argv[3]
			filename_out = sys.argv[5]
			#input key
			key = raw_input("\nNhap ma tran key 2x2: ")
			key_array = [[int(x) for x in z] for z in key]
			key_matrix = np.reshape(key_array,(-1,2))
			#input string
			string = raw_input("\nNhap mess: ")
			bin_string =''.join(convert_string_to_bin(string))
			bin_array = []
			for i in bin_string:
				bin_array.append(int(i))
			#open and convert image to matrix
			matrix = convert_to_matrix(filename_in)
			subMatrix = divide_matrix(matrix,2,2)
			check = False
			#hide mess
			i = 0
			count = 0
			for Fi in subMatrix:
				if i >= len(bin_string):
					break
				count +=1
				and_result = and_matrix(Fi,key_matrix)
				sum_bit_1_matrix = num_Of_Bit1(and_result)
				sum_bit_1_key = num_Of_Bit1(key_matrix)
				#check if Fi can hide 1 bit of mess
				if sum_bit_1_matrix > 0 and sum_bit_1_matrix < sum_bit_1_key:
					if sum_bit_1_matrix % 2 != bin_array[i]:
						if sum_bit_1_matrix == 1:
							m,n = find_match(key_matrix,Fi,(1,0))
							SetValue(Fi,m,n,1)
						elif sum_bit_1_matrix == (sum_bit_1_key - 1):
							m,n = find_match(key_matrix,Fi,(1,1))
							SetValue(Fi,m,n,0)
						else:
							m,n = get_random(Fi,key_matrix,1)
							reverse_matrix(Fi,m,n)
					i+=1
				#create a output file
				if i == len(bin_string):
					temp = merge(subMatrix,140,200)
					out = save_file(temp,filename_out)
					temp_1 = convert_to_matrix(filename_out)
					sub_temp = divide_matrix(temp_1,2,2)
					merge = merge(sub_temp,140,200)
					save_file(merge,filename_out)
					print "\nDo dai doan tin: %d\n" % len(string)
					print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
					check = True
			if check == True:
				print "\nDone\n\t\t\t------------- Unicorn-Team -------------n"
			else:
				print "Something error !!!"

		#Decryp			
		elif sys.argv[1] == "-D" and len(sys.argv) == 4:
			filename_in = sys.argv[3]
			#input key
			intput_key = raw_input("\nNhap ma tran key 2x2: ")
			key_array = [[int(x) for x in z] for z in intput_key]
			key_matrix = np.reshape(key_array,(-1,2))
			#string
			length = raw_input("\nNhap vao do dai tin duoc giau: ")
			string = ""
			#open and convert image to matrix
			matrix = convert_to_matrix(filename_in)
			subMatrix = divide_matrix(matrix,2,2)
			#Decryp
			i = 0
			count = 0
			for Fi in subMatrix:
				if i >= 8*int(length):
					break
				count+=1
				and_result = and_matrix(Fi,key_matrix)
				sum_bit_1_matrix = num_Of_Bit1(and_result)
				sum_bit_1_key = num_Of_Bit1(key_matrix)
				b = num_Of_Bit1(and_result)
				#Check if Fi cover a hidden bit
				if sum_bit_1_matrix > 0 and sum_bit_1_matrix < sum_bit_1_key:
					if b % 2 == 0:
						string+= "0"
					else:
						string+= "1"
					i+=1
			#add bit 0 if missing
			leng = len(string)
			miss = 8 - (leng % 8)
			if miss != 8:
				for i in range(miss):
					string+= "0"
			#create output string
			out = [string[i:i+8] for i in range(0, len(string), 8)]
			output_string = convert_bin_to_string(out)
			print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
			print "Doan mess duoc giau: \n%s" % output_string
			print "\nDone\n\t\t\t------------- Unicorn-Team -------------\n"
		else:
			print "\nWrong parameter, please check\n"
	else:
		print "\nUsage: python wu_lee.py -[option] -i input_file -o output_file\n-E: Encryp mode\n-D: Decryp mode\n"

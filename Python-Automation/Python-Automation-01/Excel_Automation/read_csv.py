import csv

def print_csv(csv_reader):
    for row in csv_reader:
        print(row)

csv_file = open("test_csv.csv")
reader = csv.reader(csv_file)
print_csv(reader)

write_file = open("test_csv.csv", "a+", newline='\n')
writer = csv.writer(write_file)
writer.writerow(['jloka_01', 'jloka_02', 'jloka_03'])
writer.writerow(['jloka_04', 'jloka_05', 'jloka_06'])
write_file.close()
csv_file.seek(0)
print_csv(reader)
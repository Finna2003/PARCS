from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n = self.read_input()
        step = len(n) / len(self.workers)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            start_index = i * step
            end_index = (i + 1) * step if i < len(self.workers) - 1 else len(n)
            mapped.append(self.workers[i].mymap(n[start_index:end_index]))

        print ('Map finished: ', mapped)

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(plaintext):
        ciphertext = ''
        for i in range(len(plaintext)):
          char = plaintext[i]
          if char.isalpha():
            if char.isupper():
                index = ord(char) - ord('A')
                new_char = chr(ord('Z') - index)
                ciphertext += new_char
            else:
                index = ord(char) - ord('a')
                new_char = chr(ord('z') - index)
                ciphertext += new_char
          else:
            ciphertext += char
        return ciphertext

    @staticmethod
    @expose
    def myreduce(mapped):
        output = ""
        for x in mapped:
            output += x.value
        return output

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            text = f.read()
        return text 


    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
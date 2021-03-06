import sys

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import subprocess
from subprocess import STDOUT, PIPE


def home_page(request):
    return render(request, 'editor/home_page.html')


def run(cmd):
    print('start')
    print(cmd)
    print('end')

    language = cmd[0]
    if language in ['python', 'ruby']:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
    elif language == 'cpp':
        cpp_cmd = "g++ " + cmd[1] + " `pkg-config --cflags --libs opencv` -lm  -o out2;./out2"

        s1 = subprocess.check_output(cpp_cmd, shell=True)
        print("TYPE ==> ", type(s1), " size : ", sys.getsizeof(s1))
        print(s1.decode("utf-8"))
        return 1, s1, None
    elif language == 'javascript':
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
    elif language == 'java':
        proc = subprocess.Popen(cmd,
                                stdout=PIPE,
                                stderr=STDOUT)
        input = subprocess.Popen(cmd, stdin=PIPE)
        print(proc.stdout.read())

        # proc = subprocess.Popen(cmd,
        #                         stdout=subprocess.PIPE,
        #                         stderr=subprocess.PIPE,
        #                         )
        # stdout, stderr = proc.communicate()
        return proc.returncode, input, input
    elif language == 'c':
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
    else:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr


def result(request):
    s = request.POST['script']
    language = request.POST['language']
    temp_path = settings.STATIC_ROOT + "/"
    file_name = ''
    if language == 'python':
        file_name = "temp.py"
    elif language == 'java':
        file_name = "Temp.java"
        # temp_path = "Temp"
    elif language == 'ruby':
        file_name = 'temp.rb'
    elif language == 'c':
        file_name = 'temp.c'
    elif language == 'cpp':
        file_name = 'temp.cpp'
    elif language == 'javascript':
        file_name = 'temp.js'
    else:
        file_name = "Temp.java"
    temp_path += file_name
    with open(temp_path, 'w') as f:
        f.write(s)
        f.close()
    _, out, err = run([language, temp_path])

    print('*****')
    print(out)
    print('-----')
    print(err)
    print('=====')

    if out:
        out_decoded = out.decode('utf-8')
    else:
        out_decoded = ''

    if err:
        if err.decode('utf-8') != '':
            spliter = file_name + '", '
            err_decoded = err.decode('utf-8').split(spliter)[1]
        else:
            err_decoded = ''
    else:
        err_decoded = ''

    data = {'output': "{0} {1}".format(out_decoded, err_decoded)}

    # data = {'output': "{0} {1}".format(out.decode('utf-8'),
    #                                    err.decode('utf-8').split('temp.rb",')[1] if err.decode('utf-8') != '' else '')}

    # data = {'output': "{0} {1}".format(out.decode('utf-8'), err.decode('utf-8'))}
    # data = {'output': "{0} {1}".format(out.decode('utf-8'), '')}

    return JsonResponse(data)
